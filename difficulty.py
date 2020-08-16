from tkinter import *


def run_choices_gui():
    master = Tk()
    master.title('Minesweeper')
    var = IntVar()
    var.set(1)

    def quit_loop():
        global selection
        selection = var.get()
        master.destroy()

    Label(master, text = "Welcome to minesweeper! Please select the difficulty level").grid(row=0, sticky=W)
    Radiobutton(master, text = "Easy", variable=var, value=0).grid(row=1, sticky=W)
    Radiobutton(master, text = "Medium", variable=var, value=1).grid(row=2, sticky=W)
    Radiobutton(master, text="Hard", variable=var, value=2).grid(row=3, sticky=W)
    Button(master, text = "Select", command=quit_loop).grid(row=4, sticky=W)

    master.mainloop()

    return selection
