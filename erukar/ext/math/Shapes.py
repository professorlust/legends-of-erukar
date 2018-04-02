class Shapes:
    def rect(x_range, y_range):
        x0, xf = x_range
        y0, yf = y_range
        for x in range(x0, xf+1):
            for y in range(y0, yf+1):
                yield (x,y)

