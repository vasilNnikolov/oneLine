import tkinter as tk

import oneLineLibrary as one
from PIL import ImageTk, Image


def set_final_screen(app, instruction_type, pixel_type):
    app.clear_window()
    if instruction_type == "Export" and pixel_type == "Pixel":
        app.set_final_screen_pixel_export()
        # app.set_next_button(command=app.window.destroy, text="Color", enabled=True)
    elif instruction_type == "Step by step" and pixel_type == "Pixel":
        app.set_final_screen_pixel_SBS()
    elif instruction_type == "Export" and pixel_type == "Superpixel":
        app.set_final_screen_superpixel_export()
    elif instruction_type == "Step by step" and pixel_type == "Superpixel":
        app.set_final_screen_superpixel_SBS()

    # set back button
    app.set_back_button(command=lambda: app.set_second_window(), enabled=True)


def set_final_screen_pixel_export(app):
    app.window.title("Confirm Export")
    sidelength = app.nPixels

    image = Image.open(app.filename).resize((sidelength, sidelength)).convert("LA")
    canvas_size = (int(0.7 * app.size[1]), int(0.7 * app.size[1]))

    image_to_show = image.resize(canvas_size, resample=Image.NEAREST)
    output = one.make_picture_circular(image_to_show)

    image_canvas = tk.Canvas(app.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
    image_canvas.place(x=int(0.2 * app.size[0]), y=50)
    img = ImageTk.PhotoImage(output)
    image_canvas.create_image(int(canvas_size[0] / 2), int(canvas_size[1] / 2), image=img)
    image_canvas.image = img

    # draw on image
    # bind sth to <B1-Motion>
    def set_pixel_list(event):
        x, y = event.x, event.y
        pixel_sidelength = canvas_size[0] / app.nPixels
        pixel_coordinates = (int(x / pixel_sidelength), int(y / pixel_sidelength))
        if pixel_coordinates not in app.pixel_list:
            # check if pixel borders the last pixel on the list
            is_bordering_last_pixel = True
            fill = "green"
            if len(app.pixel_list) == 0:
                # draw the starting pixel red
                fill = "red"
            else:
                is_bordering_last_pixel = -1 <= (pixel_coordinates[0] - app.pixel_list[-1][0]) <= 1
                is_bordering_last_pixel &= -1 <= (pixel_coordinates[0] - app.pixel_list[-1][0]) <= 1
            if is_bordering_last_pixel:
                image_canvas.create_rectangle((pixel_coordinates[0] * pixel_sidelength,
                                               pixel_coordinates[1] * pixel_sidelength,
                                               (pixel_coordinates[0] + 1) * pixel_sidelength,
                                               (pixel_coordinates[1] + 1) * pixel_sidelength),
                                              fill=fill)

                app.pixel_list.append(pixel_coordinates)

    image_canvas.bind("<B1-Motion>", set_pixel_list)

    # make undo button, removes last pixel placed
    def reset_last_pixel():
        pixel_to_remove = app.pixel_list[-1]
        app.pixel_list.pop(-1)
        print(app.pixel_list)
        print(pixel_to_remove)

    tk.Button(app.window, text="Undo", command=reset_last_pixel).place(x=0.5 * app.size[0], y=0.9 * app.size[1])

def set_final_screen_superpixel_export(app):
    pass

def set_final_screen_pixel_SBS(app):
    pass

def set_final_screen_superpixel_SBS(app):
    pass
