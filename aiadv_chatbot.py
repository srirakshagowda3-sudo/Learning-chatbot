import tkinter as tk
from tkinter import scrolledtext
from google import genai
from google.genai import types
import json
import os
import threading
from datetime import datetime, timezone, timedelta


# ==========================================
# GEMINI CONFIGURATION
# ==========================================

API_KEY = ""

client = genai.Client(
    api_key=API_KEY
)

MODEL = "gemini-3.6-flash"

MEMORY_FILE = "memory.json"

PDF_FILE =  "t john ai bot file.pdf"

# ==========================================
# UPLOAD KNOWLEDGE BASE
# ==========================================

try:

    knowledge_file = client.files.upload(
        file=PDF_FILE
    )

    print("Knowledge base uploaded successfully.")

except Exception as e:

    knowledge_file = None

    print("Knowledge base upload error:", e)


# ==========================================
# LOCAL TIME TOOL
# ==========================================

def get_local_time() -> str:
    """
    Gets the current local time and date in India.
    """

    india_timezone = timezone(
        timedelta(
            hours=5,
            minutes=30
        )
    )

    now = datetime.now(
        india_timezone
    )

    return now.strftime(
        "%I:%M %p, %A, %d %B %Y"
    )


# ==========================================
# CALCULATOR TOOL
# ==========================================

def calculator(expression: str) -> str:
    """
    Calculates a mathematical expression.

    Args:
        expression: A mathematical expression such as
        25 * 48 or (100 + 50) / 2.
    """

    try:

        allowed_characters = (
            "0123456789"
            "+-*/().% "
        )

        if not expression:

            return "I couldn't calculate that."

        if not all(
            character in allowed_characters
            for character in expression
        ):

            return "Invalid mathematical expression."

        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:

        return "I couldn't calculate that."


# ==========================================
# SRI GPT SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """

You are SriGPT, a friendly AI chatbot.

PERSONALITY:

- Friendly
- Supportive
- Casual when appropriate
- Funny when appropriate
- Clear and easy to understand
- Helpful with coding
- Good at Python, Java, C and C++
- Give working code when appropriate
- Explain things step-by-step when needed
- Never be rude or insulting
- Remember useful information from previous conversations


COMMUNICATION STYLE:

Match the user's communication style naturally.

If the user uses Gen-Z slang, abbreviations,
or very casual language, respond with a similar
level of casual Gen-Z language.

If the user speaks normally or formally,
respond normally and clearly.

Do not force Gen-Z slang.

Do not use slang just because the chatbot
is called SriGPT.

Do not use emojis.

Always prioritize the user's current message.


PERMANENT MEMORY:

The application provides previous conversations
from memory.json.

Use previous conversation information when
it is useful.

Do not claim to remember something that is
not present in the provided conversation history.


KNOWLEDGE BASE:

You have access to a T. John Group of Institutions
knowledge-base PDF.

When the user asks about:

- T. John Group of Institutions
- T. John College
- Courses
- Departments
- Campus
- Facilities
- College information

use the provided PDF as the primary source.

Do not invent college-specific information.

If the requested information is not available
in the PDF, clearly say that it is not available
in the current knowledge base.

For current information such as admission dates,
fees, events or current course availability,
tell the user to verify the official T. John website.


TOOLS:

You have two tools:

1. get_local_time
2. calculator

If the user asks for the current time,
current date and time, or similar information,
use get_local_time.

If the user asks for a mathematical calculation,
use calculator.

The user should NEVER need to type a Python
function name.

For example, if the user says:

"time"

use get_local_time automatically.

If the user says:

"25 * 48"

use calculator automatically.

Return the result naturally to the user.
"""


# ==========================================
# CENTRAL CONFIG
# ==========================================

config = types.GenerateContentConfig(

    system_instruction=SYSTEM_PROMPT,

    tools=[
        get_local_time,
        calculator
    ]
)


# ==========================================
# PERMANENT MEMORY
# ==========================================

def load_memory():

    if not os.path.exists(
        MEMORY_FILE
    ):

        return []

    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_memory():

    try:

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                conversation_history,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:

        print(
            "Memory save error:",
            e
        )


conversation_history = load_memory()


# ==========================================
# BUILD MEMORY PROMPT
# ==========================================

def build_prompt(user_message):

    prompt = ""

    prompt += "Previous conversation:\n\n"

    recent_history = conversation_history[-30:]

    for message in recent_history:

        if message["role"] == "user":

            prompt += (
                "User: "
                + message["content"]
                + "\n"
            )

        elif message["role"] == "assistant":

            prompt += (
                "SriGPT: "
                + message["content"]
                + "\n"
            )

    prompt += "\nCurrent user message:\n"

    prompt += user_message

    return prompt


# ==========================================
# GEMINI CHAT RESPONSE
# ==========================================

def get_response(user_message):

    try:

        # Build memory + current message
        prompt = build_prompt(
            user_message
        )


        # ======================================
        # CREATE GEMINI CHAT
        # ======================================

        chat = client.chats.create(

            model=MODEL,

            config=config

        )


        # ======================================
        # SEND MESSAGE
        # ======================================

        if knowledge_file is not None:

            response = chat.send_message(

                message=[
                    knowledge_file,
                    prompt
                ]

            )

        else:

            response = chat.send_message(

                message=prompt

            )


        # ======================================
        # RETURN RESPONSE
        # ======================================

        if response.text:

            return response.text

        return (
            "I couldn't generate a response."
        )


    except Exception as e:

        return (
            "Oops, something went wrong:\n"
            + str(e)
        )


# ==========================================
# DISPLAY RESPONSE
# ==========================================

def display_response(
    user_message,
    bot_response
):

    thinking_label.config(
        text=""
    )


    # ======================================
    # SHOW BOT RESPONSE
    # ======================================

    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.insert(
        tk.END,
        "SriGPT: ",
        "bot_name"
    )

    chat_box.insert(
        tk.END,
        bot_response + "\n\n",
        "bot_text"
    )

    chat_box.config(
        state=tk.DISABLED
    )

    chat_box.see(
        tk.END
    )


    # ======================================
    # SAVE USER MESSAGE
    # ======================================

    conversation_history.append({

        "role": "user",

        "content": user_message

    })


    # ======================================
    # SAVE BOT RESPONSE
    # ======================================

    conversation_history.append({

        "role": "assistant",

        "content": bot_response

    })


    # ======================================
    # SAVE MEMORY FILE
    # ======================================

    save_memory()


    # ======================================
    # ENABLE INPUT
    # ======================================

    input_box.config(
        state=tk.NORMAL
    )

    send_button.config(
        state=tk.NORMAL
    )

    input_box.focus()


# ==========================================
# BACKGROUND RESPONSE
# ==========================================

def generate_response(
    user_message
):

    bot_response = get_response(
        user_message
    )

    window.after(

        0,

        lambda: display_response(

            user_message,

            bot_response

        )

    )


# ==========================================
# SEND MESSAGE
# ==========================================

def send_message(event=None):

    user_message = input_box.get(
        "1.0",
        tk.END
    ).strip()


    if not user_message:

        return "break"


    # ======================================
    # SHOW USER MESSAGE
    # ======================================

    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.insert(
        tk.END,
        "You: ",
        "user_name"
    )

    chat_box.insert(
        tk.END,
        user_message + "\n\n",
        "user_text"
    )

    chat_box.config(
        state=tk.DISABLED
    )

    chat_box.see(
        tk.END
    )


    # ======================================
    # CLEAR INPUT
    # ======================================

    input_box.delete(
        "1.0",
        tk.END
    )


    # ======================================
    # THINKING
    # ======================================

    thinking_label.config(
        text="SriGPT is thinking..."
    )


    # ======================================
    # DISABLE INPUT
    # ======================================

    input_box.config(
        state=tk.DISABLED
    )

    send_button.config(
        state=tk.DISABLED
    )


    # ======================================
    # BACKGROUND THREAD
    # ======================================

    thread = threading.Thread(

        target=generate_response,

        args=(user_message,),

        daemon=True

    )

    thread.start()

    return "break"


# ==========================================
# CLEAR MEMORY
# ==========================================

def clear_memory():

    global conversation_history

    conversation_history = []


    if os.path.exists(
        MEMORY_FILE
    ):

        try:

            os.remove(
                MEMORY_FILE
            )

        except Exception as e:

            print(
                "Could not delete memory:",
                e
            )


    chat_box.config(
        state=tk.NORMAL
    )

    chat_box.delete(
        "1.0",
        tk.END
    )

    chat_box.insert(
        tk.END,
        "SriGPT: ",
        "bot_name"
    )

    chat_box.insert(
        tk.END,
        "Memory cleared. Fresh start.\n\n",
        "bot_text"
    )

    chat_box.config(
        state=tk.DISABLED
    )


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title(
    "SriGPT - GenZ AI Chatbot"
)

window.geometry(
    "700x700"
)

window.configure(
    bg="#1e1e1e"
)


# ==========================================
# TITLE
# ==========================================

title = tk.Label(

    window,

    text="SriGPT",

    font=(
        "Arial",
        24,
        "bold"
    ),

    bg="#1e1e1e",

    fg="white"

)

title.pack(
    pady=(15, 3)
)


# ==========================================
# SUBTITLE
# ==========================================

subtitle = tk.Label(

    window,

    text="Your AI buddy",

    font=(
        "Arial",
        11
    ),

    bg="#1e1e1e",

    fg="lightgray"

)

subtitle.pack(
    pady=(0, 5)
)


# ==========================================
# CHAT BOX
# ==========================================

chat_box = scrolledtext.ScrolledText(

    window,

    wrap=tk.WORD,

    font=(
        "Arial",
        12
    ),

    bg="#252526",

    fg="white",

    insertbackground="white",

    state=tk.DISABLED

)

chat_box.pack(

    padx=15,

    pady=10,

    fill=tk.BOTH,

    expand=True

)


# ==========================================
# TEXT COLORS
# ==========================================

chat_box.tag_config(

    "user_name",

    foreground="#4FC3F7",

    font=(
        "Arial",
        12,
        "bold"
    )

)

chat_box.tag_config(

    "user_text",

    foreground="white"

)

chat_box.tag_config(

    "bot_name",

    foreground="#81C784",

    font=(
        "Arial",
        12,
        "bold"
    )

)

chat_box.tag_config(

    "bot_text",

    foreground="white"

)


# ==========================================
# THINKING LABEL
# ==========================================

thinking_label = tk.Label(

    window,

    text="",

    font=(
        "Arial",
        11,
        "italic"
    ),

    bg="#1e1e1e",

    fg="lightgray"

)

thinking_label.pack(
    pady=(0, 5)
)


# ==========================================
# INPUT FRAME
# ==========================================

input_frame = tk.Frame(

    window,

    bg="#1e1e1e"

)

input_frame.pack(

    fill=tk.X,

    padx=15,

    pady=(5, 10)

)


# ==========================================
# INPUT BOX
# ==========================================

input_box = tk.Text(

    input_frame,

    height=3,

    font=(
        "Arial",
        12
    ),

    bg="#252526",

    fg="white",

    insertbackground="white",

    wrap=tk.WORD

)

input_box.pack(

    side=tk.LEFT,

    fill=tk.BOTH,

    expand=True,

    padx=(0, 10)

)


# ==========================================
# SEND BUTTON
# ==========================================

send_button = tk.Button(

    input_frame,

    text="Send",

    font=(
        "Arial",
        12,
        "bold"
    ),

    bg="#4CAF50",

    fg="white",

    activebackground="#45a049",

    activeforeground="white",

    padx=25,

    pady=12,

    command=send_message

)

send_button.pack(
    side=tk.RIGHT
)


# ==========================================
# CLEAR MEMORY BUTTON
# ==========================================

clear_button = tk.Button(

    window,

    text="Clear Memory",

    font=(
        "Arial",
        10
    ),

    bg="#333333",

    fg="white",

    activebackground="#444444",

    activeforeground="white",

    command=clear_memory

)

clear_button.pack(
    pady=(0, 10)
)


# ==========================================
# ENTER KEY
# ==========================================

input_box.bind(
    "<Return>",
    send_message
)


# ==========================================
# START MESSAGE
# ==========================================

chat_box.config(
    state=tk.NORMAL
)


if conversation_history:

    chat_box.insert(

        tk.END,

        "SriGPT: ",

        "bot_name"

    )

    chat_box.insert(

        tk.END,

        "Welcome back. I remember our previous chats.\n\n",

        "bot_text"

    )

else:

    chat_box.insert(

        tk.END,

        "SriGPT: ",

        "bot_name"

    )

    chat_box.insert(

        tk.END,

        "Yo! I'm SriGPT. What's up? Ask me anything or throw some code at me.\n\n",

        "bot_text"

    )


chat_box.config(
    state=tk.DISABLED
)


# ==========================================
# START APPLICATION
# ==========================================

input_box.focus()

window.mainloop()