import tkinter as tk
import oneLIneLibrary as one
from tkinter import filedialog
from PIL import ImageTk, Image

class OneLineProgram:
    def __init__(self):
        self.window = tk.Tk()
        self.size = (1000, 700)
        self.window.geometry(f"{self.size[0]}x{self.size[1]}")
        self.filename = None
        self.allowed_images_types = ["jpg", "jpeg", "png"]
        self.set_start_screen()

    def set_start_screen(self):
        self.clear_window()
        self.window.title("Choose an image file")

        # set controll buttons
        self.set_next_button(enabled=False)
        self.set_back_button(command=self.window.destroy, enabled=True)
        tk.Button(self.window, text="Select Image", command=lambda: (self.get_filename(),
                                                                     self.set_next_button(command=lambda: self.set_second_window(),
                                                                                          enabled=self.verify_filename()),
                                                                     self.set_canvas())
                  ).place(x=0.4*self.size[0], y=0.8*self.size[1])

    def verify_filename(self):
        if len(self.filename) > 0 and len(self.filename.split(".")) > 0:
            if self.filename.split(".")[1] in self.allowed_images_types:
                return True
        return False

    def get_filename(self):
        filetype_string = ""
        for type in self.allowed_images_types:
            filetype_string += f".{type} "

        self.filename = filedialog.askopenfilename(initialdir="~/Pictures",
                                              title="Select an image",
                                              filetypes=[("Images", filetype_string)])

    def set_next_button(self, command=None, enabled=False):
        """
        sets the Next button for every screen of the app
        :param command: the lambda function to be executed when the Next button is pressed
        :param enabled: whether the next button should be active or not
        :return: none
        """
        next_button = tk.Button(self.window, text="Next")
        next_button.config(state="normal" if enabled else "disabled")
        next_button.config(command=command)
        next_button.place(x=0.8*self.size[0], y=0.8*self.size[1])

    def set_back_button(self, command=None, enabled=False):
        """
        sets the back button for every screen of the app
        :param command: the lambda function to be executed when the Back button is pressed
        :param enabled: whether the Back button should be active or not
        :return: none
        """
        back_button = tk.Button(self.window, text="Back")
        back_button.config(state="normal" if enabled else "disabled")
        back_button.config(command=command)
        back_button.place(x=0.1*self.size[0], y=0.8*self.size[1])

    def set_canvas(self):
        if self.verify_filename():
            canvas_size = (int(0.6*self.size[0]), int(0.6*self.size[1]))

            # open image, and resize it
            pil_image = Image.open(self.filename)
            w, h = pil_image.size
            resize_horisontal = w/canvas_size[0]
            resize_vertical = h/canvas_size[1]
            resize = max(resize_horisontal, resize_vertical)
            pil_image = pil_image.resize((int(w/resize), int(h/resize)))

            # set canvas showing image
            image_canvas = tk.Canvas(self.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
            image_canvas.place(x=int(0.2*self.size[0]), y=50)
            img = ImageTk.PhotoImage(pil_image)
            image_canvas.create_image(int(canvas_size[0]/2), int(canvas_size[1]/2), image=img)
            image_canvas.image = img

    def clear_window(self):
        for element in self.window.winfo_children():
            element.destroy()

    def set_second_window(self):
        self.clear_window()
        self.window.title("Choose image parameters")

        # create pixel type label
        text_pixelisation_type = tk.StringVar(self.window)
        text_pixelisation_type.set("Pixelisation type")
        pixel_type_label = tk.Label(textvariable=text_pixelisation_type)
        pixel_type_label.place(x=int(0.3*self.size[0]), y=int(0.1*self.size[1]))

        # create pixel type dropdown menu
        pixel_options = ["Pixel", "Superpixel"]

        pixel_type = tk.StringVar(self.window)
        pixel_type.set(pixel_options[0])
        pixel_dropdown = tk.OptionMenu(self.window, pixel_type, *pixel_options)
        pixel_dropdown.place(x=int(0.5*self.size[0]), y=int(0.1*self.size[1]))

        # create instruction type label
        text_instruction_type = tk.StringVar(self.window)
        text_instruction_type.set("Instruction type")
        instruction_type_label = tk.Label(textvariable=text_instruction_type)
        instruction_type_label.place(x=int(0.3*self.size[0]), y=int(0.3*self.size[1]))

        # create instruction type dropdown menu
        instruction_options = ["Export", "Step by step"]

        instruction_type = tk.StringVar(self.window)
        instruction_type.set(instruction_options[0])
        instruction_type_dropdown = tk.OptionMenu(self.window, instruction_type, *instruction_options)
        instruction_type_dropdown.place(x=int(0.5*self.size[0]), y=int(0.3*self.size[1]))

        # set controll buttons
        def next_button_action():
            if instruction_type.get() == instruction_options[1]: # step by step
                pass
            else: # export the image
                # go to the next screen, with total pixel number field and filename field
                pass

        self.set_next_button(command=lambda: next_button_action(), enabled=True)
        self.set_back_button(command=self.set_start_screen, enabled=True)


def main():
    program = OneLineProgram()
    program.window.mainloop()


if __name__ == "__main__":
    main()