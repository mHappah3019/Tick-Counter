import tkinter as tk
import time

instances_names_array = ["Tick1", "Tick2", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3"]

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):

            tk.Frame.__init__(self,parent) #"parent" shall be MainApplication
            
            #USING COLORS FOR CLARITY

            self.canvas = tk.Canvas(master=self, borderwidth=3, bg="black") #master denotes the parent window, that is the object whose class we are defining
            
            #We are creating the frame that shall be later embedded in the canvas as a per-se window
            self.frame = tk.Frame(self.canvas, bd=2, bg="yellow")
            
            #We want the object frame whose class we are defining to be the parent of scrollbar
            self.vsb = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.canvas.yview) #ig we are telling to python to scroll the canvas in the "y" direction
            #We are connecting the scrollbar to the canvas:
            #in particular, with this instruction we are telling the scrollbar
            #to keep its "relative position" in regards to the canvas
            self.canvas.configure(yscrollcommand=self.vsb.set)

           
            self.vsb.pack(side="right", fill="y") #inserting the scrollbar in the right side  of the ScrollableFrame
            self.canvas.pack(side="left", fill="both", expand=True) #inserting the canvas in the left side of the ScrollableFrame

            #creating the window where the self.frame (the frame where TickFrame instances will actually be set) is "virtually" set to be
            self.canvas_frame = self.canvas.create_window((0,0), window=self.frame, anchor="nw",
                                  tags="self.frame")



            self.frame.bind("<Configure>", self.onFrameConfigure)
            self.canvas.bind("<Configure>", self.FrameWidth)

            #We are specifying that the frame for the Tick instances has only one visible column
            self.frame.columnconfigure(0, weight=1, minsize=200) 

            #OOP approach: self.frame of the ScrollableFrame is being populated
            #self.frame holds the nx1 grid of instances
            self.populate()
    
    def populate(self):
        for count, name in enumerate(instances_names_array):
            
            self.frame.rowconfigure(count, weight=1) # setting only the rows where Tick instances are appended to be visible
            instance = TickFrame(self.frame, name, relief=tk.SUNKEN, borderwidth=2)
            #instance = TickFrame(self.frame, name)
            instance.grid(row=count, column=0, sticky = "nsew")

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        #we are in fact setting the scroll region to be the bounding box of everything that is in the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)



class TickFrame(tk.Frame):
        def __init__(self, parent, name,*args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs) #"parent" shall be the frame inside the canvas that it implemented as a virtual window
            

            name_lbl = tk.Label(master=self, text=name, width=25, height=2)
            decrease_btn = tk.Button(master=self, text="-")
            count_lbl = tk.Label(master=self, text=" ")
            increase_btn = tk.Button(master=self, text="+")
            info_btn = tk.Button(master=self, text="...")


            self.columnconfigure([0,1,2,3,4], weight=1) #we are setting every Tick instance to have only the 5 columns corresponding to our widget to be useful
            self.rowconfigure(0, weight=1) #being any Tick instance implemented with a grid geometry manager we need to have only the "first" row to be visible
            
            #
            name_lbl.grid(row=0, column=0, sticky="nsew") #don't know if sticky is necessary
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
    root.geometry("400x300")
    
    mainapp = MainApplication(root)
    mainapp.pack(side="top", fill="both", expand=True)
    example = ScrollableFrame(mainapp)
    mainapp.columnconfigure(0, weight=1)
    mainapp.rowconfigure(0, weight=1)
    example.grid(column=0, row=0, sticky="nsew")

    root.mainloop()