import random
import tkinter as tk

import numpy as np

import oneLineLibrary as one
import oneLineHexagons as olh
import calibrate_spiral
from main import OneLineProgram

from PIL import ImageTk, Image
from random import randint, shuffle

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

def are_centers_neighbouring(center_1, center_2, hex_height):
    return 0.9 * hex_height ** 2 < (center_1[0] - center_2[0]) ** 2 + (
            center_1[1] - center_2[1]) ** 2 < 1.1 * hex_height ** 2

def set_final_screen_hexagon_export(app: OneLineProgram):
    image = Image.open(app.filename)
    canvas_size = (int(0.7 * app.size[1]), int(0.7 * app.size[1]))
    output_hexagon_height = 35
    output_image_size = (int(output_hexagon_height*app.nPixels), int(output_hexagon_height*app.nPixels))

    image_to_show = image.resize(canvas_size)
    output = image_to_show.convert("LA")
    output_pixels = output.load()

    # draw hexagons on the image
    hexagon_height = int(canvas_size[1]/app.nPixels)
    hexagon_centers = olh.get_hexagon_centers(canvas_size[0], canvas_size[1], hexagon_height)
    full_image_matrix = olh.hexagon_matrix_full_image(canvas_size[0], canvas_size[1], hexagon_height)
    image_colors = []
    for c in hexagon_centers:
        clamped_center = (max(0, min(c[0], canvas_size[0] - 1)),
                          max(0, min(c[1], canvas_size[1] - 1)))
        image_colors.append(output_pixels[clamped_center])
    for x in range(full_image_matrix.shape[0]):
        for y in range(full_image_matrix.shape[1]):
            output_pixels[x, y] = image_colors[int(full_image_matrix[x][y])]

    output = one.make_picture_circular(output)

    image_canvas = tk.Canvas(app.window, width=canvas_size[0], height=canvas_size[1], bg="cyan")
    image_canvas.place(x=int(0.2 * app.size[0]), y=50)
    img = ImageTk.PhotoImage(output)
    image_canvas.create_image(int(canvas_size[0] / 2), int(canvas_size[1] / 2), image=img)
    image_canvas.image = img

    lines = []
    yellow_circles = []
    # draw on image
    # bind sth to <B1-Motion>

    def set_pixel_list(event):
        x, y = event.x, event.y

        if 0 <= x < full_image_matrix.shape[0] and 0 <= y < full_image_matrix.shape[1]:
            # get the index of the hexagon
            hexagon_index = int(full_image_matrix[x][y])
            if hexagon_index not in app.pixel_list:
                is_bordering_last_pixel = True
                fill = "yellow"
                if len(app.pixel_list) == 0:
                    # draw the starting pixel red
                    fill = "red"
                    # app.pixel_list.append(hexagon_index)
                else:
                    current_center, last_center = hexagon_centers[hexagon_index], hexagon_centers[app.pixel_list[-1]]
                    if not are_centers_neighbouring(current_center, last_center, hexagon_height):
                        is_bordering_last_pixel = False

                if is_bordering_last_pixel:
                    # draw hexagon with appropriate fill
                    center_x, center_y = hexagon_centers[hexagon_index][0], hexagon_centers[hexagon_index][1]

                    # draw yellow circle to show the hexagon has been selected
                    yellow_circle_radius = hexagon_height//2
                    yellow_circle = image_canvas.create_oval(center_x - yellow_circle_radius,
                                                             center_y - yellow_circle_radius,
                                                             center_x + yellow_circle_radius,
                                                             center_y + yellow_circle_radius,
                                                             fill=fill)
                    yellow_circles.append(yellow_circle)

                    if len(app.pixel_list) > 0:
                        # draw line from current to last pixel
                        last_hexagon_x, last_hexagon_y = hexagon_centers[app.pixel_list[-1]]
                        last_hexagon_x, last_hexagon_y = int(last_hexagon_x), int(last_hexagon_y)
                        connecting_line = image_canvas.create_line(center_x, center_y, last_hexagon_x, last_hexagon_y, width=2, fill="red")
                        lines.append(connecting_line)

                    app.pixel_list.append(hexagon_index)

    image_canvas.bind("<B1-Motion>", set_pixel_list)

    # make undo button, removes last pixel placed
    def reset_last_pixel():
        if len(app.pixel_list) > 0:
            pixel_to_remove = app.pixel_list[-1]
            app.pixel_list.pop(-1)

            # get the color of the pixel that is to be returned to the original image
            if len(lines) > 0:
                image_canvas.delete(lines[-1])
                lines.pop(-1)
            if len(yellow_circles) > 0:
                image_canvas.delete(yellow_circles[-1])
                yellow_circles.pop(-1)

    undo_button = tk.Button(app.window, text="Undo", command=reset_last_pixel)
    undo_button.place(x=0.5 * app.size[0], y=0.9 * app.size[1])
    app.window.bind("u", lambda event: reset_last_pixel())

    # make finish button
    def finish_drawing_path():
        command = input("are you sure you want to finish drawing the path?: y/n")
        if command.lower() == "y":
            app.window.unbind("u")
            filename_without_extension = app.filename.split(".")[0]

            # save hexagon order to txt file
            output_hexagon_centers = olh.get_hexagon_centers(output_image_size[0], output_image_size[1], output_hexagon_height)
            shuffled_pixels = [output_hexagon_centers[i] for i in app.pixel_list]
            # random.shuffle(shuffled_pixels)
            with open(f"{filename_without_extension}_centers_order_final_v3.txt", "w") as f:
                f.writelines([f"{pixel_coordinates}\n" for pixel_coordinates in shuffled_pixels])

            # make output image
            final_image = make_final_hexagon_image_3(app, output_image_size, output_hexagon_height)
            final_image.save(f"{filename_without_extension}_hexagon_output_final_v3.jpg")

    tk.Button(app.window, text="Finish", command=finish_drawing_path).place(x=0.8*app.size[0], y=0.9*app.size[1])

def make_final_hexagon_image(app: OneLineProgram, canvas_size, hexagon_height):
    """
    make the final target image once the path of hexagons has been selected
    :param app:
    :param canvas_size: (w, h) of image combo
    :param hexagon_height:
    :return: the final image
    """
    w, h = canvas_size
    print(w, h)

    output_image = Image.new("L", (w, h), 255)

    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)
    hexagon_matrix = olh.get_hexagon_matrix(hexagon_height)
    original_image = Image.open(app.filename).convert("L").resize((w, h), resample=Image.BICUBIC)
    original_pixels = original_image.load()

    hexagon_area = np.count_nonzero(hexagon_matrix == 1)
    curve_start = hexagon_centers[app.pixel_list[0]]
    curve_end = hexagon_centers[app.pixel_list[-1]]

    # if start borders end, append start to the end of pixel list, and end to the start
    if 0.9 * hexagon_height ** 2 < (curve_start[0] - curve_end[0]) ** 2 + (curve_start[1] - curve_end[1]) ** 2 < 1.1 * hexagon_height ** 2:
        app.pixel_list.insert(0, app.pixel_list[-1])
        app.pixel_list.append(app.pixel_list[1])

    for hexagon_order, center_index in enumerate(app.pixel_list):
        # get intensity of the region in the matrix
        c = hexagon_centers[center_index]
        is_close_to_border = olh.is_center_close_to_border(w, h, c, hexagon_height)
        total_intensity = 0
        partial_hexagon_area = 0
        for x in range(int(c[0] - hexagon_matrix.shape[0] // 2), int(c[0] + hexagon_matrix.shape[0] // 2)):
            for y in range(int(c[1] - hexagon_matrix.shape[1] // 2), int(c[1] + hexagon_matrix.shape[1] // 2)):
                matrix_x = int(x - c[0] + hexagon_matrix.shape[0] // 2)
                matrix_y = int(y - c[1] + hexagon_matrix.shape[1] // 2)
                if 0 <= x < w and 0 <= y < h and hexagon_matrix[matrix_x][matrix_y] == 1:
                    total_intensity += original_pixels[x, y]
                    if is_close_to_border:
                        partial_hexagon_area += 1

        if not is_close_to_border:
            total_intensity /= hexagon_area
        elif partial_hexagon_area != 0:
            total_intensity /= partial_hexagon_area
        else:
            total_intensity = 0

        # set the color of the hexagon to total_intensity
        turns = (255 - total_intensity) / 255 * 15

        start_point, end_point = (0, 0), (0, 0)
        current_center = hexagon_centers[center_index]

        if 0 < hexagon_order < len(app.pixel_list) - 2:
            next_center = hexagon_centers[app.pixel_list[hexagon_order + 1]]
            previous_center = hexagon_centers[app.pixel_list[hexagon_order - 1]]

            start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                           (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

            end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                         (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        image_to_paste = olh.make_hexagon_spiral(turns,
                                                 (int(1.4 * hexagon_height), hexagon_height),
                                                 start_point,
                                                 end_point, add_end_points=True)
        output_image.paste(image_to_paste, (int(c[0] - 0.7 * hexagon_height), int(c[1] - hexagon_height // 2)),
                           mask=image_to_paste.convert("RGBA"))

    return output_image

def make_final_hexagon_image_2(app: OneLineProgram, canvas_size, hexagon_height):
    """
    make the final target image once the path of hexagons has been selected
    :param app:
    :param canvas_size: (w, h) of image combo
    :param hexagon_height:
    :return: the final image
    """
    w, h = canvas_size
    print(w, h)

    output_image = Image.new("L", (w, h), 255)

    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)
    hexagon_matrix = olh.get_hexagon_matrix(hexagon_height)
    original_image = Image.open(app.filename).convert("L").resize((500, 500))
    ow, oh = original_image.size
    scale_factor = ow/w
    original_hexagon_height = int(hexagon_height*scale_factor)
    original_hexagon_matrix = olh.get_hexagon_matrix(original_hexagon_height)
    original_pixels = original_image.load()

    hexagon_area = np.count_nonzero(hexagon_matrix == 1)
    curve_start = hexagon_centers[app.pixel_list[0]]
    curve_end = hexagon_centers[app.pixel_list[-1]]

    # if start borders end, append start to the end of pixel list, and end to the start
    if 0.9 * hexagon_height ** 2 < (curve_start[0] - curve_end[0]) ** 2 + (curve_start[1] - curve_end[1]) ** 2 < 1.1 * hexagon_height ** 2:
        app.pixel_list.insert(0, app.pixel_list[-1])
        app.pixel_list.append(app.pixel_list[1])
    progress_index = 1
    for hexagon_order, center_index in enumerate(app.pixel_list):
        # progress bar
        progress = hexagon_order/len(app.pixel_list)
        if progress > progress_index/100:
            print(f"Progress: {progress:.2f}%")
            progress_index += 1

        # get intensity of the region in the matrix
        c = hexagon_centers[center_index]
        is_close_to_border = olh.is_center_close_to_border(w, h, c, hexagon_height)
        total_intensity = 0
        partial_hexagon_area = 0
        original_matrix_shape = original_hexagon_matrix.shape
        for x in range(int(c[0]*scale_factor - original_matrix_shape[0] // 2), int(c[0]*scale_factor + original_matrix_shape[0] // 2)):
            for y in range(int(c[1]*scale_factor - original_matrix_shape[1] // 2), int(c[1]*scale_factor + original_matrix_shape[1] // 2)):
                matrix_x = int(x - c[0]*scale_factor + original_matrix_shape[0] // 2)
                matrix_y = int(y - c[1] + original_matrix_shape[1] // 2)
                if 0 <= x < w*scale_factor and 0 <= y < h*scale_factor and original_hexagon_matrix[matrix_x][matrix_y] == 1:
                    total_intensity += original_pixels[x, y]
                    if is_close_to_border:
                        partial_hexagon_area += 1

        if not is_close_to_border:
            total_intensity /= hexagon_area
        elif partial_hexagon_area != 0:
            total_intensity /= partial_hexagon_area
        else:
            total_intensity = 0

        # set the color of the hexagon to total_intensity
        turns = (255 - total_intensity) / 255 * 15

        start_point, end_point = (0, 0), (0, 0)
        current_center = hexagon_centers[center_index]

        if 0 < hexagon_order < len(app.pixel_list) - 2:
            next_center = hexagon_centers[app.pixel_list[hexagon_order + 1]]
            previous_center = hexagon_centers[app.pixel_list[hexagon_order - 1]]

            start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                           (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

            end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                         (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        image_to_paste = olh.make_hexagon_spiral(turns,
                                                 (int(1.4 * hexagon_height), hexagon_height),
                                                 start_point,
                                                 end_point, add_end_points=True)
        output_image.paste(image_to_paste, (int(c[0] - 0.7 * hexagon_height), int(c[1] - hexagon_height // 2)),
                           mask=image_to_paste.convert("RGBA"))

    return output_image

def make_final_hexagon_image_3(app: OneLineProgram, canvas_size, hexagon_height):
    # get turns for each color
    calibrate_spiral.make_calibration_file(hexagon_height)
    with open("calibration_file.txt", "r") as calib_file:
        turns_by_color = [float(line.split(": ")[1]) for line in calib_file.readlines()]

    w, h = canvas_size
    output_image = Image.new("L", (w, h), 255)
    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)

    original_image = Image.open(app.filename).convert("L").resize((700, 700))
    original_w, original_h = original_image.size

    # for each hexagon center in pixel list get the average color
    progress_index = 1
    for hexagon_order, center_index in enumerate(app.pixel_list):
        # print progress
        progress = hexagon_order/len(app.pixel_list)
        if progress > progress_index/100:
            print(f"Progress: {progress:.2f}%")
            progress_index += 1

        hex_center = hexagon_centers[center_index]
        scaled_hex_center = (int(hex_center[0]*original_w/w), int(hex_center[1]*original_h/h))
        # clamp values of scaled hex center
        scaled_hex_center = (max(0, min(scaled_hex_center[0], original_w - 1)),
                             max(0, min(scaled_hex_center[1], original_h - 1)))
        color = original_image.getpixel(scaled_hex_center)

        # get turns from color
        # turns = (255 - color) / 255 * 15
        turns = turns_by_color[color]

        start_point, end_point = (0, 0), (hexagon_height, hexagon_height)
        current_center = hexagon_centers[center_index]

        if hexagon_order == 0:
            previous_center = hexagon_centers[app.pixel_list[-1]]
            current_center = hexagon_centers[app.pixel_list[0]]
            next_center = hexagon_centers[app.pixel_list[1]]
            if are_centers_neighbouring(previous_center, current_center, hexagon_height):
                start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                               (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

                end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                             (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        elif 0 < hexagon_order < len(app.pixel_list) - 1:
            next_center = hexagon_centers[app.pixel_list[hexagon_order + 1]]
            previous_center = hexagon_centers[app.pixel_list[hexagon_order - 1]]

            start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                           (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

            end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                         (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        elif hexagon_order == len(app.pixel_list) - 1:
            previous_center = hexagon_centers[app.pixel_list[-2]]
            current_center = hexagon_centers[app.pixel_list[-1]]
            next_center = hexagon_centers[app.pixel_list[0]]
            if are_centers_neighbouring(next_center, current_center, hexagon_height):
                start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                               (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

                end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                             (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))



        image_to_paste = olh.make_hexagon_spiral(turns,
                                                 (int(1.4 * hexagon_height), hexagon_height),
                                                 start_point,
                                                 end_point)
        output_image.paste(image_to_paste, (int(hex_center[0] - 0.7 * hexagon_height), int(hex_center[1] - hexagon_height // 2)),
                           mask=image_to_paste.convert("RGBA"))

    return output_image

def hexagon_image_from_given_file(canvas_size, hexagon_height):
    # get turns for each color
    calibrate_spiral.make_calibration_file(hexagon_height)
    with open("calibration_file.txt", "r") as calib_file:
        turns_by_color = [float(line.split(": ")[1]) for line in calib_file.readlines()]

    w, h = canvas_size
    output_image = Image.new("L", (w, h), 255)
    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)

    original_image = Image.open("cute_image_4.jpg").convert("L").resize((700, 700))
    original_w, original_h = original_image.size

    # get pixel list from file with centers
    centers_order_filename = "cute_image_4_centers_order_final.txt"
    with open(centers_order_filename, "r") as centers_file:
        centers_in_order = [tuple(map(float, x[1:-2].split(", "))) for x in centers_file.readlines()]

    # for each hexagon center in pixel list get the average color
    progress_index = 1
    for hexagon_order, hex_center in enumerate(centers_in_order):
        # print progress
        progress = hexagon_order/len(centers_in_order)
        if progress > progress_index/100:
            print(f"Progress: {progress:.2f}%")
            progress_index += 1

        scaled_hex_center = (int(hex_center[0]*original_w/w), int(hex_center[1]*original_h/h))
        # clamp values of scaled hex center
        scaled_hex_center = (max(0, min(scaled_hex_center[0], original_w - 1)),
                             max(0, min(scaled_hex_center[1], original_h - 1)))
        color = original_image.getpixel(scaled_hex_center)

        # get turns from color
        # turns = (255 - color) / 255 * 15
        turns = turns_by_color[color]

        start_point, end_point = (0, 0), (hexagon_height, hexagon_height)
        current_center = hex_center

        if hexagon_order == 0:
            previous_center = centers_in_order[-1]
            current_center = centers_in_order[0]
            next_center = centers_in_order[1]
            if are_centers_neighbouring(previous_center, current_center, hexagon_height):
                start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                               (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

                end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                             (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        elif 0 < hexagon_order < len(centers_in_order) - 1:
            next_center = centers_in_order[hexagon_order + 1]
            previous_center = centers_in_order[hexagon_order - 1]

            start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                           (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

            end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                         (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

        elif hexagon_order == len(centers_in_order) - 1:
            previous_center = centers_in_order[-2]
            current_center = centers_in_order[-1]
            next_center = centers_in_order[0]
            if are_centers_neighbouring(next_center, current_center, hexagon_height):
                start_point = ((previous_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                               (previous_center[1] - current_center[1])/2 + int(0.5*hexagon_height))

                end_point = ((next_center[0] - current_center[0])/2 + int(0.7*hexagon_height),
                             (next_center[1] - current_center[1])/2 + int(0.5*hexagon_height))



        image_to_paste = olh.make_hexagon_spiral(turns,
                                                 (int(1.4 * hexagon_height), hexagon_height),
                                                 start_point,
                                                 end_point)
        output_image.paste(image_to_paste, (int(hex_center[0] - 0.7 * hexagon_height), int(hex_center[1] - hexagon_height // 2)),
                           mask=image_to_paste.convert("RGBA"))

    return output_image

def hexagon_image_random_start_end_2(filename, canvas_size, hexagon_height):
    # get turns for each color
    calibrate_spiral.make_calibration_file(hexagon_height)
    with open("calibration_file.txt", "r") as calib_file:
        turns_by_color = [float(line.split(": ")[1]) for line in calib_file.readlines()]

    w, h = canvas_size
    output_image = Image.new("L", (w, h), 255)
    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)

    original_image = Image.open(filename).convert("L").resize((700, 700))
    original_w, original_h = original_image.size

    # for each hexagon center in pixel list get the average color
    progress_index = 1
    for hexagon_order, hex_center in enumerate(hexagon_centers):
        # print progress
        progress = hexagon_order/len(hexagon_centers)
        if progress > progress_index/100:
            print(f"Progress: {progress:.2f}%")
            progress_index += 1

        scaled_hex_center = (int(hex_center[0]*original_w/w), int(hex_center[1]*original_h/h))
        if 0 <= scaled_hex_center[0] < original_w and 0 <= scaled_hex_center[1] < original_h:
            color = original_image.getpixel(scaled_hex_center)

            turns = turns_by_color[color]

            start_point, end_point = (0, 0), (hexagon_height, hexagon_height)

            image_to_paste = olh.make_hexagon_spiral(turns,
                                                     (int(1.4 * hexagon_height), hexagon_height),
                                                     start_point,
                                                     end_point)
            output_image.paste(image_to_paste, (int(hex_center[0] - 0.7 * hexagon_height), int(hex_center[1] - hexagon_height // 2)),
                               mask=image_to_paste.convert("RGBA"))

    return output_image

def hexagon_image_random_start_end(filename, canvas_size, hexagon_height):
    w, h = canvas_size

    output_image = Image.new("L", (w, h), 255)

    hexagon_centers = olh.get_hexagon_centers(w, h, hexagon_height)
    hexagon_matrix = olh.get_hexagon_matrix(hexagon_height)
    original_image = Image.open(filename).convert("L").resize((500, 500))
    scale_factor = original_image.size[0]/w
    original_hexagon_height = int(hexagon_height*scale_factor)
    original_hexagon_matrix = olh.get_hexagon_matrix(original_hexagon_height)
    original_pixels = original_image.load()

    original_hexagon_area = np.count_nonzero(original_hexagon_matrix == 1)

    progress_index = 1
    for hexagon_order, c in enumerate(hexagon_centers):
        if (c[0] - w/2)**2 + (c[1] - h/2)**2 > (h**2)/4:
            continue



        # get intensity of the region in the matrix
        is_close_to_border = olh.is_center_close_to_border(w, h, c, hexagon_height)
        total_intensity = 0
        partial_hexagon_area = 0
        for x in range(int(c[0]*scale_factor - original_hexagon_matrix.shape[0] // 2), int(c[0]*scale_factor + original_hexagon_matrix.shape[0] // 2)):
            for y in range(int(c[1]*scale_factor - original_hexagon_matrix.shape[1] // 2), int(c[1]*scale_factor + original_hexagon_matrix.shape[1] // 2)):
                matrix_x = int(x - c[0]*scale_factor + original_hexagon_matrix.shape[0] // 2)
                matrix_y = int(y - c[1]*scale_factor + original_hexagon_matrix.shape[1] // 2)
                if 0 <= x < w*scale_factor and 0 <= y < h*scale_factor and original_hexagon_matrix[matrix_x][matrix_y] == 1:
                    total_intensity += original_pixels[x, y]
                    if is_close_to_border:
                        partial_hexagon_area += 1

        if not is_close_to_border:
            total_intensity /= original_hexagon_area
        elif partial_hexagon_area != 0:
            total_intensity /= partial_hexagon_area
        else:
            total_intensity = 0

        # set the color of the hexagon to total_intensity
        turns = (255 - total_intensity) / 255 * 15

        start_point, end_point = (0, 0), (hexagon_height, hexagon_height)
        current_center = c

        image_to_paste = olh.make_hexagon_spiral(turns,
                                                 (int(1.4 * hexagon_height), hexagon_height),
                                                 start_point,
                                                 end_point)
        output_image.paste(image_to_paste, (int(c[0] - 0.7 * hexagon_height), int(c[1] - hexagon_height // 2)),
                           mask=image_to_paste.convert("RGBA"))

    return output_image

def set_final_screen_pixel_SBS(app):
    pass

def set_final_screen_superpixel_SBS(app):
    pass


if __name__ == "__main__":
    output_hexagon_height = 35
    nPixels = 100
    output_image_size = (int(output_hexagon_height*nPixels), int(output_hexagon_height*nPixels))

    final_image_2 = hexagon_image_from_given_file(output_image_size, output_hexagon_height)
    final_image_2.show()
    final_image_2.save("cute_image_4_output_final_2.jpg")

