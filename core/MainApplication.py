from pynput import keyboard
from csv_wip import current_date, get_remaining_ms, save_daily_counts, is_same_date, check_count_reset, load_last_date, get_remaining_ms, skip_last, delete_counts
from datetime import datetime

""" from database_interaction import *
from database123_interaction import *  #TODO: fix this shit
 """
from functools import partial
from pynput.keyboard import Listener
import tkinter as tk
import csv
import os
import sys

TICK_INSTANCES = "tick-instances.csv"


#ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")


objects = [] #TODO: define its use in a comment


class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
            tk.Frame.__init__(self, parent) #"parent" shall be MainApplication for the "instance panel" and root for the "instance manager"
            
            #USING COLORS FOR CLARITY

            self.parent = parent

            self.canvas = tk.Canvas(master=self, borderwidth=3, bg="black") #master denotes the parent window, that is the object whose class we are defining (parent is ScrollableFrame object)
            
            #We are creating the frame that shall be later embedded in the canvas as a per-se window
            self.frame = tk.Frame(self.canvas, bd=2, bg="yellow")
            
            #We want the object frame whose class we are defining to be the parent of scrollbar (parent of scrollbar is ScrollableFrame object)
            self.vsb = tk.Scrollbar(master=self, orient=tk.VERTICAL, command=self.canvas.yview) #ig we are telling python to scroll the canvas in the "y" direction
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


    def instances_populate(self):
        #We are specifying that the frame (for the Tick instances in case of MainApplication) has only one visible column
        self.frame.columnconfigure(0, weight=1, minsize=200) 
        with open(TICK_INSTANCES, "r") as file:
            csv_file = csv.DictReader(file)

            for i, row in skip_last(enumerate(csv_file)):
                self.frame.rowconfigure(i, weight=1) # setting only the rows where Tick instances are appended to be visible
                instance = TickFrame(self.frame, row["Name"], row["Daily"], row["Comb"], relief=tk.SUNKEN, borderwidth=2, bg="blue", bd=2)
                instance.grid(row=i, column=0, sticky="nsew")

        #TORESTORE: link_combinations() #watch function definition additional comments


    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        # we are in fact setting the scroll region to be the bounding box of everything that is in the canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width = canvas_width)




class TickFrame(tk.Frame):
        def __init__(self, parent, name, number, combination, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs) #"parent" shall be the frame inside the canvas that is implemented as a virtual window (self.frame)
            
            self.parent = parent
            self.session_count = 0 #count shall be read from the csv file but session_count is naturally instantiated to 0
            self.name = name #definisco anche un attributo "nome" per provare ad accedere più facilmente agli oggetti
                             #in un secondo momento
            
            #TODO:  see if defining the binding here (in init) is better than defining all of them together (as implemented in link_combinations)
            self.combination = combination #will help us in link_combinations function

            self.name_lbl = tk.Label(master=self, text=name, width=25, height=2)
            self.decrease_btn = tk.Button(master=self, text="-", command=self.decrement)
            self.count_lbl = tk.Label(master=self, text=str(number)) #number represents the daily counter
            self.increase_btn = tk.Button(master=self, text="+", command=self.increment) #when this button is clicked we shall increment session_count for this particular instance
            
            #this way I can call create_with_arg with arguments (1 in this case)
            create_with_arg = partial(InstancesManager.create_window, self)
            self.info_btn = tk.Button(master=self, text="...", command=create_with_arg)


            self.columnconfigure([0,1,2,3,4], weight=1) #we are setting every Tick instance to have only the 5 columns corresponding to the number of our widgets to be useful
            self.rowconfigure(0, weight=1) #being any Tick instance implemented with a grid geometry manager we need to have only the "first" row to be visible
            
            self.name_lbl.grid(row=0, column=0, sticky="nsew") #don't know if sticky is necessary
            self.decrease_btn.grid(row=0, column=1, sticky="nsew") #leaving it like this for illustrative purposes
            self.count_lbl.grid(row=0, column=2)
            self.increase_btn.grid(row=0, column=3)
            self.info_btn.grid(row=0, column=4)


            objects.append(self) #"populate" (ScrollableFrame) creates tick instances, hence they are added to an array that keeps track of all of them
            #print(f"tickframe {self.name} instantiated")


        def increment(self, event=None):
            self.session_count += 1
            self.count_lbl['text'] = str(int(self.count_lbl['text']) + 1) #shows in the label the new value; the old value is simply incremented by one
        

        def decrement(self):
            self.session_count -= 1
            self.count_lbl['text'] = str(int(self.count_lbl['text']) - 1) #shows in the label the new value; the old value is simply incremented by one




class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        check_count_reset() #...if we should reset, either the "Daily", "Weekly", "Monthly" counters or all of em and...
                            #plus, it triggers all the functions to save the stats in dailies.csv, weeklies.csv, monthlies.csv
                            #should be run before populating the application with all the data (when instantiating ScrollableFrame)

        self.parent = parent #"parent" shall be "root"
        #needed for "hiding" all the empty columns
        self.columnconfigure(0, weight=1, minsize=200)

        #virtually holds the nx1 grid of instances
        #the actual frame is set inside the canvas, that is inside instancesPanel
        self.instancesPanel = ScrollableFrame(parent=self)
        #OOP approach: self.frame of the ScrollableFrame is being populated
        #self.frame holds the nx1 grid of instances
        self.instancesPanel.instances_populate()

        self.instancesPanel.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)

        #holds ADD button, for now
        self.extraPanel = tk.Frame(self, bg="white")
        self.extraPanel.grid(column=0, row=1, sticky="nsew")
        self.rowconfigure(1, weight=0, minsize=25)

        self.extraPanel.columnconfigure(0, weight=1, minsize=200) #setting up extraPanel
        self.extraPanel.rowconfigure(0, weight=1, minsize=20) #setting up extraPanel

        #implementation of the ADD button
        ADD_btn = tk.Button(self.extraPanel, text="ADD", command=InstancesAdder.create_window)
        ADD_btn.grid(row=0, column=0, sticky="nsew")


    #this function, first, reads the "old" version of all the data
    #then, it takes all the data and brings it in the form of a matrix;
    #it updates the data inside the matrix
    #then overwrites the file
    def __exit__(self, bool_refresh=None):

        #TODO: define all the code below as single function
        with open(TICK_INSTANCES, "r") as file: 
            csv_file = csv.reader(file)
            matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                    #NB. numbers are converted into string values

            for i, instance in (enumerate(objects)):
                print(f"tickframe {instance.name} updating")
                daily_value = int(matrix[i+1][2]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][2] = daily_value #actually updating the daily value
                
                weekly_value = int(matrix[i+1][3]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][3] = weekly_value #actually updating the weekly value
            
                monthly_value = int(matrix[i+1][4]) + instance.session_count #we are converting to int the first value cause it is originally a string type
                matrix[i+1][4] = monthly_value #actually updating the monthly value
            

        with open(TICK_INSTANCES, "w", newline="") as file1:
            csv_file1 = csv.writer(file1)
            csv_file1.writerows(matrix)

        print("Applicazione chiusa con successo")




class InstancesAdder(ScrollableFrame):
    def __init__(self, parent, app=None, *args, **kwargs):
        ScrollableFrame.__init__(self, parent)  #parent shall be "root"

        self.parent = parent #"parent" shall be "root"
        self.app = app #TODO: understand the use of this apparently fucking useless attribute

        self.labels = [  #pay attention to all the ":"s
            "Name:",
            "Hotkey:",
            "POS:"
        ]

        self.infos_populate() #calling it now for simplicity purposes

        self.frm_buttons = tk.Frame(parent)     #so this shiet doesn't really belong here or yes???
        self.frm_buttons.pack(fill=tk.X, side=tk.BOTTOM, ipadx=5, ipady=5)

        # Create the "Submit" button and pack it to the
        #   left side of `frm_buttons`
        self.btn_submit = tk.Button(master=self.frm_buttons, text="Submit", command=self.add_instance) #add_instance will refresh the application
        self.btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)

        # Create the "Clear" button and pack it to the
        #   right side of `frm_buttons`
        # TODO: determine if I really need this Clear button
        self.btn_clear = tk.Button(master=self.frm_buttons, text="Clear")
        self.btn_clear.pack(side=tk.RIGHT, ipadx=10)


    @staticmethod
    def create_window():                                     #Wants to simulate a "Factory", can call this method without an instance, but creates an instance
        window = tk.Toplevel(root)                           
        instance_adder = InstancesAdder(parent=window)   #creating the frame (parent is the new window created in the previous line of code) ... #TODO: probably defining "window" as "parent" is darn useless, cause to refresh the application we use "mainloop"
        instance_adder.pack(fill="both", expand=True)      #and directly packing it inside its parent (new window)


    def add_instance(self):
        with open(TICK_INSTANCES, "r") as file:
            csv_file = csv.reader(file)
            matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                    #NB. numbers are converted into string values


            name = self.labels_entries["Name:"].get()    #all the labels end with ":"
            comb = self.labels_entries["Hotkey:"].get()
            pos = self.labels_entries["POS:"].get()

            fields = [name, comb, 0, 0, 0]

            matrix.insert(-1, fields) #I'm happy that I don't have to handle the case where the file ends with one (or multiple) namespaces since matrix just "reads", and shows, rows with actual content

        with open(TICK_INSTANCES, "w", newline="") as file1:
            csv_file1 = csv.writer(file1)
            csv_file1.writerows(matrix)

        refresh() #closes MainApplication, hence it closes InstancesAdder too

    def infos_populate(self):
        self.frm_form = tk.Frame(master=self.frame, relief=tk.SUNKEN, borderwidth=3)

        # Pack the frame into the window
        self.frm_form.pack(fill=tk.X)

        self.frm_form.columnconfigure(0, weight=1) # make only "Label" and "Entry" columns visible...
        self.frm_form.columnconfigure(1, weight=2) # ...since we are using a grid

        self.labels_entries = {} #redefining the dictionary as empty before populating the frame, since we'll encounter a bug anytime we add a new tickframe instance

        for idx, text in enumerate(self.labels):
            self.frm_form.rowconfigure(idx, weight=1) #make the row at index "idx" visible (all the other rows are kept hidden)
            # Create a Label widget with the text from the labels list
            label = tk.Label(master=self.frm_form, text=text)
            # Create an Entry widget
            entry = tk.Entry(master=self.frm_form, width=10)
            # Use the grid geometry manager to place the Label and
            # Entry widgets in the row whose index is idx
            label.grid(row=idx, column=0, sticky="e")
            entry.grid(row=idx, column=1, sticky="nsew")

            # populates dictionary as:
            # keys correspond to text, directly taken from labels
            # values are represented by entries object (references)
            self.labels_entries[text] = entry
        



class InstancesManager(InstancesAdder):
    def __init__(self, parent, instance, app, *args, **kwargs):
        self.instance = instance #TODO: Understand: why tf this works?????  https://stackoverflow.com/questions/8998608/why-superclass-attributes-are-not-available-in-the-current-class-namespace

        InstancesAdder.__init__(self, parent)

        self.instance = instance #TODO: Understand: why tf this does NOT work????? 

        self.btn_delete = tk.Button(master=self.frm_buttons, text="Delete", command=self.delete_instance)
        self.btn_delete.pack(side=tk.LEFT, padx=10, ipadx=10)


    @staticmethod
    def create_window(instance):                                     #Wants to simulate a "Factory", can call this method without an instance, but creates an instance
        window = tk.Toplevel(root)                           
        instance_manager = InstancesManager(parent=window, instance=instance, app=tk.mainloop)   #creating the frame (parent is the new window created in the previous line of code) ...
        instance_manager.pack(fill="both", expand=True)


    def delete_instance(self):
        delete_counts(self.instance.name) #this function then calls all the "deletion" functions (1 for dailies, 1 for weeklies, 1 for monthlies and 1 for tick-instances1) 
        refresh()                         #we shall reload the application to get the GUI for all the instances we have KEPT


    def infos_populate(self):
        super().infos_populate()
        self.labels_entries["Name:"].insert(0, self.instance.name)
        #TODO: add "insertions" for Combination, POS and other parameters


def get_passed_ms():
    now = datetime.now()
    hours = int(now.hour)
    #print(hours)
    minutes = hours*60 + int(now.minute)
    #print(minutes)
    seconds = minutes*60 + int(now.second)
    #print(seconds)
    return seconds*1000 #millisecondi


def get_remaining_ms():
    ms_in_aday = 86400000
    return (ms_in_aday - get_passed_ms())


def vp_start_gui():
    global root
    root = tk.Tk()
    root.geometry("400x300")
    
    mainapp = MainApplication(root)
    mainapp.pack(side="top", fill="both", expand=True)

    root.after(get_remaining_ms(), refresh)

    root.mainloop()
    mainapp.__exit__()


def refresh():  #https://stackoverflow.com/questions/44199332/removing-and-recreating-a-tkinter-window-with-a-restart-button
    del objects[:]
    root.destroy()
    root.after(3000)
    vp_start_gui()


def order_matrix(): #TODO: implement
    #INPUT unordered matrix
    #OUTPUT ordered matrix based on POS header
    pass


#TODO: implement a new binding method cause "bind" from Tkinter doesn't work when app is out of focus

#for every object (in objects) we have defined a specific instance (of class TickFrame)
#and every instance holds a "combination" attribute that we can use to then bind the increment of the count for every instance to the specific combination
#we could have used a dictionary but this way we are making use of OOP: taking combination directly from instance
def link_combinations():                                
    for object in objects:
        key = object.combination
        #print(key)
        root.bind(f"<Control-{key}>", object.increment)


def on_press_all(pressed_key):
        for object in objects:
            key = object.combination
            print(pressed_key)
            on_press_single(pressed_key, key, object)


def on_press_single(pressed_key, key, object):
    same = str(pressed_key).strip("\'") == str(key)
    print(same)

    #TODO: fix this shit
    if same: #add condition for control + alt to be held together
        object.increment()


def on_activate():
    print("Global hotkey activated!")


def for_canonical(f):
    return lambda k: f(listener.canonical(k))


hotkey = keyboard.HotKey(
    keyboard.HotKey.parse("<ctrl>+<alt>+h"),
    on_activate
)


if __name__ == "__main__":
    listener = Listener(on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release))
    listener.start()

    vp_start_gui()

    listener.stop()
    listener.join()

