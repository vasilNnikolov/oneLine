import tkinter as tk
from tkinter import filedialog

def set_start_screen(window: tk.Tk):
    window.title("Choose an image file")
    tk.Button(window, text="Select image", command=get_filename).grid(row=0, column=0)


def get_filename():
    filename = filedialog.askopenfilename(initialdir="~", title="Select an image")

    print(filename)


