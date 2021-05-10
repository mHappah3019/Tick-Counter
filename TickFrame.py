import tkinter as tk

class TickFrame(tk.Frame):
    def __init__(self, parent, name):
        tk.Frame.__init__(self, parent)
        name_lbl = tk.Label(master=self, text=name, width=25)
        decrease_btn = tk.Button(master=self, text="-")
        count_lbl = tk.Label(master=self)
        decrease_btn = tk.Button(master=self, text="+")
        info_btn = tk.Button(master=self, text="...")

        self.rowconfigure

}

