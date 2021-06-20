from pynput.keyboard import Listener
from MainApplication import objects

def on_press_all(pressed_key):
    for object in objects:
        key = object.combination
        on_press_single(pressed_key, key, object)

def on_press_single(pressed_key, key, object):
    if str(pressed_key) == str(key):
        object.increment()

with Listener(on_press=on_press_all) as l:

    #TODO: try putting code to run in here https://stackoverflow.com/questions/59814041/pynput-not-letting-tkinter-make-window
    # or https://stackoverflow.com/questions/57949353/key-listener-script-with-gui-wont-work-tkinter
    l.join()

