from Cocoon.tokens import print_tokens, output_to_symbolTable
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
            print(result)
            textResult = print_tokens(filename, result)
            resultBox['state'] = 'normal'
            resultBox.delete("1.0", END)
            resultBox.insert(INSERT, textResult)
            resultBox['state'] = 'disable'

    else:
        filename = "Unnamed KKUN File"
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
            print(result)
            textResult = print_tokens(filename, result)
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
    file_path = fpath.replace('{', '').replace('}', '')
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
        listbox.selection_anchor(index)

        filename = os.path.basename(files[-1])
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

    else:
        tk.messagebox.showwarning(
            "Invalid File", "Please drop a file with .kkun extension.")

# UPDATES THE TEXTBOX DISPLAY


def update_text_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        textBox.delete("0.0", END)
        textBox.insert(INSERT, content)

# UPDATES THE TEXTBOX DISPLAY AND FILE NAME LABEL UPON SELECTION OF AN ELEMENT IN THE LISTBOX


def update_text_on_selection(event=None):
    selected_index = listbox.curselection()
    if selected_index and len(dropped_files) >= 1:
        sfile = dropped_files[selected_index[0]]
        selected_file = sfile.replace('{', '').replace('}', '')
        update_text_content(selected_file)

        # UPDATE FILENAME_LABEL WITH THE SELECTED FILENAME
        fname = os.path.basename(selected_file)
        filename = fname.replace('{', '').replace('}', '')
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, filename)
        fileName_label['state'] = 'readonly'

# OPEN FILE


def open_file_dialog():
    fpath = filedialog.askopenfilename(
        initialdir=currentdir, filetypes=(("KKUN files", "*.kkun"),))
    file_path = fpath.replace('{', '').replace('}', '')
    if file_path.lower().endswith('.kkun'):
        fileName_label['state'] = 'normal'
        filename = os.path.basename(file_path)
        update_text_content(file_path)
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
        listbox.selection_anchor(index)

# SAVE AS FILE


def save_as_file():
    filename = filedialog.asksaveasfilename(
        initialdir=currentdir,
        defaultextension=".kkun",
        filetypes=[("KKUN files", "*.kkun")],
    )
    if filename:
        with open(filename, "w") as f:
            code = textBox.get("0.0", END)
            f.write(code)

        # Update fileName_label with the selected filename
        fileName_label['state'] = 'normal'
        fileName_label.delete(0, END)
        fileName_label.insert(INSERT, os.path.basename(filename))
        fileName_label['state'] = 'readonly'

        # Update the listbox selection
        update_listbox_selection(filename)

# UPDATE LIST BOX SELECTION


def update_listbox_selection(filename):
    listbox.selection_clear(0, END)

    if 'Drag and Drop Files Here' in listbox.get(0, END):
        listbox.delete(0, 0)

    if os.path.basename(filename) not in listbox.get(0, END):
        listbox.insert(END, os.path.basename(filename))
        dropped_files.append(filename)

    index = listbox.get(0, END).index(os.path.basename(filename))
    listbox.selection_set(index)
    listbox.selection_anchor(index)

# UPDATE LINE NUMBERS


def update_line_numbers():
    # Disable the binding temporarily to prevent updating line numbers
    textBox.unbind('<KeyRelease>')

    # Delete previous line numbers
    line_numbers.config(state='normal')
    line_numbers.delete("1.0", END)

    # Get the number of lines in the main textBox
    total_lines = textBox.index("end-1c").split('.')[0]

    # Calculate the width based on the maximum line number
    width = len(total_lines)
    line_numbers.configure(width=width)

    # Insert line numbers
    for i in range(1, int(total_lines) + 1):
        line_numbers.insert(
            tk.END, f"{i}\n" if i < int(total_lines) else str(i))

    # Update the scrollbar range and move the yview of the line numbers to the position of the scrollbar
    line_numbers.config(yscrollcommand=scrollbarY.set)
    line_numbers.yview_moveto(scrollbarY.get()[0])

    # Set the state of line_numbers to 'disabled' to make it read-only
    line_numbers.config(state='disabled')

    # Re-enable the binding after updating line numbers
    textBox.bind('<KeyRelease>', lambda event: update_line_numbers())

# TEXTBOX UPDATER WITH NUMBER LINE


def update_text_content(file_path):
    # Clear existing content in line_numbers and textBox
    line_numbers.delete("1.0", tk.END)
    textBox.delete("1.0", tk.END)

    with open(file_path, 'r') as file:
        content = file.readlines()

        # Insert line numbers and content
        for i, line in enumerate(content, start=1):
            line_numbers.insert(tk.END, f"{i: >4} {line}")
            textBox.insert(tk.END, line)
            # Call the update_line_numbers function to set up initially
            update_line_numbers()


def combine_funcs(*funcs):
    def inner_combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)

    return inner_combined_func


def on_scroll(event):
    line_numbers.yview_moveto(scrollbarY.get()[0])
    new_xview = textBox.xview()[0]
    textBox.xview_moveto(new_xview)
    update_line_numbers()


def show_scrollbar():
    scrollbarX.place(x=315, y=319, height=14, width=613)
    update_line_numbers()


def hide_scrollbar():
    scrollbarX.place_forget()
    update_line_numbers()


def check_scrollbar(*args):
    if float(args[0]) <= 0.0 and float(args[1]) >= 1.0:
        hide_scrollbar()
    else:
        show_scrollbar()


def on_wheelscroll(*args):
    line_numbers.yview_moveto(float(args[0]))
    textBox.yview_moveto(float(args[0]))


def prevent_scroll(event):
    return "break"


def new_file():
    fileName_label['state'] = 'normal'
    fileName_label.delete(0, END)
    fileName_label.insert(0, 'Write a code: ')
    fileName_label['state'] = 'readonly'

    listbox.selection_clear(0, END)

    textBox.delete("1.0", END)
    update_line_numbers()


def delete():
    listbox.delete(ANCHOR)
    new_file()


def delete_all():
    listbox.delete(0, END)
    new_file()


def run_buttons():
    # RUN LEXER BUTTON.IMAGE
    runLexerButton_img = PhotoImage(file=f"public/img/runLexerButton.png")

    # RUN LEXER BUTTON.WIDGET
    runLexerButton = tk.Button(
        window,
        image=runLexerButton_img,
        command=run_lexer)
    runLexerButton.image = runLexerButton_img
    runLexerButton.pack()

    # RUN LEXER BUTTON.POSITION
    runLexerButton.place(x=768, y=318, width=149, height=37)

    # RUN PARSER BUTTON.IMAGE
    runParserButton_img = PhotoImage(file=f"public/img/runParserButton.png")

    # RUN PARSER BUTTON.WIDGET
    runParserButton = tk.Button(
        window,
        image=runParserButton_img,
        command=run_lexer)
    runParserButton.image = runParserButton_img
    runParserButton.pack()

    # RUN PARSER BUTTON.POSITION
    runParserButton.place(x=768, y=283, width=149, height=37)

    # RUN INTERPRETER BUTTON.IMAGE
    runInterpreterButton_img = PhotoImage(
        file=f"public/img/runInterpreterButton.png")

    # RUN INTERPRETER BUTTON.WIDGET
    runInterpreterButton = tk.Button(
        window,
        image=runInterpreterButton_img,
        command=run_lexer)
    runInterpreterButton.image = runInterpreterButton_img
    runInterpreterButton.pack()

    # RUN INTERPRETER BUTTON.POSITION
    runInterpreterButton.place(x=768, y=248, width=149, height=37)


def run_options():
    run_buttons()


# WINDOW
window = TkinterDnD.Tk()
window.geometry("983x689")
window.iconbitmap("public/img/cocoonIcon.ico")
window.title("Cocoon Lexical Analyzer")
window.configure(bg="#252525")
dropped_files = []

# CANVAS
canvas = Canvas(
    window,
    bg="#252525",
    height=689,
    width=983,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

# BACKGROUND
background_img = PhotoImage(file=f"public/img/background.png")
background = canvas.create_image(
    489.5, 344.0,
    image=background_img)

# RESULTBOX.IMAGE
resultBox_img = PhotoImage(file=f"public/img/img_textBox0.png")
resultBox_bg = canvas.create_image(
    630.0, 564.0,
    image=resultBox_img)

# RESULTBOX.WIDGET
resultBox = Text(
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0)
resultBox['state'] = 'disable'

# RESULTBOX.POSITION
resultBox.place(
    x=315, y=471,
    width=613,
    height=186)

# FILES LABEL
file_label = Label(
    window,
    text=" Files:",
    background="#BEBEBE",
    font=("Anonymous Pro Regular", int(16.0)))
file_label.place(x=79, y=29, width=58, height=18)

# TEXTBOX.IMAGE
textBox_img = PhotoImage(file=f"public/img/img_textBox1.png")
textBox_bg = canvas.create_image(
    630.0, 204.0,
    image=textBox_img)

# TEXTBOX.FRAME TO HOLD BOTH TEXT WIDGETS
text_frame = Frame(window, bg="#d5d5d5")
text_frame.place(x=315, y=75, width=613, height=258)

# LINE NUMBERS.WIDGET
line_numbers = Text(
    text_frame,
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0,
    wrap=NONE,
    padx=5,
    pady=5,
    width=4  # Set an initial width
)

# LINE NUMBERS.POSITION
line_numbers.pack(side=LEFT, fill=Y)

# TEXTBOX.WIDGET
textBox = Text(
    text_frame,
    bd=0,
    bg="#d5d5d5",
    highlightthickness=0,
    wrap=NONE,
    padx=5,
    pady=5,
)

# TEXTBOX.POSITION
textBox.pack(side=LEFT, fill=Y)

# TEXTBOX BIND
textBox.bind('<Configure>', lambda e: update_line_numbers())

# YVIEW SCROLLBAR FOR TEXTBOX
scrollbarY = Scrollbar(window, command=combine_funcs(
    textBox.yview, line_numbers.yview))
scrollbarY.place(x=928, y=75, height=258, width=19)

# YVIEW TEXTBOX.CONFIGURE
textBox['yscrollcommand'] = combine_funcs(on_wheelscroll, scrollbarY.set)

# TEXTBOX.POSITION
textBox.pack(side=BOTTOM, fill=X)

# XVIEW SCROLLBAR FOR TEXTBOX
scrollbarX = Scrollbar(window, command=textBox.xview, orient=HORIZONTAL)

# X SCROLL BAR DRAG
scrollbarX.bind("<B1-Motion>", on_scroll)

# SCROLLBAR HIDE
hide_scrollbar()

# TEXTBOX.CONFIGURE
textBox['xscrollcommand'] = combine_funcs(scrollbarX.set, check_scrollbar)

# LINENUMBERS BIND
line_numbers.bind('<MouseWheel>', prevent_scroll)

# SCROLLBAR BIND
scrollbarY.bind("<B1-Motion>", on_scroll)

# SCROLLBAR FOR RESULTBOX
result_scrollbar = Scrollbar(window, command=resultBox.yview)
result_scrollbar.place(x=928, y=471, height=185.5, width=19)
resultBox['yscrollcommand'] = result_scrollbar.set

# RESULT TEXT
canvas.create_text(
    349.0, 449,
    text=" Result:",
    fill="#252525",
    font=("Anonymous Pro Regular", int(16.0)))

# FILE NAME LABEL
fileName_label = Entry(
    foreground="#D5D5D5",
    background="#1A3A35",
    disabledforeground="#D5D5D5",
    disabledbackground="#1A3A35",
    readonlybackground="#1A3A35",
    relief="flat",
    font=("Anonymous Pro Regular", int(16.0)))
fileName_label.insert(-1, 'Write a code: ')
fileName_label['state'] = 'readonly'

# FILE NAME LABEL.POSITION
fileName_label.place(x=315, y=25, width=637.69)

# LISTBOX WIDGET
listbox = Listbox(
    bd=0,
    bg="#d5d5d5",
    selectbackground="#1A3A35",
    selectmode=SINGLE,
    highlightthickness=0)
listbox.place(x=89, y=111, width=172, height=537)

# LISTBOX DND
listbox.insert(0, "Drag and Drop Files Here")
listbox.drop_target_register(DND_FILES)

# LISTBOX BIND
listbox.dnd_bind('<<Drop>>', handle_drop)
listbox.bind('<<ListboxSelect>>', update_text_on_selection)

# NEW FILE BUTTON.IMAGE
newFileButton_img = PhotoImage(file="public/img/newFileButton.png")

# NEW FILE BUTTON.WIDGET
newFileButton = Button(
    image=newFileButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=new_file,
    relief="flat"
)

# NEW FILE BUTTON.POSITION
newFileButton.place(
    x=343, y=353,
    width=114, height=35.16
)

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
    x=457, y=353,
    width=146, height=35.16
)

# RUN OPTIONS BUTTON.IMAGE
runOptionsButton_img = PhotoImage(file=f"public/img/runOptionsButton.png")

# RUN OPTIONS BUTTON.WIDGET
runOptionsButton = Button(
    image=runOptionsButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=run_buttons,
    relief="flat")

# RUN OPTIONS BUTTON.POSITION
runOptionsButton.place(
    x=768, y=353,
    width=149, height=35.16)

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

# CLEAR BUTTON.IMAGE
clearButton_img = PhotoImage(file=f"public/img/clearButton.png")

# CLEAR BUTTON.WIDGET
clearButton = Button(
    image=clearButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=delete,
    relief="flat")

# CLEAR BUTTON.POSITION
clearButton.place(
    x=88, y=613,
    width=77, height=35)

# CLEAR ALL BUTTON.IMAGE
clearAllButton_img = PhotoImage(file="public/img/clearAllButton.png")

# CLEAR ALL BUTTON.WIDGET
clearAllButton = Button(
    image=clearAllButton_img,
    borderwidth=0,
    highlightthickness=0,
    command=delete_all,
    relief="flat")

# CLEAR ALL BUTTON.POSITION
clearAllButton.place(
    x=165, y=613,
    width=96, height=35)

# WINDOW
window.resizable(False, False)
window.mainloop()
