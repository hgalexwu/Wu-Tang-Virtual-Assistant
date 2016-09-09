import wolframalpha, wikipedia, Tkinter, PIL, os
from PIL import Image, ImageTk
import pyttsx
import threading


# WolframAlpha developer's API APP_ID
APP_ID = "LG74T5-V98P5V55TK"


def get_answer(event):
    # 1.0 means first line, 0th character
    global answer
    answer = initialize_assistant(event.widget.get())
    # Clear text
    event.widget.delete(0, "end")
    show_answer(answer)


def show_answer(answer):
    label1.grid_forget()
    entry.grid_forget()

    global label2
    label2 = Tkinter.Label(root, text="The answer you are looking for is:")
    label2.grid(column=1, row=0, sticky=Tkinter.S, padx=5)

    global response
    response = Tkinter.Label(root, text=answer, wraplength=1000)
    response.grid(column=1, row=1, sticky=Tkinter.N)

    global button
    button = Tkinter.Button(root, text="Ask another question", command=return_main)
    button.grid(column=1, row=2, sticky=Tkinter.S)
    t = threading.Thread(target=speak)
    t.start()

def return_main():
    label2.destroy()
    response.destroy()
    button.destroy()

    label1.grid(column=1, row=0, sticky=Tkinter.W+Tkinter.S)
    entry.grid(column=1, row=1, sticky=Tkinter.N)


def initialize_assistant(input):
    global result
    # try to get a wolframalpha result first, then a wikipedia result if it doesn't work
    try:
        # WolframAlpha result
        client = wolframalpha.Client(APP_ID)
        result = next(client.query(input).results).text
        return result
    except:
        if (len(input) > 3) and input.split(" ")[0].lower() == "who" and input.split(" ")[1].lower() == "is":
            query = ""
            for word in input.split(" "):
                if word.lower() != "who" and word.lower() != "is":
                    query += word + " "
            result = wikipedia.summary(query)
        else:
            result = wikipedia.summary(input)
        # Wikipedia result
        return result


def create_gui():

    global root
    root = Tkinter.Tk()
    # Make window non resizable
    root.resizable(width=False, height=False)

    # Set Wu tang avatar image
    img = Image.open("kid.jpg")
    img = img.resize((120, 150), Image.ANTIALIAS)
    img = PIL.ImageTk.PhotoImage(img)
    panel1 = Tkinter.Label(root, image=img)
    panel1.grid(column=0, rowspan=2)

    # Set Title
    root.title("Wu Tang, the Python Digital Assistant")

    global label1
    label1 = Tkinter.Label(root, text="Hello. I am Wu Tang\nI'm the World's Greatest Digital Assistant\nHow can I help you today?")
    label1.grid(column=1, row=0, padx=5, sticky=Tkinter.W+Tkinter.S)

    global entry
    entry = Tkinter.Entry(root)
    entry.bind('<Return>', get_answer)
    entry.grid(column=1, row=1, sticky=Tkinter.N)

    # Start GUI
    root.mainloop()


def speak():
    engine = pyttsx.init()
    engine.say(answer)
    engine.startLoop()

if __name__ == '__main__':
    create_gui()



