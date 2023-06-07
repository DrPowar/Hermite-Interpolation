import math
import numpy
import matplotlib.pyplot as plt
import os


class Point:
    def __init__(self, x, y, dx=None, ddx=None):
        self.x = x  # coordinate x
        self.y = y  # y coordinate
        self.dx = dx  # first order derivative
        self.ddx = ddx  # second derivative

    def validate_dx_ddx(self):
        if self.dx is not None and self.ddx is not None:
            raise ValueError("Both dx and ddx cannot be defined simultaneously.")


def hermite_polynomial_coefficients(points):
    left_part = []
    right_part = []

    # Algorithm 1 - finding the order of a polynomial
    order = len(points) - 1
    for point in points:
        if not isinstance(point, Point):
            raise ValueError("Array elements must be instances of the Point class")

        if point.dx is not None:
            order += 1
        elif point.ddx is not None:
            order += 1

    # Algorithm 2 - the right part of SLAR
    for point in points:
        right_part.append(point.y)
    for point in points:
        if point.dx is not None:
            right_part.append(point.dx)
        elif point.ddx is not None:
            right_part.append(point.ddx)

    # Algorithm 3 - finding the coefficients of a polynomial
    for point in points:
        point_coefficients = []
        for i in range(order, -1, -1):
            point_coefficients.append(point.x ** i)
        left_part.append(point_coefficients)

    for point in points:
        point_coefficients = []
        for i in range(order, -1, -1):
            if point.dx is not None:
                point_coefficients.append(i * point.x ** (i - 1))
            elif point.ddx is not None:
                point_coefficients.append((i * (i - 1)) * point.x ** (i - 2))
        if len(point_coefficients) > 0: left_part.append(point_coefficients)

    return numpy.linalg.solve(left_part, right_part)


# Interpolation function
def hermit_interpolation(points, step):
    end = points[0].x
    start = points[0].x

    for point in points:
        if point.x > end:
            end = point.x
        if point.x < start:
            start = point.x

    coefficients = hermite_polynomial_coefficients(points)

    order = len(coefficients) - 1
    y_result = []
    x_result = []
    x = start
    while x < end:
        y = 0
        for i in range(order, -1, -1):
            y += coefficients[order - i] * x ** i
        y_result.append(y)
        x_result.append(x)
        x += step
    return y_result, x_result

def plot_visualization(x_values, y_values, points):
    highlight_points = []
    for point in points:
        one_point = []
        one_point.append(point.x)
        one_point.append(point.y)
        highlight_points.append(one_point)

    highlight_x = [point[0] for point in highlight_points]
    highlight_y = [point[1] for point in highlight_points]

    plt.scatter(highlight_x, highlight_y, marker='o', color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)

    plt.plot(x_values, y_values)
    plt.show()

def data_input():
    input_size = int(input("Enter the number of points:"))
    points = []
    i = 0

    while i < input_size:
        x = input(f"Enter the x value for {i + 1} point (not less than the x value of the previous point):")
        y = input(f"Enter the y value for {i + 1} point:")
        dx = input(
            f"Enter the value of the derivative of the first order for {i + 1} point (enter - if you do not want to specify the derivative of the first order):")
        ddx = input(
            f"Enter the value of the derivative of the second order for {i + 1} point (enter - if you do not want to specify the derivative of the second order):")

        if dx == "-":
            dx = None
        if ddx == "-":
            ddx = None

        point = Point(float(x), float(y), dx if dx is None else float(dx), ddx if ddx is None else float(ddx))

        if point.validate_dx_ddx() == True:
            continue
        else:
            points.append(point)
            i += 1

    y_values, x_values = hermit_interpolation(points, 0.05)

    # Tab function
    for i in range(len(x_values)):
        print(f"X: {x_values[i]:<3.2f}, Y: {y_values[i]:<10.5f}")

    # Chart
    plot_visualization(x_values, y_values, points)


arr = data_input()