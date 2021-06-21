import tkinter as tk
import oneLineLibrary as one
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

        self.filename = filedialog.askopenfilename(initialdir="~/software/oneLine/oneLineProject",
                                              title="Select an image",
                                              filetypes=[("Images", filetype_string)])

    def set_next_button(self, command=None, enabled=False, text="Next"):
        """
        sets the Next button for every screen of the app
        :param command: the lambda function to be executed when the Next button is pressed
        :param enabled: whether the next button should be active or not
        :return: none
        """
        next_button = tk.Button(self.window, text=text)
        next_button.config(state="normal" if enabled else "disabled")
        next_button.config(command=command)
        next_button.place(x=0.8*self.size[0], y=0.8*self.size[1])

    def set_back_button(self, command=None, enabled=False, text="Back"):
        """
        sets the back button for every screen of the app
        :param command: the lambda function to be executed when the Back button is pressed
        :param enabled: whether the Back button should be active or not
        :return: none
        """
        back_button = tk.Button(self.window, text=text)
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
        pixel_type_label = tk.Label(self.window, text="Pixelisation type")
        pixel_type_label.place(x=int(0.3*self.size[0]), y=int(0.1*self.size[1]))

        # create pixel type dropdown menu
        pixel_options = ["Pixel", "Superpixel"]

        pixel_type = tk.StringVar(self.window)
        pixel_type.set(pixel_options[0])
        pixel_dropdown = tk.OptionMenu(self.window, pixel_type, *pixel_options)
        pixel_dropdown.place(x=int(0.5*self.size[0]), y=int(0.1*self.size[1]))

        # create instruction type label
        instruction_type_label = tk.Label(text="Instruction type")
        instruction_type_label.place(x=int(0.3*self.size[0]), y=int(0.3*self.size[1]))

        # create instruction type dropdown menu
        instruction_options = ["Export", "Step by step"]

        instruction_type = tk.StringVar(self.window)
        instruction_type.set(instruction_options[0])
        instruction_type_dropdown = tk.OptionMenu(self.window, instruction_type, *instruction_options)
        instruction_type_dropdown.place(x=int(0.5*self.size[0]), y=int(0.3*self.size[1]))

        # create number of pixels label
        nPixels_label = tk.Label(text="Sidelength")
        nPixels_label.place(x=int(0.3*self.size[0]), y=int(0.5*self.size[1]))

        # create number of pixels input field
        nPixels_variable = tk.StringVar()
        nPixels_variable.set("100")
        nPixels_entry = tk.Entry(self.window, textvariable=nPixels_variable)
        nPixels_entry.place(x=int(0.5*self.size[0]), y=int(0.5*self.size[1]))

        # set controll buttons
        def next_button_action():
            # verify whether input data is correct
            # not done yet
            self.nPixels = int(nPixels_variable.get())
            self.pixel_list = []
            self.set_final_screen(instruction_type.get(), pixel_type.get())
        self.set_next_button(command=lambda: next_button_action(), enabled=True)
        self.set_back_button(command=self.set_start_screen, enabled=True)

    def set_final_screen(self, instruction_type, pixel_type):
        self.clear_window()
        if instruction_type == "Export" and pixel_type == "Pixel":
            self.set_final_screen_pixel_export()
            # self.set_next_button(command=self.window.destroy, text="Color", enabled=True)
        elif instruction_type == "Step by step" and pixel_type == "Pixel":
            self.set_final_screen_pixel_SBS()
        elif instruction_type == "Export" and pixel_type == "Superpixel":
            self.set_final_screen_superpixel_export()
        elif instruction_type == "Step by step" and pixel_type == "Superpixel":
            self.set_final_screen_superpixel_SBS()

        # set back button
        self.set_back_button(command=lambda: self.set_second_window(), enabled=True)

    def set_final_screen_pixel_export(self):
        self.window.title("Confirm Export")
        sidelength = self.nPixels

        image = Image.open(self.filename).resize((sidelength, sidelength)).convert("LA")
        canvas_size = (int(0.7 * self.size[1]), int(0.7 * self.size[1]))

        image_to_show = image.resize(canvas_size, resample=Image.NEAREST)
        output = one.make_picture_circular(image_to_show)

        image_canvas = tk.Canvas(self.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
        image_canvas.place(x=int(0.2 * self.size[0]), y=50)
        img = ImageTk.PhotoImage(output)
        image_canvas.create_image(int(canvas_size[0] / 2), int(canvas_size[1] / 2), image=img)
        image_canvas.image = img

        # draw on image
        # bind sth to <B1-Motion>
        def set_pixel_list(event):
            x, y = event.x, event.y
            pixel_sidelength = canvas_size[0] / self.nPixels
            pixel_coordinates = (int(x/pixel_sidelength), int(y/pixel_sidelength))
            if pixel_coordinates not in self.pixel_list:
                # check if pixel borders the last pixel on the list
                is_bordering_last_pixel = True
                fill = "green"
                if len(self.pixel_list) == 0:
                    # draw the starting pixel red
                    fill = "red"
                else:
                    is_bordering_last_pixel = -1 <= (pixel_coordinates[0] - self.pixel_list[-1][0]) <= 1
                    is_bordering_last_pixel &= -1 <= (pixel_coordinates[0] - self.pixel_list[-1][0]) <= 1
                if is_bordering_last_pixel:
                    image_canvas.create_rectangle((pixel_coordinates[0]*pixel_sidelength,
                                                   pixel_coordinates[1]*pixel_sidelength,
                                                   (pixel_coordinates[0] + 1)*pixel_sidelength,
                                                   (pixel_coordinates[1] + 1)*pixel_sidelength),
                                                  fill=fill)

                    self.pixel_list.append(pixel_coordinates)

        image_canvas.bind("<B1-Motion>", set_pixel_list)

        # make undo button, removes last pixel placed
        def reset_last_pixel():
            pixel_to_remove = self.pixel_list[-1]
            self.pixel_list.pop(-1)
            print(self.pixel_list)
            print(pixel_to_remove)
        tk.Button(self.window, text="Undo", command=reset_last_pixel).place(x=0.5*self.size[0], y=0.9*self.size[1])


    def set_final_screen_superpixel_export(self):
        pass

    def set_final_screen_pixel_SBS(self):
        pass

    def set_final_screen_superpixel_SBS(self):
        pass

if __name__ == "__main__":
    program = OneLineProgram()
    program.window.mainloop()
