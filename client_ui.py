# Person 1 - GUI / Display
from tkinter import *
from PIL import Image, ImageTk
import io

img_refs = []

def create_main_window():
    root = Tk()
    root.title('Chatroom')
    root.geometry('800x500')
    root.resizable(0,0)
    root.config(background="#5A5353")

    root.columnconfigure(0,weight=100)
    root.rowconfigure(0, weight=95)
    root.rowconfigure(1,weight=5)

    return root

def create_chat_section(root):
    chatF = Frame(root,background="#5A5353")
    chatF.grid(row=0,column=0,sticky='nsew')

    canvas = Canvas(chatF, background="#5A5353")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(chatF, orient="vertical", command=canvas.yview, background="#5A5353")
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    chat_frame = Frame(canvas, background="#5A5353")
    canvas.create_window((0, 0), window=chat_frame, anchor="nw")

    chat_frame.bind("<Configure>", on_configure)

    return canvas, chat_frame

def on_configure(event):
    event.widget.master.configure(scrollregion=event.widget.master.bbox("all"))

def create_text_section(root):
    textF = Frame(root, background='#FFFFFF')
    textF.grid(row=1, column=0, sticky='nsew')

    textF.rowconfigure(0,weight=100)
    textF.columnconfigure(0,weight=90)
    textF.columnconfigure(1,weight=5)
    textF.columnconfigure(2,weight=5)

    textMessage = Entry(textF,border=0,borderwidth=0,relief="flat",highlightthickness=0, foreground='black')
    textMessage.grid(row=0, column=0, sticky='nsew')

    return textF, textMessage

def display_message(chat_frame, canvas, msg):
    lbl = Label(chat_frame, text=msg, anchor="w")
    lbl.pack(anchor="w", pady=5)
    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def display_image(chat_frame, canvas, img_data):
    img = Image.open(io.BytesIO(img_data))
    img.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(img)

    img_refs.append(photo)

    lbl = Label(chat_frame, image=photo, background="#5A5353")
    lbl.pack(anchor="w", pady=5)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def load_button_images():
    imgS = Image.open('sendImg.png')
    img_resizedS = imgS.resize((30, 30), Image.LANCZOS)
    photoS = ImageTk.PhotoImage(img_resizedS)

    imgA = Image.open('attachment.png')
    img_resizedA = imgA.resize((30, 30), Image.LANCZOS)
    photoA = ImageTk.PhotoImage(img_resizedA)

    return photoS, photoA