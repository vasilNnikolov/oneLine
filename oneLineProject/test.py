impor![](cute_image_3_random_SE.jpg)t finalScreen

if __name__ == "__main__":
    nPixels = 100
    hexagon_height = 20
    w = nPixels * hexagon_height
    h = w
    filenames = ["cute_image_5.jpg"]
    for f in filenames:
        final_image = finalScreen.hexagon_image_random_start_end(f, (w, h), hexagon_height)

        final_image.save(f"{f.split('.')[0]}_random_SE.jpg")
