
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def equation_plane_plot(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, xyzArray):
    """
    :return: plots each segement and according Plane
    """

    a1 = x2 - x1
    b1 = y2 - y1
    c1 = z2 - z1
    a2 = x3 - x1
    b2 = y3 - y1
    c2 = z3 - z1
    a = b1 * c2 - b2 * c1
    b = a2 * c1 - a1 * c2
    c = a1 * b2 - b1 * a2
    d = (- a * x1 - b * y1 - c * z1)

    z = (1 / c) * (a * x1 + b * y1 + c * z1 - a * x4 - b * y4)

    if z > z4:
        sign = 1

    else:
        sign = -1

    dist = z - z4

    # plot the original points. We use zip to get 1D lists of x, y and z
    # coordinates.
    p1 = [x1, y1, z1]
    p2 = [x2, y2, z2]
    p3 = [x3, y3, z3]

    # point coordinates for scatter
    X = [x[0] for x in xyzArray]
    Y = [x[1] for x in xyzArray]
    Z = [x[2] for x in xyzArray]

    xx, yy= np.meshgrid(range(int(min(X)-2), int(max(X))+2), range(int(min(Y)-2), int(max(Y))+2))
    z = (-a * xx - b * yy - d) * 1. /c


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # plot the surface

    ax.plot_surface(xx, yy, z, alpha=0.2)
    ax.plot(*zip(p1, p2, p3), color='r', linestyle=' ', marker='o')
    ax.scatter(X, Y, Z, color='green')

    # adjust the view so we can see the point/plane alignment

    ax.view_init(0, 22)
    plt.tight_layout()
    plt.show()

    return dist, sign

if __name__ == '__main__':
    print("This function should be used in a automated way.")
    x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, xyzArray = input(
        "Input: x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, xyzArray: ").split(",")
    equation_plane_plot(x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4, xyzArray)