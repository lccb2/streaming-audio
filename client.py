import socket
import pyaudio
import struct

HOST = "127.0.0.1"
PORT = 50007

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def recv_exact(sock, size):
    #Garantir o tamanho dos blocos
    data = b''
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            return None
        data += packet
    return data


print("Conectando ao servidor")
client_socket = socket.create_connection((HOST, PORT))
print("Conectado!\n")

#Inicializar PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True)

while True:
    #Ler os blocos
    header = recv_exact(client_socket, 4)
    if not header:
        print("O servidor encerrou a conexão")
        break

    (block_size,) = struct.unpack(">I", header)

    if block_size == 0:
        print("\nFim da musica! Estou obcecada!!")
        break

    #Ler o bloco exato
    audio_data = recv_exact(client_socket, block_size)
    if not audio_data:
        print("Erro ao receber bloco")
        break

    #Tocar musica
    stream.write(audio_data)

stream.stop_stream()
stream.close()
p.terminate()
client_socket.close()
print("Cliente finalizado")
