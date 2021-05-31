import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image

class OneLineProgram:
    def __init__(self):
        self.window = tk.Tk()
        self.size = (1000, 700)
        self.window.geometry(f"{self.size[0]}x{self.size[1]}")
        self.next_button = tk.Button(self.window, text="Next")
        self.back_button = tk.Button(self.window, text="Back")
        self.filename = None
        self.allowed_images_types = ["jpg", "jpeg", "png"]
        self.set_start_screen()

    def set_start_screen(self):
        self.clear_window()
        self.window.title("Choose an image file")

        # set controll buttons
        self.set_next_button(command=None, enabled=False)
        self.set_back_button(command=self.window.destroy, enabled=True)
        tk.Button(self.window, text="Select Image", command=lambda: (self.get_filename(),
                                                                     self.set_next_button(enabled=self.verify_filename()),
                                                                     self.set_canvas())
                  ).place(x=0.4*self.size[0], y=0.8*self.size[1])





    def verify_filename(self):
        if self.filename.split(".")[1] in self.allowed_images_types:
            return True
        return False

    def get_filename(self):
        filetype_string = ""
        for type in self.allowed_images_types:
            filetype_string += f".{type} "

        self.filename = filedialog.askopenfilename(initialdir="~",
                                              title="Select an image",
                                              filetypes=[("Images", filetype_string)])

    def set_next_button(self, command=None, enabled=False):
        """
        sets the Next button for every screen of the app
        :param command: the lambda function to be executed when the Next button is pressed
        :param enabled: whether the next button should be active or not
        :return: none
        """
        self.next_button.config(state="normal" if enabled else "disabled")
        self.next_button.config(command=command)
        self.next_button.place(x=0.8*self.size[0], y=0.8*self.size[1])

    def set_back_button(self, command=None, enabled=False):
        """
        sets the back button for every screen of the app
        :param command: the lambda function to be executed when the Back button is pressed
        :param enabled: whether the Back button should be active or not
        :return: none
        """
        self.back_button.config(state="normal" if enabled else "disabled")
        self.back_button.config(command=command)
        self.back_button.place(x=0.1*self.size[0], y=0.8*self.size[1])

    def set_canvas(self):
        if self.verify_filename():
            print(f"valid filename: {self.filename}")
            # set canvas showing image
            canvas_size = (int(0.6*self.size[0]), int(0.6*self.size[1]))
            image_label = tk.Label(self.window, bg="cyan")
            pil_image = Image.open(self.filename).resize(canvas_size)
            pil_image.show()
            img = ImageTk.PhotoImage(pil_image)
            image_label["image"] = img
            image_label.place(x=0, y=0)


    def clear_window(self):
        for element in self.window.slaves():
            element.destroy()

def main():
    program = OneLineProgram()
    program.window.mainloop()

if __name__ == "__main__":
    main()