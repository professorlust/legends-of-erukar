class Range:
    def make(x0, xf, y0, yf):
        for x in range(x0, xf+1):
            for y in range(y0, yf+1):
                yield (x,y)
