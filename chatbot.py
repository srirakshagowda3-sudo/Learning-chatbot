name = input("you: your name ?")
print("nice to meet you," + name)
print("nice to meet you," +name + " !type bye to leave")
message = input(f"{name}:  what do you want to say ? ")
def chat(message):
    message = message.lower()
    if "hello" in message or "hi" in message:
        print("bot : hello" + name + "!")
    elif "joke" in message:
        print("bot : why did the chicken cross the road? to get to the other side !")
    else:
        print("bot : i am not sure how to answer that.")
reply = chat(message)
print("bot : ",reply)

