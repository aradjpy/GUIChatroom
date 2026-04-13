# ==============================
# Main File
# ==============================

import threading

from client_ui import *
from client_network import *
from client_media import *

# Build UI
root = create_main_window()
canvas, chat_frame = create_chat_section(root)
textF, textMessage = create_text_section(root)

# Networking
client = create_client()

# Name
CliName = ask_client_name()

# Images
photoS, photoA = load_button_images()

# Buttons
create_send_button(textF, photoS, client, textMessage, CliName, call_send)
create_attach_button(textF, photoA, client)

# Listener thread
thread = threading.Thread(
    target=listen_for_messages,
    args=(client, chat_frame, canvas, display_message, display_image),
    daemon=True
)
thread.start()

# Run
root.mainloop()