import os
from tkinter import *
import pandas as pd
import random


class GUI:
    def __init__(self):
        self.window_params = {
            "bgcolor": "#B1DDC6",
        }

        self.resources = {
            "words": "resources/words.csv",
            "learned": "resources/learned.csv",
            "card_front": "resources/card_front.png",
            "card_back": "resources/card_back.png",
            "wrong": "resources/wrong.png",
            "right": "resources/right.png",
        }

        self.card_word = None
        self.card_lan = None
        self.card_background = None
        self.flip_timer = None
        self.f_image = None
        self.b_image = None
        self.b2_image = None
        self.b1_image = None
        self.window = None
        self.canvas = None
        self.thechosen = {}
        self.words = {}
        self.learned = {}

        # Load words
        try:
            self.words = pd.read_csv(self.resources["words"]).to_dict(orient="records")
        except FileNotFoundError:
            raise f"File not found: {self.resources['words']}"

        # Load learned
        try:
            self.learned = pd.read_csv(self.resources["learned"]).to_dict(orient="records")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            self.learned = []

        self.to_learn = [x for x in self.words if x not in self.learned]

        self.setup()

    def setup(self):
        self.window = Tk()
        self.window.config(bg=self.window_params["bgcolor"], padx=50, pady=50)
        self.window.title("words app")
        self.canvas = Canvas(width=800, height=526, bg=self.window_params["bgcolor"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, columnspan=2)

        self.f_image = PhotoImage(file=self.resources["card_front"])
        self.b_image = PhotoImage(file=self.resources["card_back"])

        self.card_background = self.canvas.create_image(400, 263, image=self.f_image)

        self.card_lan = self.canvas.create_text(400, 100, text="Title", font=("Helvetica", 60, "bold"))
        self.card_word = self.canvas.create_text(400, 200, text="Words", font=("Helvetica", 24, "italic"), fill="black")

        # Events
        self.b1_image = PhotoImage(file=self.resources["wrong"])
        self.b2_image = PhotoImage(file=self.resources["right"])

        # create button without borders
        button1 = Button(text="No", bg="red", image=self.b1_image, borderwidth=0, highlightthickness=0,
                         command=self.next_card)
        button1.grid(row=1, column=1)

        button2 = Button(text="Yes", bg="green", image=self.b2_image, borderwidth=0, highlightthickness=0,
                         command=lambda: [self.add_to_learn(), self.next_card()])
        button2.grid(row=1, column=0)

    def start(self):
        self.next_card()
        self.window.mainloop()

    def next_card(self):
        self.thechosen = random.choice(self.words)
        self.canvas.itemconfig(self.card_background, image=self.f_image)
        self.canvas.itemconfig(self.card_lan, text="Kabyle", fill="#1abc9c")
        self.canvas.itemconfig(self.card_word, text=self.thechosen["kabyle"])
        self.flip_timer = self.window.after(3000, func=self.flip_card)

    def flip_card(self):
        self.canvas.itemconfig(self.card_lan, text="English", fill="#ecf0f1")
        self.canvas.itemconfig(self.card_word, text=self.thechosen["english"])
        self.canvas.itemconfig(self.card_background, image=self.b_image)

    def add_to_learn(self):
        try:
            self.learned.append(self.thechosen)
            pd.DataFrame(self.learned).to_csv(self.resources["learned"], index=False)
        except Exception as e:
            print(e)

