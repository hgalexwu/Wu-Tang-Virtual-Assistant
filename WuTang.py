import wolframalpha, wikipedia, Tkinter, PIL, pyttsx, threading
from PIL import Image, ImageTk
import speech_recognition as sr

# WolframAlpha developer's API APP_ID
APP_ID = "LG74T5-V98P5V55TK"


# Get the answer after clicking on "enter"
def get_answer(event):
    # get text from text box (entry) and pass it to a function
    global answer
    answer = initialize_assistant(event.widget.get())
    # Clear text
    event.widget.delete(0, "end")
    # show the answer on the GUI
    show_answer(answer)


# Show answer on GUI
def show_answer(answer):
    # Temporarily forget the intro text and the text box
    label1.grid_forget()
    entry.grid_forget()

    # Create a new intro text
    global label2
    label2 = Tkinter.Label(root, text="The answer you are looking for is:")
    label2.grid(column=1, row=0, sticky=Tkinter.S, padx=5)

    # Create a response text
    global response
    response = Tkinter.Label(root, text=answer, wraplength=1000)
    response.grid(column=1, row=1, sticky=Tkinter.N)

    # Create a button that returns to main GUI screen when clicked on
    global button
    button = Tkinter.Button(root, text="Ask another question", command=return_main)
    button.grid(column=1, row=2, sticky=Tkinter.S)

    # Start a new thread that calls function speak and that will "text to voice" the result
    # Use of a thread because the function runandwait blocks so it would stop the GUI
    t = threading.Thread(target=speak)
    t.start()


# Return to the main GUI
def return_main():
    # Destroy the response, the intro text and the button
    label2.destroy()
    response.destroy()
    button.destroy()

    # ReDisplay the intro text and the text box for queries
    label1.grid(column=1, row=0, sticky=Tkinter.W+Tkinter.S)
    entry.grid(column=1, row=1, sticky=Tkinter.N)


# Speech recognizer function that is invoked when clicked on button
def speech_recognizer():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            entry.insert(0, r.recognize_google(audio))
        except sr.UnknownValueError:
            show_answer("Sorry, Google Speech recognition couldn't understand the audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Initialize the assistant and send in the input
def initialize_assistant(input):
    global result
    # try to get a wolframalpha result first, then a wikipedia result if it doesn't work
    try:
        # WolframAlpha result
        client = wolframalpha.Client(APP_ID)
        result = next(client.query(input).results).text
        return result
    except:
        # For queries such as "who is thomas edison", there are a few bugs and this little tweak fixes it
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


# Create GUI function
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

    # Create intro text
    global label1
    label1 = Tkinter.Label(root, text="Hello. I am Wu Tang\nI'm the World's Greatest Digital Assistant\nHow can I help you today?")
    label1.grid(column=1, row=0, padx=5, sticky=Tkinter.W+Tkinter.S)

    # Create text box
    global entry
    entry = Tkinter.Entry(root)
    entry.bind('<Return>', get_answer)
    entry.grid(column=1, row=1, sticky=Tkinter.N)

    # Create speech button
    global speechButton
    speechButton = Tkinter.Button(root, text="Use Voice", command=speech_recognizer)
    speechButton.grid(column=1, row=2, sticky=Tkinter.S)

    # Start GUI
    root.mainloop()


# Speak
def speak():
    # Initialize speech engine
    engine = pyttsx.init()
    # Queue the answer
    engine.say(answer)
    # Speak
    engine.startLoop()


if __name__ == '__main__':
    create_gui()



