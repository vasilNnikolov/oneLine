import finalScreen

if __name__ == "__main__":
    nPixels = 100
    hexagon_height = 20
    w = nPixels * hexagon_height
    h = w
    filenames = ["cute_image_4.jpg"]
    for f in filenames:
        final_image = finalScreen.hexagon_image_random_start_end_2(f, (w, h), hexagon_height)

        final_image.save(f"{f.split('.')[0]}_random_SE_2.jpg")
