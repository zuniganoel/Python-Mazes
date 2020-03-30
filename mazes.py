import tkinter as tk


class Maze():
    def __init__(self):
        self.walls = {}


class MazeGUI():
    def __init__(self, parent):
        self.parent = parent

        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()


        self.Maze = Maze()
        self.lines = []

        self.line_color = self.rgb_to_hex(255, 255, 255)
        self.wall_color = self.rgb_to_hex(100, 0, 0)
        self.bg_color = self.rgb_to_hex(0, 0, 0)


        self.gui_setup()
        self.size_setup()
        self.bind_events()

    def size_setup(self, grid_size = 25, cell_size = None):
        self.grid_size = grid_size
        self.cell_size = int(self.screen_height // self.grid_size // 1.2)

        if cell_size != None and cell_size != self.cell_size and cell_size * grid_size < self.screen_height:
            self.cell_size = cell_size

        self.window_size = self.cell_size * self.grid_size

        window_pos_x = (self.screen_width - self.window_size) // 2
        window_pos_y = (self.screen_height - self.window_size) // 2
        window_geometry = f'{self.window_size}x{self.window_size}+{window_pos_x}+{window_pos_y}'

        self.parent.geometry(window_geometry)

        self.draw_grid()

    def gui_setup(self):
        self.canvas = tk.Canvas(self.parent, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.menubar = tk.Menu(self.parent)
        self.menubar.add_command(label='Grid', command=self.grid_popup)
        self.menubar.add_command(label='Colors', command=self.colors_popup)
        self.menubar.add_command(label='Exit', command=self.parent.quit)

        self.parent.config(menu=self.menubar)

    def draw_grid(self):
        for item in self.lines:
            self.canvas.delete(item)
        del self.lines[:]

        for key in self.Maze.walls.keys():
            self.canvas.delete(self.Maze.walls[key])
        self.Maze.walls.clear()

        for i in range(0, self.window_size, self.cell_size):
            self.lines.append(self.canvas.create_line(
                i, 0, i, self.window_size, fill=self.line_color))
            self.lines.append(self.canvas.create_line(
                0, i, self.window_size, i, fill=self.line_color))

    def bind_events(self):
        for event in ['<Button 1>', '<B1-Motion>', '<Button 3>', '<B3-Motion>']:
            self.canvas.bind(event, self.mouse_event)
    
    def close(self, event):
        if str(event.widget) == '.!toplevel':
            event.widget.destroy()

    def grid_popup(self):
        win = tk.Toplevel(class_='grid')
        win.iconbitmap(default='icons/blank.ico')
        win.title('Edit Grid')
        win.resizable(False, False)
        win.focus()
        win.bind('<FocusOut>', self.close)
        window_size_x = 300
        window_size_y = 150

        window_pos_x = (self.screen_width - window_size_x) // 2
        window_pos_y = (self.screen_height - window_size_y) // 2

        window_geometry = f'{window_size_x}x{window_size_y}+{window_pos_x}+{window_pos_y}'
        win.geometry(window_geometry)

        tk.Label(win, text=" Grid Size").grid(row=0,column=0)
        grid_size_input_var = tk.IntVar()
        grid_size_input_var.set(self.grid_size)
        grid_size_input = tk.Entry(win, justify='right', width=10, textvariable=grid_size_input_var)
        grid_size_input.grid(row=0,column=1)

        tk.Label(win, text=" Cell Size").grid(row=1,column=0)
        cell_size_input_var = tk.IntVar()
        cell_size_input_var.set(self.cell_size)
        cell_size_input = tk.Entry(win, justify='right', width=10, textvariable=cell_size_input_var)
        cell_size_input.grid(row=1,column=1)

        args = (win, grid_size_input_var, cell_size_input_var)

        save_button = tk.Button(win, text="Save", command=lambda: self.save_settings(args)).grid(row=2, column=0)
        cancel_button = tk.Button(win, text="Cancel", command=win.destroy).grid(row=2, column=1)

 

    def colors_popup(self):
        win = tk.Toplevel()
        win.iconbitmap(default='icons/blank.ico')
        win.title('Window Colors')
        win.resizable(False, False)

        window_size_x = 500
        window_size_y = 200

        window_pos_x = (self.screen_width - window_size_x) // 2
        window_pos_y = (self.screen_height - window_size_y) // 2

        window_geometry = f'{window_size_x}x{window_size_y}+{window_pos_x}+{window_pos_y}'
        win.geometry(window_geometry)

        tk.Label(win, text="  Grid Color", anchor='w', width=16).grid(row=0,column=0)
        tk.Label(win, text="  Wall Color", anchor='w', width=16).grid(row=1,column=0)
        tk.Label(win, text="  Background Color", anchor='w', width=16).grid(row=2,column=0)

        tk.Entry(win).grid(row=0,column=1)
        tk.Entry(win).grid(row=1,column=1)
        tk.Entry(win).grid(row=2,column=1)

        save_button = tk.Button(win, text="Save", command=self.save_settings).grid(row=3, column=0)
        cancel_button = tk.Button(win, text="Cancel", command=win.destroy).grid(row=3, column=1)
        win.focus()
        win.bind('<FocusOut>', self.close)

    def save_settings(self, args):
        if args[0].title() == 'Edit Grid':
            self.size_setup(args[1].get(), args[2].get())
        args[0].destroy()


    def rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def mouse_event(self, event):
        start_x = event.x // self.cell_size * self.cell_size
        start_y = event.y // self.cell_size * self.cell_size

        coords = start_x, start_y, start_x + self.cell_size, start_y + self.cell_size

        if (event.num == 1 or 'Button1' in str(event)) and coords not in self.Maze.walls.keys():
            self.Maze.walls[coords] = self.canvas.create_rectangle(
                coords, fill=self.wall_color)

        elif (event.num == 3 or 'Button3' in str(event)) and coords in self.Maze.walls.keys():
            self.canvas.delete(self.Maze.walls.pop(coords))


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(default='icons/blank.ico')
    root.title('Python Mazes')
    root.resizable(False, False)
    MazeGUI(root)
    root.mainloop()
