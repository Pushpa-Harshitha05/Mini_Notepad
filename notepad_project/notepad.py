from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import font
import os

file = 0
default_font_size = 14


def new_file_create(event=None):
    root.title("Untitled - NoteBook")
    text_area.delete(1.0, END)


def new_window_create(event=None):
    def new_file_create(event=None):
        new_window.title("Untitled - NoteBook")
        text_area.delete(1.0, END)

    def open_file(event=None):
        global file
        types = (("All files", "*.*"), ("Text files", "*.txt"))
        file = askopenfilename(defaultextension=".txt", initialdir="C:/", filetypes=types)
        if file == "":
            file = None
        else:
            new_window.title(os.path.basename(file) + " - NoteBook")
            # opens the file, read and write the contents of the file.
            with open(file, "r") as rf:
                text_area.delete(1.0, END)
                text_area.insert(1.0, rf.read())

    def save_file(event=None):
        global file
        if file == 0:
            file_typ = (("All files", "*.*"), ("Text files", "*.txt"))
            file = asksaveasfilename(initialfile="Untitled.txt", filetypes=file_typ)
            if file == "":
                file = None
            else:
                f = open(file, "w")
                f.write(text_area.get(1.0, END))
                f.close()

                new_window.title(os.path.basename(file) + " - NoteBook")
        else:
            f = open(file, "w")
            # saving the file with current text in the notebook text.
            f.write(text_area.get(1.0, END))
            f.close()

    def save_file_as(event=None):
        global file
        f_types = (("All files", "*.*"), ("Text files", "*.txt"))
        file = asksaveasfilename(initialfile="Untitled.txt", filetypes=f_types)
        f = open(file, "w")
        # saving the file with current text in the notebook text.
        f.write(text_area.get(1.0, END))
        f.close()

        new_window.title(os.path.basename(file) + " - NoteBook")

    def cut_text(event=None):
        # Deleting the text in the current text of the file.
        text_area.event_generate("<<Cut>>")

    def copy_text(event=None):
        # Copying the text in the file.
        text_area.event_generate("<<Copy>>")

    def paste_text(event=None):
        # Pastes the copied text in the file.
        text_area.event_generate("<<Paste>>")

    def change(f_name):
        selected = f_name
        try:
            sel_start, sel_end = text_area.index("sel.first"), text_area.index("sel.last")
            if sel_start and sel_end:
                text_area.tag_remove("selected_text", "1.0", END)
                text_area.tag_add("selected_text", sel_start, sel_end)
                text_area.tag_config("selected_text", font=(selected, 12))
                text_area.tag_remove("sel", "1.0", END)
        except TclError:
            pass

    def change_font(f):
        return lambda: change(f)

    def get_underline():
        try:
            start_index, end_index = text_area.index("sel.first"), text_area.index("sel.last")
            current_tags = text_area.tag_names(start_index)
            if 'underline' in current_tags:
                text_area.tag_remove('underline', start_index, end_index)
            else:
                text_area.tag_add('underline', start_index, end_index)
                text_area.tag_configure('underline', underline=True)
        except TclError:
            pass

    def increase_font_size(event=None):
        global default_font_size
        try:
            start, end = text_area.index("sel.first"), text_area.index("sel.last")
            text_area.tag_add("font_tag", start, end)
            text_area.tag_configure("font_tag", font=("", default_font_size))
            current_font = text_area.tag_configure("font_tag")["font"]
            default_font_size = int(current_font[4][-2:]) + 2
        except TclError:
            pass

    def decrease_font_size(event=None):
        global default_font_size
        try:
            start, end = text_area.index("sel.first"), text_area.index("sel.last")
            text_area.tag_add("font_tag", start, end)
            text_area.tag_configure("font_tag", font=("", default_font_size))
            current_font = text_area.tag_configure("font_tag")["font"]
            default_font_size = int(current_font[4][-2:]) - 2
        except TclError:
            pass

    def get_help(event=None):
        showinfo("Help-NoteBook",
                 "Shortcut commands : \n(Note that the commands are case-sensitive 'Ctrl+n' is not same "
                 "as 'Ctrl+N')\n\n New File - Ctrl+n\n New Window - Ctrl+Shift+n\n Open File - Ctrl+o\n "
                 "Save File - Ctrl+s\n Save File as - Ctrl+S\n Cut Text - Ctrl+x \n Copy Text - Ctrl+c\n "
                 "Paste Text - Ctrl+v\n")

    if __name__ == "__main__":
        new_window = Tk()
        new_window.geometry("1550x1550")
        new_window.title("NoteBook")
        new_window.wm_iconbitmap("notepad_icon.ico")

        global text_area
        text_area = Text(new_window, font="lucida 14", undo=True)
        text_area.pack(expand=True, fill=BOTH)

        global scrollbar
        scrollbar = Scrollbar(text_area, cursor="arrow")
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=text_area.yview)
        text_area.config(yscrollcommand=scrollbar.set)

        global mainmenu
        mainmenu = Menu(new_window)

        global filemenu
        filemenu = Menu(mainmenu, tearoff=0)
        filemenu.add_command(label="New File", accelerator="Ctrl+n", command=new_file_create)
        filemenu.add_command(label="New Window", accelerator="Ctrl+Shift+n", command=new_window_create)
        filemenu.add_separator()
        filemenu.add_command(label="Open", accelerator="Ctrl+o", command=open_file)
        filemenu.add_command(label="Save", accelerator="Ctrl+s", command=save_file)
        filemenu.add_command(label="Save as", accelerator="Ctrl+S", command=save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label="Close Window", command=quit)

        new_window.bind_all("<Control-n>", new_file_create)
        new_window.bind_all("<Control-N>", new_window_create)
        new_window.bind_all("<Control-o>", open_file)
        new_window.bind_all("<Control-s>", save_file)
        new_window.bind_all("<Control-S>", save_file_as)

        mainmenu.add_cascade(label='File', menu=filemenu)

        global editmenu
        editmenu = Menu(mainmenu, tearoff=0)
        editmenu.add_command(label="Cut", accelerator="Ctrl+x", command=cut_text)
        editmenu.add_separator()
        editmenu.add_command(label="Copy", accelerator="Ctrl+c", command=copy_text)
        editmenu.add_command(label="Paste", accelerator="Ctrl+v", command=paste_text)

        new_window.bind_all("<Control-x>", cut_text)
        new_window.bind_all("<Control-c>", copy_text)
        new_window.bind_all("<Control-v>", paste_text)

        mainmenu.add_cascade(label="Edit", menu=editmenu)

        global helpmenu, font_menu
        helpmenu = Menu(mainmenu, tearoff=0)
        font_menu = Menu(helpmenu, tearoff=0)

        global fonts, i
        fonts = font.families()
        for i in fonts:
            font_menu.add_command(label=i, command=change_font(i))

        helpmenu.add_cascade(label="Font", menu=font_menu)
        helpmenu.add_command(label="Underline", command=get_underline)
        helpmenu.add_separator()
        helpmenu.add_command(label="Increase Font size", command=increase_font_size)
        helpmenu.add_command(label="Decrease Font size", command=decrease_font_size)
        helpmenu.add_separator()
        helpmenu.add_command(label="Help", accelerator="Ctrl+h", command=get_help)

        new_window.bind_all("<Control-h>", get_help)

        mainmenu.add_cascade(label="View", menu=helpmenu)

        new_window.config(menu=mainmenu)


def open_file(event=None):
    global file
    types = (("All files", "*.*"), ("Text files", "*.txt"))
    file = askopenfilename(defaultextension=".txt", initialdir="C:/", filetypes=types)
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - NoteBook")
        # opens the file, read and write the contents of the file.
        with open(file, "r") as rf:
            text_area.delete(1.0, END)
            text_area.insert(1.0, rf.read())


def save_file(event=None):
    global file
    if file == 0:
        file_typ = (("All files", "*.*"), ("Text files", "*.txt"))
        file = asksaveasfilename(initialfile="Untitled.txt", filetypes=file_typ)
        if file == "":
            file = None
        else:
            f = open(file, "w")
            f.write(text_area.get(1.0, END))
            f.close()

            root.title(os.path.basename(file) + " - NoteBook")
    else:
        f = open(file, "w")
        # saving the file with current text in the notebook text.
        f.write(text_area.get(1.0, END))
        f.close()


def save_file_as(event=None):
    global file
    f_types = (("All files", "*.*"), ("Text files", "*.txt"))
    file = asksaveasfilename(initialfile="Untitled.txt", filetypes=f_types)
    f = open(file, "w")
    # saving the file with current text in the notebook text.
    f.write(text_area.get(1.0, END))
    f.close()

    root.title(os.path.basename(file) + " - NoteBook")


def cut_text(event=None):
    # Deleting the text in the current text of the file.
    text_area.event_generate("<<Cut>>")


def copy_text(event=None):
    # Copying the text in the file.
    text_area.event_generate("<<Copy>>")


def paste_text(event=None):
    # Pastes the copied text in the file.
    text_area.event_generate("<<Paste>>")


def change(f_name):
    selected = f_name
    try:
        sel_start, sel_end = text_area.index("sel.first"), text_area.index("sel.last")
        if sel_start and sel_end:
            text_area.tag_remove("selected_text", "1.0", END)
            text_area.tag_add("selected_text", sel_start, sel_end)
            text_area.tag_config("selected_text", font=(selected, 12))
            text_area.tag_remove("sel", "1.0", END)
    except TclError:
        pass


def change_font(f):
    return lambda: change(f)


def get_underline():
    try:
        start_index, end_index = text_area.index("sel.first"), text_area.index("sel.last")
        current_tags = text_area.tag_names(start_index)
        if 'underline' in current_tags:
            text_area.tag_remove('underline', start_index, end_index)
        else:
            text_area.tag_add('underline', start_index, end_index)
            text_area.tag_configure('underline', underline=True)
    except TclError:
        pass


def increase_font_size(event=None):
    global default_font_size
    try:
        start, end = text_area.index("sel.first"), text_area.index("sel.last")
        text_area.tag_add("font_tag", start, end)
        text_area.tag_configure("font_tag", font=("", default_font_size))
        current_font = text_area.tag_configure("font_tag")["font"]
        default_font_size = int(current_font[4][-2:]) + 2
    except TclError:
        pass


def decrease_font_size(event=None):
    global default_font_size
    try:
        start, end = text_area.index("sel.first"), text_area.index("sel.last")
        text_area.tag_add("font_tag", start, end)
        text_area.tag_configure("font_tag", font=("", default_font_size))
        current_font = text_area.tag_configure("font_tag")["font"]
        default_font_size = int(current_font[4][-2:]) - 2
    except TclError:
        pass


def get_help(event=None):
    showinfo("Help-NoteBook",
             "Shortcut commands : \n(Note that the commands are case-sensitive 'Ctrl+n' is not same "
             "as 'Ctrl+N')\n\n New File - Ctrl+n\n New Window - Ctrl+Shift+n\n Open File - Ctrl+o\n "
             "Save File - Ctrl+s\n Save File as - Ctrl+S\n Cut Text - Ctrl+x \n Copy Text - Ctrl+c\n "
             "Paste Text - Ctrl+v\n")


if __name__ == "__main__":
    root = Tk()
    root.geometry("1550x1550")
    root.title("NoteBook")
    root.wm_iconbitmap("notepad_icon.ico")

    text_area = Text(root, font="lucida 14", undo=True)
    text_area.pack(expand=True, fill=BOTH)

    scrollbar = Scrollbar(text_area, cursor="arrow")
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text_area.yview)
    text_area.config(yscrollcommand=scrollbar.set)

    mainmenu = Menu(root)

    filemenu = Menu(mainmenu, tearoff=0)
    filemenu.add_command(label="New File", accelerator="Ctrl+n", command=new_file_create)
    filemenu.add_command(label="New Window", accelerator="Ctrl+Shift+n", command=new_window_create)
    filemenu.add_separator()
    filemenu.add_command(label="Open", accelerator="Ctrl+o", command=open_file)
    filemenu.add_command(label="Save", accelerator="Ctrl+s", command=save_file)
    filemenu.add_command(label="Save as", accelerator="Ctrl+S", command=save_file_as)
    filemenu.add_separator()
    filemenu.add_command(label="Close Window", command=quit)

    root.bind_all("<Control-n>", new_file_create)
    root.bind_all("<Control-N>", new_window_create)
    root.bind_all("<Control-o>", open_file)
    root.bind_all("<Control-s>", save_file)
    root.bind_all("<Control-S>", save_file_as)

    mainmenu.add_cascade(label='File', menu=filemenu)

    editmenu = Menu(mainmenu, tearoff=0)
    editmenu.add_command(label="Cut", accelerator="Ctrl+x", command=cut_text)
    editmenu.add_command(label="Undo", accelerator="Ctrl+z", command=text_area.edit_undo)
    editmenu.add_separator()
    editmenu.add_command(label="Copy", accelerator="Ctrl+c", command=copy_text)
    editmenu.add_command(label="Paste", accelerator="Ctrl+v", command=paste_text)

    root.bind_all("<Control-x>", cut_text)
    root.bind_all("<Control-c>", copy_text)
    root.bind_all("<Control-v>", paste_text)

    mainmenu.add_cascade(label="Edit", menu=editmenu)

    helpmenu = Menu(mainmenu, tearoff=0)
    font_menu = Menu(helpmenu, tearoff=0)

    fonts = font.families()
    for i in fonts:
        font_menu.add_command(label=i, command=change_font(i))

    helpmenu.add_cascade(label="Font", menu=font_menu)
    helpmenu.add_command(label="Underline", command=get_underline)
    helpmenu.add_separator()
    helpmenu.add_command(label="Increase Font size", command=increase_font_size)
    helpmenu.add_command(label="Decrease Font size", command=decrease_font_size)
    helpmenu.add_separator()
    helpmenu.add_command(label="Help", accelerator="Ctrl+h", command=get_help)

    root.bind_all("<Control-h>", get_help)

    mainmenu.add_cascade(label="View", menu=helpmenu)

    # config() is used to associate mainmenu with the root window.
    root.config(menu=mainmenu)

    root.mainloop()
