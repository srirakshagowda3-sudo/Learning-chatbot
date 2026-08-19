import tkinter as tk
from tkinter import scrolledtext

window = tk.Tk()
window.title("SriGPT")
window.geometry("800x700")
window.minsize(600, 500)
window.configure(bg="#F4F6F8")

window.rowconfigure(1, weight=1)
window.columnconfigure(0, weight=1)

title = tk.Label(
    window,
    text="SriGPT",
    font=("Arial", 24, "bold"),
    bg="#F4F6F8",
    fg="#222222"
)
title.grid(row=0, column=0, pady=15)

chat_box = scrolledtext.ScrolledText(
    window,
    font=("Arial", 12),
    wrap=tk.WORD,
    bg="white"
)
chat_box.grid(
    row=1,
    column=0,
    padx=20,
    pady=10,
    sticky="nsew"
)

chat_box.tag_config("user", foreground="#16803C")
chat_box.tag_config("bot", foreground="#2457C5")

chat_box.insert(
    tk.END,
    "SriGPT: Hello! I am SriGPT. Ask me anything about programming or tell me how you feel.\n\n",
    "bot"
)


def chatbot_reply(message):

    message = message.lower().strip()

    if "python" in message:
        return "Python is a high-level programming language known for its simple syntax. It is used for automation, web development, data science and artificial intelligence."

    elif "java" in message:
        return "Java is an object-oriented programming language widely used for applications, backend systems and Android development."

    elif "c++" in message or "cpp" in message:
        return "C++ is a powerful programming language based on C. It supports object-oriented programming and is commonly used for software and game development."

    elif message == "c" or "c language" in message:
        return "C is a procedural programming language widely used for system programming, embedded systems and learning programming fundamentals."

    elif "pointer" in message:
        return "A pointer is a variable that stores the memory address of another variable. Pointers are especially important in C and C++."

    elif "loop" in message:
        return "A loop repeats a block of code. Common types include for and while loops."

    elif "function" in message:
        return "A function is a reusable block of code designed to perform a particular task."

    elif "variable" in message:
        return "A variable is a named storage location used to store a value."

    elif "sad" in message or "bad" in message or "unhappy" in message:
        return "I'm sorry you're feeling this way. Do you want to tell me what happened?"

    elif "happy" in message or "feeling good" in message or "great" in message:
        return "I'm glad you're feeling good. What made your day better?"

    elif "angry" in message or "mad" in message:
        return "It sounds like something is bothering you. Want to talk about it?"

    elif "stressed" in message or "stress" in message:
        return "It sounds like you have a lot on your mind. Take a breath and tell me what's troubling you."

    elif "tired" in message or "exhausted" in message:
        return "You sound tired. Take some time to rest."

    elif "talk to me" in message:
        return "Of course. I'm here to talk. What's on your mind?"

    elif "bored" in message:
        return "Let's change that. We can talk about movies, studies, technology or hobbies."

    elif "how are you" in message:
        return "I'm doing well. Thanks for asking. How are you?"

    elif "your name" in message or "who are you" in message:
        return "I am SriGPT, your Python chatbot."

    elif "thank" in message:
        return "You're welcome. I'm happy to help."

    elif message in ["hi", "hello", "hey", "hii", "hiii"]:
        return "Hello! It is nice to talk with you."

    elif "bye" in message:
        return "Goodbye. Take care and have a great day."

    elif "joke" in message:
        return "Why did the computer go to the doctor? Because it had a virus."

    else:
        return "I'm listening. Tell me more about that."


def send_message(event=None):

    message = message_entry.get().strip()

    if message == "":
        return

    chat_box.insert(
        tk.END,
        "You: " + message + "\n",
        "user"
    )

    reply = chatbot_reply(message)

    chat_box.insert(
        tk.END,
        "SriGPT: " + reply + "\n\n",
        "bot"
    )

    message_entry.delete(0, tk.END)
    chat_box.see(tk.END)


bottom_frame = tk.Frame(
    window,
    bg="#F4F6F8"
)

bottom_frame.grid(
    row=2,
    column=0,
    sticky="ew",
    padx=20,
    pady=15
)

bottom_frame.columnconfigure(0, weight=1)

message_entry = tk.Entry(
    bottom_frame,
    font=("Arial", 13)
)

message_entry.grid(
    row=0,
    column=0,
    sticky="ew",
    ipady=10
)

send_button = tk.Button(
    bottom_frame,
    text="Send",
    font=("Arial", 11, "bold"),
    command=send_message
)

send_button.grid(
    row=0,
    column=1,
    padx=(10, 0),
    ipadx=20,
    ipady=7
)

message_entry.bind("<Return>", send_message)

message_entry.focus()

window.mainloop()