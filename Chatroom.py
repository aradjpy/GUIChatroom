from tkinter import *
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd

import socket as st
from PIL import Image, ImageTk
import threading
import time
import io

HEADER = 64
PORT = 8080
SERVER = '172.20.10.5' # 172.20.10.5
ADD = (SERVER, PORT)
FORMAT = 'utf-8'
DIS = '!DIS'
sentM = ''

client = st.socket(st.AF_INET, st.SOCK_STREAM)
client.connect(ADD)

img_refs = []

root = Tk()
root.title('Chatroom')
root.geometry('800x500')
root.resizable(0,0)
root.config(background="#5A5353")

CliName = sd.askstring(title='Name', prompt='Please enter your name')
print(CliName)


root.columnconfigure(0,weight=100)
root.rowconfigure(0, weight=95)
root.rowconfigure(1,weight=5)

chatF = Frame(root,background="#5A5353")
chatF.grid(row=0,column=0,sticky='nsew')

canvas = Canvas(chatF, background="#5A5353")
canvas.pack(side="left", fill="both", expand=True)

scrollbar = Scrollbar(chatF, orient="vertical", command=canvas.yview, background="#5A5353")
scrollbar.pack(side="right", fill="y")

canvas.configure(yscrollcommand=scrollbar.set)

chat_frame = Frame(canvas, background="#5A5353")

canvas.create_window((0, 0), window=chat_frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

chat_frame.bind("<Configure>", on_configure)

def listenForMessages():
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
                    displayImage(image_bytes)
                else:
                    displayMessage(data.decode(FORMAT))
        except Exception as e:
            print(f"Error receiving: {e}")
            break

def displayMessage(msg):
    lbl = Label(chat_frame, text=msg, anchor="w")
    lbl.pack(anchor="w", pady=5)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def displayImage(img_data):
    img = Image.open(io.BytesIO(img_data))
    img.thumbnail((200, 200)) 
    photo = ImageTk.PhotoImage(img)
    img_refs.append(photo) 
    lbl = Label(chat_frame, image=photo, background="#5A5353")
    lbl.pack(anchor="w", pady=5)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def send(msg):
    msg = '~' + CliName + ': ' + msg + '\nAt: ' + str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5])
    messg = msg.encode(FORMAT)
    msgLen = len(messg) 
    sendLen = str(msgLen).encode(FORMAT)
    sendLen = sendLen + b' ' * (HEADER - len(sendLen))
    
    client.send(sendLen)
    client.send(messg)

def callSend():
    global textMessage
    sentM = str(textMessage.get())
    send(sentM)
    textMessage.delete(0,tk.END)

def attachFile():
    fileP = fd.askopenfilename(
        title='Select a file',
        filetypes=[("images", "*.png *.jpg *.jpeg")]
    )
    if fileP:
        with open(fileP, "rb") as f:
            img_data = f.read()
        
        payload = b"IMG:" + img_data
        payload_len = len(payload)
        
        header = str(payload_len).encode(FORMAT).ljust(HEADER)
        client.sendall(header)
        client.sendall(payload)

textF = Frame(root, background='#FFFFFF')
textF.grid(row=1, column=0, sticky='nsew')

textF.rowconfigure(0,weight=100)
textF.columnconfigure(0,weight=90)
textF.columnconfigure(1,weight=5)
textF.columnconfigure(2,weight=5)

textMessage = Entry(textF,border=0,borderwidth=0,relief="flat",highlightthickness=0, foreground='black')
textMessage.grid(row=0, column=0, sticky='nsew')

imgS = Image.open('sendImg.png')
img_resizedS = imgS.resize((30, 30), Image.LANCZOS)
photoS = ImageTk.PhotoImage(img_resizedS)

sendT = Button(textF,bg='#FFFFFF', image=photoS,width=1,height=1,command=callSend)
sendT.image = photoS
sendT.grid(row=0, column=2, sticky='nsew')

imgA = Image.open('attachment.png')
img_resizedA = imgA.resize((30, 30), Image.LANCZOS)
photoA = ImageTk.PhotoImage(img_resizedA)

sendA = Button(textF,bg='#FFFFFF', image=photoA,width=1,height=1,command=attachFile)
sendA.image = photoA
sendA.grid(row=0, column=1, sticky='nsew', padx=5)

thread = threading.Thread(target=listenForMessages, daemon=True)
thread.start()
root.mainloop()
