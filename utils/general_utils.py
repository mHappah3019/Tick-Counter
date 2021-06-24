import os


def skip_last(iterator):  #TODO: understand this
    prev = next(iterator)
    for item in iterator:
        yield prev
        prev = item


def find_abs_path(file):
    cwd = os.path.abspath(os.path.dirname(__file__))
    given_path = f"../../Tick-Counter/data/{file}"
    csv_path = os.path.abspath(os.path.join(cwd, given_path))
    return csv_path


print(find_abs_path("dailies.csv"))