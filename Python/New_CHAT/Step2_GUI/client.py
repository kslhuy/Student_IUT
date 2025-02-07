from tkinter import Tk, Text, Entry, Button, END
"""
This script creates a simple chat interface using Tkinter.
Classes:
    None
Functions:
    send_message(): Retrieves the message from the input box, clears the input box, and inserts the message into the chat log.
Variables:
    root (Tk): The main window of the Tkinter application.
    chat_log (Text): A Text widget to display the chat log.
    input_box (Entry): An Entry widget to input messages.
    send_button (Button): A Button widget to send the message.
"""

root = Tk()
root.title("Chat")

chat_log = Text(root, height=15, width=50)
chat_log.pack()

input_box = Entry(root, width=40)
input_box.pack()

def send_message():
    message = input_box.get()
    input_box.delete(0, END)
    chat_log.insert(END, f"You: {message}\n")

send_button = Button(root, text="Send", command=send_message)
send_button.pack()

root.mainloop()
