import tkinter as tk

window = tk.Tk()

#window.rowconfigure(i, weight=1, minsize=50) "for loop"

#holds nx1 grid of instances
instancesPanel = tk.Frame(window)

#holds ADD button, for now
extraPanel = tk.Frame(window)

tick_instances = {
    tick1: "combinazione1",
    tick2: "combinazione2",
    tick3: "combinazione3"
}

window.columnconfigure(0, weight=1, minsize = 200)
for tick_instance in tick_instances:
    window.rowconfigure(i, weight=1, minsize = 50)
    tickfrm = TickFrame(parent=instancesPanel, name=name)
    tickfrm.grid(row=i, sticky = "nswe") #"i" può essere implementato con un "enum loop"



""" for i in range(3):
    window.rowconfigure(i, weight=1, minsize = 50)
    instance_frm = tk.Frame(master=window, relief = tk.SUNKEN, borderwidth=2, bg="yellow")

    instance_frm.grid(row=i, sticky = "nsew")

    
    name_lbl = tk.Label(master=instance_frm, text=f"Tick {i+1}", width=25)
    decrease_btn = tk.Button(master=instance_frm, text="-", height=1, width=2)
    count_lbl = tk.Label(master=instance_frm, width = 5)
    increase_btn = tk.Button(master=instance_frm, text="+", height=1, width=2, relief=tk.RAISED, borderwidth=3)
    info_btn = tk.Button(master=instance_frm, text="...", height=1, width=2)

    instance_frm.rowconfigure(0, weight = 1, minsize = 50)
    instance_frm.columnconfigure([0,1,2,3], weight=1)
    #couldn't understand why setting the columnconfigure with a loop didn't work

    name_lbl.grid(row= 0, column=0, sticky = "nsew")
    decrease_btn.grid(row= 0, column=1)
    count_lbl.grid(row= 0, column=2)
    increase_btn.grid(row= 0, column=3)
    info_btn.grid(row= 0, column=4, padx=5)
 """



window.mainloop()