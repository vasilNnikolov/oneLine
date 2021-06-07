import math
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


def make_spiral(turns, image_size, start_point, end_point):
    # r = R0 - (R0-c/2)/angle * theta - c/(1 + e^(-k1*(theta - angle))) + c/(1+e^(k2*theta))
    # k1 determines how sharp the central bar is
    # k2 determines how sharp the start and end of the spiral are
    # c determines the size of the central bar and the start and end of the spiral
    # (r, theta) -> (r, theta + k*(R-r))
    R = min(image_size)/2
    result = Image.new("LA", image_size, 0)
    N = 300
    draw = ImageDraw.Draw(result)
    line_width = 2
    for i in range(N):
        r = R*(N/2 - i)/N
        theta = math.pi/3

        r_new = r
        theta_new = theta + turns*(R -r)
        center = (image_size[0]/2 + r_new*math.cos(theta_new), image_size[1]/2 + r_new*math.sin(theta_new))
        draw.ellipse((center[0] - line_width,
                      center[1] - line_width,
                      center[0] + line_width,
                      center[1] + line_width), fill="white")

    return result

img = make_spiral(5, (500, 500), 0, 0)

img.show()





