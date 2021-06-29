import tkinter as tk
import oneLineLibrary as one
import fileSelector
import chooseImageParams
import finalScreen
import appNativeFunctions

from tkinter import filedialog
from PIL import ImageTk, Image, ImageOps, ImageDraw

class OneLineProgram:
    def __init__(self):
        self.window = tk.Tk()
        self.size = (1500, 1000)
        self.window.geometry(f"{self.size[0]}x{self.size[1]}")
        self.filename = None
        self.allowed_images_types = ["jpg", "jpeg", "png"]
        self.pixel_list = [] # list of lists of pixel orders, in a loop
        # len(pixel_list) should be small
        self.nPixels = 100
        self.set_start_screen()
    # app native functions
    def set_next_button(self, command=None, enabled=False, text="Next"):
        appNativeFunctions.set_next_button(self, command, enabled, text)

    def set_back_button(self, command=None, enabled=False, text="Back"):
        appNativeFunctions.set_back_button(self, command, enabled, text)

    def clear_window(self):
        appNativeFunctions.clear_window(self)

    # first screen functions
    def set_start_screen(self):
        fileSelector.set_start_screen(self)

    def verify_filename(self):
        return fileSelector.verify_filename(self)

    def get_filename(self):
        fileSelector.get_filename(self)

    def set_canvas(self):
        fileSelector.set_canvas(self)

    # second screen functions
    def set_second_window(self):
        chooseImageParams.set_second_window(self)

    # final screen functions
    def set_final_screen(self, instruction_type, pixel_type):
        finalScreen.set_final_screen(self, instruction_type, pixel_type)

    def set_final_screen_pixel_export(self):
        finalScreen.set_final_screen_pixel_export(self)

    def set_final_screen_superpixel_export(self):
        finalScreen.set_final_screen_superpixel_export(self)

    def set_final_screen_pixel_SBS(self):
        finalScreen.set_final_screen_pixel_SBS(self)

    def set_final_screen_superpixel_SBS(self):
        finalScreen.set_final_screen_superpixel_SBS(self)

if __name__ == "__main__":
    program = OneLineProgram()
    program.window.mainloop()
