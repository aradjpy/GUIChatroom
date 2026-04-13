# Person 3 - Media / Buttons

from tkinter import Button
from tkinter import filedialog as fd
from tkinter import simpledialog as sd

HEADER = 64
FORMAT = 'utf-8'

def ask_client_name():
    CliName = sd.askstring(title='Name', prompt='Please enter your name')
    print(CliName)
    return CliName

def attach_file(client):
    fileP = fd.askopenfilename(
        title='Select a file',
        filetypes=[("images", "*.png *.jpg *.jpeg")]
    )

    if fileP:
        with open(fileP, "rb") as f:
            img_data = f.read()

        payload = b"IMG:" + img_data
        payload_len = len(payload)

        header = str(payload_len).encode(FORMAT)
        header = header + b' ' * (HEADER - len(header))

        client.sendall(header)
        client.sendall(payload)


def create_send_button(parent, image_obj, client, textMessage, CliName, call_send):
    def send_action():
        call_send(client, textMessage, CliName)

    sendT = Button(parent, bg='#FFFFFF', image=image_obj, width=1, height=1, command=send_action)
    sendT.image = image_obj
    sendT.grid(row=0, column=2, sticky='nsew')

def create_attach_button(parent, image_obj, client):
    def attach_action():
        attach_file(client)

    sendA = Button(parent, bg='#FFFFFF', image=image_obj, width=1, height=1, command=attach_action)
    sendA.image = image_obj
    sendA.grid(row=0, column=1, sticky='nsew', padx=5)