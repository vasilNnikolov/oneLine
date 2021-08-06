import random

from PIL import Image, ImageDraw
import numpy as np


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

if __name__ == "__main__":
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




