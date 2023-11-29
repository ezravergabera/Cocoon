from tkinter import *


def btn_clicked():
    print("Button Clicked")


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

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    630.0, 204.0,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#d5d5d5",
    highlightthickness = 0)

entry1.place(
    x = 315, y = 75,
    width = 630,
    height = 256)

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

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 70.5, y = 59,
    width = 209,
    height = 33)

window.resizable(False, False)
window.mainloop()
