from csv import reader
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

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

font = ('Arial', 18)


class MCML_Frame(tk.Frame):
    ''' Top level GUI for the MCML statisticians to work on the
    current meet's stats. '''

    def __init__(self, master, create_function, analyze_function):
        tk.Frame.__init__(self, master, width=600)
        self.pack()

        self.create_function = create_function
        self.analyze_function = analyze_function

        # Menu
        self.menu = Menu_Frame(self)
        self.menu.pack()

        # Create Files Options
        self.create_frame = Options_Frame(self)

        # Analyze Data Options
        self.analyze_frame = Analyze_Frame(self)

    def show_error_message(self, error: str) -> None:
        """ Displays an error message to the user. No side effects. """
        messagebox.showerror(title="ERROR", message=error)

    # The following four methods are to modify the contents of the main frame.
    def show_creation_options(self):
        self.empty()
        self.create_frame.pack()

    def show_analyzing_options(self):
        self.empty()
        self.analyze_frame.pack()

    def show_menu(self):
        self.empty()
        self.menu.pack()

    def empty(self):
        children = self.winfo_children()
        for child in children:
            child.pack_forget()


class Menu_Frame(tk.Frame):
    ''' Provides the main menu. '''

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=600)

        # Row 0
        row_0 = tk.Frame(self)
        row_0.pack(**row_packing_args)

        create_button = tk.Button(
            row_0, text='Create Meet Files', width=20, font=font,
            command=self.master.show_creation_options)
        create_button.pack(**inner_packing_args)

        analyze_data_button = tk.Button(
            row_0, text='Analayze Meet Data', width=20, font=font,
            command=self.master.show_analyzing_options)
        analyze_data_button.pack(**inner_packing_args)

        # Blank Row for spacing
        row_1 = tk.Frame(self)
        row_1.pack(**row_packing_args)


class Analyze_Frame(tk.Frame):
    ''' Allows the user to analyze the existing meet data and generate
    csv results files and PDF reports.'''

    def __init__(self, master):
        tk.Frame.__init__(self, master, width=600)

        label_args = {
            "font": font,
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
                                   font=font, width=20)
        self.year_entry.pack(**inner_packing_args)

        self.choices = ['1', '2', '3', '4', '5', 'All-Star']
        self.meet_entry = ttk.Combobox(row_1, values=self.choices,
                                       font=font, width=18)
        if self.meet_entry.get() == '':
            self.meet_entry.current(0)
        self.meet_entry.pack(**inner_packing_args)
        row_1.option_add('*TCombobox*Listbox.font', font)

        # Row 2
        row_2 = tk.Frame(self)
        row_2.pack(**row_packing_args)
        create_button = tk.Button(row_2, text='Create Reports', font=font,
                                  command=self.analyze)
        create_button.pack(side=tk.TOP)

        # Blank Row for spacing
        row_3 = tk.Frame(self)
        row_3.pack(**row_packing_args)

    def analyze(self):
        pass


class Options_Frame(tk.Frame):
    ''' Allows the user to set the meet information and create the
    csv file for the meet. '''

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

        font = font

        label_args = {
            "font": font,
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
                                   font=font, width=20)
        self.year_entry.pack(**inner_packing_args)

        self.choices = ['1', '2', '3', '4', '5', 'All-Star']
        self.meet_entry = ttk.Combobox(row_1, values=self.choices,
                                       font=font, width=18)
        self.meet_entry.current(0)
        self.meet_entry.bind("<<ComboboxSelected>>", self.selection_changed)
        self.meet_entry.pack(**inner_packing_args)
        row_1.option_add('*TCombobox*Listbox.font', font)

        # Row 2
        self.row_2 = tk.Frame(self)
        self.row_2.pack(**row_packing_args)
        # set the default selection for the meet
        self.set_selection(self.choices[0])

        # Row 3
        row_3 = tk.Frame(self)
        row_3.pack(**row_packing_args)
        create_button = tk.Button(row_3, text='Create Meet Files',
                                  font=font, command=self.create)
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
                                        font=font, anchor='w', width=20)
            categories_label.pack(side=tk.TOP, fill=tk.X, expand=True, padx=10,
                                  pady=(0, 10))
            for category in self.categories[meet]:
                cat_val = tk.IntVar(self.row_2, value=category)
                cat_entry = tk.Entry(self.row_2, textvariable=cat_val,
                                     font=font)
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
            self.master.show_error_message(message)
        except FileNotFoundError as err:
            message = err.args[0]
            self.master.show_error_message(message)
        else:
            messagebox.showinfo(
                title="Success!",
                message=("The meet file was created successfully.\n\nIt is "
                         f"called '{meet}' and can be found in the {year} "
                         "directory.\n\nYou can open and edit it in Excel, "
                         "Open Office, Google Sheets, or any spreadsheet "
                         "editor of your choice.\n\nWhen you are done, you "
                         "can use this program to analyze the student scores "
                         "and generate reports."))
            self.master.show_menu()
