from tkinter import *
import csv
import tkinter
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

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



class Window:

    def __init__(self, page):
        self.window = Tk()
        page = IntVar(master=self.window, value=page)
        # -------------------------------------------------- Initial Extraction
        self.l, self.keys, self.d = dictExtract()
        self.count = 0
        scraper_button = Button(text='Scrape', command=lambda: self.scraper('cock'))
        scraper_button.grid(row=5, column=1)
        # -------------------------------------------------- WORD Label
        try:
            self.bar1 = tkinter.StringVar(self.window, str(self.d[page.get()]).capitalize())
            self.wrd1 = Label(self.window, textvariable=self.bar1, font="helvetica 11 underline")
            self.wrd1.grid(row=0, column=3)
        except KeyError:
            print("out of index")


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

        # Custom input method utilizing interface
        # Importing a custom message
        def prompt(text):
            # Instantiating the popup
            self.top = Toplevel(self.window)
            self.top.geometry('440x400')
            label = Label(self.top, text=text)
            label.grid(row=0, column=0, columnspan=2)

            user_input_word = StringVar()
            user_input_desc1 = StringVar()
            user_input_desc2 = StringVar()
            user_input_desc3 = StringVar()
            user_input_desc4 = StringVar()
            user_input_desc5 = StringVar()
            user_input_desc6 = StringVar()
            user_input_desc7 = StringVar()
            user_input_desc8 = StringVar()
            user_input_desc9 = StringVar()

            word_entry = Entry(self.top, width=25, textvariable=user_input_word)
            desc_entry1 = Entry(self.top, width=40, textvariable=user_input_desc1)
            desc_entry2 = Entry(self.top, width=40, textvariable=user_input_desc2)
            desc_entry3 = Entry(self.top, width=40, textvariable=user_input_desc3)
            desc_entry4 = Entry(self.top, width=40, textvariable=user_input_desc4)
            desc_entry5 = Entry(self.top, width=40, textvariable=user_input_desc5)
            desc_entry6 = Entry(self.top, width=40, textvariable=user_input_desc6)
            desc_entry7 = Entry(self.top, width=40, textvariable=user_input_desc7)
            desc_entry8 = Entry(self.top, width=40, textvariable=user_input_desc8)
            desc_entry9 = Entry(self.top, width=40, textvariable=user_input_desc9)

            slider = Scale(self.top, from_=0, to=200, length=300,tickinterval=10, orient=VERTICAL)
            slider.grid(column=4, row=0, rowspan=10)

            word_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry1.grid(row=2, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry2.grid(row=3, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry3.grid(row=4, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry4.grid(row=5, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry5.grid(row=6, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry6.grid(row=7, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry7.grid(row=8, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry8.grid(row=9, column=0, columnspan=2, pady=5, padx=(10,0))
            desc_entry9.grid(row=10, column=0, columnspan=2, pady=5, padx=(10,0))

            pos_label = Label(self.top, text='part of speech')
            desc_label1 = Label(self.top, text='description1')
            desc_label2 = Label(self.top, text='description2')
            desc_label3 = Label(self.top, text='description3')
            desc_label4 = Label(self.top, text='description4')
            desc_label5 = Label(self.top, text='description5')
            desc_label6 = Label(self.top, text='description6')
            desc_label7 = Label(self.top, text='description7')
            desc_label8 = Label(self.top, text='description8')

            pos_label.grid(row=2, column=3, pady=5)
            desc_label1.grid(row=3, column=3, pady=5)
            desc_label2.grid(row=4, column=3, pady=5)
            desc_label3.grid(row=5, column=3, pady=5)
            desc_label4.grid(row=6, column=3, pady=5)
            desc_label5.grid(row=7, column=3, pady=5)
            desc_label6.grid(row=8, column=3, pady=5)
            desc_label7.grid(row=9, column=3, pady=5)
            desc_label8.grid(row=10, column=3, pady=5)


            button = Button(self.top, text='Confirm', command=lambda: self.top.destroy())
            button.grid(row=11, column=3, pady=10)

            self.top.grab_set()
            self.top.wait_window()
            # Return user's input
            return (user_input_word.get(), user_input_desc1.get(), user_input_desc2.get(), user_input_desc3.get(),
                    user_input_desc4.get(), user_input_desc5.get(), user_input_desc6.get(), user_input_desc7.get(),
                    user_input_desc8.get(), user_input_desc9.get())

        def add_new_word():
            word, pos, desc1, desc2, desc3 ,desc4, desc5, desc6, desc7, desc8 = prompt('Enter new word')
            f = []
            if word != '':
                f.append(word)
                with open("dir/word_list.csv", "a") as y:
                    writer = csv.writer(y)
                    writer.writerow(f)
            else:
                print('no word was submitted ...')

            f = []
            if pos != '':
                f.append(pos); print(f'{pos} appended!')
            if desc1 != '':
                f.append(desc1); print(f'{desc1} appended!')
            if desc2 != '':
                f.append(desc2); print(f'{desc2} appended!')
            if desc3 != '':
                f.append(desc3); print(f'{desc3} appended!')
            if desc4 != '':
                f.append(desc4); print(f'{desc4} appended!')
            if desc5 != '':
                f.append(desc5); print(f'{desc5} appended!')
            if desc6 != '':
                f.append(desc6); print(f'{desc6} appended!')
            if desc7 != '':
                f.append(desc7); print(f'{desc7} appended!')
            if desc8 != '':
                f.append(desc8); print(f'{desc8} appended!')

            save_me = {word:f}
            if word != '':
                with open('dir/dess.txt', "a") as x:
                    save_me = str(save_me)
                    x.write(save_me + "\n")
                    print(f'successfully saved the following word pair:\n{save_me}')
            else:
                print('Exited without adding new word')


        i = get_current_index()
        x = IntVar(self.window); x.set(i)
        self.indexlab = Label(self.window, textvariable=x)
        self.indexlab.grid(row=0, column=5)
        self.index, self.vars, self.descs = self.Current(x.get())
        self.indexlist = []
        self.findind = 0
        for key in self.vars.keys():
            self.indexlist.append(key)

        # -------------------------------------------------- Button: Add New Word
        self.NewWordButton = Button(self.window, text="+", command=lambda: add_new_word())
        self.NewWordButton.grid(row=0, column=1)
# -------------------------------------------------- Button: Load Words
        self.WordsButton = Button(self.window, text="Words", command=lambda: self.Button_Words(wordUnload()))
        self.WordsButton.grid(row=0, column=0)
# -------------------------------------------------- Button: Next
        self.NextButton = Button(self.window, text=">", command=lambda: self.Next(x))
        self.NextButton.grid(row=0, column=99)
# -------------------------------------------------- Button: Previous
        self.PreviousButton = Button(self.window, text="<", command=lambda: self.Previous(x))
        self.PreviousButton.grid(row=0, column=2)

        try: # --------------------------------------------- Description Label 1
            self.var1 = tkinter.StringVar(self.window, str(self.descs[1]))
            self.dsc1 = Label(self.window, textvariable=self.var1,
                              font="Helvetica 9 italic", anchor="w", justify=LEFT, pady=5)
            self.dsc1.grid(row=1, column=3, pady=5, sticky="W")
        except KeyError:
            print("Description out of index in Label 1")
        try: # --------------------------------------------- Description Label 2
            self.var2 = tkinter.StringVar(self.window, str(self.descs[2]))
            self.dsc2 = Label(self.window, textvariable=self.var2, anchor="w", justify=LEFT, pady=5)
            self.dsc2.grid(row=2, column=3, pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 2")
        try: # --------------------------------------------- Description Label 3
            self.var3 = tkinter.StringVar(self.window, str(self.descs[3]))
            self.dsc3 = Label(self.window, textvariable=self.var3, anchor="w", justify=LEFT, pady=5)
            self.dsc3.grid(row=3, column=3,pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 3")
        try: # --------------------------------------------- Description Label 4
            self.var4 = tkinter.StringVar(self.window, str(self.descs[4]))
            self.dsc4 = Label(self.window, textvariable=self.var4, anchor="w", justify=LEFT)
            self.dsc4.grid(row=4, column=3,pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 4")
        try: # --------------------------------------------- Description Label 5
            self.var5 = tkinter.StringVar(self.window, str(self.descs[5]))
            self.dsc5 = Label(self.window, textvariable=self.var5, anchor="w", justify=LEFT)
            self.dsc5.grid(row=5, column=3,pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 5")
        try: # --------------------------------------------- Description Label 6
            self.var6 = tkinter.StringVar(self.window, str(self.descs[6]))
            self.dsc6 = Label(self.window, textvariable=self.var6, anchor="w", justify=LEFT)
            self.dsc6.grid(row=6, column=3,pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 6")
        try: # --------------------------------------------- Description Label 7
            self.var7 = tkinter.StringVar(self.window, str(self.descs[7]))
            self.dsc7 = Label(self.window, textvariable=self.var7, anchor="w", justify=LEFT)
            self.dsc7.grid(row=7, column=3,pady=1, sticky="W")
        except KeyError:
            print("Description out of index in Label 7")

        try: # --------------------------------------------- Description Label 8
            self.var8 = tkinter.StringVar(self.window, str(self.descs[8]))
            self.dsc8 = Label(self.window, textvariable=self.var8, anchor="w", justify=LEFT)
            self.dsc8.grid(row=8, column=3, sticky="W")
        except KeyError:
            print("Description out of index in Label 8")
        try: # --------------------------------------------- Description Label 9
            self.var9 = tkinter.StringVar(self.window, str(self.descs[9]))
            self.dsc9 = Label(self.window, textvariable=self.var9, anchor="w", justify=LEFT)
            self.dsc9.grid(row=9, column=3, sticky="W")
        except KeyError:
            print("Description out of index in Label 9")
        try: # --------------------------------------------- Description Label 10
            self.var10 = tkinter.StringVar(self.window, str(self.descs[10]))
            self.dsc10 = Label(self.window, textvariable=self.var10, anchor="w", justify=LEFT)
            self.dsc10.grid(row=10, column=3, sticky="W")
        except KeyError:
            print("Description out of index in Label 10")
        finally:
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

        # -------------------------------------------------- Function: Current
    def wrap_by_word(self, s, n):
        # Returns a string where \\n is inserted between every n words
        a = s.split()
        ret = ''
        for i in range(0, len(a), n):
            ret += ' '.join(a[i:i + n]) + '\n'

        return ret

    def Current(self, index):
        print(f"index-------------\n{index}\n-------------")
        # l = list of words (amiable, avert etc.)
        # keys = list of dicts (words:meanings)
        # d = numbered dict of words (1: amiable etc.)
        l, keys, d = dictExtract()
        print(f'l\'s value: {l}\nkeys\' value: {keys}\nd\'s value: {d}')
        vars, momo = strVarSet(l, keys)
        count = 0  # separate integer keys for descriptions
        descs = {}  # dict
        for f in vars[index]:  # for values in DictList[index]
            count = count + 1 # separate integer keys from descriptions
            f = self.wrap_by_word(f, 15)
            f = f.rstrip('\n')
            descs[count] = f  # Extracting descriptions for Labels
            print("ff\n\n", f)
        print("Current returning Descs: \n\n", descs)
        try:
            self.bar1.set(d[index].capitalize())
            self.var1.set(descs[1])
        except AttributeError:
            print("failed to update descs 1")
        except KeyError:
            self.var1.set('')
        try:
            self.var2.set(descs[2])
        except AttributeError:
            print('failed to update descs 2')
        except KeyError:
            self.var2.set('')
        try:
            self.var3.set(descs[3])
        except AttributeError:
            print('failed to update descs 3')
        except KeyError:
            self.var3.set('')
        try:
            self.var4.set(descs[4])
        except AttributeError:
            print('failed to update descs 4')
        except KeyError:
            self.var4.set('')
        try:
            self.var5.set(descs[5])
        except AttributeError:
            print('failed to update descs 5')
        except KeyError:
            self.var5.set('')
        try:
            self.var6.set(descs[6])
        except AttributeError:
            print('failed to update descs 6')
        except KeyError:
            self.var6.set('')
        try:
            self.var7.set(descs[7])
        except AttributeError:
            print('failed to update descs 7')
        except KeyError:
            self.var7.set('')
        try:
            self.var8.set(descs[8])
        except AttributeError:
            print('failed to update descs 8')
        except KeyError:
            self.var8.set('')
        return index, vars, descs

    def delete_word(self, word):
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

    # -------------------------------------------------- Function: Button_Words
    def Button_Words(self, words):
        words_window = Toplevel(self.window)
        self.words_list = Listbox(words_window, selectmode=SINGLE, width=35)
        self.words_list.grid(row=1, column=1); y = 0
        print('words print: ', words)
        for word in words:
            y += 1
            self.words_list.insert(y, word)
        print(self.words_list.get(first=0))
        del_button = Button(words_window, text='Delete', command= lambda: self.delete_word(self.words_list.curselection())).grid(row=3, column=2)


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

        # header = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > button:nth-child(1)")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > button:nth-child(1)")))
        see_more_clicked = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > span:nth-child(3) > button:nth-child(1)").click()
        part_of_speech = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(1) > span:nth-child(1) > span:nth-child(1)")
        l.append(part_of_speech.text)
        desc_element1 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)")
        l.append(desc_element1.text)
        desc_element2 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2)")
        l.append(desc_element2.text)
        desc_element3 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3)")
        l.append(desc_element3.text)
        desc_element4 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
        l.append(desc_element4.text)
        desc_element5 = driver.find_element(By.CSS_SELECTOR, "section.css-109x55k:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)")
        print(desc_element5.text)

        new_dict = str({word:l})
        with open('dir/dess.txt', "a") as x:
            x.write(new_dict)
        with open('dir/word_list.csv', "a") as x:
            writer = csv.writer(x)
            writer.writerow([word])
        print(new_dict)





l, s, d = dictExtract()
vars, keydict = (l, s)

Window(1)

