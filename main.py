from tkinter import *
from tkinter import messagebox
import random 
import json
import pandas
thechosen={}
liste1={}
bgcolor="#B1DDC6"
try:
    data=pandas.read_csv("Words_game/tolearn.csv")
except FileNotFoundError : 
    new_data=pandas.read_csv("Words_game/words.csv")
    liste1=new_data.to_dict(orient="records")
else :
    liste1=data.to_dict(orient="records")
## -------------------------- Printing words --------------------
def next_card():
    global thechosen ,flip_timer 
    window.after_cancel(flip_timer)
    thechosen = random.choice(liste1)
    canvas.itemconfig(card_background,image=f_image)
    canvas.itemconfig(card_lan,fill="black",text="kabyle")
    canvas.itemconfig(card_word,text=thechosen["kabyle "],fill="black")
    flip_timer=window.after(3000,func=flip_card)
## ------------------------------- Flip ---------------------------
def flip_card():
    canvas.itemconfig(card_lan,text="English",fill="white")
    canvas.itemconfig(card_word,text=thechosen["English"],fill="white")
    canvas.itemconfig(card_background,image=b_image)
## ------------------------------- Time ---------------------------
def Save():
      liste1.remove(thechosen)
      new_file=pandas.DataFrame(liste1)
      new_file.to_csv("Words_game/tolearn.csv",index=False)
      next_card()
## ------------------------------- Setup ---------------------------
window=Tk()
window.config(bg=bgcolor,padx=50,pady=50)
window.title("words app")
flip_timer=window.after(3000,func=flip_card)
### ---------- The images and buttons ----------------- 
canvas=Canvas(width=800,height=526,bg=bgcolor,highlightthickness=0)

f_image=PhotoImage(file="Words_game/card_front.png")

b_image=PhotoImage(file="Words_game/card_back.png")

card_background=canvas.create_image(400,263,image=f_image)

card_lan=canvas.create_text(400,200,text="Title",font=("arial",60,"italic"))
card_word=canvas.create_text(400,263,text="Words",font=("arial",40,"italic"))
canvas.grid(row=0,column=0,columnspan=2)
b2_image=PhotoImage(file="Words_game/right.png")
button1=Button(text="Yes",bg="green",image= b2_image,highlightthickness=0,command=Save)
button1.grid(row=1,column=0)

b1_image=PhotoImage(file="Words_game/wrong.png")
button1=Button(text="No",bg="red",image=b1_image,highlightthickness=0, command=next_card)
button1.grid(row=1,column=1)
next_card()
window.mainloop()
