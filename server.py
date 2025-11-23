import socket
import threading
import struct


HOST = "0.0.0.0"     
PORT = 50007         #Porta do servidor
CHUNK_SIZE = 8192    #Definir o tamanho dos pedaços enviados como 8 KB
AUDIO_FILE = "musica.wav" 

def handle_client(conn, addr):
    print(f"Cliente conectado:", addr)

    try:
        #Abrir o arquivo WAV em binario
        with open(AUDIO_FILE, "rb") as audio:
            while True:
                #Ler um bloco de dados
                chunk = audio.read(CHUNK_SIZE)

                if not chunk:
                    #Se for o fim do arquivo manda tamanho 0
                    conn.sendall(struct.pack(">I", 0))
                    break

                #Mandar 4 bytes com o tamanho do bloco
                conn.sendall(struct.pack(">I", len(chunk)))
                #Mandar o bloco de áudio
                conn.sendall(chunk)

    except (ConnectionResetError, BrokenPipeError):
        print(f"Cliente desconect", addr)

    finally:
        conn.close()
        print(f"Conexão encerrada com:", addr)



print(f"Servidor iniciado na porta {PORT}")
print(f"Transmitindo o arquivo: {AUDIO_FILE}")

#Criar socket TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Aguardando clientes...\n")

while True:
    conn, addr = server.accept()

#Criar uma thread para cada cliente conectado
    thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
    thread.start()

