import pandas

BACKGROUND_COLOR = "#B1DDC6"
import pandas as pd
from tkinter import *
import random
current_card = {}
to_learn = []
#--------------------- CSV ----------------------#
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pd.read_csv("data/french_words.csv")
    to_learn = data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")
    print(type(to_learn))

def next_card():
    global current_card
    global flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(carrd_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = windows.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(carrd_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    rest_data = pandas.DataFrame(to_learn)
    print(len(rest_data))
    rest_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

#--------------------- UI -----------------------#
windows = Tk()
windows.title("Flashy")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000, func=flip_card)


#Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background =canvas.create_image(400,263,image=card_front_img)
#Labels
card_title = canvas.create_text(400, 150, text="", font=("Ariel",40,"italic"))
carrd_word = canvas.create_text(400, 253, text="", font=("Ariel",60,"bold"))

canvas.grid(column=0, row=0, columnspan=2)



#Buttons
check_img = PhotoImage(file="images/right.png")
known_button = Button(image=check_img, highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, command=is_known)
known_button.grid(column=1, row=1)

cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, bd=0, bg=BACKGROUND_COLOR, command=next_card)
unknown_button.grid(column=0, row=1)


next_card()

windows.mainloop()
