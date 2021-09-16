import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# hexagon_centers_filename = input("Enter the hexagon centers filename: ")
# final_image_filename = input("Enter the final image filename: ")
hexagon_centers_filename = "centers_order.txt"
final_image_filename = "hexagon__output_final.jpg"

try:
    final_image = Image.open(final_image_filename)
    with open(hexagon_centers_filename, "r") as f:
        centers = f.readlines()

    centers = [tuple(map(float, c[1:-2].split(", "))) for c in centers]

    root = tk.Tk()
    root.geometry("1000x1000")

    canvas = tk.Canvas(root, width=800, height=800)
    canvas.place(x=100, y=100)

    def on_next_center():
        # generate image to be shown in image canvas
        if len(centers) > 0:
            current_center = centers.pop(0)
            current_hexagon_image = final_image.crop((current_center[0] - 50,
                                                      current_center[1] - 50,
                                                      current_center[0] + 50,
                                                      current_center[1] + 50)).resize((800, 800))

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
            # edit the file by removing the hexagon centers which have been drawn
            with open(hexagon_centers_filename, "w") as f:
                f.writelines([f"{c}\n" for c in centers])

            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)


    tk.mainloop()

except Exception:
    print("Error in filenames")
