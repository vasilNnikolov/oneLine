import tkinter as tk

from tkinter import filedialog
from PIL import ImageTk, Image


def set_start_screen(app):
    app.clear_window()
    app.window.title("Choose an image file")

    # set controll buttons
    app.set_next_button(enabled=False)
    app.set_back_button(command=app.window.destroy, enabled=True)
    tk.Button(app.window, text="Select Image", command=lambda: (app.get_filename(),
                                                                 app.set_next_button(
                                                                     command=lambda: app.set_second_window(),
                                                                     enabled=app.verify_filename()),
                                                                 app.set_canvas())
              ).place(x=0.4 * app.size[0], y=0.8 * app.size[1])


def verify_filename(app):
    if len(app.filename) > 0 and len(app.filename.split(".")) > 0:
        if app.filename.split(".")[1] in app.allowed_images_types:
            return True
    return False

def get_filename(app):
    filetype_string = ""
    for type in app.allowed_images_types:
        filetype_string += f".{type} "

    app.filename = filedialog.askopenfilename(initialdir="~/software/oneLine/oneLineProject",
                                          title="Select an image",
                                          filetypes=[("Images", filetype_string)])

def set_canvas(app):
    if app.verify_filename():
        canvas_size = (int(0.6*app.size[0]), int(0.6*app.size[1]))

        # open image, and resize it
        pil_image = Image.open(app.filename)
        w, h = pil_image.size
        resize_horisontal = w/canvas_size[0]
        resize_vertical = h/canvas_size[1]
        resize = max(resize_horisontal, resize_vertical)
        pil_image = pil_image.resize((int(w/resize), int(h/resize)))

        # set canvas showing image
        image_canvas = tk.Canvas(app.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
        image_canvas.place(x=int(0.2*app.size[0]), y=50)
        img = ImageTk.PhotoImage(pil_image)
        image_canvas.create_image(int(canvas_size[0]/2), int(canvas_size[1]/2), image=img)
        image_canvas.image = img
