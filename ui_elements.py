from csv import reader
import tkinter as tk
from tkinter import ttk


class MCML_Stats(tk.Frame):
    ''' Provides a GUI for the MCML statisticians to work on the
    current meet's stats. '''

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, width=600)
        self.pack()

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

        self.font = ('Arial', 18)

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
        year_entry = tk.Entry(row_1, textvariable=year_val, font=self.font)
        year_entry.pack(**inner_packing_args)

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
        self.set_selection(self.choices[0])

        # Blank Row for spacing
        row_3 = tk.Frame(self)
        row_3.pack(**row_packing_args)

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
