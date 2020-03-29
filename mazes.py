import tkinter as tk

def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


def create_grid(event=None):
    for i in range(0, window_size, grid_size):
        lines.append(canvas.create_line(i, 0, i, window_size, fill=line_color))
        lines.append(canvas.create_line(0, i, window_size, i, fill=line_color))


def mouse_event(event):
    start_x = event.x // grid_size * grid_size
    start_y = event.y // grid_size * grid_size

    start_coords = start_x, start_y
    end_coords = start_x + grid_size, start_y + grid_size

    if event.num == 1 or 'Button1' in str(event):
        if start_coords not in walls.keys():
            wall_shape = canvas.create_rectangle(
                start_coords, end_coords, fill=wall_color)
            walls[start_coords] = wall_shape

    if event.num == 3 or 'Button3' in str(event):
        if start_coords in walls.keys():
            canvas.delete(walls.pop(start_coords))


walls = {}
lines = []

line_color = rgb_to_hex(255, 255, 255)
wall_color = rgb_to_hex(100, 0, 0)
bg_color = rgb_to_hex(0, 0, 0)

number_of_squares = 19
window_size = 1000

grid_size = window_size // number_of_squares
window_size = grid_size * number_of_squares

root = tk.Tk()
root.title('Python Mazes')
root.resizable(False, False)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_pos_x = (screen_width - window_size) // 2
window_pos_y = (screen_height - window_size) // 2

window_geometry = f'{window_size}x{window_size}+{window_pos_x}+{window_pos_y}'

root.geometry(window_geometry)

menubar = tk.Menu(root)

grid_menu = tk.Menu(menubar, tearoff=0)
grid_menu.add_command(label='Cell Size')
grid_menu.add_command(label='Grid Size')
grid_menu.add_command(label='Window Size')
menubar.add_cascade(label='Grid', menu=grid_menu)


color_menu = tk.Menu(menubar, tearoff=0)
color_menu.add_command(label='Grid Color')
color_menu.add_command(label='Wall Color')
color_menu.add_command(label='Background Color')
menubar.add_cascade(label='Colors', menu=color_menu)


menubar.add_command(label='Exit', command=root.quit)

canvas = tk.Canvas(root, bg=bg_color)
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind('<Configure>', create_grid)

for event in ['<Button 1>', '<B1-Motion>', '<Button 3>', '<B3-Motion>']:
    canvas.bind(event, mouse_event)

root.config(menu=menubar)
root.mainloop()
