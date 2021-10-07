from csv import reader
import tkinter as tk
from tkinter import ttk


class MCML_Frame(tk.Frame):
    ''' Top level GUI for the MCML statisticians to work on the
    current meet's stats. '''

    def __init__(self, master, create_function, analyze_function):
        tk.Frame.__init__(self, master, width=600)
        self.pack()

        self.create_function = create_function
        self.analyze_function = analyze_function

        self.font = ('Arial', 18)

        row_packing_args = {
            "side": tk.TOP,
            "fill": tk.X,
            "expand": True,
            "pady": 10,
        }

        inner_packing_args = {
            "side": tk.LEFT,
            "fill": tk.X,
            "expand": True,
            "padx": 10,
        }

        # Menu
        menu = tk.Frame(self)
        menu.pack(**row_packing_args)

        create_button = tk.Button(menu, text='Create Meet Files', width=20,
                                  font=self.font, command=self.create_options)
        create_button.pack(**inner_packing_args)

        analyze_data_button = tk.Button(menu, text='Analayze Meet Data',
                                        font=self.font, width=20)
        analyze_data_button.pack(**inner_packing_args)

        # Create Files Options
        self.create_frame = Options_Frame(self, font=self.font)

        # Analyze Data Options
        # self.analyze_frame = Analyze_Frame(self, analyze_function,
        # font=self.font)

    def create_options(self):
        self.empty()
        self.create_frame.pack()

    def analyze_options(self):
        self.empty()
        self.analyze_frame.pack()

    def menu(self):
        self.empty()
        self.menu.pack()

    def empty(self):
        children = self.winfo_children()
        for child in children:
            child.pack_forget()

    def create(self):
        try:
            self.create_function()
        except ValueError as err:
            message = err.args[0]
            print(message)


class Analyze_Frame(tk.Frame):
    pass


class Options_Frame(tk.Frame):
    ''' Allows the user to set the meet information. '''

    def __init__(self, master, font=('Arial', 18)):
        tk.Frame.__init__(self, master, width=600)

        row_packing_args = {
            "side": tk.TOP,
            "fill": tk.X,
            "expand": True,
            "pady": (10, 0),
        }

        inner_packing_args = {
            "side": tk.LEFT,
            "fill": tk.X,
            "expand": True,
            "padx": 10,
        }

        self.font = font

        label_args = {
            "font": self.font,
            "anchor": 'w',
            "width": 20,
        }

        self.categories = {}
        with open('Default Categories.csv', 'r') as infile:
            csv_reader = reader(infile)
            for row in csv_reader:
                self.categories[row[0]] = row[1:]

        # Row 0
        row_0 = tk.Frame(self)
        row_0.pack(**row_packing_args)

        year_label = tk.Label(row_0, text='Year:', **label_args)
        year_label.pack(**inner_packing_args)

        meet_label = tk.Label(row_0, text='Meet:', **label_args)
        meet_label.pack(**inner_packing_args)

        # Row 1
        row_1 = tk.Frame(self)
        row_1.pack(**row_packing_args)

        year_val = tk.IntVar(row_1, value=2021)
        self.year_entry = tk.Entry(row_1, textvariable=year_val,
                                   font=self.font, width=20)
        self.year_entry.pack(**inner_packing_args)

        self.choices = ['1', '2', '3', '4', '5', 'All-Star']
        self.meet_entry = ttk.Combobox(row_1, values=self.choices,
                                       font=self.font, width=18)
        self.meet_entry.current(0)
        self.meet_entry.bind("<<ComboboxSelected>>", self.selection_changed)
        self.meet_entry.pack(**inner_packing_args)
        row_1.option_add('*TCombobox*Listbox.font', self.font)

        # Row 2
        self.row_2 = tk.Frame(self)
        self.row_2.pack(**row_packing_args)
        # set the default selection for the meet
        self.set_selection(self.choices[0])

        # Row 3
        row_3 = tk.Frame(self)
        row_3.pack(**row_packing_args)
        create_button = tk.Button(row_3, text='Create', font=self.font,
                                  command=self.create)
        create_button.pack(side=tk.TOP)

        # Blank Row for spacing
        row_4 = tk.Frame(self)
        row_4.pack(**row_packing_args)

    def selection_changed(self, _):
        self.set_selection(self.meet_entry.get())

    def set_selection(self, meet):
        children = self.row_2.winfo_children()
        for child in children:
            child.destroy()

        if meet in self.categories:
            categories_label = tk.Label(self.row_2, text='Categories:',
                                        font=self.font, anchor='w', width=20)
            categories_label.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10,
                                  pady=(0, 10))
            for category in self.categories[meet]:
                cat_val = tk.IntVar(self.row_2, value=category)
                cat_entry = tk.Entry(self.row_2, textvariable=cat_val,
                                     font=self.font)
                cat_entry.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10)

    def create(self):
        year = self.year_entry.get()
        meet = self.meet_entry.get()

        if meet.isdigit():
            meet = f'Meet {meet}.csv'
        else:
            meet = f'{meet} Meet.csv'

        categories = [self.row_2.children[key].get()
                      for key in self.row_2.children
                      if 'entry' in key]

        try:
            self.master.create_function(year, meet, categories)
        except ValueError as err:
            message = err.args[0]
            print(message)
        except FileNotFoundError as err:
            message = err.args[0]
            print(message)
