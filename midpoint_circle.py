def midpoint_circle(x_center, y_center, radius):
    x = 0
    y = radius
    d = 1 - radius
    points = []

    def plot_circle_points(xc, yc, x, y):
        return [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]

    points.extend(plot_circle_points(x_center, y_center, x, y))

    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        points.extend(plot_circle_points(x_center, y_center, x, y))

    return points
