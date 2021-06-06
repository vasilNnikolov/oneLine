import tkinter as tk
from PIL import Image, ImageDraw
def make_picture_circular(image):
    w, h = image.size
    output = Image.new("LA", (w, h), 0)
    output_pixels = output.load()

    for y in range(h):
        for x in range(w):
            if (x/w - 0.5)**2 + (y/h - 0.5)**2 <= 0.25:
                output_pixels[x, y] = image.getpixel((x, y))
    return output


def make_spiral(angle, image_size, start_point, end_point):
    result = Image.new("LA", image_size, 0)



class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        # Vertical and Horizontal scrollbars
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        # Grid and configure weight.
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        # Set the scrollbars to the canvas
        self.cnvs.config(xscrollcommand=self.h_scroll.set,
                           yscrollcommand=self.v_scroll.set)
        # Set canvas view to the scrollbars
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        # Assign the region to be scrolled
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
    #     self.cnvs.bind_class(self.cnvs, "<MouseWheel>", self.mouse_scroll)
    #
    # def mouse_scroll(self, evt):
    #     if evt.state == 0 :
    #         self.cnvs.yview_scroll(-1*(evt.delta), 'units') # For MacOS
    #         self.cnvs.yview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
    #     if evt.state == 1:
    #         self.cnvs.xview_scroll(-1*(evt.delta), 'units') # For MacOS
    #         self.cnvs.xview_scroll(int(-1*(evt.delta/120)), 'units') # For windows
