import tkinter as tk
from tkinter import ttk


class Maze():
    def __init__(self):
        self.walls = {}
        self.start = None
        self.end = None

    def generate(self):
        print('Generating random maze')

    def solve(self, algorithm):
        print(f'Solving through {algorithm}')

class RGBSlider():
    def __init__(self, parent, label, current_color):
        self.parent = parent
        self.frame = tk.Frame(self.parent, highlightbackground="black", highlightthickness=2)
        self.frame.pack(fill=tk.BOTH)
        self.current_color = current_color

        color_rgb = self.hex_to_rgb(current_color)
        tk.Label(self.frame, text=label).grid(row=1,column=0)

        r = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(('r', r.get())))
        r.grid(row=0, column=1)
        r.set(color_rgb[0])

        g = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(('g', g.get())))
        g.grid(row=1, column=1)
        g.set(color_rgb[1])

        b = tk.Scale(self.frame, from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(('b', b.get())))
        b.grid(row=2, column=1)
        b.set(color_rgb[2])


    def get_color(self):
        return self.current_color


    def update_color(self, args):
        current_rgb = self.hex_to_rgb(self.current_color)
        new_color = self.current_color
        if '_r' in args[0]:
            new_color = self.rgb_to_hex(args[1], current_rgb[1], current_rgb[2])
        if '_g' in args[0]:
            new_color = self.rgb_to_hex(current_rgb[0], args[1], current_rgb[2])
        if '_b' in args[0]:
            new_color = self.rgb_to_hex(current_rgb[0], current_rgb[1], args[1])

        self.current_color = new_color

    def rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def hex_to_rgb(self, value):
        print(value)
        value = value.lstrip('#')
        length = len(value)
        return tuple(int(value[i:i+length//3], 16) for i in range(0, length, length//3))

class MazeGUI():
    def __init__(self, parent):
        self.parent = parent

        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()

        self.Maze = Maze()
        self.mode = 'walls'
        self.grid = []

        self.grid_color = self.rgb_to_hex(255, 255, 0)
        self.cell_color = self.rgb_to_hex(100, 0, 0)
        self.bg_color = self.rgb_to_hex(0, 0, 0)
        self.start_color = self.rgb_to_hex(0, 255, 0)
        self.end_color = self.rgb_to_hex(255, 0, 0)

        self.gui_setup(self.parent)
        self.size_setup()
        self.bind_events()

    def move_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def zoom(self, event):
        if event.delta > 0:
            self.canvas.scale('all', self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 1.1, 1.1)
        elif event.delta < 0:
            self.canvas.scale('all', event.x, event.y, 0.9, 0.9)
        self.canvas.scan_dragto(event.x, event.y, gain=1)
    

    def reset_zoom(self):
        self.canvas.scan_dragto(0, 0, gain=1)
        self.canvas.scale('all', 0, 0, 1, 1)


    def gui_setup(self, parent):
        self.canvas = tk.Canvas(parent, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.menubar = tk.Menu(parent)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Save', command=None)
        self.file_menu.add_command(label='Open', command=None)
        self.file_menu.add_command(label='Exit', command=parent.quit)

        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu)

        self.grid_menu = tk.Menu(self.edit_menu, tearoff=0)
        self.edit_menu.add_cascade(label='Grid', menu=self.grid_menu)
        self.grid_menu.add_command(label='Change Size', command=self.grid_popup)
        self.grid_menu.add_command(label='Restore Default', command=None)
        self.grid_menu.add_command(label='Toggle Visibility', command=self.toggle_grid)

        self.color_menu = tk.Menu(self.edit_menu, tearoff=0)
        self.edit_menu.add_cascade(label='Colors', menu=self.color_menu)
        self.color_menu.add_command(label='Customize', command=self.colors_popup)
        self.color_menu.add_command(label='Restore Default', command=None)
        self.edit_menu.add_command(label='Reset Zoom', command=self.reset_zoom)

        self.draw_menu = tk.Menu(self.edit_menu, tearoff=0)
        self.menubar.add_cascade(label='Draw', menu=self.draw_menu)
        self.draw_menu.add_command(label='Walls', command=lambda: self.switch_mode('walls'))
        self.draw_menu.add_command(label='Start Point', command=lambda: self.switch_mode('start'))
        self.draw_menu.add_command(label='End Point', command=lambda: self.switch_mode('end'))

        self.maze_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Maze', menu=self.maze_menu)
        self.maze_menu.add_command(label='Generate', command=self.Maze.generate)

        self.solve_menu = tk.Menu(self.maze_menu, tearoff=0)
        self.maze_menu.add_cascade(label='Solve', menu=self.solve_menu)
        self.solve_menu.add_command(label='A*', command=lambda: self.Maze.solve('a*'))

        parent.config(menu=self.menubar)


    def switch_mode(self, mode):
        self.mode = mode


    def size_setup(self, grid_size = 25, cell_size = None):
        self.grid_size = grid_size
        self.cell_size = int(self.screen_height // self.grid_size // 1.3)

        if cell_size != None and cell_size != self.cell_size and cell_size * grid_size < self.screen_height:
            self.cell_size = cell_size

        self.window_size = self.cell_size * self.grid_size

        window_pos_x = (self.screen_width - self.window_size) // 2
        window_pos_y = (self.screen_height - self.window_size) // 2
        geometry = f'{self.window_size}x{self.window_size}+{window_pos_x}+{window_pos_y}'

        self.parent.geometry(geometry)
        self.clear_walls()
        self.clear_grid()
        self.draw_grid()


    def clear_walls(self):
        for key in self.Maze.walls.keys():
            self.canvas.delete(self.Maze.walls[key])
        self.Maze.walls.clear()


    def draw_grid(self):
        for i in range(0, self.window_size + self.cell_size, self.cell_size):
            line_x = self.canvas.create_line(0, i, self.window_size, i, fill=self.grid_color)
            line_y = self.canvas.create_line(i, 0, i, self.window_size, fill=self.grid_color)

            self.grid.append(line_x)
            self.grid.append(line_y)


    def clear_grid(self):
        for item in self.grid:
            self.canvas.delete(item)
        del self.grid[:]


    def toggle_grid(self):
        if len(self.grid) > 0:
            self.clear_grid()
        else:
            self.draw_grid()


    def bind_events(self):
        for event in ['<Button 1>', '<B1-Motion>', '<Button 3>', '<B3-Motion>']:
            self.canvas.bind(event, self.mouse_event)
        self.canvas.bind('<MouseWheel>', self.zoom)
        self.canvas.bind('<Button 2>', self.move_start)
        self.canvas.bind('<B2-Motion>', self.move_move)


    def close(self, event):
        if str(event.widget) == '.!toplevel':
            event.widget.destroy()


    def grid_popup(self):
        win = tk.Toplevel()
        win.iconbitmap(default='icons/blank.ico')
        win.title('Edit Grid')
        win.resizable(False, False)
        win.focus()
        win.bind('<FocusOut>', self.close)

        window_size_x = 300
        window_size_y = 150

        window_pos_x = (self.screen_width - window_size_x) // 2
        window_pos_y = (self.screen_height - window_size_y) // 2

        geometry = f'{window_size_x}x{window_size_y}+{window_pos_x}+{window_pos_y}'
        win.geometry(geometry)

        tk.Label(win, text=" Grid Size ").grid(row=0,column=0)
        grid_size_input = tk.IntVar()
        grid_size_input.set(self.grid_size)
        tk.Entry(win, width=10, textvariable=grid_size_input).grid(row=0,column=1)

        tk.Label(win, text=" Cell Size ").grid(row=1,column=0)
        cell_size_input = tk.IntVar()
        cell_size_input.set(self.cell_size)
        tk.Entry(win, width=10, textvariable=cell_size_input).grid(row=1,column=1)

        args = (win, grid_size_input, cell_size_input)

        save_button = tk.Button(win, text="Save", command=
            lambda: self.save_settings(args)).grid(row=2, column=0)
        cancel_button = tk.Button(win, text="Cancel", command=win.destroy).grid(row=2, column=1)

 
    def colors_popup(self):
        win = tk.Toplevel()
        win.iconbitmap(default='icons/blank.ico')
        win.title('Edit Colors')
        win.resizable(False, False)
        win.focus()
        win.bind('<FocusOut>', self.close)

        grid = RGBSlider(win, 'Grid Color', self.grid_color)
        cell = RGBSlider(win, 'Cell Color', self.cell_color)
        bg = RGBSlider(win, 'BG Color', self.bg_color)
        start = RGBSlider(win, 'Start Color', self.start_color)
        end = RGBSlider(win, 'End Color', self.end_color)       

        button_frame = tk.Frame(win)
        button_frame.pack(fill=tk.BOTH)

        save_button = tk.Button(button_frame, text="Save", command=win.destroy)
        save_button.pack()
        close_button = tk.Button(button_frame, text="Close", command=win.destroy)
        close_button.pack()

        grid.frame.update()
        cell.frame.update()
        bg.frame.update()
        button_frame.update()
        start.frame.update()
        end.frame.update()

        window_size_x = int(grid.frame.winfo_width() * 1.25)
        window_size_y = (grid.frame.winfo_height() + 
                        cell.frame.winfo_height() + 
                        bg.frame.winfo_height() + 
                        button_frame.winfo_height() + 
                        start.frame.winfo_height() +
                        end.frame.winfo_height())

        window_pos_x = (self.screen_width - window_size_x) // 2
        window_pos_y = (self.screen_height - window_size_y) // 2

        geometry = f'{window_size_x}x{window_size_y}+{window_pos_x}+{window_pos_y}'
        win.geometry(geometry)


    def update_colors(self, args):
        if 'grid' in args[0]:
            new_color = self.grid_color
            grid_color_rgb = self.hex_to_rgb(self.grid_color)
            if '_r' in args[0]:
                new_color = self.rgb_to_hex(args[1], grid_color_rgb[1], grid_color_rgb[2])
            if '_g' in args[0]:
                new_color = self.rgb_to_hex(grid_color_rgb[0], args[1], grid_color_rgb[2])
            if '_b' in args[0]:
                new_color = self.rgb_to_hex(grid_color_rgb[0], grid_color_rgb[1], args[1])
            self.grid_color = new_color
            self.clear_grid()
            self.draw_grid()
        if 'cell' in args[0]:
            new_color = self.cell_color
            cell_color_rgb = self.hex_to_rgb(self.cell_color)
            if '_r' in args[0]:
                new_color = self.rgb_to_hex(args[1], cell_color_rgb[1], cell_color_rgb[2])
            if '_g' in args[0]:
                new_color = self.rgb_to_hex(cell_color_rgb[0], args[1], cell_color_rgb[2])
            if '_b' in args[0]:
                new_color = self.rgb_to_hex(cell_color_rgb[0], cell_color_rgb[1], args[1])
            self.cell_color = new_color
            for key in self.Maze.walls.keys():
                self.canvas.itemconfig(self.Maze.walls[key], fill=self.cell_color)
        if 'bg' in args[0]:
            new_color = self.bg_color
            bg_color_rgb = self.hex_to_rgb(self.bg_color)
            if '_r' in args[0]:
                new_color = self.rgb_to_hex(args[1], bg_color_rgb[1], bg_color_rgb[2])
            if '_g' in args[0]:
                new_color = self.rgb_to_hex(bg_color_rgb[0], args[1], bg_color_rgb[2])
            if '_b' in args[0]:
                new_color = self.rgb_to_hex(bg_color_rgb[0], bg_color_rgb[1], args[1])
            self.bg_color = new_color
            self.canvas.config(bg=self.bg_color)
        if 'start' in args[0]:
            new_color = self.start_color
            start_color_rgb = self.hex_to_rgb(self.start_color)
            if '_r' in args[0]:
                new_color = self.rgb_to_hex(args[1], start_color_rgb[1], start_color_rgb[2])
            if '_g' in args[0]:
                new_color = self.rgb_to_hex(start_color_rgb[0], args[1], start_color_rgb[2])
            if '_b' in args[0]:
                new_color = self.rgb_to_hex(start_color_rgb[0], start_color_rgb[1], args[1])
            self.start_color = new_color
            self.canvas.itemconfig(self.Maze.start, fill=self.start_color)
        if 'end' in args[0]:
            new_color = self.end_color
            end_color_rgb = self.hex_to_rgb(self.end_color)
            if '_r' in args[0]:
                new_color = self.rgb_to_hex(args[1], end_color_rgb[1], end_color_rgb[2])
            if '_g' in args[0]:
                new_color = self.rgb_to_hex(end_color_rgb[0], args[1], end_color_rgb[2])
            if '_b' in args[0]:
                new_color = self.rgb_to_hex(end_color_rgb[0], end_color_rgb[1], args[1])
            self.end_color = new_color
            self.canvas.itemconfig(self.Maze.end, fill=self.end_color)

    def save_settings(self, args):
        if args[0].title() == 'Edit Grid':
            self.size_setup(args[1].get(), args[2].get())
        elif args[0].title() == 'Edit Colors':
            pass
        args[0].destroy()


    def rgb_to_hex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)

    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        length = len(value)
        return tuple(int(value[i:i+length//3], 16) for i in range(0, length, length//3))


    def mouse_event(self, event):
        start_x = event.x // self.cell_size * self.cell_size
        start_y = event.y // self.cell_size * self.cell_size

        mid_point = start_x + self.cell_size // 2, start_y + self.cell_size // 2
        radius = self.cell_size // 4

        if self.mode == 'walls':
            coords = start_x, start_y, start_x + self.cell_size, start_y + self.cell_size
            if (event.num == 1 or 'Button1' in str(event)) and coords not in self.Maze.walls.keys():
                if coords[0] >= 0 and coords[1] >= 0 and coords[2] <= self.window_size and coords[3] <= self.window_size: 
                    wall = self.canvas.create_rectangle(coords, fill=self.cell_color)
                    self.canvas.tag_lower(wall)    
                    self.Maze.walls[coords] = wall

            elif (event.num == 3 or 'Button3' in str(event)) and coords in self.Maze.walls.keys():
                self.canvas.delete(self.Maze.walls.pop(coords))
        elif self.mode == 'start':
            coords = (mid_point[0] - radius, 
                    mid_point[1] - radius, 
                    mid_point[0] + radius, 
                    mid_point[1] + radius)

            if not self.Maze.start == None:
                self.canvas.delete(self.Maze.start)
            start = self.canvas.create_oval(coords, fill=self.start_color)
            self.Maze.start = start

        elif self.mode == 'end':
            coords = (mid_point[0] - radius, 
                    mid_point[1] - radius, 
                    mid_point[0] + radius, 
                    mid_point[1] + radius)

            if not self.Maze.end == None:
                self.canvas.delete(self.Maze.end)
            end = self.canvas.create_oval(coords, fill=self.end_color)
            self.Maze.end = end



if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(default='icons/blank.ico')
    root.title('Python Mazes')
    root.resizable(False, False)
    MazeGUI(root)
    root.mainloop()