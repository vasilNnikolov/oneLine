import tkinter as tk

def set_next_button(app, command=None, enabled=False, text="Next"):
    """
    sets the Next button for every screen of the app
    :param command: the lambda function to be executed when the Next button is pressed
    :param enabled: whether the next button should be active or not
    :return: none
    """
    next_button = tk.Button(app.window, text=text)
    next_button.config(state="normal" if enabled else "disabled")
    next_button.config(command=command)
    next_button.place(x=0.8 * app.size[0], y=0.8 * app.size[1])


def set_back_button(app, command=None, enabled=False, text="Back"):
    """
    sets the back button for every screen of the app
    :param command: the lambda function to be executed when the Back button is pressed
    :param enabled: whether the Back button should be active or not
    :return: none
    """
    back_button = tk.Button(app.window, text=text)
    back_button.config(state="normal" if enabled else "disabled")
    back_button.config(command=command)
    back_button.place(x=0.1 * app.size[0], y=0.8 * app.size[1])

def clear_window(app):
    for element in app.window.winfo_children():
        element.destroy()
