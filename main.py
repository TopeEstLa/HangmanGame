from tkinter import *
from tkinter import messagebox
from datetime import datetime

import uuid
import random

from history import History

game = ""
level = ""

run = True
selected_word = ""

fail = 1
max_fail = 0

guessed_letter = []

han = [['c1', 'h1'], ['c2', 'h2'], ['c3', 'h3'], ['c4', 'h4'], ['c5', 'h5'], ['c6', 'h6'], ['c7', 'h7'], ['c8', 'h8'],
       ['c9', 'h9'], ['c10', 'h10']]
h123 = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10']


def getWord():
    file = open('words.txt', 'r')
    lines = file.readlines()
    index = random.randint(0, len(lines))
    return lines[index].strip('\n')


def load_game():
    global game, fail, max_fail, selected_word, guessed_letter, level

    selected_word = getWord()
    print(selected_word)
    guessed_letter = []
    max_fail = 10

    if level == "Easy":
        fail = 1
    elif level == "Normal":
        fail = 3
    elif level == "Hard":
        fail = 4

    game = Tk()

    game.geometry('905x700')
    game.title("Hangman - Game")
    game.config(bg='#E7FFFF')


def choose_level():
    root = Tk()

    root.geometry('905x700')
    root.title('Hangman - Game (Select LVL)')
    root.config(bg='#E7FFFF')

    level_list = [
        "Easy",
        "Normal",
        "Hard"
    ]

    variable = StringVar(root)
    variable.set(level_list[0])

    opt = OptionMenu(root, variable, *level_list)
    opt.config(width=90, font=('Helvetica', 12))
    opt.pack(side="top")

    exitImage = PhotoImage(file='ressources/exit.png')
    exitButton = Button(root, bd=0, command=close, bg="#E7FFFF", activebackground="#E7FFFF", font=10, image=exitImage)
    exitButton.place(x=500, y=500)

    def callback(*args):
        global level
        level = variable.get()
        root.destroy()

    variable.trace("w", callback)

    root.mainloop()


def close():
    answer = messagebox.askyesno('ALERT', 'TU VEUX VRAIMENT LEAVE ?')

    global run

    if answer == True:
        run = False
        game.destroy()
        exit()


def letter_guess():
    letter = txt.get()
    txt.delete(0, END)
    txt.insert(0, "")

    global fail, run

    if len(letter) == 1:
        if letter not in guessed_letter:
            if letter in selected_word:
                for i in range(0, len(selected_word)):
                    if selected_word[i] == letter:
                        guessed_letter.append(letter)
                        exec('d{}.config(text="{}")'.format(i, letter.upper()))
                if len(guessed_letter) == len(selected_word):
                    create_history(True)
                    answer = messagebox.askyesno('GAME FINIE', 'TU VIENT DE GAGNER \n REJOUER ?')
                    if answer == True:
                        game.destroy()
                    else:
                        close()
            else:
                exec('c{}.destroy()'.format(fail))
                exec('c{}.place(x={},y={})'.format(fail + 1, 300, -50))
                fail += 1
                if fail == max_fail:
                    create_history(False)
                    answer = messagebox.askyesno('GAME FINIE', 'TU A PERDUE :C !\n REJOUER ?')
                    if answer == True:
                        game.destroy()
                    else:
                        close()
        else:
            messagebox.showinfo("Game", "Vous avez déjà entrer cette lettre")
    else:
        messagebox.showinfo("Game", "Vous devez entrer seulement une lettre")


def create_history(hasWin):
    global fail, level
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H:%M:%S")
    game_uuid = uuid.uuid4()
    history = History()
    history.uuid = str(game_uuid)
    history.date = dt_string
    history.win = hasWin
    history.fail = fail
    history.level = level
    history.word = selected_word

    history_file = open("game_history/" + str(game_uuid) + ".json", 'w')
    history_file.write(history.toJSON())
    history_file.close()

while run:
    choose_level()
    load_game()

    x = 200
    for i in range(0, len(selected_word)):
        x += 60
        exec('d{}=Label(game,text="_",bg="#E7FFFF",font=("arial",40))'.format(i))
        exec('d{}.place(x={},y={})'.format(i, x, 450))

    for hangman in h123:
        exec('{}=PhotoImage(file="ressources/{}.png")'.format(hangman, hangman))

    for p1 in han:
        exec('{}=Label(game,bg="#E7FFFF",image={})'.format(p1[0], p1[1]))

    exec('c1.place(x=300, y=-50)')

    exitImage = PhotoImage(file='ressources/exit.png')
    submitImage = PhotoImage(file='ressources/submit.png')

    exitButton = Button(game, bd=0, command=close, bg="#E7FFFF", activebackground="#E7FFFF", font=10, image=exitImage)
    submit = Button(game, bd=0, command=letter_guess, bg="#E7FFFF", activebackground="#E7FFFF", font=10,
                    image=submitImage)
    txt = Entry(game, font="Verdana 20", bg='#E7FFFF', justify="center")

    exitButton.place(x=770, y=10)
    txt.place(x=250, y=550)
    submit.place(x=375, y=600)

    game.mainloop()
