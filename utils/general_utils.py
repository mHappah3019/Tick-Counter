import os
from pathlib import Path


def skip_last(iterator):  #TODO: understand this
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def find_abs_path(file):
    cwd = os.path.abspath(os.path.dirname(__file__))
    print(cwd)
    given_path = f"../../Tick-Counter/data/{file}"
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path


def find_data_abs_path1(file):         #TODO: fix
    relative_path = f"./Tick-Counter/data/{file}"
    full_path = Path.cwd() / relative_path
    print(Path.cwd())
    print(full_path)
    fullpath = Path(full_path)
    return full_path

if __name__ == "__main__":
    print(find_abs_path("dailies.csv"))
    p = Path(cwd = os.path.abspath(os.path.dirname(__file__)))
    #print(Path.cwd() / "Tick-Counter" / "data")
    print(find_data_abs_path1("dailies"))