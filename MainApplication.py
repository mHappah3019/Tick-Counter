from csv_wip import current_date, get_remaining_ms, save_daily_counts, is_same_date, check_count_reset, load_last_date, get_remaining_ms
import tkinter as tk
import csv
import os
import sys


#ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

#instances_names_array = ["Tick1", "Tick2", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3", "Tick3"]

objects = []

#TODO: import this function directly from csv_wip.py
def skip_last(iterator):
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item



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
        with open("tick-instances1.csv", "r") as file:
            csv_file = csv.DictReader(file)
            for i, row in skip_last(enumerate(csv_file)):
                self.frame.rowconfigure(i, weight=1) # setting only the rows where Tick instances are appended to be visible
                instance = TickFrame(self.frame, row["Name"], row["Daily"], relief=tk.SUNKEN, borderwidth=2, bg="blue", bd=2)
                instance.grid(row=i, column=0, sticky = "nsew")



    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        # we are in fact setting the scroll region to be the bounding box of everything that is in the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    
    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)




class TickFrame(tk.Frame):
        def __init__(self, parent, name, number, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs) #"parent" shall be the frame inside the canvas that it implemented as a virtual window
            
            self.session_count = 0 #count shall be read from the csv file
            self.name = name #definisco anche un attributo "nome" per provare ad accedere piu' facilmente agli oggetti
                             #in un secondo momento

            self.name_lbl = tk.Label(master=self, text=name, width=25, height=2)
            self.decrease_btn = tk.Button(master=self, text="-")
            self.count_lbl = tk.Label(master=self, text=str(number))
            self.increase_btn = tk.Button(master=self, text="+", command=self.increment) #when this button is clicked we shall increment session_count for this particular instance
            self.info_btn = tk.Button(master=self, text="...")


            self.columnconfigure([0,1,2,3,4], weight=1) #we are setting every Tick instance to have only the 5 columns corresponding to the number of our widgets to be useful
            self.rowconfigure(0, weight=1) #being any Tick instance implemented with a grid geometry manager we need to have only the "first" row to be visible
            
            self.name_lbl.grid(row=0, column=0, sticky="nsew") #don't know if sticky is necessary
            self.decrease_btn.grid(row=0, column=1, sticky="nsew") #leaving it like this for illustrative purposes
            self.count_lbl.grid(row=0, column=2)
            self.increase_btn.grid(row=0, column=3)
            self.info_btn.grid(row=0, column=4)

            objects.append(self) #"populate" (ScrollableFrame) creates tick instances, hence they are added to an array that keeps track of all of them

        def increment(self):
            self.session_count += 1
            self.count_lbl['text'] = str(int(self.count_lbl['text']) + 1) #shows in the label the new value; the old value is simply incremented by one
            #print(self.name + ": " + str(self.session_count))




class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs) #bg="black" to check how sticky="nsew" works for the Frames (instancesPanel etc)

        check_count_reset() #...if we should reset, either the "Daily", "Weekly", "Monthly" counters or all of em and...
                            #plus, it triggers all the functions to save the stats in dailies.csv, weeklies.csv, monthlies.csv
                            #should be run before populating the application with all the data (when instantiating ScrollableFrame)

        self.parent = parent #"parent" shall be "root"
        #needed for "hiding" all the empty columns
        self.columnconfigure(0, weight=1, minsize=200)

        #virtually holds the nx1 grid of instances
        #the actual frame is set inside the canvas, that is inside instancesPanel
        self.instancesPanel = ScrollableFrame(self)
        self.instancesPanel.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)

        #holds ADD button, for now
        self.extraPanel = tk.Frame(self, bg="white")
        self.extraPanel.grid(column=0, row=1, sticky="nsew")
        self.rowconfigure(1, weight=0, minsize=25)

        self.extraPanel.columnconfigure(0, weight=1, minsize=200) #setting up extraPanel
        self.extraPanel.rowconfigure(0, weight=1, minsize=20) #setting up extraPanel

        #implementation of the ADD button
        ADD_btn = tk.Button(self.extraPanel, text="ADD")
        ADD_btn.grid(row=0, column=0, sticky="nsew")


    #this function, first, reads the "old" version of all the data
    #then, it takes all the data and brings it in the form of a matrix;
    #it updates the data inside the matrix
    #then overwrites the file
    def __exit__(self):
        with open("tick-instances1.csv", "r") as file:
            csv_file = csv.reader(file)
            matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                    #NB. numbers are converted into string values

            for i, instance in enumerate(objects):
                daily_value = int(matrix[i+1][2]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][2] = daily_value #actually updating the daily value
                
                weekly_value = int(matrix[i+1][3]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][3] = weekly_value #actually updating the weekly value
            
                monthly_value = int(matrix[i+1][4]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][4] = monthly_value #actually updating the monthly value
            
            print(matrix)

        with open("tick-instances1.csv", "w", newline="") as file1:
            csv_file1 = csv.writer(file1)
            csv_file1.writerows(matrix)




if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    
    mainapp = MainApplication(root)
    mainapp.pack(side="top", fill="both", expand=True)

    root.mainloop()
    mainapp.__exit__()