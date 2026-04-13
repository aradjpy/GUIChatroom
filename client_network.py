# Person 2 - Networking

import socket as st
import time

HEADER = 64
PORT = 8080
SERVER = '10.0.0.98'
ADD = (SERVER, PORT)
FORMAT = 'utf-8'
DIS = '!DIS'

def create_client():
    client = st.socket(st.AF_INET, st.SOCK_STREAM)
    client.connect(ADD)
    return client

def listen_for_messages(client, chat_frame, canvas, display_message, display_image):
    while True:
        try:
            msgLen_data = client.recv(HEADER).decode(FORMAT).strip()

            if msgLen_data:
                msgLen = int(msgLen_data)
                data = b""

                while len(data) < msgLen:
                    chunk = client.recv(min(msgLen - len(data), 4096))
                    if not chunk:
                        break
                    data += chunk

                if data.startswith(b"IMG:"):
                    image_bytes = data[4:]
                    display_image(chat_frame, canvas, image_bytes)
                else:
                    display_message(chat_frame, canvas, data.decode(FORMAT))

        except Exception as e:
            print("Error receiving:", e)
            break

def send_message(client, CliName, msg):
    msg = '~' + CliName + ': ' + msg + '\nAt: ' + str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5])
    messg = msg.encode(FORMAT)

    msgLen = len(messg)
    sendLen = str(msgLen).encode(FORMAT)
    sendLen = sendLen + b' ' * (HEADER - len(sendLen))

    client.send(sendLen)
    client.send(messg)

def call_send(client, textMessage, CliName):
    sentM = str(textMessage.get())
    send_message(client, CliName, sentM)
    textMessage.delete(0, 'end')