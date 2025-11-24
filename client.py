import socket
import pyaudio
import struct
import threading
import queue
import time

HOST = "127.0.0.1"
PORT = 50007

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Quantidade de segunds para o buffer
BUFFER_SECONDS = 3.0

#Função para que cada pacote tenha o tamanho correto
def recv_exact(sock, size):
    data = b''  #Data vazio
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:      #Se vazio: ou perdeu a conexão ou foi fechada
            return None
        data += packet
    return data

#Thread de recebimento dos blocos e os coloca no buffer
def receiver_thread(sock, audio_queue, finished_event):
    try:
        while True:
            header = recv_exact(sock, 4)  #Tamanho máximo: 4 bytes
            if not header:
                print("O servidor encerrou a conexão (sem header).")
                break

            (block_size,) = struct.unpack(">I", header)

            if block_size == 0:
                print("\nFim da música! Estou obcecada!!")
                break

            audio_data = recv_exact(sock, block_size)
            if not audio_data:
                print("Erro ao receber bloco de áudio.")
                break

            # Coloca o bloco na fila (bloqueia se buffer estiver cheio)
            audio_queue.put(audio_data)
    finally:
        # Sinaliza que não virão mais dados
        finished_event.set()
        sock.close()

def main():
    #Conexão ao servidor
    print("Conectando ao servidor...")
    client_socket = socket.create_connection((HOST, PORT))
    print("Conectado!\n")

    # Inicializar PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True)

    # Fila usada como buffer de reprodução e sinalizador de fim
    audio_queue = queue.Queue(maxsize=200)  #Máximo de 200 blocos, ajuste se quiser
    finished_event = threading.Event()

    # Inicia a thread que recebe os dados do servidor
    t = threading.Thread(
        target=receiver_thread,
        args=(client_socket, audio_queue, finished_event),  #Lê os dados, enfila os blocos e sinaliza o fim
        daemon=True
    )
    t.start()

    # Calcula quantos bytes correspondem a BUFFER_SECONDS
    sample_width = p.get_sample_size(FORMAT)
    bytes_per_second = RATE * CHANNELS * sample_width
    target_buffer_bytes = int(BUFFER_SECONDS * bytes_per_second)

    print(f"Pré-carregando ~{BUFFER_SECONDS} segundos de áudio no buffer...")
    buffered_bytes = 0

    #Pré-buffer (espera acumular alguns segundos de áudio antes de tocar para não iniciar sem ele)
    prebuffer_chunks = []
    while buffered_bytes < target_buffer_bytes and not (finished_event.is_set() and audio_queue.empty()):
        try:
            chunk = audio_queue.get(timeout=0.1)
            prebuffer_chunks.append(chunk)
            buffered_bytes += len(chunk)
        except queue.Empty:
            # Ainda não chegou nada, continua tentando
            pass

    #Tocar o que já foi bufferizado
    for chunk in prebuffer_chunks:
        stream.write(chunk)

    print("Começando a reprodução contínua...")

    #Reprodução contínua: consome da fila enquanto houver dados ou até o fim
    while True:
        # Se não virá mais dado e o buffer está vazio (música acabou), podemos encerrar
        if finished_event.is_set() and audio_queue.empty():
            break

        try:
            chunk = audio_queue.get(timeout=0.1)
            stream.write(chunk)
        except queue.Empty:
            # Se demorar um pouco por causa da rede, o buffer segura;
            # se ficar vazio mesmo após o fim, o laço encerra pela condição acima.
            pass

    #Finaliza o cliente
    print("Reprodução finalizada.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("Cliente finalizado.")

if __name__ == "__main__":
    main()
