import tkinter as tk

import ImageDraw

import oneLineLibrary as one
import oneLineHexagons as olh
from main import OneLineProgram

from PIL import ImageTk, Image
from random import randint

def set_final_screen(app, instruction_type, pixel_type):
    app.clear_window()
    if instruction_type == "Export" and pixel_type == "Pixel":
        app.set_final_screen_pixel_export()
    elif instruction_type == "Step by step" and pixel_type == "Pixel":
        app.set_final_screen_pixel_SBS()
    elif instruction_type == "Export" and pixel_type == "Hexagon":
        app.set_final_screen_hexagon_export()
    elif instruction_type == "Step by step" and pixel_type == "Superpixel":
        app.set_final_screen_superpixel_SBS()

    # set back button
    app.set_back_button(command=lambda: app.set_second_window(), enabled=True)

def set_final_screen_pixel_export(app):
    app.window.title("Confirm Export")
    sidelength = app.nPixels

    image = Image.open(app.filename).resize((sidelength, sidelength)).convert("LA")
    canvas_size = (int(0.7 * app.size[1]), int(0.7 * app.size[1]))
    pixel_sidelength = canvas_size[0] / app.nPixels

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
        pixel_coordinates = (int(x / pixel_sidelength), int(y / pixel_sidelength))
        if pixel_coordinates not in app.pixel_list:
            # check if pixel borders the last pixel on the list
            is_bordering_last_pixel = True
            fill = "green"
            if len(app.pixel_list) == 0:
                # draw the starting pixel red
                fill = "red"
            else:
                horizontal_distance = abs(pixel_coordinates[0] - app.pixel_list[-1][0])
                vertical_distance = abs(pixel_coordinates[1] - app.pixel_list[-1][1])
                is_bordering_last_pixel = (horizontal_distance == 1 and vertical_distance == 0)
                is_bordering_last_pixel |= (horizontal_distance == 0 and vertical_distance == 1)
            if is_bordering_last_pixel:
                # set the last pixel to green
                image_canvas.create_rectangle((pixel_coordinates[0] * pixel_sidelength,
                                               pixel_coordinates[1] * pixel_sidelength,
                                               (pixel_coordinates[0] + 1) * pixel_sidelength,
                                               (pixel_coordinates[1] + 1) * pixel_sidelength),
                                              fill=fill, outline="")
                app.pixel_list.append(pixel_coordinates)

                # set the path to yellow
                if len(app.pixel_list) > 2:
                    second_to_last_pixel = app.pixel_list[-2]
                    image_canvas.create_rectangle((second_to_last_pixel[0] * pixel_sidelength,
                                                   second_to_last_pixel[1] * pixel_sidelength,
                                                   (second_to_last_pixel[0] + 1) * pixel_sidelength,
                                                   (second_to_last_pixel[1] + 1) * pixel_sidelength),
                                                  fill="yellow", outline="")
                    # draw line representing the connection from one pixel to the next
                    start_point = ((app.pixel_list[-3][0] + 0.5)*pixel_sidelength, (app.pixel_list[-3][1] + 0.5)*pixel_sidelength)

                    end_point = ((app.pixel_list[-2][0] + 0.5)*pixel_sidelength, (app.pixel_list[-2][1] + 0.5)*pixel_sidelength)

                    image_canvas.create_line(start_point[0], start_point[1], end_point[0], end_point[1], fill="black")


    image_canvas.bind("<B1-Motion>", set_pixel_list)

    # make undo button, removes last pixel placed
    def reset_last_pixel():
        if len(app.pixel_list) > 0:
            pixel_to_remove = app.pixel_list[-1]
            app.pixel_list.pop(-1)

            # get the color of the pixel that is to be returned to the original image
            grayscale_color = image.getpixel(pixel_to_remove)[0]
            image_canvas.create_rectangle((pixel_to_remove[0] * pixel_sidelength,
                                           pixel_to_remove[1] * pixel_sidelength,
                                           (pixel_to_remove[0] + 1) * pixel_sidelength,
                                           (pixel_to_remove[1] + 1) * pixel_sidelength),
                                          fill=f'#{grayscale_color:02x}{grayscale_color:02x}{grayscale_color:02x}',
                                          outline="") # tkinter dOeSnT sUpPoRt RgB

            # set the new last pixel to green
            if len(app.pixel_list) > 1:
                last_pixel = app.pixel_list[-1]
                image_canvas.create_rectangle((last_pixel[0] * pixel_sidelength,
                                               last_pixel[1] * pixel_sidelength,
                                               (last_pixel[0] + 1) * pixel_sidelength,
                                               (last_pixel[1] + 1) * pixel_sidelength),
                                              fill="green",
                                              outline="")

    tk.Button(app.window, text="Undo", command=reset_last_pixel).place(x=0.5 * app.size[0], y=0.9 * app.size[1])

def set_final_screen_hexagon_export(app: OneLineProgram):
    image = Image.open(app.filename)
    canvas_size = (int(0.7 * app.size[1]), int(0.7 * app.size[1]))
    pixel_sidelength = canvas_size[0] / app.nPixels

    image_to_show = image.resize(canvas_size)
    output = one.make_picture_circular(image_to_show)
    output_pixels = output.load()

    # draw hexagons on the image
    hexagon_height = int(canvas_size[0]/app.nPixels)
    hexagon_centers = olh.get_hexagon_centers(canvas_size[0], canvas_size[1], hexagon_height)
    full_image_matrix = olh.hexagon_matrix_full_image(canvas_size[0], canvas_size[1], hexagon_height)
    random_colors = [(randint(0, 255), 0) for c in hexagon_centers]
    for x in range(full_image_matrix.shape[0]):
        for y in range(full_image_matrix.shape[1]):
            output_pixels[x, y] = random_colors[int(full_image_matrix[x][y])]

    image_canvas = tk.Canvas(app.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
    image_canvas.place(x=int(0.2 * app.size[0]), y=50)
    img = ImageTk.PhotoImage(output)
    image_canvas.create_image(int(canvas_size[0] / 2), int(canvas_size[1] / 2), image=img)
    image_canvas.image = img


    center_dots = []
    lines = []
    # draw on image
    # bind sth to <B1-Motion>
    def set_pixel_list(event):
        x, y = event.x, event.y

        # get the index of the hexagon
        hexagon_index = int(full_image_matrix[x][y])
        if hexagon_index not in app.pixel_list:
            is_bordering_last_pixel = True
            fill = "green"
            if len(app.pixel_list) == 0:
                # draw the starting pixel red
                fill = "red"
                app.pixel_list.append(hexagon_index)
            else:
                current_center, last_center = hexagon_centers[hexagon_index], hexagon_centers[app.pixel_list[-1]]
                distance_between_centers_squared = ((current_center[0] - last_center[0])**2 + (current_center[1] - last_center[1])**2)
                if not 0.9*hexagon_height**2 < distance_between_centers_squared < 1.1*hexagon_height**2:
                    is_bordering_last_pixel = False

            if is_bordering_last_pixel:
                # draw hexagon with appropriate fill
                # add a dot in the center of the hexagon, connect it with the last dot
                r = 1
                center_x, center_y = hexagon_centers[hexagon_index][0], hexagon_centers[hexagon_index][1]
                center_dot = image_canvas.create_oval(center_x - r, center_y - r, center_x + r, center_y + r, fill=fill)
                center_dots.append(center_dot)

                # draw line from current to last pixel
                last_hexagon_x, last_hexagon_y = hexagon_centers[app.pixel_list[-1]]
                last_hexagon_x, last_hexagon_y = int(last_hexagon_x), int(last_hexagon_y)
                connecting_line = image_canvas.create_line(center_x, center_y, last_hexagon_x, last_hexagon_y, width=2, fill="red")
                lines.append(connecting_line)
                print(len(app.pixel_list))
                app.pixel_list.append(hexagon_index)


    image_canvas.bind("<B1-Motion>", set_pixel_list)

    # make undo button, removes last pixel placed
    def reset_last_pixel():
        if len(app.pixel_list) > 0:
            pixel_to_remove = app.pixel_list[-1]
            app.pixel_list.pop(-1)

            # get the color of the pixel that is to be returned to the original image
            image_canvas.delete(lines[-1])
            lines.pop(-1)
            image_canvas.delete(center_dots[-1])
            center_dots.pop(-1)

    tk.Button(app.window, text="Undo", command=reset_last_pixel).place(x=0.5 * app.size[0], y=0.9 * app.size[1])

def set_final_screen_pixel_SBS(app):
    pass

def set_final_screen_superpixel_SBS(app):
    pass

