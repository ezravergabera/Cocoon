import os
import cocoon
from tkinter import *
from tkinter import filedialog

currentdir = os.path.dirname(os.path.abspath(__file__))
dragged_file = None  # Global variable to store the dragged file path

def btn_clicked():
    print("Button Clicked")

def run_lexer():
    if fileName_label.get() != "Write a code: ":
        filename = fileName_label.get()
        text = textBox.get("1.0", END)

        result, error = cocoon.run(filename, text)

        if error:
            print(error.as_string())
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, error.as_string())
            resultBox['state'] = 'disable'
        else:
            cocoon.output_to_symbolTable(result)
            result.pop()
            print(result)
            textResult = ''
            textResult += (format("File name:", ">20") + "      " + filename + "\n")
            textResult += (format('TOKENS', '>20') + '      ' + 'LEXEMES' + "\n")
            textResult += ('-----------------------------------------------' + "\n")
            textResult += (cocoon.tok_to_str(result))
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, textResult)
            resultBox['state'] = 'disable'

    else:
        text = textBox.get("1.0", END)

        result, error = cocoon.run("<stdin>", text)

        if error:
            print(error.as_string())
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, error.as_string())
            resultBox['state'] = 'disable'
        else:
            cocoon.output_to_symbolTable(result)
            result.pop()
            print(result)
            textResult = ''
            textResult += (format("File name:", ">20") + "      " + "<stdin>" + "\n")
            textResult += (format('TOKENS', '>20') + '      ' + 'LEXEMES' + "\n")
            textResult += ('-----------------------------------------------' + "\n")
            textResult += (cocoon.tok_to_str(result))
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, textResult)
            resultBox['state'] = 'disable'
    
def read_file(file):
    with open(file, "r") as f:
        text = f.read()
        textBox.delete("1.0", END)
        textBox.insert(INSERT, text)

def check_clipboard():
    try:
        file_path = window.clipboard_get()
        if file_path.lower().endswith('.kkun'):
            textBox.delete(0, END)
            textBox.insert(0, file_path)
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

def on_drop():
    global dragged_file
    file_path = dragged_file
    if file_path.lower().endswith('.kkun'):
        print("hello")
        textBox.delete(0, END)
        textBox.insert(0, file_path)
        listbox.insert("end", file_path)

def open_file_dialog():
    file_path = filedialog.askopenfilename(initialdir=currentdir, filetypes=(("KKUN files", "*.kkun"),))
    if file_path.lower().endswith('.kkun'):
        fileName_label['state'] = 'normal'
        filename = file_path.split("/")
        read_file(filename[-1])
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename[-1])

window = Tk()

window.geometry("983x689")
window.title("Cocoon Lexical Analyzer")
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


background_img = PhotoImage(file = f"public/img/background.png")
background = canvas.create_image(
    489.5, 344.0,
    image=background_img)


resultBox_img = PhotoImage(file = f"public/img/img_textBox0.png")
resultBox_bg = canvas.create_image(
    630.0, 564.0,
    image = resultBox_img)


resultBox = Text(
    bd = 0,
    bg = "#d5d5d5",
    highlightthickness = 0)


resultBox.place(
    x = 315, y = 471,
    width = 630,
    height = 184)


file_label = Label(
    window,
    text = " Files:",
    background= "#BEBEBE",
    font = ("Anonymous Pro Regular", int(16.0)))
file_label.place(x=79, y=29, width=58, height=18)


textBox_img = PhotoImage(file=f"public/img/img_textBox1.png")
textBox_bg = canvas.create_image(
    630.0, 204.0,
    image=textBox_img)


textBox = Text(
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0)

textBox.place(
    x=315, y=75,
    width=630,
    height=256)


canvas.create_text(
    349.0, 449,
    text = " Result:",
    fill = "#252525",
    font = ("Anonymous Pro Regular", int(16.0)))


fileName_label = Entry(
    foreground = "#D5D5D5",
    background = "#1A3A35",
    disabledforeground = "#D5D5D5",
    disabledbackground = "#1A3A35",
    readonlybackground = "#1A3A35",
    relief="flat",
    font = ("Anonymous Pro Regular", int(16.0)))
fileName_label.insert(-1, 'Write a code: ')
fileName_label.place(x=315, y=25)
fileName_label['state'] = 'readonly'


img0 = PhotoImage(file = f"public/img/img0.png")
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


runLexerButton = PhotoImage(file = f"public/img/img1.png")
b1 = Button(
    image = runLexerButton,
    borderwidth = 0,
    highlightthickness = 0,
    command = run_lexer,
    relief = "flat")


b1.place(
    x = 708, y = 352,
    width = 177,
    height = 35)


openFileButton = PhotoImage(file=f"public/img/img2.png")
browse_button = Button(
    image=openFileButton,
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
listbox.place(x=89, y=111, width=172, height=537)
listbox.insert(0, "Drag and Drop Files Here")

listbox.bind('<B1-Motion>', on_drag_start)
listbox.bind('<Enter>', on_drag_enter)
listbox.bind('<Leave>', on_drag_leave)
listbox.bind('<ButtonRelease-1>', on_drop)

window.resizable(False, False)
window.mainloop()