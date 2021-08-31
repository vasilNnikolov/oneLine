def test_spiral_making():
    import oneLineHexagons as olh
    w, h = 700, 500
    olh.make_hexagon_spiral(10, (w, h), (-100, 600), (400, -400)).show()

if __name__ == "__main__":
    test_spiral_making()