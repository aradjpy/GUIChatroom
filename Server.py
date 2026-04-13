import socket
import threading

HEADER = 64
PORT = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80)) 
SERVER = s.getsockname()[0]
s.close()
ADD = ("0.0.0.0", PORT)
FORMAT = 'utf-8'
DIS = '!DIS'
clientS = []
oldMessages = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADD)

def handle_client(cnc, add):
    print(f"new connection {add} connected")
    connected = True
    try:
        clientS.append(cnc)
        while connected:
            msgLen_data = cnc.recv(HEADER)
            if not msgLen_data:
                break
            
            msgLen_str = msgLen_data.decode(FORMAT).strip()
            if msgLen_str:
                msgLen = int(msgLen_str) 
                # Receive raw bytes first to check for image prefix
                raw_data = b""
                while len(raw_data) < msgLen:
                    chunk = cnc.recv(min(msgLen - len(raw_data), 4096))
                    if not chunk: break
                    raw_data += chunk

                # Check if it's an image or text
                is_img = raw_data.startswith(b"IMG:")
                
                if not is_img:
                    msg = raw_data.decode(FORMAT)
                    if msg == DIS:
                        connected = False
                    print(f'{add} : {msg}')

                # Broadcast to all
                for client in clientS[:]:
                    try:
                        # Send the same header and raw data
                        client.sendall(msgLen_data)
                        client.sendall(raw_data)
                    except:
                        clientS.remove(client)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cnc in clientS:
            clientS.remove(cnc)
        cnc.close()

def start():
    print(f'Listening on : {SERVER}')
    server.listen()
    while True:
        cnc, add = server.accept()
        thread = threading.Thread(target=handle_client,args=(cnc,add))
        thread.start()
        print(f'Active connections are {threading.active_count() - 1}')
print("starting server")

start()
