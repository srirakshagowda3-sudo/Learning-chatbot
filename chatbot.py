import tkinter as tk
from tkinter import scrolledtext

window = tk.Tk()
window.title("My Chatbot")
window.geometry("500x600")

# Heading
title = tk.Label(
    window,
    text="My Chatbot",
    font=("Arial", 18, "bold")
)
title.pack(pady=10)

# Chat area
chat_box = scrolledtext.ScrolledText(
    window,
    width=55,
    height=25,
    wrap=tk.WORD
)
chat_box.pack(padx=10, pady=10)

chat_box.insert(tk.END, "Bot: Hello! I am your chatbot.\n")
chat_box.insert(tk.END, "Bot: What is your name?\n\n")

# Name input
name_entry = tk.Entry(window, width=40)
name_entry.pack(pady=5)

def start_chat():
    name = name_entry.get()

    if name == "":
        chat_box.insert(tk.END, "Bot: Please enter your name.\n")
    else:
        chat_box.insert(tk.END, "You: " + name + "\n")
        chat_box.insert(tk.END, "Bot: Nice to meet you, " + name + "!\n\n")
        name_entry.config(state="disabled")
        name_button.config(state="disabled")

name_button = tk.Button(
    window,
    text="Enter Name",
    command=start_chat
)
name_button.pack(pady=5)

# Message input
message_entry = tk.Entry(window, width=40)
message_entry.pack(pady=10)

def chatbot_message():
    message = message_entry.get().lower()
    name = name_entry.get()

    if message == "":
        return

    if "hello" in message or "hi" in message:
        reply = "Hello " + name + "! How are you?"
    elif "how are you" in message:
        reply = "I'm doing great! Thanks for asking."
    elif "your name" in message:
        reply = "I am My Chatbot, your simple AI assistant."
    elif "joke" in message:
        reply = "Why did the chicken cross the road? To get to the other side."
    elif "thank" in message:
        reply = "You're welcome!"
    elif "who are you" in message:
        reply = "I am a simple rule-based chatbot created using Python."
    elif "bye" in message:
        reply = "Goodbye " + name + "! Have a great day!"
    else:
        reply = "I'm not sure how to answer that, but I'm still learning."

    chat_box.insert(tk.END, "You: " + message_entry.get() + "\n")
    chat_box.insert(tk.END, "Bot: " + reply + "\n\n")

    message_entry.delete(0, tk.END)
    chat_box.see(tk.END)

send_button = tk.Button(
    window,
    text="Send",
    command=chatbot_message
)
send_button.pack(pady=5)

window.mainloop()