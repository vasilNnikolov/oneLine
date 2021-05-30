import tkinter as tk
import graphics


def main():
    window = tk.Tk()

    window.geometry("1000x700")

    graphics.set_start_screen(window)

    window.mainloop()


if __name__ == "__main__":
    main()