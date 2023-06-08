import dearpygui.dearpygui as dpg
from main import Point, hermit_interpolation

dpg.create_context()

i = 0
end_items = []
start_items = []
input_count = 0
points = []

y_values, x_values = [], []

x_dots, y_dots = [], []

def input_point_value():
    global i

    if i == input_count:
        return

    x = dpg.get_value(input_X)
    y = dpg.get_value(input_Y)
    dx = dpg.get_value(input_DX)
    ddx = dpg.get_value(input_DDX)

    if dx == "-":
        dx = None
    if ddx == "-":
        ddx = None

    try:
        point = Point(float(x), float(y), dx if dx is None else float(dx), ddx if ddx is None else float(ddx))
    except:
        dpg.set_value(input_DX, "DX and DDX cannot be simultaneously defined at the same point.")
        dpg.set_value(input_DDX, "DX and DDX cannot be simultaneously defined at the same point.")
        dpg.set_value(input_X, "Wrong value")
        dpg.set_value(input_Y, "Wrong value.")
        return

    if point.validate_dx_ddx() == True:
        dpg.set_value(input_DX, "DX and DDX cannot be simultaneously defined at the same point.")
        dpg.set_value(input_DDX, "DX and DDX cannot be simultaneously defined at the same point.")
    elif len(points) >= 1 and points[i - 1].x >= float(x):
        dpg.set_value(input_X, "Wrong value")
        dpg.set_value(input_Y, "Wrong value.")
    else:
        points.append(point)
        i += 1
        dpg.set_value(input_X, "")
        dpg.set_value(input_Y, "")
        dpg.set_value(input_DX, "")
        dpg.set_value(input_DDX, "")
        if i == input_count:
            plot_visualization()
            return
        dpg.set_value(text_X,
                      f"Enter the x value for point {i + 1}:")
        dpg.set_value(text_Y, f"Enter the y value for point {i + 1}:")
        dpg.set_value(text_DX,
                      f"Enter the dx value for {i + 1}:")
        dpg.set_value(text_DDX,
                      f"Enter the ddx value of {i + 1}:")

def restart_button():
    global i, points, input_count
    i = 0
    points = []
    input_count = 0

    for item in end_items:
        dpg.hide_item(item)
    for item in start_items:
        dpg.show_item(item)

    dpg.set_item_callback(start_button, input_data_button)

    dpg.set_value(text_X,
                  f"Enter the x value for point {i + 1}:")
    dpg.set_value(text_Y, f"Enter the y value for point {i + 1}:")
    dpg.set_value(text_DX,
                  f"Enter the dx value for {i + 1}:")
    dpg.set_value(text_DDX,
                  f"Enter the ddx value of {i + 1}:")


def plot_visualization():
    global y_values, x_values, x_dots, y_dots
    y_values, x_values = hermit_interpolation(points, 0.05)

    x_dots = [point.x for point in points]
    y_dots = [point.y for point in points]

    max_plot_x = max(x_values) + 1
    min_plot_x = min(x_values) - 1

    max_plot_y = max(y_values) + 1
    min_plot_y = min(y_values) - 1

    dpg.set_value('series_tag', [x_values, y_values])

    dpg.set_value('scatter_series', [x_dots, y_dots])
    dpg.set_axis_limits("x_axis", min_plot_x, max_plot_x)

    dpg.set_axis_limits("y_axis", min_plot_y, max_plot_y)


def input_data_button():
    global input_count
    try:
        if int(dpg.get_value(input_data)) >= 1:
            input_count = int(dpg.get_value(input_data))
            # dpg.hide_item(input_data)
            # dpg.hide_item(text_count)
            for item in start_items:
                dpg.hide_item(item)

            dpg.set_item_callback(start_button, input_point_value)
            for item in end_items:
                dpg.show_item(item)
        else:
            dpg.set_value(input_data, "You must enter number bigger then 1")
    except ValueError:
        dpg.set_value(input_data, "You must enter number bigger then 1")



with dpg.window(label="Tutorial", tag="Primary Window", width=970, height=475):
    # user data set when button is created
    text_count = dpg.add_text("Enter the number of points:")
    input_data = dpg.add_input_text(width=200)

    text_X = dpg.add_text(
        f"Enter the x value for point {i + 1}:",
        show=False)
    input_X = dpg.add_input_text(show=False, width=200)
    text_Y = dpg.add_text(f"Enter the y value for point {i + 1}:", show=False)
    input_Y = dpg.add_input_text(show=False, width=200)
    text_DX = dpg.add_text(
        f"Enter the dx value for {i + 1}:",
        show=False)
    input_DX = dpg.add_input_text(show=False, width=200)
    text_DDX = dpg.add_text(
        f"Enter the ddx value of {i + 1}:",
        show=False)
    input_DDX = dpg.add_input_text(show=False, width=200)

    with dpg.group(horizontal=True):
        start_button = dpg.add_button(label="Ok", callback=input_data_button, user_data="Some Data", width=96, height=50)
        restart_button = dpg.add_button(label="Restart", callback=restart_button, width=96, height=50)


    text_hint = dpg.add_text(
        f"\n The value of x for n point must be no "
        f"\n less than the value of x for n - 1 point."
        f"\n\n For one point, only one derivative can "
        f"\n be determined, i.e. either the derivative "
        f"\n of the first or second order. \n\n Enter -,"
        f"if you don`t want enter derivative "
        f"\n value",
        show=False, color=(255, 255, 0))

    end_items = [text_X, input_X, text_Y, input_Y, text_DX, input_DX, text_DDX, input_DDX, text_hint]
    start_items = [input_data, text_count]

    with dpg.plot(label="Line Series", width=600, height=400, pos=(325, 25), tag="Plot"):
        # optionally create legend
        dpg.add_plot_legend()
        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        # series belong to a y axis
        dpg.add_line_series(x_values, y_values, label="Interpolation", parent="y_axis", tag="series_tag")
        dpg.add_scatter_series(x_dots, y_dots, label="Points", parent="y_axis", tag="scatter_series")


    dpg.create_viewport(title='Hermite Interpolation', width=950, height=475)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()