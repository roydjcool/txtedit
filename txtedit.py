# This is simple text Editor with basic features like
# Creating, editing, and viewing of a file.

from tkinter import *
from tkinter import filedialog
from tkinter import font, Tk, Text, Button, Frame
import enchant
import re, threading
import speech_recognition as sr
from gtts import gTTS
import os

root = Tk()
root.title('IGNOU - Textedit!')
# root.iconbitmap('C:/Users/shashank.arya/Desktop/mcs044 mini project - Text Editor/gui/icon.ico')
root.geometry('800x500')

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set variable for open file name
global already_open_filename
already_open_filename = False

global selected
selected = True

# create a toolbar frame
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X)

# Create Main Frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# Create Scrollbar for Text Editor
ver_scroll = Scrollbar(my_frame)
ver_scroll.pack(side=RIGHT, fill=Y)

# horizontal Scrollbar
hor_scroll = Scrollbar(my_frame, orient=HORIZONTAL)
hor_scroll.pack(side=BOTTOM, fill=X)

# Create Text Box
text_area = Text(my_frame, width=800, height=500, font=("calibri", 16), selectbackground="yellow",
               selectforeground="black", undo=True, yscrollcommand=ver_scroll.set, wrap=WORD,
               xscrollcommand=hor_scroll)
text_area.pack(fill=Y, expand=1)

# Configure Scrollbar
ver_scroll.config(command=text_area.yview)
hor_scroll.config(command=text_area.xview)

#cofigure Status Bar

# status_var = tk.StringVar()
# status_var.set("Line: 1 | Column: 1")
# status_bar = tk.Label(root, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
# status_bar.pack(side=tk.BOTTOM, fill=tk.X)



# create new file function

def new_file():
    # Delete Previous text
    text_area.delete("1.0", END)
    # update Status with New File
    root.title('New File - Text Pad!')
    status_bar.config(text="New File    ")

    global already_open_filename
    already_open_filename = FALSE


# create open file function
def open_file():
    text_area.delete("1.0", END)
    # Grab file name
    text_file = filedialog.askopenfilename(initialdir="C:/gui/", title="Open File", filetypes=(
        ("text files", "*.txt"), ("html files", "*.html"), ("Python Files", "*.py"), ("All File", "*.*")))

    if text_file:
        # make file name global so we can access it later
        global already_open_filename
        already_open_filename = text_file

    # update Status bars
    name = text_file
    status_bar.config(text=f'{name}')
    name.replace("C:/gui/", "")
    root.title(f'{name} - TextPad!')
    # open the file
    text_file = open(text_file, 'r')
    content = text_file.read()
    # Insert character in textbox
    text_area.insert(END, content)
    # close the opened file
    text_file.close()


# save an existing file
def save_file():
    global already_open_filename
    if already_open_filename:
        # save the file
        text_file = open(already_open_filename, 'w')
        text_file.write(text_area.get("1.0", END))
        # close the file
        text_file.close()
        status_bar.config(text=f' Saved: {already_open_filename}')
    else:
        save_as_file()


# save as file
def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/gui/", title="Save File", filetypes=(
        (("text files", "*.txt"), ("html files", "*.html"), ("Python Files", "*.py"), ("All File", "*.*"))))
    if text_file:
        # update status bars
        name = text_file
        status_bar.config(text=f'{name}')
        name = name.replace("C:/gui/", "")
        root.title(f'{name} - Textpad!')

        # save the file
        text_file = open(text_file, 'w')
        text_file.write(text_area.get("1.0", END))
        text_file.close()


# Cut Text

def cut_text(e=None):
    # check to see if keyboard shortcut is used
    if text_area.tag_ranges("sel"):  # Check if there is text selected
        selected_text = text_area.get("sel.first", "sel.last")
        text_area.delete("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(selected_text)


# Copy Text

def copy_text(e=None):
    if text_area.tag_ranges("sel"):  # Check if there is text selected
       selected_text = text_area.get("sel.first", "sel.last")
       root.clipboard_clear()
       root.clipboard_append(selected_text)

# Paste Text

def paste_text(e=None):  # Allow for optional event argument
    try:
        position = text_area.index(INSERT)
        selected_text = root.clipboard_get()
        text_area.insert(position, selected_text)
    except TclError:  # Handle the case where clipboard does not contain text
        pass


# bold text
def bold_it():
    bold_font = font.Font(text_area, text_area.cget("font"))
    bold_font.configure(weight="bold")

    # current tags
    current_tags = text_area.tag_names("sel.first")

    # configure a tag
    text_area.tag_configure("bold", font=bold_font)

    # if statement
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")


# Italic text
def italic_it():
    italics_font = font.Font(text_area, text_area.cget("font"))
    italics_font.configure(slant="italic")
    # configure a tag
    text_area.tag_configure("italic", font=italics_font)

    # current tags
    current_tags = text_area.tag_names("sel.first")

    # if statement
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")


# underline text
def underline_it():
    underline_font = font.Font(text_area, text_area.cget("font"))
    underline_font.configure(underline=1)

    text_area.tag_configure("underline", font=underline_font)

    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")


# Find a char or string in the file
def find_text():
    search_toplevel = Toplevel(root)
    search_toplevel.title('Find Text')
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e',
                                                                                      padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
           command=lambda: search_output(
               search_entry_widget.get(), ignore_case_value.get(),
               text_area, search_toplevel, search_entry_widget)
           ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

    def close_search_window():
        text_area.tag_remove('match', '1.0', END)
        search_toplevel.destroy()

    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    return "break"


def search_output(needle, if_ignore_case, text_area, search_toplevel, search_box):
    text_area.tag_remove('match', '1.0', END)
    matches_found = 0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = text_area.search(needle, start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{} + {}c'.format(start_pos, len(needle))
            text_area.tag_add('match', start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        text_area.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))


# print a file

# def print_output():
#     # Get the text from the input text area
#     input_text = input_text_area.get("1.0", tk.END)
    
#     # Print the text in the output text area
#     output_text_area.insert(tk.END, input_text)

# Delete Selected Portion
    
def delete():
    global selected
    text_area.delete.index(selected)


def spell_check_text(event=None):
    # Get the current text in the text widget
    text = text_area.get("1.0", END)
    
    # Create a dictionary object
    dictionary = enchant.Dict("en_US")
    
    # Remove existing tags
    text_area.tag_remove("incorrect", "1.0", END)
    
    # Get all words in the text, excluding special characters
    words = re.findall(r'\b[A-Za-z]+\b', text)

    
    # Iterate over each word and check spelling
    for word in words:
        if not dictionary.check(word):
            start_index = "1.0"
            while True:
                start_index = text_area.search(word, start_index, END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(word)}c"
                text_area.tag_add("incorrect", start_index, end_index)
                start_index = end_index
    
    # Configure a tag to underline incorrect words with red color
    text_area.tag_config("incorrect", underline=True, foreground="red")


# Variable to track if voice input is active
voice_input_active = False

# Function to handle voice input
def handle_voice_input():
    global voice_input_active
    voice_input_active = True
    recognizer = sr.Recognizer()
    while voice_input_active:
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                text_area.insert("end-1c", text)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error fetching results; {0}".format(e))

# Start voice input in a separate thread
def start_voice_input():
    global voice_input_active
    if not voice_input_active:
        voice_input_active = True
        threading.Thread(target=handle_voice_input).start()

# Stop voice input
def stop_voice_input():
    global voice_input_active
    voice_input_active = False


# Function to convert text to speech
def text_to_speech():
    text = text_area.get("1.0", END)
    tts = gTTS(text=text, lang='en')
    tts.save("text_to_speech.mp3")
    os.system("start text_to_speech.mp3")

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create File menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_command(label="Print", command=print)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Create Edit Menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=text_area.edit_undo, accelerator="Ctrl+z")
edit_menu.add_command(label="Cut", command=lambda: cut_text(), accelerator="Ctrl+x")
edit_menu.add_command(label="Copy", command=lambda: copy_text(), accelerator="Ctrl+c")
edit_menu.add_command(label="Paste", command=lambda: paste_text(), accelerator="Ctrl+v")
edit_menu.add_command(label="Redo", command=text_area.edit_redo, accelerator="Ctrl+y")
edit_menu.add_command(label="Delete", command=delete)

# Status bar at the bottom
status_bar = Label(root, text='Ready', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# edit Bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

# create button

bold_button = Button(toolbar_frame, text="Bold", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=5)

italics_button = Button(toolbar_frame, text="Italics", command=italic_it)
italics_button.grid(row=0, column=1, sticky=W, padx=5)

underline_button = Button(toolbar_frame, text="Underline", command=underline_it)
underline_button.grid(row=0, column=2, sticky=W, padx=5)

find_button = Button(toolbar_frame, text="Find", command=find_text)
find_button.grid(row=0, column=3, sticky=W, padx=5)

# Button to trigger voice input
voice_input_button = Button(toolbar_frame, text="Start Voice Input", command=start_voice_input)
voice_input_button.grid(row=0, column=4, sticky=W, padx=5)

# Button to trigger voice input
voice_input_button = Button(toolbar_frame, text="Stop Voice Input", command=stop_voice_input)
voice_input_button.grid(row=0, column=5, sticky=W, padx=5)

# # Button to trigger voice input
voice_input_button = Button(toolbar_frame, text="Text to Speech", command=text_to_speech)
voice_input_button.grid(row=0, column=6, sticky=W, padx=5)

# Bind the spell_check_text function to the KeyRelease event
text_area.bind("<KeyRelease>", spell_check_text)


root.mainloop()
