from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    data_dict = original_data.to_dict(orient="records")
else:
    data_dict = data.to_dict(orient="records")
finally:
    item = {}


def change_french_word():
    global item, flip_timer
    window.after_cancel(flip_timer)
    item = random.choice(data_dict)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word_text, text=item["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=card_flip)


def know_words():
    global item, flip_timer
    data_dict.remove(item)
    new_data = pd.DataFrame(data_dict)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    window.after_cancel(flip_timer)
    item = random.choice(data_dict)
    canvas.itemconfig(title, text="French", fill="black")
    canvas.itemconfig(word_text, text=item["French"], fill="black")
    canvas.itemconfig(canvas_image, image=front_image)
    flip_timer = window.after(3000, func=card_flip)


def card_flip():
    canvas.itemconfig(canvas_image, image=back_image)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word_text, text=item["English"], fill="white")


# Create a window object
window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR, padx=50, pady=50)

# Run the function card_flip after 3 seconds
flip_timer = window.after(3000, func=card_flip)

# Create an image
back_image = PhotoImage(file='images/card_back.png')
front_image = PhotoImage(file='images/card_front.png')
canvas = Canvas(width=800, height=526)
canvas_image = canvas.create_image(400, 263, image=front_image)
title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"), fill="black")
word_text = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), fill="black")
canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=cross_image, highlightthickness=0, background=BACKGROUND_COLOR, border=0,
                      command=change_french_word)
wrong_button.grid(row=1, column=0)

right_image = PhotoImage(file='images/right.png')
right_button = Button(image=right_image, highlightthickness=0, background=BACKGROUND_COLOR, border=0,
                      command=know_words)
right_button.grid(row=1, column=1)

change_french_word()

# Set a loop in case the window closes
window.mainloop()
