import tkinter as tk
import tkinter.filedialog
import gzip

import ExtraUtils
import ExtraUI
import Maze

class FileManager():
    def __init__(self):
        self.file = None
        self.grid_data_compressed = None
        self.maze_data_compressed = None
        self.grid_data = None
        self.maze_data = None

    def Save(self, grid_data, maze_data):
        self.grid_data = grid_data
        self.maze_data = maze_data

        self.compress_grid_data()
        self.compress_wall_data()

        self.file.write(self.grid_data_compressed)
        self.file.write(self.wall_data_compressed)

    def Open(self):

        return []

    def Close(self):
        if self.file != None:
            self.file.close()

    def getFile(self):
        return self.file

    def setFile(self, path):
        self.file = open(path, "wb+")

    def compress_grid_data(self):
        byte_array = []
        for index, item in enumerate(self.grid_data):
            if index < 2:
                byte_array.append(item)
            else:
                byte_array.extend(
                    [int_val for int_val in ExtraUtils.hex_to_rgb(item)])

        self.grid_data_compressed = gzip.compress(bytearray(byte_array))

    def compress_wall_data(self):
        byte_array = []
        for item in list(self.maze_data[0].keys()):
            byte_array.extend([coord // self.grid_data[0]
                               for coord in item[:2]])

        self.wall_data_compressed = gzip.compress(bytearray(byte_array))


class MazeGUI():
    def __init__(self, parent):
        self.file_manager = FileManager()
        self.parent = parent

        self.screen_width = self.parent.winfo_screenwidth()
        self.screen_height = self.parent.winfo_screenheight()

        self.maze = Maze.Maze()
        self.mode = 'walls'
        self.grid = []

        self.grid_color = ExtraUtils.rgb_to_hex(255, 255, 0)
        self.cell_color = ExtraUtils.rgb_to_hex(100, 0, 0)
        self.bg_color = ExtraUtils.rgb_to_hex(0, 0, 0)
        self.start_color = ExtraUtils.rgb_to_hex(0, 255, 0)
        self.end_color = ExtraUtils.rgb_to_hex(255, 0, 0)

        self.gui_setup(self.parent)
        self.size_setup()
        self.bind_events()

    def gui_setup(self, parent):
        self.canvas = tk.Canvas(parent, bg=self.bg_color)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        menu_controller = ExtraUI.MenuBar(parent)

        menu_controller.addNewCascade(
            {menu_controller.root(): ['File', 'Edit', 'Draw', 'Maze', 'About'],
            'Edit': ['Grid', 'Color'], 'Maze': ['Generate', 'Solve']})

        menu_controller.addNewCommands('File', {'Save': self.save_data,
            'Open': self.open_data, 'Exit': self.clean_close})

        menu_controller.addNewCommands('Grid', {'Change Size': self.grid_popup,
            'Defaults': None, 'Toggle': self.toggle_grid})

        menu_controller.addNewCommands('Color', {'Customize': self.colors_popup,
            'Defaults': None})

        menu_controller.addNewCommands('Draw', 
            {'Walls': lambda: self.switch_mode('walls'),
            'Start Pos': lambda: self.switch_mode('start'),
            'End Pos': lambda: self.switch_mode('end')})

        parent.config(menu=menu_controller.root())

    def switch_mode(self, mode):
        self.mode = mode

    def clean_close(self):
        self.file_manager.Close()
        self.parent.quit()

    def size_setup(self, grid_size=25, cell_size=None):
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
        for key in self.maze.walls.keys():
            self.canvas.delete(self.maze.walls[key])
        self.maze.walls.clear()

    def draw_grid(self):
        for i in range(0, self.window_size + self.cell_size, self.cell_size):
            line_x = self.canvas.create_line(
                0, i, self.window_size, i, fill=self.grid_color)
            line_y = self.canvas.create_line(
                i, 0, i, self.window_size, fill=self.grid_color)

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

        tk.Label(win, text=" Grid Size ").grid(row=0, column=0)
        grid_size_input = tk.IntVar()
        grid_size_input.set(self.grid_size)
        tk.Entry(win, width=10, textvariable=grid_size_input).grid(
            row=0, column=1)

        tk.Label(win, text=" Cell Size ").grid(row=1, column=0)
        cell_size_input = tk.IntVar()
        cell_size_input.set(self.cell_size)
        tk.Entry(win, width=10, textvariable=cell_size_input).grid(
            row=1, column=1)

        args = (win, grid_size_input, cell_size_input)

        save_button = tk.Button(win, text="Save", command=lambda: self.save_settings(
            args)).grid(row=2, column=0)
        cancel_button = tk.Button(
            win, text="Cancel", command=win.destroy).grid(row=2, column=1)

    def colors_popup(self):
        win = tk.Toplevel()
        win.iconbitmap(default='icons/blank.ico')
        win.title('Edit Colors')
        win.resizable(False, False)
        win.focus()
        win.bind('<FocusOut>', self.close)

        grid = ExtraUI.RGBSlider(win, 'Grid Color', self.grid_color)
        cell = ExtraUI.RGBSlider(win, 'Cell Color', self.cell_color)
        bg = ExtraUI.RGBSlider(win, 'BG Color', self.bg_color)
        start = ExtraUI.RGBSlider(win, 'Start Color', self.start_color)
        end = ExtraUI.RGBSlider(win, 'End Color', self.end_color)

        button_frame = tk.Frame(win)
        button_frame.pack(fill=tk.BOTH)

        args = (win, grid, cell, bg, start, end)

        save_button = tk.Button(button_frame, text="Save",
                                command=lambda: self.save_settings(args))
        save_button.pack()
        close_button = tk.Button(
            button_frame, text="Close", command=win.destroy)
        close_button.pack()

        win.update()

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

    def save_data(self):
        if self.file_manager.getFile() == None:
            path = tk.filedialog.asksaveasfilename(filetypes=(
                ("Maze files", "*.mazbin"), ("all files", "*.*")))

            if path != '':
                path += '.mazbin'
                self.file_manager.setFile(path)

        grid_data = (self.cell_size, self.grid_size, self.cell_color,
                     self.grid_color, self.bg_color, self.start_color, self.end_color)
        maze_data = (self.maze.walls, self.maze.start, self.maze.end)
        if self.file_manager.getFile() != None:
            print('here')
            self.file_manager.Save(grid_data, maze_data)

    def open_data(self):
        pass

    def save_settings(self, args):
        if args[0].title() == 'Edit Grid':
            self.size_setup(args[1].get(), args[2].get())
        elif args[0].title() == 'Edit Colors':
            for item in args[1:]:
                if item.get_label() == 'Grid Color':
                    self.grid_color = item.get_color()
                if item.get_label() == 'Cell Color':
                    self.cell_color = item.get_color()
                if item.get_label() == 'BG Color':
                    self.bg_color = item.get_color()
                if item.get_label() == 'Start Color':
                    self.start_color = item.get_color()
                if item.get_label() == 'End Color':
                    self.end_color = item.get_color()
                self.clear_grid()
                self.draw_grid()
                for wall in self.maze.walls:
                    self.canvas.itemconfig(
                        self.maze.walls[wall], fill=self.cell_color)
                self.canvas.itemconfig(self.maze.start, fill=self.start_color)
                self.canvas.itemconfig(self.maze.end, fill=self.end_color)
                self.canvas.config(bg=self.bg_color)
            self.parent.update()

        args[0].destroy()

    def mouse_event(self, event):
        start_x = event.x // self.cell_size * self.cell_size
        start_y = event.y // self.cell_size * self.cell_size
        end_x = start_x + self.cell_size
        end_y = start_y + self.cell_size

        mid_point = start_x + self.cell_size // 2, start_y + self.cell_size // 2
        radius = self.cell_size // 4

        coords = start_x, start_y, end_x, end_y
        if start_x > -1 and start_y > -1:
            if self.mode == 'walls':
                if (event.num == 1 or 'Button1' in str(event)) and coords not in self.maze.walls.keys():
                    if len(self.canvas.find_enclosed(*coords)) == 0:
                        wall = self.canvas.create_rectangle(
                            coords, fill=self.cell_color)
                        self.canvas.tag_lower(wall)
                        self.maze.walls[coords] = wall

                elif (event.num == 3 or 'Button3' in str(event)) and coords in self.maze.walls.keys():
                    self.canvas.delete(self.maze.walls.pop(coords))
            elif self.mode == 'start':
                if not False in [self.canvas.type(item) == 'line' for item in self.canvas.find_overlapping(*coords)]:
                    coords = (mid_point[0] - radius,
                              mid_point[1] - radius,
                              mid_point[0] + radius,
                              mid_point[1] + radius)

                    if not self.maze.start == None:
                        self.canvas.delete(self.maze.start)
                    start = self.canvas.create_oval(
                        coords, fill=self.start_color)
                    self.maze.start = start

            elif self.mode == 'end':
                if len(self.canvas.find_overlapping(*coords)) == 0:
                    coords = (mid_point[0] - radius,
                              mid_point[1] - radius,
                              mid_point[0] + radius,
                              mid_point[1] + radius)

                    if not self.maze.end == None:
                        self.canvas.delete(self.maze.end)
                    end = self.canvas.create_oval(coords, fill=self.end_color)
                    self.maze.end = end


if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(default='icons/blank.ico')
    root.title('Python Mazes')
    root.resizable(False, False)
    MazeGUI(root)
    root.mainloop()
