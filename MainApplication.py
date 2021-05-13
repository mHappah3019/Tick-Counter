import tkinter as tk

instances_names_array = ["Tick1", "Tick2", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3"]


class TickFrame(tk.Frame):
        def __init__(self, parent, name):
            tk.Frame.__init__(self, parent) #"parent" shall be "instancesPanel"
            

            # TORESTORE: name_lbl = tk.Label(master=self, text=name, width=25)
            name_lbl = tk.Label(master=self, text=name, width=25, height=3)
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
        #TORESTORE: instancesPanel = tk.Frame(self)
        #TORESTORE: instancesPanel.grid(column=0, row=0, sticky="nsew")
        self.rowconfigure(0, weight=1, minsize=100)

        #TORESTORE: instancesPanel.columnconfigure(0, weight=3, minsize=200) #setting only one column, the others are all hidden

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


        #Create a frame for the canvas and scrollbar
        frame0 = tk.Frame(self)
        frame0.grid(row=0, column=0, sticky = "nsew")
    
        frame0.columnconfigure(0, weight=1)
        frame0.rowconfigure(0, weight=1)


        def onCanvasConfigure(e):
            canvas.itemconfig('frame', height=canvas.winfo_height(), width=canvas.winfo_width())

        #Add a canvas in that frame
        canvas = tk.Canvas(frame0, bg="yellow")
        canvas.grid(column=0, row=0, sticky = "nsew")


        #Create a vertical scrollbar linked to the canvas
        vsbar = tk.Scrollbar(frame0, orient=tk.VERTICAL, command=canvas.yview)
        vsbar.grid(row=0, column=1, sticky="nsew")
        canvas.configure(yscrollcommand=vsbar.set)
        
        #Create a frame on the canvas to contain TickFrames
        instancesPanel = tk.Frame(canvas, bg="red", bd=2)
        instancesPanel.columnconfigure(0, weight=3, minsize=200)

        canvas.create_window((0,0), window=instancesPanel, anchor="nw", tags="frame")

        canvas.bind("<Configure>", onCanvasConfigure)

        #TODO: make the scrollbar work when TickFrames have weight = 0

        for count, name in enumerate(instances_names_array):
            #TORESTORE: instancesPanel.rowconfigure(count, weight=1)
            instancesPanel.rowconfigure(count, weight=0)
            # TODO: capire come si può passare come argomenti relief e borderwidth
            #instance = TickFrame(instancesPanel, name, relief=tk.SUNKEN, borderwidth=2)
            instance = TickFrame(instancesPanel, name)
            instance.grid(row=count, column=0, sticky = "nsew")


        
        



if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)

    root.mainloop()