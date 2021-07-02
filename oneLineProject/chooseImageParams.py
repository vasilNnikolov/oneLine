import tkinter as tk

def set_second_window(app):
    app.clear_window()
    app.window.title("Choose image parameters")

    # create pixel type label
    pixel_type_label = tk.Label(app.window, text="Pixelisation type")
    pixel_type_label.place(x=int(0.3 * app.size[0]), y=int(0.1 * app.size[1]))

    # create pixel type dropdown menu
    pixel_options = ["Pixel", "Superpixel"]

    pixel_type = tk.StringVar(app.window)
    pixel_type.set(pixel_options[0])
    pixel_dropdown = tk.OptionMenu(app.window, pixel_type, *pixel_options)
    pixel_dropdown.place(x=int(0.5 * app.size[0]), y=int(0.1 * app.size[1]))

    # create instruction type label
    instruction_type_label = tk.Label(text="Instruction type")
    instruction_type_label.place(x=int(0.3 * app.size[0]), y=int(0.3 * app.size[1]))

    # create instruction type dropdown menu
    instruction_options = ["Export", "Step by step"]

    instruction_type = tk.StringVar(app.window)
    instruction_type.set(instruction_options[0])
    instruction_type_dropdown = tk.OptionMenu(app.window, instruction_type, *instruction_options)
    instruction_type_dropdown.place(x=int(0.5 * app.size[0]), y=int(0.3 * app.size[1]))

    # create number of pixels label
    nPixels_label = tk.Label(text="Sidelength")
    nPixels_label.place(x=int(0.3 * app.size[0]), y=int(0.5 * app.size[1]))

    # create number of pixels input field
    nPixels_variable = tk.StringVar()
    nPixels_variable.set("20")
    nPixels_entry = tk.Entry(app.window, textvariable=nPixels_variable)
    nPixels_entry.place(x=int(0.5 * app.size[0]), y=int(0.5 * app.size[1]))

    # set controll buttons
    def next_button_action():
        # verify whether input data is correct
        # not done yet
        app.nPixels = int(nPixels_variable.get())
        app.pixel_list = []
        app.set_final_screen(instruction_type.get(), pixel_type.get())

    app.set_next_button(command=lambda: next_button_action(), enabled=True)
    app.set_back_button(command=app.set_start_screen, enabled=True)
