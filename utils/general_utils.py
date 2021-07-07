import os
import sys
from pathlib import Path
from idlelib.tooltip import Hovertip

sys.path.append("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

import utils.hover_messages as hm


def skip_last(iterator):  #TODO: understand this
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def find_data_abs_path(file):
    relative_path = f"./Tick-Counter/data/{file}"
    print("\n\n\n")
    full_path = Path.cwd() / relative_path           #TODO: fix cwd, running from vscode gives Tick Counter as cwd, running from cli.exe gives Tick-Counter
    print(Path.cwd())
    print("\n\n\n")
    return full_path


def bind_hover_message(frame, hover_messages_key, hover_message=None):
    hover_messages_value = hm.hover_messages.get(hover_messages_key)
    if hover_message:
        if hover_messages_value:
            hover_messages_value += f"\n{hover_message}"
        else:
            hover_messages_value = hover_message
    tip = Hovertip(frame, hover_messages_value, hover_delay=500)
    

if __name__ == "__main__":
    #print(find_abs_path("dailies.csv"))
    #p = Path(cwd = os.path.abspath(os.path.dirname(__file__)))
    #print(Path.cwd() / "Tick-Counter" / "data")
    print(find_data_abs_path("dailies.csv"))