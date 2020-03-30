import tkinter as tk


class Maze():
    def __init__(self):
        self.walls = {}


class MazeGUI():
    def __init__(self, parent):
        self.parent = parent

        self.walls = Maze().walls
        self.lines = []

        self.line_color = self.rgb_to_hex(255, 255, 255)
        self.wall_color = self.rgb_to_hex(100, 0, 0)
        self.bg_color = self.rgb_to_hex(0, 0, 0)

        self.menubar = tk.Menu(parent)

        self.grid_menu = tk.Menu(self.menubar, tearoff=0)
        self.grid_menu.add_command(label='Cell Size')
        self.grid_menu.add_command(label='Grid Size')
        self.grid_menu.add_command(label='Window Size')
        self.menubar.add_cascade(label='Grid', menu=self.grid_menu)

        self.color_menu = tk.Menu(self.menubar, tearoff=0)
        self.color_menu.add_command(label='Grid Color')
        self.color_menu.add_command(label='Wall Color')
        self.color_menu.add_command(label='Background Color')
        self.menubar.add_cascade(label='Colors', menu=self.color_menu)

        self.menubar.add_command(label='Exit', command=parent.quit)

        self.canvas = tk.Canvas(parent, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.setup(parent)

        for event in ['<Button 1>', '<B1-Motion>', '<Button 3>', '<B3-Motion>']:
            self.canvas.bind(event, self.mouse_event)

        parent.config(menu=self.menubar)

    def setup(self, parent):
        self.number_of_squares = 19
        self.window_size = 1000

        self.grid_size = self.window_size // self.number_of_squares
        window_size = self.grid_size * self.number_of_squares

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        self.window_pos_x = (screen_width - self.window_size) // 2
        self.window_pos_y = (screen_height - self.window_size) // 2

        window_geometry = f'{self.window_size}x{self.window_size}+{self.window_pos_x}+{self.window_pos_y}'

        parent.geometry(window_geometry)

        for i in range(0, window_size, self.grid_size):
            self.lines.append(self.canvas.create_line(
                i, 0, i, window_size, fill=self.line_color))
            self.lines.append(self.canvas.create_line(
                0, i, window_size, i, fill=self.line_color))

    def rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def mouse_event(self, event):
        start_x = event.x // self.grid_size * self.grid_size
        start_y = event.y // self.grid_size * self.grid_size

        coords = start_x, start_y, start_x + self.grid_size, start_y + self.grid_size

        if (event.num == 1 or 'Button1' in str(event)) and coords not in self.walls.keys():
            self.walls[coords] = self.canvas.create_rectangle(
                coords, fill=self.wall_color)

        elif (event.num == 3 or 'Button3' in str(event)) and coords in self.walls.keys():
            self.canvas.delete(self.walls.pop(coords))


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Python Mazes')
    root.resizable(False, False)
    MazeGUI(root)
    root.mainloop()
