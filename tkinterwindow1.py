import tkinter as tk

window = tk.Tk()

instance_frame = tk.Frame(master = window, relief = tk.SUNKEN, borderwidth=2)

for i in range(3):
    window.rowconfigure(i, weight=1, minsize=75)
    window.columnconfigure(0, weight=1, minsize=75)



    instance_frame = tk.Frame(master = window, relief = tk.SUNKEN, borderwidth=2, bg="yellow")
    instance_frame.pack(fill = tk.BOTH, expand = True)
    name_lbl = tk.Label(master=instance_frame, text=f"Tick {i+1}", width=25)
    decrease_btn = tk.Button(master=instance_frame, text="-", height=1, width=2)
    count_lbl = tk.Label(master=instance_frame)
    increase_btn = tk.Button(master=instance_frame, text="+", height=1, width=2, relief=tk.RAISED, borderwidth=3)
    
    name_lbl.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    decrease_btn.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    count_lbl.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)
    increase_btn.pack(side = tk.LEFT, fill = tk.BOTH, expand = True)

window.mainloop()