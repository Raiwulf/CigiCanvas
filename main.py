import json
import os.path
import random
import webbrowser
from tkinter import colorchooser
from tkinter import messagebox
import pygetwindow as gw
import customtkinter as CTk

CTk.set_appearance_mode("dark")
CTk.set_default_color_theme("dark-blue")

root = CTk.CTk()
root.geometry("420x380+256+256")
root.title("Cigi Canvas")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)


class Canvas:
    def __init__(self, name, y, x, width, height, textcolor, fgcolor, alpha, userInput):
        self.name = name
        self.y = y
        self.x = x
        self.width = width
        self.height = height
        self.textcolor = textcolor
        self.fgcolor = fgcolor
        self.alpha = alpha
        self.userInput = userInput

    def to_dict(self):
        return {
            'name': self.name,
            'y': self.y,
            'x': self.x,
            'width': self.width,
            'height': self.height,
            'textcolor': self.textcolor,
            'fgcolor': self.fgcolor,
            'alpha': self.alpha,
            'userInput': self.userInput,
        }

    @staticmethod
    def load_from_file(filename):
        canvas_list = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                file_contents = f.read()
                if file_contents.strip() and file_contents.strip() != '[]':
                    data = json.loads(file_contents)
                    for canvas_data in data:
                        canvas = Canvas(canvas_data['name'], canvas_data['y'], canvas_data['x'],
                                        canvas_data['width'], canvas_data['height'], canvas_data['textcolor'],
                                        canvas_data['fgcolor'], canvas_data['alpha'], canvas_data['userInput'])
                        canvas_list.append(canvas)
                else:
                    example_canvas = Canvas('Sample', 0, 0, 256, 256, 'black', 'white', 100,
                                            'Welcome!\nThis is your first canvas')
                    with open(filename, 'w') as k:
                        json.dump([example_canvas.to_dict()], k, indent=4)
                    canvas_list.append(example_canvas)
        else:
            example_canvas = Canvas('Sample', 0, 0, 256, 256, 'black', 'white', 100,
                                    'Welcome!\nThis is your first canvas')
            with open(filename, 'w') as f:
                json.dump([example_canvas.to_dict()], f, indent=4)
            canvas_list.append(example_canvas)

        return canvas_list


loadedCanvas = Canvas.load_from_file('saved_canvas.json')


def write_to_file(filename, canvas_data):
    data = {}
    for item in canvas_data.find_all():
        data[item] = canvas_data.itemcget(item, 'text')

    if os.path.isfile(filename):
        with open(filename, 'r') as rw:
            existing_data = json.load(rw)
        for new_obj in data:
            for i, existing_obj in enumerate(existing_data):
                if existing_obj["name"] == new_obj["name"]:
                    existing_data[i] = new_obj
                    break
            else:
                existing_data.append(new_obj)
        data = existing_data

    with open(filename, 'w') as rw:
        json.dump(data, rw)


leftFrame = CTk.CTkFrame(master=root)
leftFrame.grid(row=0, column=0, sticky="nsew")
leftFrame.grid_columnconfigure(4, weight=1)

rightFrame = CTk.CTkFrame(master=root)
rightFrame.grid(row=0, column=1)

coords = CTk.CTkTextbox(master=rightFrame, font=("Roboto", 24))
coords.grid(row=0, column=0, sticky="NSEW")
label = CTk.CTkLabel(master=leftFrame, text="Canvas Manager", font=("Roboto", 24))
label.grid(row=0, column=0, sticky="ew", padx=8, pady=8)


def goURL():
    webbrowser.open_new("https://www.cigiverse.com/cigilabs/cigicanvas")


def on_label_enter(event):
    signature.configure(text_color="cyan")


def on_label_leave(event):
    signature.configure(text_color="white")


signature = CTk.CTkLabel(master=leftFrame, text="© 2023 CigiLabs", font=("Roboto", 16))
signature.bind("<Button-1>", lambda e: goURL())
signature.place(relx=0.02,
                rely=1.0,
                anchor='sw')
signature.bind("<Enter>", on_label_enter)
signature.bind("<Leave>", on_label_leave)


def onCanvasSelected(event):
    canvas_name = combo.get()
    get_window_coordinates(canvas_name)


def get_window_coordinates(canvas_name):
    windows = gw.getWindowsWithTitle(canvas_name)
    if len(windows) == 0:
        coords.delete("0.0", "end-1c")
        coords.insert("0.0", "<= Click Draw")
        return
    window = windows[0].box
    if window is None:
        coords.delete("0.0", "end-1c")
        coords.insert("0.0", "<= Click Draw")
        return
    else:
        y, x, width, height = window.top, window.left, window.width, window.height
        coords.delete("0.0", "end-1c")
        coords.insert("0.0", f"y : {y}    x : {x}\n\nwidth : {width}\nheight : {height}")
        return y, x, width, height


combo = CTk.CTkComboBox(master=leftFrame,
                        values=[canvas.name for canvas in loadedCanvas],
                        command=onCanvasSelected)
combo.grid(row=1, column=0, sticky="ew", padx=8, pady=8)


def reloadJson():
    global loadedCanvas
    loadedCanvas = Canvas.load_from_file('saved_canvas.json')
    combo.configure(values=[canvas.name for canvas in loadedCanvas])


def canvas_action(create_new_canvas=True):
    if create_new_canvas:
        canvas_data = Canvas(entry.get(), 0, 0, 400, 400, alpha=100,
                             textcolor="#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)]),
                             fgcolor="#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)]),
                             userInput="")
    else:
        canvas_data = None
        for canvas in loadedCanvas:
            if canvas.name == combo.get():
                canvas_data = canvas
                break

    kek = CTk.CTk(fg_color=canvas_data.fgcolor)
    kek.geometry(f"{canvas_data.width}x{canvas_data.height}""+"f"{canvas_data.y}""+"f"{canvas_data.x}")
    kek.attributes('-alpha', canvas_data.alpha / 100)

    kekframe = CTk.CTkFrame(master=kek, fg_color="gray13")
    kekframe.grid(row=0, column=0, sticky="nsew")
    kekframe.grid_propagate(True)
    kekframe.grid_columnconfigure(2, weight=1)

    kekAppBar = CTk.CTkFrame(master=kekframe, fg_color="gray13", height=32)
    kekAppBar.grid(row="0", column=0, sticky="nsew")

    def setBorder():
        if borderless.get():
            kek.overrideredirect(True)
            kek.wm_attributes("-topmost", 1)
        else:
            kek.overrideredirect(False)
            kek.wm_attributes("-topmost", 0)

    borderless = CTk.CTkCheckBox(master=kekAppBar, text="", command=setBorder, width=32, height=32)
    borderless.grid(row=0, column=0, sticky="w", padx=4)

    def chooseTextColor():
        color = colorchooser.askcolor()[1]
        canvasEntry.configure(text_color=color)

    textcolor = CTk.CTkButton(master=kekAppBar, text="Text",
                              command=chooseTextColor, width=16, height=16)
    textcolor.grid(row=0, column=1, sticky="w")

    def chooseFgColor():
        color = colorchooser.askcolor()[1]
        canvasEntry.configure(fg_color=color)

    fgcolor = CTk.CTkButton(master=kekAppBar, text="BG", command=chooseFgColor, width=16, height=16)
    fgcolor.grid(row=0, column=2, sticky="w")

    def setAlpha(alpha):
        kek.attributes('-alpha', alpha / 100)

    def saveCanvas():
        canvas_data.userInput = canvasEntry.get("1.0", "end-1c")
        canvas_data.alpha = 100
        canvas_data.textcolor = canvasEntry.cget("text_color")
        canvas_data.fgcolor = canvasEntry.cget("fg_color")
        title = kek.winfo_toplevel().wm_title()
        position = get_window_coordinates(title)
        canvas_data.x = position[0]
        canvas_data.y = position[1]
        canvas_data.width = position[2]
        canvas_data.height = position[3]
        canvas_data_dict = canvas_data.to_dict()
        if os.path.isfile('saved_canvas.json'):
            with open('saved_canvas.json', 'r') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        for i, data in enumerate(existing_data):
            if data['name'] == canvas_data.name:
                existing_data[i] = canvas_data_dict
                break
        else:
            existing_data.append(canvas_data_dict)

        with open('saved_canvas.json', 'w') as f:
            json.dump(existing_data, f)
        Canvas.load_from_file('saved_canvas.json')

    saveBtn = CTk.CTkButton(master=kekAppBar, text="Save", command=saveCanvas, width=16, height=16)
    saveBtn.grid(row=0, column=3, sticky="w", padx=8, pady=8)

    slider = CTk.CTkSlider(master=kekAppBar, command=setAlpha,
                           to=100, from_=32, fg_color=canvas_data.textcolor, width=128)
    slider.grid(row=0, column=4, padx=4, pady=4, sticky="w")

    canvasEntry = CTk.CTkTextbox(master=kekframe, width=50, height=10,
                                 text_color=canvas_data.textcolor, fg_color=canvas_data.fgcolor,
                                 font=CTk.CTkFont(family="Roboto", size=16))
    canvasEntry.insert("0.0", canvas_data.userInput)
    canvasEntry.grid(row=1, column=0, pady=16, columnspan=4, sticky="nsew")

    kek.configure(bg=canvas_data.textcolor)
    kek.title(canvas_data.name)

    reloadJson()
    combo.option_add(value=kek.winfo_name(), pattern=Canvas)
    combo.set(canvas_data.name)

    def onClose():
        reply = messagebox.askyesnocancel("Quit", "Do you want to save the canvas before you quit?")

        def on_yes():
            canvas_data.userInput = canvasEntry.get("1.0", "end-1c")
            canvas_data.alpha = 100
            canvas_data.textcolor = canvasEntry.cget("text_color")
            canvas_data.fgcolor = canvasEntry.cget("fg_color")
            title = kek.winfo_toplevel().wm_title()
            position = get_window_coordinates(title)
            canvas_data.x = position[0]
            canvas_data.y = position[1]
            canvas_data.width = position[2]
            canvas_data.height = position[3]
            canvas_data_dict = canvas_data.to_dict()
            if os.path.isfile('saved_canvas.json'):
                with open('saved_canvas.json', 'r') as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            for i, data in enumerate(existing_data):
                if data['name'] == canvas_data.name:
                    existing_data[i] = canvas_data_dict
                    break
            else:
                existing_data.append(canvas_data_dict)

            with open('saved_canvas.json', 'w') as f:
                json.dump(existing_data, f)
            Canvas.load_from_file('saved_canvas.json')
            kek.destroy()
            reloadJson()

        def on_no():
            kek.destroy()
            reloadJson()

        def on_cancel():
            return

        if reply is None:
            on_cancel()
        elif reply:
            on_yes()
        else:
            on_no()

    kek.protocol("WM_DELETE_WINDOW", onClose)

    def onChange(event):
        title = kek.winfo_toplevel().wm_title()
        position = get_window_coordinates(title)
        if position is not None:
            newWidth = position[2]
            newHeight = position[3]
            canvasEntry.configure(width=newWidth, height=newHeight)

    kek.bind("<Configure>", onChange)
    kek.mainloop()
    pass


def create_canvas():
    canvas_action(create_new_canvas=True)


def draw_canvas():
    canvas_action(create_new_canvas=False)


buttonRefresh = CTk.CTkButton(master=leftFrame, text="Refresh", command=reloadJson)
buttonRefresh.grid(row=2, column=0, sticky="ew", padx=8, pady=8)

buttonDraw = CTk.CTkButton(master=leftFrame, text="Draw", command=draw_canvas)
buttonDraw.grid(row=3, column=0, sticky="ew", padx=8, pady=8)

entry = CTk.CTkEntry(master=leftFrame, placeholder_text="Enter Canvas Name")
entry.grid(row=4, column=0, sticky="ew", padx=8, pady=8)

buttonCreate = CTk.CTkButton(master=leftFrame, text="Create Canvas", command=create_canvas)
buttonCreate.grid(row=5, column=0, sticky="ew", padx=8, pady=8)


def removeCanvas():
    global loadedCanvas
    loadedCanvas = Canvas.load_from_file('saved_canvas.json')
    canvas_name = combo.get()

    for i, canvas in enumerate(loadedCanvas):
        if canvas.name == canvas_name:
            del loadedCanvas[i]
            break

    with open('saved_canvas.json', 'w') as f:
        json.dump([canvas.to_dict() for canvas in loadedCanvas], f)

    reloadJson()
    try:
        combo.set(combo['values'][0])
    except:
        combo.set('')


buttonRemove = CTk.CTkButton(master=leftFrame, text="Remove Canvas", command=removeCanvas)
buttonRemove.grid(row=6, column=0, sticky="ew", padx=8, pady=8)

root.mainloop()