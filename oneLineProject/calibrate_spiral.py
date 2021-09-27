import oneLineHexagons as olh


MAX_TURNS = 8

def get_fill(turns, hexagon_height):
    """
    percentage of the hexagon that is filled with black pixels
    :param turns:
    :param hexagon_height:
    :return:
    """
    hex_spiral = olh.make_hexagon_spiral(turns,
                                         (int(1.4 * hexagon_height), hexagon_height),
                                         (0, 0),
                                         (hexagon_height, hexagon_height))
    pixels = hex_spiral.load()
    black_pixels_count = 0
    w, h = hex_spiral.size
    for x in range(w):
        for y in range(h):
            if pixels[x, y][0] < 10 and pixels[x, y][1] > 100:
                black_pixels_count += 1

    return black_pixels_count/(w*h)

def make_calibration_file(hexagon_height):
    n_points = 256
    max_fill = get_fill(MAX_TURNS, hexagon_height)
    turn_values = [i*MAX_TURNS/n_points for i in range(n_points)]
    colors = [max(0, 255*(1 - get_fill(turns, hexagon_height)/max_fill)) for turns in turn_values]

    colors_output = [] # value is turns needed to achieve the particular color
    for target_color in range(256):
        if target_color > max(colors):
            colors_output.append(0)
        else:
            for i in range(n_points - 1):
                if colors[i] > target_color > colors[i + 1]:
                    # interpolate turns
                    target_turns = turn_values[i + 1] + (target_color - colors[i + 1])/(colors[i] - colors[i + 1])*MAX_TURNS/n_points
                    colors_output.append(target_turns)
                    break
                if i == n_points - 2:
                    colors_output.append(MAX_TURNS)

    with open("calibration_file.txt", "w") as file:
        file.writelines([f"{color}: {turns}\n" for color, turns in enumerate(colors_output)])


if __name__ == "__main__":
    make_calibration_file(35)
