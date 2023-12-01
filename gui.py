from Cocoon.tokens import tok_to_str, output_to_symbolTable
from shell import run
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

currentdir = os.path.dirname(os.path.abspath(__file__))
dragged_file = None  # Global variable to store the dragged file path

def btn_clicked():
    print("Button Clicked")

def run_lexer():
    if fileName_label.get() != "Write a code: ":
        filename = fileName_label.get()
        text = textBox.get("1.0", END)

        result, error = run(filename, text)

        if error:
            print(error.as_string())
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, error.as_string())
            resultBox['state'] = 'disable'
        else:
            output_to_symbolTable(result)
            result.pop()
            print(result)
            textResult = ''
            textResult += (format("File name:", ">20") + "      " + filename + "\n")
            textResult += (format('TOKENS', '>20') + '      ' + 'LEXEMES' + "\n")
            textResult += ('-----------------------------------------------' + "\n")
            textResult += (tok_to_str(result))
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, textResult)
            resultBox['state'] = 'disable'

    else:
        text = textBox.get("1.0", END)

        result, error = run("<stdin>", text)

        if error:
            print(error.as_string())
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, error.as_string())
            resultBox['state'] = 'disable'
        else:
            output_to_symbolTable(result)
            result.pop()
            print(result)
            textResult = ''
            textResult += (format("File name:", ">20") + "      " + "<stdin>" + "\n")
            textResult += (format('TOKENS', '>20') + '      ' + 'LEXEMES' + "\n")
            textResult += ('-----------------------------------------------' + "\n")
            textResult += (tok_to_str(result))
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


# DRAG AND DROP SECTION

def handle_drop(event):
    file_path = event.data
    if file_path.lower().endswith('.kkun'):
        dropped_files.append(file_path)

        listbox.delete(0, tk.END)
        for file in dropped_files:
            listbox.insert(tk.END, os.path.basename(file))

        update_text_content(file_path)

        filename = os.path.basename(file_path)
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

    else:
        tk.messagebox.showwarning("Invalid File", "Please drop a file with .kkun extension.")

def update_text_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        textBox.delete(1.0, tk.END)
        textBox.insert(tk.END, content)

def update_text_on_selection(event=None):
    selected_index = listbox.curselection()
    if selected_index:
        selected_file = dropped_files[selected_index[0]]
        update_text_content(selected_file)

         # Update fileName_label with the selected filename
        filename = os.path.basename(selected_file)
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

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

        # Append the opened file to the dropped_files list
        dropped_files.append(file_path)

        # Update the listbox with the opened file
        listbox.delete(0, tk.END)
        for file in dropped_files:
            listbox.insert(tk.END, os.path.basename(file))

def save_as_file():
    filename = filedialog.asksaveasfilename(
        initialdir=currentdir,
        defaultextension=".kkun",
        filetypes=[("KKUN files", "*.kkun")],
    )
    if filename:
        with open(filename, "w") as f:
            code = textBox.get("1.0", END)
            f.write(code)
        
        # Update filename label
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, os.path.basename(filename))
        fileName_label['state'] = 'readonly'

        # Append the newly saved file to the dropped_files list
        dropped_files.append(filename)

        # Update the listbox with the new file
        listbox.delete(0, tk.END)
        for file in dropped_files:
            listbox.insert(tk.END, os.path.basename(file))


window = TkinterDnD.Tk()

window.geometry("983x689")
window.title("Cocoon Lexical Analyzer")
window.configure(bg = "#252525")
dropped_files = []

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

resultBox['state'] = 'disable'

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


#Frame to hold both text widgets
text_frame = Frame(window, bg="#d5d5d5")
text_frame.place(x=315, y=75, width=630, height=256)

textBox = Text(
    text_frame,
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0,
    wrap=NONE,
    padx=5,
    pady=5
)
textBox.pack(side=LEFT, fill=Y)

# Scrollbar for both text widgets
scrollbar = Scrollbar(window, command=textBox.yview)
scrollbar.place(x=948, y=75, height=256)

result_scrollbar = Scrollbar(window, command=resultBox.yview)
result_scrollbar.place(x=945, y=471, height=184)

textBox['yscrollcommand'] = scrollbar.set
resultBox['yscrollcommand'] = result_scrollbar.set



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

saveAsButton_img = PhotoImage(file=f"public/img/img0.png")
saveAsButton = Button(
    image=saveAsButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=save_as_file,
    relief="flat"
)

saveAsButton.place(
    x=372.66, y=352.79,
    width=177.45, height=35.16
)


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
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', handle_drop)
listbox.bind('<<ListboxSelect>>', update_text_on_selection)

window.resizable(False, False)
window.mainloop()