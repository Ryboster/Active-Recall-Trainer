from tkinter import *
import csv
import tkinter

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import random

# -------------------------------------------------- Function: strVarSet
# Forms dictionary of keywords
def strVarSet(keys, values):
    y = 0 # y = dict's index
    vars = {}
    print('VALUES: ', values)
    # Values is a list of dicts (['{words:meanings}', '{words:meanings}'])'. The dicts are kept as strings
    # eval() method is used to convert the strings to dicts. See dictExtract()
    for item in values:
        # Eval transforms the string dicts into real dicts
        x = eval(item)
        for xtem in x:
            # Forming a numbered dict of meanings
            y = y + 1
            vars[y] = x[xtem]
    y = 0
    keydict = {}
    for key in keys:
        y += 1
        # Forming a numbered dict of keywords
        keydict[y] = key
    print('strvarset: ', keydict)
    # Returning a numbered dict of keywords and a numbered dict of meanings
    return vars, keydict


# -------------------------------------------------- Function: DictExtract
def dictExtract():
    with open("dir/dess.txt", "r") as y:
        x = y.readlines(); d = str(x)
        Dict = eval(d)
    l = []
    for item in Dict:
        print("first print -----\n", item)
        x = eval(item)
        for key in x:
            l.append(key)
    y = 0; d = {}
    for word in l:
        y += 1
        d[y] = word
    print("\ndictExtract() returning: \n", d, "\n", Dict)
    return l, Dict, d




with open("dir/word_list.csv", "r") as word_list:
    word_list = csv.reader(word_list)
    count1 = 0
    for row in word_list:
        count1 = count1 + 1
        row = str(row).strip("[").strip("]").strip("\'")
        print(row)

def wordUnload():
    x=[]
    with open("dir/word_list.csv", "r") as y:
        reader = csv.reader(y)
        for read in reader:
            f = str(read)
            f = f.strip("[").strip("]").strip("\'")
            print(f)
            x.append(f)
    print(x)
    return x

unloadedw = wordUnload()


class Scrollable(Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """
    def __init__(self, frame, width=16):

        scrollbar = Scrollbar(frame, width=width)
        scrollbar.pack(side=RIGHT, fill=Y, expand=True)

        self.canvas = Canvas(frame, yscrollcommand=scrollbar.set, height=540, width=440)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0, 0, window=self, anchor=NW)
    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width=canvas_width)
    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))


class Window:

    def __init__(self, page):
        self.window = Tk()
        self.window.title('A.R.T')
        page = IntVar(master=self.window, value=page)
        # -------------------------------------------------- Initial Extraction
        self.l, self.keys, self.d = dictExtract()
        self.count = 0
        # -------------------------------------------------- WORD Label
        try:
            self.bar1 = tkinter.StringVar(self.window, str(self.d[page.get()]).capitalize())
            self.wrd1 = Label(self.window, textvariable=self.bar1, font="helvetica 11 underline")
            self.wrd1.grid(row=0, column=3)
        except KeyError:
            print("Word label out of index on startup")


        # --------------------------------------------------- Get Index of the current word
        def get_current_index():
            l, s, d = dictExtract()
            vars, keydict = strVarSet(l, s)
            print('bar1 print', self.bar1.get())
            keys = [k for k, v in keydict.items() if self.bar1.get() in str(v).capitalize()]
            print("Keydict items: ", keydict.items())
            print("KEYS:", keys, len(keys))
            x = str(keys).strip('[').strip(']'.strip('\'').strip("\'"))
            print('XXXXXXXXXXXXXX\n', x, '\n', type(x), self.bar1.get())
            x = int(x)
            return x

        def add_new_word(text, kind):
            # Instantiating the popup
            self.top = Toplevel(self.window)
            self.top.geometry('520x340')
            self.top.title('New word')
            self.canvas = Canvas(self.top, width=460, height=340); self.canvas.pack()
            self.frame = Frame(self.canvas); self.frame.pack()
            scrollable_frame = Scrollable(self.frame, width=16)
            label = Label(scrollable_frame, text=text)

            def enable_or_disable_scraping():
                ''' Scraping the word's meanings'''
                if scrape_radio_value.get() == 1:
                    desc_entry1.grid_forget(); pos_label.grid_forget()
                    desc_entry2.grid_forget(); desc_label1.grid_forget()
                    desc_entry3.grid_forget(); desc_label2.grid_forget()
                    desc_entry4.grid_forget(); desc_label3.grid_forget()
                    desc_entry5.grid_forget(); desc_label4.grid_forget()
                    desc_entry6.grid_forget(); desc_label5.grid_forget()
                    desc_entry7.grid_forget(); desc_label6.grid_forget()
                    desc_entry8.grid_forget(); desc_label7.grid_forget()
                    desc_entry9.grid_forget(); desc_label8.grid_forget()
                    submit_button.configure(command=lambda: self.scraper(user_input_word.get()))
                    print('user_input_word:', user_input_word.get())
                    print('word_entry:', word_entry.get())
                elif scrape_radio_value.get() == 0:
                    '''Manual word addition'''
                    #word_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry1.grid(row=2, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry2.grid(row=3, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry3.grid(row=4, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry4.grid(row=5, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry5.grid(row=6, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry6.grid(row=7, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry7.grid(row=8, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry8.grid(row=9, column=0, columnspan=2, pady=5, padx=(10, 0))
                    desc_entry9.grid(row=10, column=0, columnspan=2, pady=5, padx=(10, 0))
                    pos_label.grid(row=2, column=3, pady=5)
                    desc_label1.grid(row=3, column=3, pady=5)
                    desc_label2.grid(row=4, column=3, pady=5)
                    desc_label3.grid(row=5, column=3, pady=5)
                    desc_label4.grid(row=6, column=3, pady=5)
                    desc_label5.grid(row=7, column=3, pady=5)
                    desc_label6.grid(row=8, column=3, pady=5)
                    desc_label7.grid(row=9, column=3, pady=5)
                    desc_label8.grid(row=10, column=3, pady=5)
                    submit_button.configure(command=lambda: submit())

            scrape_radio_value = IntVar()
            manual_radio_button = Radiobutton(scrollable_frame, text='Manual', variable=scrape_radio_value, value=0, command=lambda: enable_or_disable_scraping())
            scrape_radio_button = Radiobutton(scrollable_frame, text='Automatic', variable=scrape_radio_value, value=1, command=lambda: enable_or_disable_scraping())
            manual_radio_button.grid(row=11, column=0)
            scrape_radio_button.grid(row=11, column=1)
            label.grid(row=0, column=0, columnspan=2)

            user_input_word = StringVar()
            user_input_desc1 = StringVar()

            word_entry = Entry(scrollable_frame, width=25, textvariable=user_input_word)
            if kind == 'word':
                desc_entry1 = Entry(scrollable_frame, width=40, textvariable=user_input_desc1)
                desc_entry1.grid(row=2, column=0, columnspan=2, pady=5, padx=(10, 0))
                pos_label = Label(scrollable_frame, text='part of speech')
            desc_entry2 = Text(scrollable_frame, width=40, height=3)
            desc_entry3 = Text(scrollable_frame, width=40, height=3)
            desc_entry4 = Text(scrollable_frame, width=40, height=3)
            desc_entry5 = Text(scrollable_frame, width=40, height=3)
            desc_entry6 = Text(scrollable_frame, width=40, height=3)
            desc_entry7 = Text(scrollable_frame, width=40, height=3)
            desc_entry8 = Text(scrollable_frame, width=40, height=3)
            desc_entry9 = Text(scrollable_frame, width=40, height=3)

            word_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry2.grid(row=3, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry3.grid(row=4, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry4.grid(row=5, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry5.grid(row=6, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry6.grid(row=7, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry7.grid(row=8, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry8.grid(row=9, column=0, columnspan=2, pady=5, padx=(10, 0))
            desc_entry9.grid(row=10, column=0, columnspan=2, pady=5, padx=(10, 0))

            desc_label1 = Label(scrollable_frame, text='description1')
            desc_label2 = Label(scrollable_frame, text='description2')
            desc_label3 = Label(scrollable_frame, text='description3')
            desc_label4 = Label(scrollable_frame, text='description4')
            desc_label5 = Label(scrollable_frame, text='description5')
            desc_label6 = Label(scrollable_frame, text='description6')
            desc_label7 = Label(scrollable_frame, text='description7')
            desc_label8 = Label(scrollable_frame, text='description8')

            desc_label1.grid(row=3, column=3, pady=5)
            desc_label2.grid(row=4, column=3, pady=5)
            desc_label3.grid(row=5, column=3, pady=5)
            desc_label4.grid(row=6, column=3, pady=5)
            desc_label5.grid(row=7, column=3, pady=5)
            desc_label6.grid(row=8, column=3, pady=5)
            desc_label7.grid(row=9, column=3, pady=5)
            desc_label8.grid(row=10, column=3, pady=5)

            def submit():
                f = []
                word = user_input_word.get()
                pos = user_input_desc1.get()
                desc1 = desc_entry2.get(1.0, END)
                desc2 = desc_entry3.get(1.0, END)
                desc3 = desc_entry4.get(1.0, END)
                desc4 = desc_entry5.get(1.0, END)
                desc5 = desc_entry6.get(1.0, END)
                desc6 = desc_entry7.get(1.0, END)
                desc7 = desc_entry8.get(1.0, END)
                desc8 = desc_entry9.get(1.0, END)

                if pos != '':
                    f.append(pos); print(f'{pos} appended!')
                if desc1 != '' or desc1 != '\n':
                    f.append(desc1); print(f'{desc1} appended!')
                if desc2 != '' or desc2 != '\n':
                    f.append(desc2); print(f'{desc2} appended!')
                if desc3 != '' or desc3 != '\n':
                    f.append(desc3); print(f'{desc3} appended!')
                if desc4 != '' or desc4 != '\n':
                    f.append(desc4); print(f'{desc4} appended!')
                if desc5 != '' or desc5 != '\n':
                    f.append(desc5); print(f'{desc5} appended!')
                if desc6 != '' or desc6 != '\n':
                    f.append(desc6); print(f'{desc6} appended!')
                if desc7 != '' or desc7 != '\n':
                    f.append(desc7); print(f'{desc7} appended!')
                if desc8 != '' or desc8 != '\n':
                    f.append(desc8); print(f'{desc8} appended!')
                f = [item.strip() for item in f]
                f = [item.replace('\n', '') for item in f]
                f = [item for item in f if item != '']

                print('list: ', f)
                if kind == 'word':
                    if word != '':
                        with open("dir/word_list.csv", "a") as y:
                            writer = csv.writer(y)
                            writer.writerow([word])
                    else:
                        print('no word was submitted ...')
                    save_me = {word: f}
                    if word != '':
                        with open('dir/dess.txt', "a") as x:
                            save_me = str(save_me)
                            x.write(save_me + "\n")
                            print(f'successfully saved the following word pair:\n{save_me}')
                    else:
                        print('Exited without adding new word')
                    self.top.destroy()
                elif kind == "idiom":
                    if word != '':
                        save_me = {word:f}
                        with open('dir/idioms.txt', "a") as x:
                            save_me = str(save_me)
                            x.write(save_me + '\n')
                            print(f'successfully saved the following idiom pair:\n{save_me}')
                        self.top.destroy()


            submit_button = Button(scrollable_frame, text='Confirm', command=lambda: submit())
            submit_button.grid(row=11, column=3, pady=10)
            scrollable_frame.update()


        i = get_current_index()
        x = IntVar(self.window); x.set(i)
        self.index_label = Label(self.window, textvariable=x)
        self.index_label.grid(row=0, column=5)
        self.index, self.vars, self.descs = self.Current(x.get())
        self.indexlist = []
        self.findind = 0
        for key in self.vars.keys():
            self.indexlist.append(key)

        # -------------------------------------------------- Button: Add New Word
        self.NewWordButton = Button(self.window, text="+", command=lambda: add_new_word('Enter new word', "word"))
        self.NewWordButton.grid(row=0, column=1)
        # -------------------------------------------------- Button: Add new Idiom
        self.new_idiom_button = Button(self.window, text='+', command=lambda: add_new_word('Enter new idiom', "idiom"))
        self.new_idiom_button.grid(row=1, column=1)
        # -------------------------------------------------- Button: Idioms
        self.idioms_button = Button(self.window, text='Idioms', command=lambda: self.idioms_button_function())
        self.idioms_button.grid(row=1, column=0)
        # -------------------------------------------------- Button: Random
        self.random_button = Button (self.window, text='Random', command=lambda: print(random.randint(1, 30000)))
        self.random_button.grid(row=2, column=0)
        # -------------------------------------------------- Button: Settings
        self.settings_button = Button(self.window, text='Settings', command=lambda: print('settings innit'))
        self.settings_button.grid(row=3, column=0)
        # -------------------------------------------------- Button: Exit
        self.exit_button = Button(self.window, text='Quit', command=lambda: self.window.quit())
        self.exit_button.grid(row=4, column=0)
# -------------------------------------------------- Button: Load Words
        self.WordsButton = Button(self.window, text="Words", command=lambda: self.words_button(wordUnload()))
        self.WordsButton.grid(row=0, column=0)
# -------------------------------------------------- Button: Next
        self.NextButton = Button(self.window, text=">", command=lambda: self.Next(x))
        self.NextButton.grid(row=0, column=99)
# -------------------------------------------------- Button: Previous
        self.PreviousButton = Button(self.window, text="<", command=lambda: self.Previous(x))
        self.PreviousButton.grid(row=0, column=2)

        try:  # --------------------------------------------- Description Label 1
            self.var1 = tkinter.StringVar(self.window, str(self.descs[1]))
            self.dsc1 = Label(self.window, textvariable=self.var1,
                              font="Helvetica 9 italic", anchor="w", justify=LEFT, pady=5)
            self.dsc1.grid(row=1, column=3, pady=5, sticky="W")
        except KeyError:
            print("Description out of index in Label 1")
        try:  # --------------------------------------------- Description Label 2
            self.var2 = tkinter.StringVar(self.window, str(self.descs[2]))
            self.dsc2 = Label(self.window, textvariable=self.var2, anchor="w", justify=LEFT, pady=5)
            self.dsc2.grid(row=2, column=3, pady=1, sticky="W")
        except KeyError:
            self.var2 = tkinter.StringVar(self.window, '')
            self.dsc2 = Label(self.window, textvariable=self.var2, anchor="w", justify=LEFT, pady=5)
            self.dsc2.grid(row=2, column=3, pady=1, sticky="W")
            print("Description out of index in Label 2")
        try:  # --------------------------------------------- Description Label 3
            self.var3 = tkinter.StringVar(self.window, str(self.descs[3]))
            self.dsc3 = Label(self.window, textvariable=self.var3, anchor="w", justify=LEFT, pady=5)
            self.dsc3.grid(row=3, column=3, pady=1, sticky="W")
        except KeyError:
            self.var3 = tkinter.StringVar(self.window, '')
            self.dsc3 = Label(self.window, textvariable=self.var3, anchor="w", justify=LEFT, pady=5)
            self.dsc3.grid(row=3, column=3, pady=1, sticky="W")
            print("Description out of index in Label 3")
        try:  # --------------------------------------------- Description Label 4
            self.var4 = tkinter.StringVar(self.window, str(self.descs[4]))
            self.dsc4 = Label(self.window, textvariable=self.var4, anchor="w", justify=LEFT)
            self.dsc4.grid(row=4, column=3, pady=1, sticky="W")
        except KeyError:
            self.var4 = tkinter.StringVar(self.window, None)
            self.dsc4 = Label(self.window, textvariable=self.var4, anchor="w", justify=LEFT)
            self.dsc4.grid(row=4, column=3, pady=1, sticky="W")
            print("Description out of index in Label 4")
        try:  # --------------------------------------------- Description Label 5
            self.var5 = tkinter.StringVar(self.window, str(self.descs[5]))
            self.dsc5 = Label(self.window, textvariable=self.var5, anchor="w", justify=LEFT)
            self.dsc5.grid(row=5, column=3, pady=1, sticky="W")
        except KeyError:
            self.var5 = tkinter.StringVar(self.window, None)
            self.dsc5 = Label(self.window, textvariable=self.var5, anchor="w", justify=LEFT)
            self.dsc5.grid(row=5, column=3, pady=1, sticky="W")
            print("Description out of index in Label 5")
        try:  # --------------------------------------------- Description Label 6
            self.var6 = tkinter.StringVar(self.window, str(self.descs[6]))
            self.dsc6 = Label(self.window, textvariable=self.var6, anchor="w", justify=LEFT)
            self.dsc6.grid(row=6, column=3, pady=1, sticky="W")
        except KeyError:
            self.var6 = tkinter.StringVar(self.window, '')
            self.dsc6 = Label(self.window, textvariable=self.var6, anchor="w", justify=LEFT)
            self.dsc6.grid(row=6, column=3, pady=1, sticky="W")
            print("Description out of index in Label 6")
        try:  # --------------------------------------------- Description Label 7
            self.var7 = tkinter.StringVar(self.window, str(self.descs[7]))
            self.dsc7 = Label(self.window, textvariable=self.var7, anchor="w", justify=LEFT)
            self.dsc7.grid(row=7, column=3, pady=1, sticky="W")
        except KeyError:
            self.var7 = tkinter.StringVar(self.window, '')
            self.dsc7 = Label(self.window, textvariable=self.var7, anchor="w", justify=LEFT)
            self.dsc7.grid(row=7, column=3, pady=1, sticky="W")
            print("Description out of index in Label 7")

        try:  # --------------------------------------------- Description Label 8
            self.var8 = tkinter.StringVar(self.window, str(self.descs[8]))
            self.dsc8 = Label(self.window, textvariable=self.var8, anchor="w", justify=LEFT)
            self.dsc8.grid(row=8, column=3, sticky="W")
        except KeyError:
            self.var8 = tkinter.StringVar(self.window, '')
            self.dsc8 = Label(self.window, textvariable=self.var8, anchor="w", justify=LEFT)
            self.dsc8.grid(row=8, column=3, sticky="W")
            print("Description out of index in Label 8")
        try:  # --------------------------------------------- Description Label 9
            self.var9 = tkinter.StringVar(self.window, str(self.descs[9]))
            self.dsc9 = Label(self.window, textvariable=self.var9, anchor="w", justify=LEFT)
            self.dsc9.grid(row=9, column=3, sticky="W")
        except KeyError:
            self.var9 = tkinter.StringVar(self.window, '')
            self.dsc9 = Label(self.window, textvariable=self.var9, anchor="w", justify=LEFT)
            self.dsc9.grid(row=9, column=3, sticky="W")
            print("Description out of index in Label 9")
        try:  # --------------------------------------------- Description Label 10
            self.var10 = tkinter.StringVar(self.window, str(self.descs[10]))
            self.dsc10 = Label(self.window, textvariable=self.var10, anchor="w", justify=LEFT)
            self.dsc10.grid(row=10, column=3, sticky="W")
        except KeyError:
            print("Description out of index in Label 10")
            self.var10 = tkinter.StringVar(self.window, '')
            self.dsc10 = Label(self.window, textvariable=self.var10, anchor="w", justify=LEFT)
            self.dsc10.grid(row=10, column=3, sticky="W")
        finally:
            self.Previous(x) # this is here just to hide unused labels
            get_current_index()



        self.loadword1 = tkinter.StringVar(self.window)

        self.window.mainloop()
    #def GetIndex(self):

    # -------------------------------------------------- Function: DictExtract
    def dictExtract(self):
        with open("dir/dess.txt", "r") as y:
            x = y.readlines(); d = str(x)
            list_of_dicts = eval(d)
        l = []
        for dictionary in list_of_dicts:
            # Dictionaries come as strings, x transforms them into dicts
            x = eval(dictionary)
            for key in x:
                # Appending each dictionaries' key onto a list
                l.append(key)
        y = 0; numbered_dict = {}
        for word in l:
            y += 1
            numbered_dict[y] = word
        print("\ndictExtract()\nreturning\n", d, "\n", list_of_dicts)
        return l, list_of_dicts, numbered_dict


    def wrap_by_word(self, s, n):
        # Returns a string where \\n is inserted between every n words
        a = s.split()
        ret = ''
        for i in range(0, len(a), n):
            ret += ' '.join(a[i:i + n]) + '\n'

        return ret
        # -------------------------------------------------- Function: Current
    def Current(self, index):
        print(f"index-------------\n{index}\n-------------")
        # l = list of words (amiable, avert etc.)
        # keys = list of dicts (words:meanings)
        # d = numbered dict of words (1: amiable etc.)
        l, keys, d = dictExtract()
        print(f'l\'s value: {l}\nkeys\' value: {keys}\nd\'s value: {d}')
        vars, momo = strVarSet(l, keys)
        print(f'vars:', vars, 'momo:', momo)
        count = 0  # separate integer keys for descriptions
        descriptions_dict = {}  # dict
        # for values in DictList[index]
        for f in vars[index]:
            count = count + 1 # separate integer keys from descriptions
            f = self.wrap_by_word(f, 15)
            f = f.rstrip('\n')
            descriptions_dict[count] = f  # Extracting descriptions for Labels
        print("Current returning descriptions_dict: \n\n", descriptions_dict)

        # ---------------------------------------------------------------------- Updating labels
        # Labels should automatically disappear off grid if they don't contain any text.
        # Otherwise empty labels take up space
        # ------------------------------------- Updating label 1: self.dsc1
        try:
            if descriptions_dict[1] != '':
                try:
                    try:
                        self.dsc1.grid(row=1, column=3, pady=5, sticky="W"); print('self.dsc1 re-gridded!')
                    except TclError:
                        print('dsc1 remains gridded!')
                    self.bar1.set(d[index].capitalize())
                    self.var1.set(descriptions_dict[1])
                except AttributeError:
                    print("failed to update descs 1")
                except KeyError:
                    self.var1.set('')
            elif descriptions_dict[1] is '':
                print('forgetting self.dsc1 ...')
                self.dsc1.grid_forget()
        except KeyError:
            print('descriptions_dict[1] doesn\'t exist')
            try:
                self.dsc1.grid_forget()
                print('forgetting self.dsc1 ...')
            except AttributeError:
                print('self.dsc1 does not exist')
        # ------------------------------------- Updating label 2: self.dsc2
        try:
            if descriptions_dict[2] != '':
                try:
                    try:
                        self.dsc2.grid(row=2, column=3, pady=1, sticky="W"); print('self.dsc2 re-gridded!')
                    except TclError:
                        print('dsc2 remains gridded!')
                    self.var2.set(descriptions_dict[2])
                except AttributeError:
                    print('failed to update descs 2')
                except KeyError:
                    self.var2.set('')
            elif descriptions_dict[2] is '':
                print('forgetting self.dsc2 ...')
                self.dsc2.grid_forget()
        except KeyError:
            print('descriptions_dict[2] doesn\'t exist')
            try:
                self.dsc2.grid_forget()
                print('forgetting self.dsc2 ...')
            except AttributeError:
                print('self.dsc2 does not exist')
        # ------------------------------------- Updating label 3: self.dsc3
        try:
            if descriptions_dict[3] != '':
                try:
                    try:
                        self.dsc3.grid(row=3, column=3, pady=1, sticky="W"); print('self.dsc3 re-gridded!')
                    except TclError:
                        print('dsc3 remains gridded!')
                    self.var3.set(descriptions_dict[3])
                except AttributeError:
                    print('failed to update descs 3')
                except KeyError:
                    self.var3.set('')
            elif descriptions_dict[3] is '':
                print('forgetting self.dsc3 ...')
                self.dsc3.grid_forget()
        except KeyError:
            print('descriptions_dict[3] doesn\'t exist')
            try:
                self.dsc3.grid_forget()
                print('forgetting self.dsc3 ...')
            except AttributeError:
                print('self.dsc3 does not exist')
        # ------------------------------------- Updating label 4: self.dsc4
        try:
            if descriptions_dict[4] != '':
                try:
                    try:
                        self.dsc4.grid(row=4, column=3, pady=1, sticky="W"); print('self.dsc4 re-gridded!')
                    except TclError:
                        print('self.dsc4 remains gridded!')
                    self.var4.set(descriptions_dict[4])
                except AttributeError:
                    print('failed to update descs 4')
                except KeyError:
                    self.var4.set('')
            elif descriptions_dict[4] is '' or descriptions_dict[4] is None:
                print('forgetting self.dsc4 ...')
                self.dsc4.grid_forget()
        except KeyError:
            print('descriptions_dict[4] doesn\'t exist')
            try:
                self.dsc4.grid_forget()
                print('forgetting self.dsc4 ...')
            except AttributeError:
                print('self.dsc4 does not exist')
        # ------------------------------------- Updating label 5: self.dsc5
        try:
            if descriptions_dict[5] != '':
                try:
                    try:
                        self.dsc5.grid(row=5, column=3, pady=1, sticky="W"); print('self.dsc5 re-gridded!')
                    except TclError:
                        print('self.dsc5 remains gridded!')
                    self.var5.set(descriptions_dict[5])
                except AttributeError:
                    print('failed to update descs 5')
                except KeyError:
                    self.var5.set('')
            elif descriptions_dict[5] is '' or descriptions_dict[5] is None:
                print('forgetting self.dsc5 ...')
                self.dsc5.grid_forget()
        except KeyError:
            print('descriptions_dict[5] doesn\'t exist')
            try:
                self.dsc5.grid_forget()
                print('forgetting self.dsc5 ...')
            except AttributeError:
                print('self.dsc5 does not exist')
        # ------------------------------------- Updating label 6: self.dsc6
        try:
            if descriptions_dict[6] != '':
                try:
                    try:
                        self.dsc6.grid(row=6, column=3, pady=1, sticky="W"); print('self.dsc6 re-gridded!')
                    except TclError:
                        print('self.dsc6 remains gridded!')
                    self.var6.set(descriptions_dict[6])
                except AttributeError:
                    print('failed to update self.dsc6')
                except KeyError:
                    self.var6.set('')
            elif descriptions_dict[6] is '' or descriptions_dict[6] is None:
                print('forgetting self.dsc6 ...')
                self.dsc6.grid_forget()
        except KeyError:
            print('descriptions_dict[6] doesn\'t exist')
            try:
                self.dsc6.grid_forget()
                print('forgetting self.dsc6 ...')
            except AttributeError:
                print('self.dsc6 does not exist')
        # ------------------------------------- Updating label 7: self.dsc7
        try:
            if descriptions_dict[7] != '':
                try:
                    try:
                        self.dsc7.grid(row=7, column=3, pady=1, sticky="W"); print('self.dsc7 re-gridded!')
                    except TclError:
                        print('self.dsc7 remains gridded!')
                    self.var7.set(descriptions_dict[7])
                except AttributeError:
                    print('failed to update self.dsc7')
                except KeyError:
                    self.var7.set('')
            elif descriptions_dict[7] is '' or descriptions_dict[7] is None:
                print('forgetting self.dsc7 ...')
                self.dsc7.grid_forget()
        except KeyError:
            print('descriptions_dict[7] doesn\'t exist')
            try:
                self.dsc7.grid_forget()
                print('forgetting self.dsc7 ...')
            except AttributeError:
                print('self.dsc7 does not exist')
        # ------------------------------------- Updating label 8: self.dsc8
        try:
            if descriptions_dict[8] != '':
                try:
                    try:
                        self.dsc8.grid(row=8, column=3, pady=1, sticky="W"); print('self.dsc8 re-gridded!')
                    except TclError:
                        print('self.dsc8 remains gridded!')
                    self.var8.set(descriptions_dict[8])
                except AttributeError:
                    print('failed to update self.dsc8')
                except KeyError:
                    self.var8.set('')
            elif descriptions_dict[8] is '' or descriptions_dict[8] is None:
                print('forgetting self.dsc8 ...')
                self.dsc8.grid_forget()
        except KeyError:
            print('descriptions_dict[8] doesn\'t exist')
            try:
                self.dsc8.grid_forget()
                print('forgetting self.dsc8 ...')
            except AttributeError:
                print('self.dsc8 does not exist')
        # ------------------------------------- Updating label 9: self.dsc9
        try:
            if descriptions_dict[9] != '':
                try:
                    try:
                        self.dsc9.grid(row=9, column=3, pady=1, sticky="W"); print('self.dsc9 re-gridded!')
                    except TclError:
                        print('self.dsc9 remains gridded!')
                    self.var9.set(descriptions_dict[9])
                except AttributeError:
                    print('failed to update self.dsc9')
                except KeyError:
                    self.var9.set('')
            elif descriptions_dict[9] is '' or descriptions_dict[9] is None:
                print('forgetting self.dsc9 ...')
                self.dsc9.grid_forget()
        except KeyError:
            print('descriptions_dict[9] doesn\'t exist')
            try:
                self.dsc9.grid_forget()
                print('forgetting self.dsc9 ...')
            except AttributeError:
                print('self.dsc9 does not exist')
        # ------------------------------------- Updating label 10: self.dsc10
        try:
            if descriptions_dict[10] != '':
                try:
                    try:
                        self.dsc10.grid(row=10, column=3, pady=1, sticky="W"); print('self.dsc10 re-gridded!')
                    except TclError:
                        print('self.dsc10 remains gridded!')
                    self.var10.set(descriptions_dict[10])
                except AttributeError:
                    print('failed to update self.dsc10')
                except KeyError:
                    self.var10.set('')
            elif descriptions_dict[10] is '' or descriptions_dict[10] is None:
                print('forgetting self.dsc10 ...')
                self.dsc10.grid_forget()
        except KeyError:
            print('descriptions_dict[10] doesn\'t exist')
            try:
                self.dsc10.grid_forget()
                print('forgetting self.dsc10 ...')
            except AttributeError:
                print('self.dsc10 does not exist')

        return index, vars, descriptions_dict

    def delete_word(self, word, kind):
        if kind == 'word':
            l, s, d = dictExtract()
            numbered_descs, numbered_words = strVarSet(l, s)
            all_items = self.words_list.get(0, END) # Get all positions on list
            selection = self.words_list.curselection() # Returns a tuple of coordinates relating to selection (somehow)
            selected_word = [all_items[item] for item in selection] # Finds selected word
            selected_word = str(selected_word).strip('[').strip('\'').strip(']').strip('\'')
            list1 = []
            # Iterate over keys of numbered_words dict (numbers)
            for number in list(numbered_words):
                # Finds selected index
                if numbered_words[number] == selected_word:
                    numbered_words.pop(number)
                    numbered_descs.pop(number)
                    y = 0
                    new_numbered_words = {}
                    new_numbered_descs = {}

                    for key in dict(numbered_words):
                        y += 1
                        new_numbered_descs[y] = numbered_descs[key]
                        new_numbered_words[y] = numbered_words[key]

                    for key in new_numbered_words:
                        list1.append({new_numbered_words[key]:new_numbered_descs[key]})
                    z = open('dir/dess.txt', "r+")
                    z.truncate()
                    z.close(); del z
                    with open('dir/dess.txt', "a") as x:
                        final_list = []
                        for item in list1:
                            item = str(item) + '\n'
                            x.write(str(item))
                    z = open('dir/word_list.csv', "w+")
                    z.close()
                    final_list = []
                    for key in new_numbered_words:
                        final_list.append(new_numbered_words[key])
                    with open('dir/word_list.csv', "w") as x:
                        writer = csv.writer(x)
                        for item in final_list:
                            writer.writerow([item])
                    self.words_list.delete(0, END)
                    words = wordUnload(); y = 0
                    for word in words:
                        y += 1
                        self.words_list.insert(y, word)

        elif kind == 'idiom':
            list_of_keys = []; new_dict = {}
            with open('dir/idioms.txt', "r") as x:
                dicts = x.readlines(); dicts = list(dicts)
                #print('dicts:', dicts)
            for dictionary in dicts:
                #print('DICTIONARY PRINT', dictionary)
                x = eval(dictionary)
                #print('DICTIONARY PRINT', dictionary)
                for key in x:
                    if key not in new_dict:
                        new_dict[key] = []
                    str_dict = str(x[key]).rstrip(']').lstrip('[').replace('\\', "")
                    new_dict[key] = str_dict
                    print('appending to NEW_DICT', new_dict[key])
            new_dict.pop(word)
            truncee = open('dir/idioms.txt', "r+")
            truncee.truncate(); truncee.close()
            self.idioms_list.delete(0, END); i = 0
            with open('dir/idioms.txt', "a") as file:
                for key in new_dict:
                    print('new_dict(key):', new_dict[key])
                    print('new_dict by itself: ', new_dict)
                    i += 1
                    file.write(str({key:new_dict[key]}) + '\n')
                    self.idioms_list.insert(i, key)

            self.idioms_list.update()
            print('new_dict=', new_dict)

    def edit_window(self, word, kind):
        print('word:', word)
        print('kind:', kind)
        self.edit_top = Toplevel(self.window)
        self.edit_top.geometry('540x340')
        self.edit_top.title(f'Edit {kind}')
        self.edit_canvas = Canvas(self.edit_top, width=460, height=340); self.edit_canvas.pack()
        self.edit_frame = Frame(self.edit_canvas); self.edit_frame.pack()
        scrollable_frame = Scrollable(self.edit_frame, width=16)

        numbered_keys = {}; numbered_descriptions = {}; i = 0; list_of_descriptions = []
        if kind == 'idiom':
            with open('dir/idioms.txt', "r") as y:
                x = y.readlines(); d = str(x)
                list_of_dicts = eval(d)
            for dictionary in list_of_dicts:
                x = eval(dictionary)
                for key in x:
                    if key == word:
                        i += 1
                        list_of_descriptions = x.values()

        elif kind == 'word':
            with open('dir/dess.txt', "r") as y:
                x = y.readlines(); d = str(x)
                list_of_dicts = eval(d)
            for dictionary in list_of_dicts:
                x = eval(dictionary)
                for key in x:
                    i += 1
                    if key == word:
                        print('x key:', x[key])
                        values = x.values()
                        list_of_descriptions = list(x[key])
                        print('list_of_descriptions:', list_of_descriptions)

            string_vars = []; text_widgets = []; i = 2
            for description in list_of_descriptions:
                var = StringVar();var.set(description)
                string_vars.append(var)

                text = Text(scrollable_frame, width=40, height=3, state=NORMAL); text.grid(column=2, row=i)
                text.insert('1.0', var.get()); i += 1; text_widgets.append(text)

            def submit():
                new_descriptions = []

                for widget in text_widgets:
                    new_descriptions.append(widget.get(1.0, END))
                save_dict = {keyword_entry.get(): new_descriptions}
                self.delete_word(word)
                if kind == 'word':
                    with open('dir/dess.txt', "a") as x:
                        x.write(str(save_dict) + '\n')
                    with open('dir/word_list.csv', "a") as x:
                        writer = csv.writer(x)
                        writer.writerow([keyword_entry.get()])
                elif kind == "idiom":
                    with open('dir/idioms.txt', "a") as x:
                        x.write(str(save_dict))

                print(f'{kind} successfully edited! New entry:\n {save_dict}')
                self.words_list.insert(END, keyword_entry.get())
                self.edit_top.destroy()



        # keyword_strvar = StringVar(); keyword_strvar.set(word)
        keyword_entry = Entry(scrollable_frame)
        keyword_entry.insert(0, word); keyword_entry.grid(column=2, row=1)
        submit_button = Button(scrollable_frame, text='Save', command=lambda: submit()).grid(column=3, row=99)
        scrollable_frame.update()

    # -------------------------------------------------- Function: button_words
    def words_button(self, words):
        words_window = Toplevel(self.window)
        self.words_list = Listbox(words_window, selectmode=SINGLE, width=35)
        self.words_list.grid(row=1, column=1); y = 0
        print('words print: ', words)
        for word in words:
            y += 1
            self.words_list.insert(y, word)
        print(self.words_list.get(first=0))

        def selected_item():
            for i in self.words_list.curselection():
                return self.words_list.get(i)
        print('selected item:', selected_item())
        del_button = Button(words_window, text='Delete', command= lambda: self.delete_word(self.words_list.curselection(), 'word')).grid(row=3, column=2)
        edit_button = Button(words_window, text='Edit', command=lambda: self.edit_window(selected_item(), "word"))
        edit_button.grid(row=2, column=2)

    def idioms_button_function(self):
        l = []
        idioms_window = Toplevel(self.window)
        self.idioms_list = Listbox(idioms_window, selectmode=SINGLE, width=35)
        self.idioms_list.grid(row=1, column=1); y = 0
        with open('dir/idioms.txt', "r") as x:
            dicts = x.readlines()
            for dictionary in dicts:
                x = eval(dictionary)
                for key in x:
                    l.append(key)
        for idiom in l:
            y += 1
            self.idioms_list.insert(y, idiom)
        def selected_item():
            for i in self.idioms_list.curselection():
                return self.idioms_list.get(i)
        del_button = Button(idioms_window, text='Delete', command=lambda: self.delete_word(selected_item(), "idiom"))
        del_button.grid(row=3, column=2)
        edit_button = Button(idioms_window, text='Edit', command=lambda: self.edit_window(selected_item(), 'idiom'))
        edit_button.grid(row=2, column=2)


        print(l)
    #def current_selection(self):
    #    for i in self.words_list.curselection()



    def Next(self, index):
        index.set(index.get()+1)
        index, vars, descs = self.Current(index.get())
        print("Current index =", index)
        global keys
        return index

    def Previous(self, index):
        if index.get() >> 1:
            index.set(index.get()-1)
            self.Current(index.get())
        elif index.get() == 1:
            self.Current(index.get())
        return index

    def scraper(self, word):

        def skip():
            if word and l:
                new_dict = str({word:l})
                with open('dir/dess.txt', "a") as x:
                    x.write(new_dict + '\n')
                with open('dir/word_list.csv', "a") as x:
                    writer = csv.writer(x)
                    writer.writerow([word])
                driver.close()
                print(new_dict)
            elif word is None or word is "" and l is "" or l is None:
                print('No data scraped. Skipping saving process...')

        if " " in word:
            word = str(word).replace(' ', '--')
        else:
            word = str(word)
        options = FirefoxOptions()
        options.binary = '/home/pc/upwork/concre/firefox/firefox-esr'

        # Instantiating the browser
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        driver.get(f'https://www.dictionary.com/browse/{word}')

        # Wait until all scripts are loaded and find header tag
        driver.implicitly_wait(10)
        l = []

        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > button:nth-child(1)")))
            driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > button:nth-child(1)").click()
            try:
                part_of_speech = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
                l.append(part_of_speech.text)
                try:
                    desc_element1 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
                    l.append(desc_element1.text); print('appended desc_element1')
                except NoSuchElementException:
                    print('desc_element1 not found'); skip(); return
                try:
                    desc_element2 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")
                    l.append(desc_element2.text); print('appended desc_element2')
                except NoSuchElementException:
                    print('desc_element2 not found'); skip(); return
                try:
                    desc_element3 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
                    l.append(desc_element3.text); print('appended desc_element3')
                except NoSuchElementException:
                    print('desc_element3 not found'); skip(); return
                try:
                    desc_element4 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
                    l.append(desc_element4.text); print('appended desc_element4')
                except NoSuchElementException:
                    print('desc_element4 not found'); skip(); return
                try:
                    desc_element5 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)")
                    l.append(desc_element5.text); print('appended desc_element5')
                except NoSuchElementException:
                    print('desc_element5 not found'); skip(); return
                try:
                    desc_element6 = driver.find_element(By.CSS_SELECTOR, "div.css-1mxqyc7:nth-child(3) > span:nth-child(1)")
                    l.append(desc_element6.text); print('appended desc_element6')
                except NoSuchElementException:
                    print('desc_element6 not found'); skip(); return
                try:
                    desc_element7 = driver.find_element(By.CSS_SELECTOR, "div.css-xuav9x:nth-child(4)")
                    l.append(desc_element7.text); print('appended desc_element7')
                except NoSuchElementException:
                    print('desc_element7 not found'); skip(); return
                try:
                    desc_element8 = driver.find_element(By.CSS_SELECTOR, "div.css-wdmbsg:nth-child(5)")
                    l.append(desc_element8.text); print('appended desc_element8')
                except NoSuchElementException:
                    print('desc_element8 not found'); skip(); return
                try:
                    desc_element9 = driver.find_element(By.CSS_SELECTOR, "div.css-gud428:nth-child(6)")
                    l.append(desc_element9.text); print('appended desc_element9')
                except NoSuchElementException:
                    print('desc_element9 not found'); skip(); return
                print(l)
            except NoSuchElementException:
                print('No description or part of speech found. Check your keyword for misspellings')
                skip(); return
        except selenium.common.exceptions.TimeoutException:
            print('see_more does not exist')
            part_of_speech = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
            l.append(part_of_speech.text)
            try:
                desc_element1 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
                l.append(desc_element1.text); print('appended desc_element1:', desc_element1.text)
            except NoSuchElementException:
                try:
                    desc_element1 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1)")
                    l.append(desc_element1.text); print('appended desc_element1:', desc_element1.text)
                except NoSuchElementException:
                    print('desc_element1 not found'); skip(); return
            try:
                desc_element2 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")
                l.append(desc_element2.text); print('appended desc_element2:', desc_element2.text)
            except NoSuchElementException:
                try:
                    desc_element2 = driver.find_element(By.CSS_SELECTOR,"section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(2)")
                    l.append(desc_element2.text); print('appended desc_element2:', desc_element2.text)
                except NoSuchElementException:
                    print('desc_element2 not found'); skip(); return
            try:
                desc_element3 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
                l.append(desc_element3.text); print('appended desc_element3:', desc_element3.text)
            except NoSuchElementException:
                try:
                    desc_element3 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(3)")
                    l.append(desc_element3.text); print('appended desc_element3:', desc_element3.text)
                except NoSuchElementException:
                    print('desc_element3 not found'); skip(); return
        skip(); return


l, s, d = dictExtract()
vars, keydict = (l, s)

Window(1)

