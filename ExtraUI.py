import tkinter as tk
import ExtraUtils

class MenuBar():
    def __init__(self, parent):
        self.cascade_items = {}
        self.menubar = tk.Menu(parent)

    def root(self):
        return self.menubar

    def addNewCascade(self, cascade_dict):
        for key in cascade_dict:
            master = key
            if str(type(key)) != "<class 'tkinter.Menu'>":
                master = self.cascade_items[key]
            for item in cascade_dict[key]:
                self.cascade_items[item] = tk.Menu(master, tearoff=0)
                master.add_cascade(label=item, menu=self.cascade_items[item])

    def addNewCommands(self, parent, commands):
        for label in commands:
            self.cascade_items[parent].add_command(label=label, command=commands[label])


class RGBSlider():
    def __init__(self, parent, label, current_color):
        self.parent = parent
        self.frame = tk.Frame(self.parent, highlightbackground="black", highlightthickness=2)
        self.frame.pack(fill=tk.BOTH)
        self.current_color = current_color

        color_rgb = utils.hex_to_rgb(current_color)
        
        self.label = label
        tk.Label(self.frame, text=label).grid(row=0,column=0)
        self.color_preview = tk.Frame(self.frame)
        self.color_preview.grid(row=1, rowspan=2, column=0)

        r = tk.Scale(self.frame, name='r', from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(r))
        r.grid(row=0, column=1)
        r.set(color_rgb[0])

        g = tk.Scale(self.frame, name='g', from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(g))
        g.grid(row=1, column=1)
        g.set(color_rgb[1])

        b = tk.Scale(self.frame, name='b', from_=0, to=255, orient='horizontal', 
            command=lambda x: self.update_color(b))
        b.grid(row=2, column=1)
        b.set(color_rgb[2])

        self.parent.update()
        self.color_preview.config(background=self.current_color, width=self.frame.winfo_width()/3, height=self.frame.winfo_width()/3)

    def get_color(self):
        return self.current_color

    def get_label(self):
        return self.label


    def update_color(self, scale):
        current_rgb = utils.hex_to_rgb(self.current_color)
        new_color = self.current_color

        if 'r' in str(scale):
            new_color = utils.rgb_to_hex(scale.get(), current_rgb[1], current_rgb[2])
        if 'g' in str(scale):
            new_color = utils.rgb_to_hex(current_rgb[0], scale.get(), current_rgb[2])
        if 'b' in str(scale):
            new_color = utils.rgb_to_hex(current_rgb[0], current_rgb[1], scale.get())

        self.current_color = new_color
        self.color_preview.config(background=self.current_color)