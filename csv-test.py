import csv


with open("tick-instances.csv", "r") as file:
            reader = csv.reader(file, delimiter=",")
            for row in reader:
                print(row)