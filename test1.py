import os
from tkinter import *
from tkinter import filedialog

dragged_file = None  # Global variable to store the dragged file path

def btn_clicked():
    print("Button Clicked")


def check_clipboard():
    try:
        file_path = window.clipboard_get()
        if file_path.lower().endswith('.kkun'):
            entry1.delete(0, END)
            entry1.insert(0, file_path)
    except TclError:
        pass

    window.after(100, check_clipboard)  # Check clipboard every 100 milliseconds

def on_drag_start(event):
    global dragged_file
    # Define data to be dragged (e.g., the selected file)
    dragged_file = listbox.get(listbox.nearest(event.y))

def on_drag_enter(event):
    listbox.itemconfig(listbox.nearest(event.y), background="lightblue")

def on_drag_leave(event):
    listbox.itemconfig(listbox.nearest(event.y), background="white")

def on_drop(event):
    file_path = event.data
    if file_path.lower().endswith('.kkun'):
        entry1.delete(0, END)
        entry1.insert(0, file_path)

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=(("KKUN files", "*.kkun"),))
    if file_path.lower().endswith('.kkun'):
        entry1.delete(0, END)
        entry1.insert(0, file_path)

window = Tk()

window.geometry("983x689")
window.configure(bg = "#252525")

canvas = Canvas(
    window,
    bg = "#252525",
    height = 689,
    width = 983,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)


background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    489.5, 344.0,
    image=background_img)


entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    630.0, 564.0,
    image = entry0_img)


entry0 = Entry(
    bd = 0,
    bg = "#d5d5d5",
    highlightthickness = 0)


entry0.place(
    x = 315, y = 471,
    width = 630,
    height = 184)


canvas.create_text(
    108.0, 37.0,
    text = " Files:",
    fill = "#252525",
    font = ("Anonymous Pro Regular", int(16.0)))


entry1_img = PhotoImage(file=f"img_textBox1.png")
entry1_bg = canvas.create_image(
    630.0, 204.0,
    image=entry1_img)


entry1 = Entry(
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0)


entry1.place(
    x=315, y=75,
    width=630,
    height=256)


canvas.create_text(
    349.0, 449,
    text = " Result:",
    fill = "#252525",
    font = ("Anonymous Pro Regular", int(16.0)))


canvas.create_text(
    377.0, 35.0,
    text = " Write a code:",
    fill = "#d5d5d5",
    font = ("Anonymous Pro Regular", int(16.0)))


img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")


b0.place(
    x = 372, y = 352,
    width = 177,
    height = 35)


img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")


b1.place(
    x = 708, y = 352,
    width = 177,
    height = 35)


img2 = PhotoImage(file=f"img2.png")
browse_button = Button(
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=open_file_dialog,
    relief="flat")

browse_button.place(x=70.5, y=59, width=209, height=33)

listbox = Listbox(
    bd=0,
    bg="#d5d5d5",
    selectbackground="lightblue",
    selectmode=SINGLE,
    highlightthickness=0)
listbox.place(x=315, y=75, width=630, height=256)

listbox.insert(0, "Drag and Drop Files Here")

listbox.bind('<B1-Motion>', on_drag_start)
listbox.bind('<Enter>', on_drag_enter)
listbox.bind('<Leave>', on_drag_leave)
listbox.bind('<ButtonRelease-1>', on_drop)

window.resizable(False, False)
window.mainloop()