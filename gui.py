from Cocoon.tokens import tok_to_str, output_to_symbolTable
from shell import run
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

# VARIABLE DECLARATION
currentdir = os.path.dirname(os.path.abspath(__file__))
dragged_file = None  # Global variable to store the dragged file path

# RUNS THE LEXER
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

def get_file_path(string):
    files = []
    
    while 'C:/' in string:
        idx = string.rfind('C:/')
        filepath = ''
        
        while idx < len(string) and string[idx] is not None:
            filepath += string[idx]
            idx += 1
        
        files.append(filepath)
        string = string.replace(filepath, "").strip()

    return files

# DRAG AND DROP SECTION
def handle_drop(event):
    if 'Drag and Drop Files Here' in listbox.get(0, END):
        listbox.delete(0, 0)
    fpath = event.data
    file_path = fpath.replace('{' , '').replace('}', '')
    files = get_file_path(file_path)
    if all(file.lower().endswith('.kkun') for file in files):
        if len(files) > 1:
            for file in files:
                if os.path.basename(file) not in listbox.get(0, END):
                    listbox.insert(tk.END, os.path.basename(file))
                    dropped_files.append(file)
        else:
                if os.path.basename(files[-1]) not in listbox.get(0, END):
                    listbox.insert(tk.END, os.path.basename(files[-1]))
                    dropped_files.append(files[-1])

        update_text_content(files[-1])   

        listbox.selection_clear(0, END)
        index = listbox.get(0, END).index(os.path.basename(files[-1]))
        listbox.selection_set(index)

        filename = os.path.basename(files[-1])
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

    else:
        tk.messagebox.showwarning("Invalid File", "Please drop a file with .kkun extension.")

# UPDATES THE TEXTBOX DISPLAY
def update_text_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        textBox.delete("0.0", END)
        textBox.insert(INSERT, content)

# UPDATES THE TEXTBOX DISPLAY AND FILE NAME LABEL UPON SELECTION OF AN ELEMENT IN THE LISTBOX
def update_text_on_selection(event=None):
    selected_index = listbox.curselection()
    if selected_index and len(dropped_files) >= 2:
        sfile = dropped_files[selected_index[0]]
        selected_file = sfile.replace('{' , '').replace('}', '')
        update_text_content(selected_file)

         # UPDATE FILENAME_LABEL WITH THE SELECTED FILENAME
        fname = os.path.basename(selected_file)
        filename = fname.replace('{' , '').replace('}', '')
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

# READS AND DISPLAYS FILE'S CONTENTS TO THE TEXTBOX
def read_file(file):
    with open(file, "r") as f:
        text = f.read()
        textBox.delete("1.0", END)
        textBox.insert(INSERT, text)

# OPEN FILE
def open_file_dialog():
    fpath = filedialog.askopenfilename(initialdir=currentdir, filetypes=(("KKUN files", "*.kkun"),))
    file_path = fpath.replace('{', '').replace('}', '')
    if file_path.lower().endswith('.kkun'):
        fileName_label['state'] = 'normal'
        filename = os.path.basename(file_path)
        read_file(file_path)
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)

        listbox.selection_clear(0, END)

        if 'Drag and Drop Files Here' in listbox.get(0, END):
            listbox.delete(0, 0)

        if os.path.basename(file_path) not in listbox.get(0, END):
            listbox.insert(END, os.path.basename(file_path))
            dropped_files.append(file_path)

        index = listbox.get(0, END).index(os.path.basename(file_path))
        listbox.selection_set(index)

# SAVE AS FILE
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
        
        fileName_label['state'] = 'normal'
        filename = os.path.basename(filename)
        read_file(filename)
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)

        listbox.selection_clear(0, END)

        if 'Drag and Drop Files Here' in listbox.get(0, END):
            listbox.delete(0, 0)

        if os.path.basename(filename) not in listbox.get(0, END):
            listbox.insert(END, os.path.basename(filename))
            dropped_files.append(filename)

        index = listbox.get(0, END).index(os.path.basename(filename))
        listbox.selection_set(index)

# WINDOW
window = TkinterDnD.Tk()
window.geometry("983x689")
window.title("Cocoon Lexical Analyzer")
window.configure(bg = "#252525")
dropped_files = []

# CANVAS
canvas = Canvas(
    window,
    bg = "#252525",
    height = 689,
    width = 983,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

# BACKGROUND
background_img = PhotoImage(file = f"public/img/background.png")
background = canvas.create_image(
    489.5, 344.0,
    image=background_img)

# RESULTBOX.IMAGE
resultBox_img = PhotoImage(file = f"public/img/img_textBox0.png")
resultBox_bg = canvas.create_image(
    630.0, 564.0,
    image = resultBox_img)

# RESULTBOX.WIDGET
resultBox = Text(
    bd = 0,
    bg = "#d5d5d5",
    highlightthickness = 0)
resultBox['state'] = 'disable'

# RESULTBOX.POSITION
resultBox.place(
    x = 315, y = 471,
    width = 630,
    height = 184)

# FILES LABEL
file_label = Label(
    window,
    text = " Files:",
    background= "#BEBEBE",
    font = ("Anonymous Pro Regular", int(16.0)))
file_label.place(x=79, y=29, width=58, height=18)

# TEXTBOX.IMAGE
textBox_img = PhotoImage(file=f"public/img/img_textBox1.png")
textBox_bg = canvas.create_image(
    630.0, 204.0,
    image=textBox_img)

# TEXTBOX.FRAME TO HOLD BOTH TEXT WIDGETS
text_frame = Frame(window, bg="#d5d5d5")
text_frame.place(x=315, y=75, width=630, height=256)

# TEXTBOX.WIDGET
textBox = Text(
    text_frame,
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0,
    wrap=NONE,
    padx=5,
    pady=5
)

# TEXTBOX.POSITION
textBox.pack(side=LEFT, fill=Y)

# SCROLLBAR FOR TEXTBOX
scrollbar = Scrollbar(window, command=textBox.yview)
scrollbar.place(x=928, y=75, height=258, width=19)
textBox['yscrollcommand'] = scrollbar.set

# SCROLLBAR FOR RESULTBOX
result_scrollbar = Scrollbar(window, command=resultBox.yview)
result_scrollbar.place(x=928, y=471, height=185.5, width=19)
resultBox['yscrollcommand'] = result_scrollbar.set

# RESULT TEXT
canvas.create_text(
    349.0, 449,
    text = " Result:",
    fill = "#252525",
    font = ("Anonymous Pro Regular", int(16.0)))

# FILE NAME LABEL
fileName_label = Entry(
    foreground = "#D5D5D5",
    background = "#1A3A35",
    disabledforeground = "#D5D5D5",
    disabledbackground = "#1A3A35",
    readonlybackground = "#1A3A35",
    relief="flat",
    font = ("Anonymous Pro Regular", int(16.0)))
fileName_label.insert(-1, 'Write a code: ')
fileName_label['state'] = 'readonly'

# FILE NAME LABEL.POSITION
fileName_label.place(x=315, y=25)

# SAVE AS BUTTON.IMAGE
saveAsButton_img = PhotoImage(file=f"public/img/saveAsButton.png")

# SAVE AS BUTTON.WIDGET
saveAsButton = Button(
    image=saveAsButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=save_as_file,
    relief="flat"
)

# SAVE AS BUTTON.POSITION
saveAsButton.place(
    x=372.66, y=352.79,
    width=177.45, height=35.16
)

# RUN LEXER BUTTON.IMAGE
runLexerButton_img = PhotoImage(file = f"public/img/runLexerButton.png")

# RUN LEXER BUTTON.WIDGET
runLexerButton = Button(
    image = runLexerButton_img,
    borderwidth = 0,
    highlightthickness = 0,
    command = run_lexer,
    relief = "flat")

# RUN LEXER BUTTON.POSITION
runLexerButton.place(
    x = 708, y = 352,
    width = 177,
    height = 35)

# OPEN FILE BUTTON.IMAGE
openFileButton_img = PhotoImage(file=f"public/img/openFileButton.png")

# OPEN FILE BUTTON.WIDGET
openFileButton = Button(
    image=openFileButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=open_file_dialog,
    relief="flat")

# OPEN FILE BUTTON.POSITION
openFileButton.place(x=70.5, y=59, width=209, height=33)

# LISTBOX WIDGET
listbox = Listbox(
    bd=0,
    bg="#d5d5d5",
    selectbackground="lightblue",
    selectmode=SINGLE,
    highlightthickness=0)
listbox.place(x=89, y=111, width=172, height=537)
listbox.insert(0, "Drag and Drop Files Here")
listbox.drop_target_register(DND_FILES)
listbox.dnd_bind('<<Drop>>', handle_drop)
listbox.bind('<<ListboxSelect>>', update_text_on_selection)

# WINDOW
window.resizable(False, False)
window.mainloop()