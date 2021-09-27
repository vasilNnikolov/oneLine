import tkinter as tk
from tkinter import messagebox
from random import shuffle

import ImageDraw
import ImageFont
import PIL.Image
from PIL import Image, ImageTk
from os import path


def on_hex_center_tutorial():
    n_lines = 50
    hexagon_centers_filename = "cute_image_4_centers_order_final_v3.txt"
    final_image_filename = "cute_image_4_hexagon_output_final_v3.jpg"

    try:
        final_image = Image.open(final_image_filename)
    except Exception:
        print("Error in filenames")

    w, h = final_image.size

    with open(hexagon_centers_filename, "r") as f:
        centers = [tuple(map(float, c[1:-2].split(", "))) for c in f.readlines()]

    shuffle(centers)

    root = tk.Tk()
    root.geometry("1000x1000")

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.place(x=100, y=100)
    hexagon_height = 35
    dw, dh = w/n_lines, h/n_lines
    font = ImageFont.truetype("Roboto-Black.ttf", 10)

    def on_next_center():
        # generate image to be shown in image canvas
        if len(centers) > 0:
            current_center = centers.pop(0)
            # find min and max coordinates for the image
            current_hexagon_image = final_image.crop((current_center[0] - dw,
                                                      current_center[1] - dh,
                                                      current_center[0] + dw,
                                                      current_center[1] + dh))

            draw = ImageDraw.Draw(current_hexagon_image)
            visible_xs = range(int(current_center[0]/dw), int(current_center[0]/dw + 2))
            visible_ys = range(int(current_center[1]/dh), int(current_center[1]/dh + 2))

            for x in visible_xs:
                draw.line(((x + 1)*dw - current_center[0], 0,
                           (x + 1)*dw - current_center[0], 2*dh))

                # draw the lines coordinates
                draw.text(((x + 1)*dw - current_center[0], 2*dh - 20),
                          str(x), font=font)
                draw.text(((x + 1)*dw - current_center[0], 20),
                          str(x), font=font)

            for y in visible_ys:
                draw.line((0, (y + 1)*dh - current_center[1],
                           2*dw, (y + 1)*dh - current_center[1]))

                # draw the lines coordinates
                draw.text((0, (y + 1)*dh - current_center[1] - 20),
                          str(n_lines - y), font=font)
                draw.text((2*dw - 50, (y + 1)*dh - current_center[1] - 20),
                          str(n_lines - y), font=font)

            draw.ellipse((dw - 2, dh - 2, dw + 2, dh + 2), fill="red")
            current_hexagon_image = current_hexagon_image.resize((800, 800))

            canvas_image = ImageTk.PhotoImage(current_hexagon_image)
            canvas.create_image(0, 0, anchor=tk.NW, image=canvas_image)
            canvas.image = canvas_image
        else:
            print("You have finished the drawing. Exiting")
            root.destroy()

    next_hexagon_button = tk.Button(root, text="Next hexagon", command=on_next_center)
    next_hexagon_button.place(x=500, y=950)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print(f"Progress: {100*(1 - len(centers)/8756):.0f}%")
            # edit the file by removing the hexagon centers which have been drawn
            with open(hexagon_centers_filename, "w") as f:
                f.writelines([f"{c}\n" for c in centers])

            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.mainloop()

def on_grid_center_tutorial():
    n_lines = 50 # 50 nails to a side of the canvas

    final_image_filename = "cute_image_4_hexagon_output_final.jpg"
    centers_of_grid_filename = "grid_centers_filename.txt"

    try:
        final_image = Image.open(final_image_filename)

    except Exception:
        print("Error in filename")
        return

    w, h = final_image.size

    if not path.isfile(centers_of_grid_filename):
        # generate file
        non_empty_squares = []
        for x in range(n_lines):
            for y in range(n_lines):
                square = final_image.crop((x*w/n_lines, y*h/n_lines, (x + 1)*w/n_lines, (y + 1)*h/n_lines))
                average_color = square.resize((1, 1), resample=PIL.Image.LANCZOS).getpixel((0, 0))
                if average_color < 254:
                    non_empty_squares.append((x, y))

        # shuffle center of grid order
        shuffle(non_empty_squares)
        with open(centers_of_grid_filename, "w") as grid_file:
            grid_file.writelines([f"{square[0]}, {square[1]}\n" for square in non_empty_squares])

    non_empty_squares = []
    with open(centers_of_grid_filename, "r") as grid_file:
        non_empty_squares = [tuple(map(int, line.split(", "))) for line in grid_file.readlines()]

    print(non_empty_squares)

    root = tk.Tk()
    root.geometry("1000x1000")

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.place(x=100, y=100)

    def on_next_center():
        # generate image to be shown in image canvas
        if len(non_empty_squares) > 0:
            current_square = non_empty_squares.pop(0)
            current_hexagon_image = final_image.crop((current_square[0]*w/n_lines,
                                                      current_square[1] * h / n_lines,
                                                      (current_square[0] + 1) * w / n_lines,
                                                      (current_square[1] + 1) * h / n_lines))
            current_hexagon_image = current_hexagon_image.resize((800, 800))

            draw = ImageDraw.Draw(current_hexagon_image)
            font = ImageFont.truetype("Roboto-Black.ttf", 40)
            draw.text((0, 0), f"{current_square[0], n_lines - current_square[1] - 1}", fill="green", font=font)

            canvas_image = ImageTk.PhotoImage(current_hexagon_image)
            canvas.create_image(0, 0, anchor=tk.NW, image=canvas_image)
            canvas.image = canvas_image
        else:
            print("You have finished the drawing. Exiting")
            root.destroy()

    next_hexagon_button = tk.Button(root, text="Next hexagon", command=on_next_center)
    next_hexagon_button.place(x=500, y=950)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            print(f"Progress: {100*(1 - len(non_empty_squares)/8756):.0f}%")
            print("Aaaaaaaaaaaaaaaaa")
            # edit the file by removing the hexagon centers which have been drawn
            with open(centers_of_grid_filename, "w") as grid_file:
                grid_file.writelines([f"{square[0]}, {square[1]}\n" for square in non_empty_squares])

            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    tk.mainloop()

if __name__ == "__main__":
    on_hex_center_tutorial()

