import math
import random
import numpy as np

from PIL import Image, ImageDraw
from oneLineLibrary import atan3, f


def get_hexagon_centers(w, h, hexagon_height):
    # first hexagon center is at (0, 0)
    centers = []
    n_vertical = int(h/hexagon_height)
    n_horisontal = int(2*w/(hexagon_height*3**0.5))
    for y in range(n_vertical + 1):
        start_y = hexagon_height*y
        centers.append((0, start_y))
        for x in range(1, n_horisontal + 1):
            if x%2 == 1:
                centers.append((x*hexagon_height*3**0.5/2, start_y + hexagon_height/2))
            else:
                centers.append((x*hexagon_height*3**0.5/2, start_y))

    return centers

def is_center_close_to_border(w, h, center, hexagon_height):
    if center[0] < hexagon_height or center[0] > h - hexagon_height or center[1] < 1.4*hexagon_height or center[1] > w - 1.4*hexagon_height:
        return True
    return False

def get_hexagon_matrix(hexagon_height):
    """
    :param hexagon_height:
    :return: an np array of width hexagon_heigth*2/sqrt(3) and height hexagon_height
    the array is one if the pixel is in the hexagon and 0 otherwise
    """
    w, h = int(hexagon_height*2/3**0.5), hexagon_height
    output = np.zeros((w, h))

    root_3 = 3**0.5

    line_equations = [lambda x: hexagon_height/2,
                      lambda x: -root_3*x + hexagon_height,
                      lambda x: root_3*x - hexagon_height,
                      lambda x: -hexagon_height/2,
                      lambda x: -root_3*x - hexagon_height,
                      lambda x: root_3*x + hexagon_height]


    for x in range(int(-w/2), int(w/2)):
        for y in range(int(-h/2), int(h/2)):
            # long messy test whether point is inside hexagon
            if y <= line_equations[0](x) and y <= line_equations[1](x) and y >= line_equations[2](x) and y >= line_equations[3](x) and y >= line_equations[4](x) and y <= line_equations[5](x):
                output[x + int(w/2)][y + int(h/2)] = 1
            else:
                output[x + int(w/2)][y + int(h/2)] = 0


    return output

def stretch_distance_hexagon(angle, hexagon_height):
    while angle > math.pi/3:
        angle -= math.pi/3

    # now angle is between 0 and 60 degrees
    circle_angle = 8/180*math.pi
    if angle < circle_angle or angle > math.pi/3 - circle_angle:
        return hexagon_height/(2*math.cos(math.pi/6 - circle_angle))
    return hexagon_height/(2*math.cos(math.pi/6 - angle))

def make_hexagon_spiral(turns, image_size, start_point, end_point):
    R = min(image_size[0], image_size[1])/2
    result = Image.new("LA", image_size, 1)
    N = 5000
    linewidth = max(1, int(image_size[0]/150))
    angle_start = atan3(image_size[1]/2 - start_point[1], start_point[0] - image_size[0]/2)
    angle_end = atan3(image_size[1]/2 - end_point[1], end_point[0] - image_size[0]/2)

    if angle_end < angle_start:
        angle_end, angle_start = angle_start, angle_end
        start_point, end_point = end_point, start_point
    alpha1 = -angle_start
    alpha2 = -angle_end + math.pi
    draw = ImageDraw.Draw(result, "LA")
    last_x_start, last_y_start = 0, 0
    last_x_end, last_y_end = 0, 0
    dN = (alpha2 - alpha1)/2
    for i in range(N, 0, -1):
        t = i/N
        theta_start = (turns - dN)*(1 - f(t)*t) - alpha1
        theta_end = (turns + dN)*(1 - f(t)*t) - alpha2
        r_start = t*stretch_distance_hexagon(theta_start, 2*R)
        r_end = t*stretch_distance_hexagon(theta_end, 2*R)

        center_start = (image_size[0]/2 + r_start*math.cos(theta_start), image_size[1]/2 - r_start*math.sin(theta_start))
        center_end = (image_size[0]/2 - r_end*math.cos(theta_end), image_size[1]/2 + r_end*math.sin(theta_end))
        if last_x_start != 0 and last_y_start != 0:
            draw.line((center_start[0], center_start[1], last_x_start, last_y_start), fill="black", width=linewidth)
            draw.line((center_end[0], center_end[1], last_x_end, last_y_end), fill="black", width=linewidth)
        last_x_start, last_y_start = center_start
        last_x_end, last_y_end = center_end

    data = result.getdata()
    new_data = []
    for d in data:
        if d[0] == 1:
            new_data.append((1, 0))
        else:
            new_data.append(d)

    result.putdata(new_data)

    return result

def pick_random_start_end(image_size):
    side_options = ["left", "right", "up", "down"]
    random.shuffle(side_options)
    sides = side_options[:2]
    ends = [[0, 0], [0, 0]]
    for side_index, s in enumerate(sides):
        if s == "left":
            ends[side_index] = (0, random.randint(0, image_size[1]))
        elif s == "right":
            ends[side_index] = (image_size[0] - 1, random.randint(0, image_size[1]))
        elif s == "up":
            ends[side_index] = (random.randint(0, image_size[0] - 1), 0)
        elif s == "down":
            ends[side_index] = (random.randint(0, image_size[0] - 1), image_size[1] - 1)

    return ends

def make_hexagon_tiling():
    w, h = 500, 500
    hexagon_height = 50
    hexagon_width = int(hexagon_height*2/3**0.5)

    image = Image.new("RGB", (w, h), (0, 0, 0))
    centers = get_hexagon_centers(w, h, hexagon_height)
    d = ImageDraw.Draw(image)
    r = 1
    hexagon_matrix = get_hexagon_matrix(hexagon_height)
    pixels = image.load()
    for c in centers:
        random_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
        for x in range(hexagon_width):
            for y in range(hexagon_height):
                if hexagon_matrix[x][y] == 1 and 0 <= x + c[0] - hexagon_width//2 < w and 0 <= y + c[1] - hexagon_height//2 < h:
                    pixels[x + c[0] - hexagon_width//2, y + c[1] - hexagon_height//2] = random_color

        d.ellipse((c[0] - 1, c[1] - r, c[0] + r, c[1] + r), fill="red")



    image.show()

def hexagon_matrix_full_image(w, h, hexagon_height):
    centers = get_hexagon_centers(w, h, hexagon_height)
    output_matrix = np.empty((w, h))
    output_matrix.fill(-1)
    hexagon_matrix = get_hexagon_matrix(hexagon_height)
    hex_matrix_w, hex_matrix_h = hexagon_matrix.shape
    for center_index, center in enumerate(centers):
        for x in range(hex_matrix_w):
            for y in range(hex_matrix_h):
                output_x = int(x - hex_matrix_w//2 + center[0])
                output_y = int(y - hex_matrix_h//2 + center[1])
                if 0 <= output_x < w and 0 <= output_y < h and hexagon_matrix[x][y] == 1:
                    output_matrix[output_x][output_y] = center_index

    return output_matrix


if __name__ == "__main__":
    print(pick_random_start_end((100, 100)))


