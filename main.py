from tkinter import *
import pandas
import random

# -------------------------- CONSTANTS --------------------------- #
BACKGROUND_COLOR = "#B1DDC6"
FONT_TYPE = "Ariel"
current_word = None
SOURCE_WORD = "Word"
ORIGINAL_WORD_LIST = "150-topic-vocab.csv"

# -------------------------- READ CSV DATA WITH PANDAS  --------------------------- #
try:
    word_list = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv(f"./data/{ORIGINAL_WORD_LIST}")
    data.to_csv("./data/words_to_learn.csv", index=False)
    DATABASE = pandas.read_csv("./data/words_to_learn.csv").to_dict(orient="records")
else:
    DATABASE = word_list.to_dict(orient="records")


# -------------------------- GENERATE RANDOM CARD  --------------------------- #
def generate_card():
    # Save newly generated word to a global var
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(DATABASE)

    canvas.itemconfig(word_front, text=current_word[SOURCE_WORD], fill="black")
    canvas.itemconfig(card_side, image=card_front_image)
    # Temporarily hide the backside
    canvas.itemconfig(word_back, text="")
    canvas.itemconfig(meaning, text="")
    canvas.itemconfig(ex_sentence, text="")

    flip_timer = window.after(3000, flip_card)


# -------------------------- FLIP THE CARD  --------------------------- #
def flip_card():
    global current_word
    # Temporarily hide the front side
    canvas.itemconfig(word_front, text="")

    canvas.itemconfig(card_side, image=card_back_image)
    canvas.itemconfig(word_back, text=current_word["Word"], fill="white")
    canvas.itemconfig(meaning, text=current_word["Meaning"], fill="white")
    canvas.itemconfig(ex_sentence, text=f"Ex: {current_word['Sentence']}", fill="white")


# -------------------------- SAVE YOUR PROGRESS  --------------------------- #
def learned_word():
    # Remove learnt word and update the DATABASE
    global current_word
    DATABASE.remove(current_word)
    updated_data = pandas.DataFrame.from_dict(DATABASE)
    updated_data.to_csv("./data/words_to_learn.csv", index=False)
    # Generate new word on the screen
    generate_card()


# -------------------------- UI SETUP --------------------------- #
window = Tk()
window.title("Flask Card")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
flip_timer = window.after(3500, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_image = PhotoImage(file="./images/card_front.png")  # Display French
card_back_image = PhotoImage(file="./images/card_back.png")  # Display English equivalent
card_side = canvas.create_image(400, 263, image=card_front_image)

word_front = canvas.create_text(400, 250, text="", width=700, font=(FONT_TYPE, 35, "italic", "bold"), justify=CENTER)
word_back = canvas.create_text(400, 100, text="", width=700, font=(FONT_TYPE, 28, "italic", "bold"), justify=CENTER)
meaning = canvas.create_text(400, 200, text="", width=700, font=(FONT_TYPE, 20, "italic"), justify=CENTER)
ex_sentence = canvas.create_text(400, 320, text="", width=700, font=(FONT_TYPE, 20), justify=CENTER)

canvas.grid(row=0, column=0, columnspan=2)

# Right and Wrong Button
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=generate_card)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=learned_word)
right_button.grid(row=1, column=1)

generate_card()
window.mainloop()
