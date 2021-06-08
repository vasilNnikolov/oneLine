import math
import tkinter as tk
import random
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

def s(t):
    return 1/(1 + math.exp(-50*(t - 0.85)))

def f(t):
    return 1.1*(1.1/(t + 0.1) - 1)*s(t) + 1

def atan3(y, x):
    if y > 0:
        return math.atan2(y, x)
    else:
        return math.atan2(y, x) + 2*math.pi

def make_spiral(turns, image_size, start_point, end_point):
    R = min(image_size[0], image_size[1])/2
    result = Image.new("RGB", image_size, "white")
    N = 1000
    angle_start = atan3(image_size[1]/2 - start_point[1], start_point[0] - image_size[0]/2)
    angle_end = atan3(image_size[1]/2 - end_point[1], end_point[0] - image_size[0]/2)

    if angle_end < angle_start:
        angle_end, angle_start = angle_start, angle_end
        start_point, end_point = end_point, start_point
        print("swap")
    print(angle_start, angle_end)
    draw = ImageDraw.Draw(result)
    line_width = 3
    last_x_start, last_y_start = 0, 0
    last_x_end, last_y_end = 0, 0
    for i in range(N, 0, -1):
        t = i/N
        r = R*t

        theta_start = turns*(1 - f(t)*t) - angle_start*s(t)
        theta_end = turns*(1 - f(t)*t) - angle_end*s(t)
        center_start = (image_size[0]/2 + r*math.cos(theta_start), image_size[1]/2 - r*math.sin(theta_start))
        center_end = (image_size[0]/2 - r*math.cos(theta_end), image_size[1]/2 + r*math.sin(theta_end))
        if last_x_start != 0 and last_y_start != 0:
            draw.line((center_start[0], center_start[1], last_x_start, last_y_start), fill="black")
            draw.line((center_end[0], center_end[1], last_x_end, last_y_end), fill="black")
        last_x_start, last_y_start = center_start
        last_x_end, last_y_end = center_end

    return result

if __name__ == "__main__":
    image_size = (500, 500)

    start_angle = 2*random.random()*math.pi
    end_angle = 2*random.random()*math.pi
    start = (250 + 250*math.cos(start_angle), 250 + 250*math.sin(start_angle))
    end = (250 + 250*math.cos(end_angle), 250 + 250*math.sin(end_angle))
    print(start, end)

    img = make_spiral(14, image_size, start, end)
    draw = ImageDraw.Draw(img)
    draw.ellipse((start[0] - 5, start[1] - 5, start[0] + 5, start[1] + 5), fill="green")
    draw.ellipse((end[0] - 5, end[1] - 5, end[0] + 5, end[1] + 5), fill="red")
    img.show()

