import sys
import os

import tkinter as tk
import csv

from pynput import keyboard
from functools import partial
from datetime import datetime
from idlelib.tooltip import Hovertip

import database_interaction
import database123_interaction
import utils.general_utils as gen
import utils.datetime_utils

import utils.hover_messages as hm






TICK_INSTANCES = gen.find_data_abs_path("tick-instances.csv")




#ATTENZIONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
#https://stackoverflow.com/questions/431684/equivalent-of-shell-cd-command-to-change-the-working-directory
#os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

#"objects" is used to access to every TickFrame object when needed (i.e. see instances_populate)
objects = []              

#"hotkeys_dictionary" is used by keyboard.GlobalHotkeys (pynput Class)
hotkeys_dictionary = {}


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
        with open(TICK_INSTANCES, "r", encoding="UTF-8") as file:
            csv_file = csv.DictReader(file)

            for i, row in gen.skip_last(enumerate(csv_file)):
                self.frame.rowconfigure(i, weight=1) # setting only the rows where Tick instances are appended to be visible
                instance = TickFrame(self.frame, row["Name"], row["Daily"], row["Comb"], relief=tk.SUNKEN, borderwidth=2, bg="blue", bd=2)
                instance.grid(row=i, column=0, sticky="nsew")

        link_combinations()


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
            
            self.combination = combination #will help us in link_combinations function

            self.name_lbl = tk.Label(master=self, text=name, width=25, height=2)
            self.decrease_btn = tk.Button(master=self, text="-", command=self.decrement)
            self.count_lbl = tk.Label(master=self, text=str(number)) #number represents the daily counter
            self.increase_btn = tk.Button(master=self, text="+", command=self.increment) #when this button is clicked we shall increment session_count for this particular instance
            
            #this way I can call "create_window" (through create_with_arg) with arguments (1 in this case)
            create_with_arg = partial(InstancesManager.create_window, self)
            self.info_btn = tk.Button(master=self, text="...", command=create_with_arg)


            self.columnconfigure([0,1,2,3,4], weight=1) #we are setting every Tick instance to have only the 5 columns corresponding to the number of our widgets to be useful
            self.rowconfigure(0, weight=1) #being any Tick instance implemented with a grid geometry manager we need to have only the "first" row to be visible
            
            self.name_lbl.grid(row=0, column=0, sticky="nsew") #don't know if sticky is necessary
            self.decrease_btn.grid(row=0, column=1, sticky="nsew") #leaving it like this for illustrative purposes
            self.count_lbl.grid(row=0, column=2)
            self.increase_btn.grid(row=0, column=3)
            self.info_btn.grid(row=0, column=4)

            name_tip = gen.bind_hover_message(self.name_lbl, "name_lbl")
            decrease_tip = gen.bind_hover_message(self.decrease_btn, "decrease_btn")
            count_tip = gen.bind_hover_message(self.count_lbl, "count_lbl")
            increase_tip = gen.bind_hover_message(self.increase_btn, "increase_btn", f"Hotkey: Ctrl+Alt+{self.combination}")
            info_tip = gen.bind_hover_message(self.info_btn, "info_btn")

            objects.append(self) #"populate" (ScrollableFrame) creates tick instances, hence they are added to an array that keeps track of all of them


        def increment(self, event=None):
            self.session_count += 1
            self.count_lbl['text'] = str(int(self.count_lbl['text']) + 1) #shows in the label the new value; the old value is simply incremented by one
        

        def decrement(self):
            self.session_count -= 1
            self.count_lbl['text'] = str(int(self.count_lbl['text']) - 1) #shows in the label the new value; the old value is simply decremented by one





class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        #...if we should reset, either the "Daily", "Weekly", "Monthly" counters or all of em and...
        #plus, it triggers all the functions to save the stats in dailies.csv, weeklies.csv, monthlies.csv
        #should be run before populating the application with all the data (when instantiating ScrollableFrame)
        database_interaction.check_count_reset()

        self.parent = parent #"parent" shall be "root"
        #needed for "hiding" all the empty columns
        self.columnconfigure(0, weight=1, minsize=200)

        #virtually holds the nx1 grid of instances
        #the actual frame is set inside the canvas, that is inside instancesPanel
        self.instancesPanel = ScrollableFrame(parent=self)

        #OOP approach: self.frame of the ScrollableFrame is being populated
        #self.frame holds the nx1 grid of instances
        self.instancesPanel.instances_populate()

        #TODO: call function that adds hover messages

        self.instancesPanel.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)

        #holds ADD button, for now
        self.extraPanel = tk.Frame(self, bg="white")
        self.extraPanel.grid(column=0, row=1, sticky="nsew")
        self.rowconfigure(1, weight=0, minsize=25)

        self.extraPanel.columnconfigure(0, weight=1, minsize=200) #setting up extraPanel
        self.extraPanel.rowconfigure(0, weight=1, minsize=20) #setting up extraPanel

        #implementation of the ADD button
        #"InstancesAdder.create_window" creates an "InstancesAdder window"
        ADD_btn = tk.Button(self.extraPanel, text="ADD", command=InstancesAdder.create_window)
        ADD_btn.grid(row=0, column=0, sticky="nsew")


    def __exit__(self): 
        #this function, first, reads the "old" version of all the data
        #then, it takes all the data and brings it in the form of a matrix;
        #it updates the data inside the matrix
        #then overwrites the file
        database_interaction.save_upon_closing(objects)

        print("Applicazione chiusa con successo")




class InstancesAdder(ScrollableFrame):
    def __init__(self, parent, *args, **kwargs):
        ScrollableFrame.__init__(self, parent)  #parent shall be "root"

        self.parent = parent #"parent" shall be "root"

        self.labels = [  #pay attention to all the ":"s
            "Name:",
            "Comb:",
            "POS:"
        ]

        self.infos_populate() #calling it now for simplicity purposes

        self.frm_buttons = tk.Frame(parent)     #so this shiet doesn't really belong here or yes???
        self.frm_buttons.pack(fill=tk.X, side=tk.BOTTOM, ipadx=5, ipady=5)

        # Create the "Submit" button and pack it to the
        #   left side of `frm_buttons`
        #   can have add_instance or modify_instance commands depending on inheritance
        self.define_submit()


    def define_submit(self):
        self.btn_submit = tk.Button(master=self.frm_buttons, text="Submit", command=self.add_instance) #add_instance will refresh the application
        self.btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)


    @staticmethod
    def create_window():                                 #Wants to simulate a "Factory", can call this method without an instance, but creates an instance
        window = tk.Toplevel(root)                           
        instance_adder = InstancesAdder(parent=window)   #creating the frame (parent is the new window created in the previous line of code)
        instance_adder.pack(fill="both", expand=True)      #and directly packing it inside its parent (new window)


    def add_instance(self):
        with open(TICK_INSTANCES, "r", encoding="UTF-8") as file:
            csv_file = csv.reader(file)
            matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                    #NB. numbers are converted into string values


            name = self.labels_entries["Name:"].get()    #all the labels end with ":"
            comb = self.labels_entries["Comb:"].get()
            pos = self.labels_entries["POS:"].get()

            fields = [name, comb, 0, 0, 0]

            matrix.insert(-1, fields) #I'm happy that I don't have to handle the case where the file ends with one (or multiple) namespaces since matrix just "reads", and shows, rows with actual content

        with open(TICK_INSTANCES, "w", newline="", encoding="UTF-8") as file1:
            csv_file1 = csv.writer(file1)
            csv_file1.writerows(matrix)

        database123_interaction.add_to_headers(name)
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
    def __init__(self, parent, instance, *args, **kwargs):

        #this instruction goes before the parent init cause self.info_populates is called inside the parent init,
        #and in my implementation it already requires having a self.instance attribute
        self.instance = instance 

        InstancesAdder.__init__(self, parent)

        self.btn_delete = tk.Button(master=self.frm_buttons, text="Delete", command=self.delete_instance) #delete_instance will refresh the application
        self.btn_delete.pack(side=tk.LEFT, padx=10, ipadx=10)


    def define_submit(self):
        self.btn_submit = tk.Button(master=self.frm_buttons, text="Submit", command=self.modify_instance) #modify_instance will refresh the application
        self.btn_submit.pack(side=tk.RIGHT, padx=10, ipadx=10)


    @staticmethod
    def create_window(instance):                                     #Wants to simulate a "Factory", can call this method without an instance, but creates an instance
        window = tk.Toplevel(root)                           
        instance_manager = InstancesManager(parent=window, instance=instance)   #creating the frame (parent is the new window created in the previous line of code) ...
        instance_manager.pack(fill="both", expand=True)


    def modify_instance(self):
        #all the labels end with ":"
        name = self.labels_entries["Name:"].get()    #if we change "Name" in the window, we intend this to be the new name for the instance
        comb = self.labels_entries["Comb:"].get()
        pos = self.labels_entries["POS:"].get()

        database123_interaction.rename_DATABASE(self.instance.name, name)
        database_interaction.rename_GUI(self.instance.name, name)
        
        refresh()
        pass


    def delete_instance(self):
        database123_interaction.delete_counts_database(self.instance.name) #this function then calls all the "deletion" functions (1 for dailies, 1 for weeklies, 1 for monthlies and 1 for tick-instances) 
        database_interaction.delete_from_GUI(self.instance.name)
        refresh()                         #we shall reload the application to get the GUI for all the instances we have KEPT


    def infos_populate(self):
        super().infos_populate() 
        self.labels_entries["Name:"].insert(0, self.instance.name)        #show the current instance info: name, combination (for now)
        self.labels_entries["Comb:"].insert(0, self.instance.combination) #


def vp_start_gui():
    global root
    root = tk.Tk()
    root.geometry("400x300")
    
    mainapp = MainApplication(root)
    mainapp.pack(side="top", fill="both", expand=True)

    root.after(utils.datetime_utils.get_remaining_ms(), refresh)

    with keyboard.GlobalHotKeys(
        hotkeys_dictionary
    ) as h: 

        print(hotkeys_dictionary)
        root.mainloop()
        h.stop()
        h.join()
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


def link_combinations():                                
    for object in objects:
        key = object.combination
        #print(key)
        if key :
            hotkeys_dictionary[f"<ctrl>+<alt>+{key}"] = object.increment


if __name__ == "__main__":
    vp_start_gui()