# Streaming de Áudio TCP (WAV) – Cliente & Servidor

## 📝 Sumário
Este projeto implementa um sistema distribuído de **streaming contínuo de áudio via TCP**, onde um **servidor transmite um arquivo WAV em blocos** e um **cliente o reproduz em tempo real** usando PyAudio. A abordagem simula um fluxo contínuo, semelhante a plataformas de streaming, mas com arquitetura simples.

---

## 📖 Informações
Este projeto demonstra os princípios fundamentais de:
- comunicação **cliente-servidor** usando *Sockets TCP*,
- **transmissão contínua** de dados binários (streaming),
- reprodução de áudio em tempo real via **PyAudio**,
- uso de **threads** para paralelizar recepção e reprodução,
- protocolo básico de envio de dados com prefixo de tamanho.

O servidor divide um arquivo WAV em blocos de 8 KB e envia cada bloco precedido por um cabeçalho de **4 bytes contendo o tamanho do chunk**.  
O cliente recebe e a música é tocada conforme os dados chegam.


---

## 🏁 Como Utilizar
Estas instruções permitem que você baixe e execute o sistema em sua máquina local.

### Clone o repositório
```bash
git clone https://github.com/SEU-USUARIO/streaming-audio.git

cd streaming-audio
```

### Pré-requisitos

- Python3
- pip

`sudo apt install python3 python3-pip`


- PyAudio

`pip install pyaudio`


---


## 📱 Usabilidade

### Rodando o Servidor 🔊

O servidor abre uma porta TCP, aceita clientes e transmite o arquivo WAV em blocos:

`python server.py`

### Rodando o Cliente 🎧

O cliente conecta ao servidor e reproduz o áudio à medida que os dados chegam.

`python client.py`


### Resultados

A solução executa o ciclo: carregar WAV → enviar em blocos → receber → decodificar → reproduzir, validando o funcionamento completo do servidor e cliente implementados.

---

## ⛏️ Tecnologias Utilizadas

- Python 3 - linguagem principal
- Sockets TCP - comunicação de rede
- Threads - concorrência simples
- PyAudio - reprodução PCM
- WAV - formato do áudio

