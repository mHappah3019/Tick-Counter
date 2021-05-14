import tkinter as tk
import time

instances_names_array = ["Tick1", "Tick2", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3"]

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):

            tk.Frame.__init__(self,parent) #"parent" shall be MainApplication
            self.canvas = tk.Canvas(self, borderwidth=3, bg="black")
            self.frame = tk.Frame(self.canvas, bd=2, bg="yellow")
            self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
            self.canvas.configure(yscrollcommand=self.vsb.set)

           
            self.vsb.pack(side="right", fill="y")
            self.canvas.pack(side="left", fill="both", expand=True)

            self.canvas.create_window((0,0), window=self.frame, anchor="nw",
                                  tags="self.frame")

            self.frame.bind("<Configure>", self.onFrameConfigure)

            self.populate()
    
    def populate(self):
        for count, name in enumerate(instances_names_array):
            
            self.frame.rowconfigure(count, weight=1)
            # TODO: capire come si può passare come argomenti relief e borderwidth
            #instance = TickFrame(instancesPanel, name, relief=tk.SUNKEN, borderwidth=2)
            instance = TickFrame(self.frame, name)
            instance.grid(row=count, column=0, sticky = "nsew")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))



class TickFrame(tk.Frame):
        def __init__(self, parent, name):
            tk.Frame.__init__(self, parent) #"parent" shall be "instancesPanel"
            

            # TORESTORE: name_lbl = tk.Label(master=self, text=name, width=25)
            name_lbl = tk.Label(master=self, text=name, width=25, height=2)
            decrease_btn = tk.Button(master=self, text="-")
            count_lbl = tk.Label(master=self, text=" ")
            increase_btn = tk.Button(master=self, text="+")
            info_btn = tk.Button(master=self, text="...")


            self.columnconfigure([0,1,2,3,4], weight=1)
            self.rowconfigure(0, weight=1)
            
    
            name_lbl.grid(row=0, column=0, sticky="nsew")

            decrease_btn.grid(row=0, column=1)
            count_lbl.grid(row=0, column=2)

            increase_btn.grid(row=0, column=3)
            info_btn.grid(row=0, column=4)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent #"parent" shall be "root"

        #needed for "hiding" all the empty columns
        self.columnconfigure(0, weight=1, minsize=200)

        #holds nx1 grid of instances
        instancesPanel = tk.Frame(self)
        instancesPanel.grid(column=0, row=0, sticky="nsew")
        self.rowconfigure(0, weight=1, minsize=100)

        instancesPanel.columnconfigure(0, weight=3, minsize=200) #setting only one column, the others are all hidden

        #frame that occupies empty space between instancesPanel and extraPanel
        #blankFrame = tk.Frame(self, bg ="blue", height=300)
        #blankFrame.grid(column=0, row=1, sticky="nsew")
        #self.rowconfigure(1, weight=3)


        #holds ADD button, for now
        extraPanel = tk.Frame(self, bg="white")
        extraPanel.grid(column=0, row=1, sticky="nsew")
        self.rowconfigure(1, weight=0, minsize=25)

        extraPanel.columnconfigure(0, weight=1, minsize=200) #setting up extraPanel
        extraPanel.rowconfigure(0, weight=1, minsize=20) #setting up extraPanel

        #implementation of the ADD button
        ADD_btn = tk.Button(extraPanel, text="ADD",)
        ADD_btn.grid(row=0, column=0, sticky="nsew")
        



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x600")
    
    mainapp = MainApplication(root)
    mainapp.pack()
    example = ScrollableFrame(mainapp)
    example.grid(column=0, row=0)

    root.mainloop()