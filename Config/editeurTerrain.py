import tkinter as tk
from typing import List

from Config.tile import Tile

"""
Code to create the graph configuration file with a simple GUI. Parameters you may change:
- number of columns (num_columns)
- number of rows (num_rows)
- the file name to save the file to (file_name)

When the code is run, click on the midpoints of two adjacent segments. The configuration file is update automatically.
The file can be then used in editeurConfig.py to specify other parameters.
"""

num_rows = 5
num_columns = 5
file_name = "graph_config.txt"


# Grid initialization, (x,y) is inverted compared to (num_rows, num_columns)
num_cells_x = num_columns
num_cells_y = num_rows

# Set the size of each cell in the grid
cell_size = 80
offset = cell_size

current_point = None

graph = [[Tile() for _ in range(num_cells_y)] for _ in range(num_cells_x)]

def saveToFile(graph: List[List[Tile]],file_name: str) -> None:
    """
    Save given graph in file
    :param graph: the graph (2d list of tiles)
    :param file_name: the file name (str)
    """
    with open(file_name,"w") as f:
        f.write("## DIMENSION ##\n")
        f.write(f"row:{num_cells_y} column:{num_cells_x}\n")
        f.write("## GROUND ##")
        for y in range(num_cells_y):
            f.write("\n")
            f.write(" ".join([str(graph[x][y].getIndex()) for x in range(num_cells_x)] ))

def create_circle(canvas, x: float, y: float, radius: float, color:str="red"):
    """
    Creates a circle in canvas
    :param canvas: tkinter canvas
    :param x: x position
    :param y: y position
    :param radius: radius value
    :param color: color of the circle (red by default)
    """
    x1 = x - radius
    y1 = y - radius
    x2 = x + radius
    y2 = y + radius
    canvas.create_oval(x1, y1, x2, y2, fill=color)

def define_vertical_points():
    """
    Returns the list of vertical midpoints, each point of the form ((xposg, yposg), x, y, "v") with (xposg, yposg) the
    position in the plot and (x,y) the position in terms of number of lines/columns.
    """
    l = []
    for x in range(num_cells_x):
        for y in range(num_cells_y+1):
            l.append(((offset + 0.5*cell_size + x * cell_size, offset + y * cell_size), x, y, "v"))
    return l

def define_horizontal_points():
    """
    Returns the list of vertical midpoints, each point of the form ((xposg, yposg), x, y, "v") with (xposg, yposg) the
    position in the plot and (x,y) the position in terms of number of lines/columns.
    """
    l = []
    for x in range(num_cells_x+1):
        for y in range(num_cells_y):
            l.append( ((offset + x * cell_size, offset + 0.5 * cell_size + y * cell_size), x, y, "h"))
    return l

def compute_tiles_from_point(point):
    """
    Computes the list of tiles adjacent to midpoint in input.
    :param point: a midpoint in the form  ((xposg, yposg), x, y, "v")
    :return: the list of adjacent tiles and corresponding direction of the poitn.
    """
    tiles = {}
    if point[-1] == "v":
        if point[2] < num_cells_y + 1:
            tiles[(point[1], point[2])] = "N"
        if point[2] > 0:
            tiles[(point[1], point[2] - 1)] = "S"
    else:
        if point[1] > 0:
            tiles[(point[1]-1, point[2])] = "E"
        if point[1]  < num_cells_x + 1:
            tiles[(point[1], point[2])] = "W"
    return tiles

def add_to_graph(point1, point2):
    """
    Adds/Remove the segment between point1 and point2. If both are already in the tile, removes them, if one of them
    is not in tile, adds both.
    """
    if point1 == point2:
        return

    tiles1 = compute_tiles_from_point(point1)
    tiles2 = compute_tiles_from_point(point2)

    for tile in tiles1.keys():
        if tile not in tiles2.keys():
            continue
        dir1 = tiles1[tile]
        dir2 = tiles2[tile]

        # Case where the link was already in the graph
        if graph[tile[0]][tile[1]].getValue(dir1) + graph[tile[0]][tile[1]].getValue(dir2) == 2:
            graph[tile[0]][tile[1]].setValue(dir1, 0)
            graph[tile[0]][tile[1]].setValue(dir2, 0)
        # Default case
        else:
            graph[tile[0]][tile[1]].setValue(dir1, 1)
            graph[tile[0]][tile[1]].setValue(dir2, 1)
        # Case checking if only one tile is at 1:
        if graph[tile[0]][tile[1]].getValue("N") + graph[tile[0]][tile[1]].getValue("W") + graph[tile[0]][tile[1]].getValue("S") + graph[tile[0]][tile[1]].getValue("E") == 1:
            graph[tile[0]][tile[1]].setValue("N", 0)
            graph[tile[0]][tile[1]].setValue("E", 0)
            graph[tile[0]][tile[1]].setValue("W", 0)
            graph[tile[0]][tile[1]].setValue("S", 0)

def handle_click(event):
    global current_point
    # Get the coordinates of the clicked cell
    x = event.x // cell_size
    y = event.y // cell_size
    closest_point = None
    for point in horizontal_points + vertical_points:
        if closest_point is None:
            closest_point = point
            continue
        (x1, y1) = point[0]
        (x1b, y1b) = closest_point[0]
        (x2, y2) = (event.x, event.y)
        if ((x1 - x2) ** 2 + (y1 - y2) ** 2) < ((x1b - x2) ** 2 + (y1b - y2) ** 2):
            closest_point = point

    # Update the state of the clicked cell
    # Redraw the grid
    if current_point is None:
        current_point = closest_point
    else:
        add_to_graph(current_point, closest_point)
        current_point = None
    draw_grid()

def draw_grid():
    # Clear the canvas
    canvas.delete("all")

    # Draw the grid lines
    for i in range(num_cells_x + 1):
        x = i * cell_size + offset
        canvas.create_line(x, offset, x, canvas_height - offset, fill="gray")
    for i in range(num_cells_y + 1):
        y = i * cell_size + offset
        canvas.create_line(offset, y, canvas_width - offset, y, fill="gray")

    # Draw the cells
    for y in range(num_cells_y):
        for x in range(num_cells_x):
            cell_color = "white"
            canvas.create_rectangle(
                x * cell_size + offset, y * cell_size + offset,
                (x + 1) * cell_size + offset, (y + 1) * cell_size + offset,
                fill=cell_color, outline="gray"
            )
    if current_point is not None:

        create_circle(canvas, current_point[0][0], current_point[0][1],cell_size / 10)
    directions = ["E","W","N","S"]
    offset_dict = {
        "E": (0.5 * cell_size, 0),
        "W": (-0.5 * cell_size, 0),
        "N": (0,-0.5 * cell_size),
        "S": (0, 0.5 * cell_size)
    }
    for x in range(num_cells_x):
        for y in range(num_cells_y):
            for i1 in range(len(directions)):
                dir1 = directions[i1]
                if graph[x][y].getValue(dir1) == 0:
                    continue
                for i2 in range(i1+1, len(directions)):
                    dir2 = directions[i2]
                    if graph[x][y].getValue(dir2) == 0:
                        continue
                    pos_center = ((x + 0.5) * cell_size, (y + 0.5) * cell_size)
                    if (dir1 in ["N","S"] and dir2 in ["N","S"]) or (dir1 in ["W","E"] and dir2 in ["W","E"]):
                        canvas.create_line(pos_center[0] + offset_dict[dir1][0] + offset, pos_center[1] + offset_dict[dir1][1] + offset,
                                   pos_center[0] + offset_dict[dir2][0] + offset, pos_center[1] + offset_dict[dir2][1] + offset, fill="black", width=5)
                    else:
                        if dir1 + dir2 in ["WS","SW"]:
                            start = 0
                            extent = 90
                        elif dir1 + dir2 in ["WN","NW"]:
                            start = -90
                            extent = 90
                        elif dir1 + dir2 in ["ES","SE"]:
                            start = 90
                            extent = 90
                        elif dir1 + dir2 in ["EN","NE"]:
                            start = 180
                            extent = 90
                        canvas.create_arc(pos_center[0] + 2*offset_dict[dir1][0] + offset, pos_center[1] + 2*offset_dict[dir1][1] + offset,
                                   pos_center[0] + 2*offset_dict[dir2][0] + offset, pos_center[1] + 2*offset_dict[dir2][1] + offset, start=start, extent=extent, style=tk.ARC, width=5)
    saveToFile(graph, file_name)

horizontal_points = define_horizontal_points()
vertical_points = define_vertical_points()

# Initialize the GUI
root = tk.Tk()
root.title("Editeur de terrain")


# Calculate the size of the canvas based on the number of cells and cell size
canvas_width = num_cells_x * cell_size + 2 * offset
canvas_height = num_cells_y * cell_size + 2 * offset

# Create a canvas to draw the grid
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Bind the click event to the canvas
canvas.bind("<Button-1>", handle_click)

# Draw the initial grid
draw_grid()

# Start the GUI event loop
root.mainloop()
