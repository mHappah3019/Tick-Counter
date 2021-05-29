from datetime import date
from collections import deque

import csv
import os

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

dates = deque(maxlen=3) # contiene 2/3 date

def save_date(today, dates):
    # prende in input un array con dates[0] == "ieri l'altro"
    # e dates[1] == "ieri"

    # rende come output lo stesso array con dates[0] = "ieri"
    # e dates[1] == "oggi"

    #appendo (ho 3 elementi), e cancello la testa

    dates.append(today)
    dates.popleft()
    

def check_count_reset(dates):
    # TODO: da chiamare ad ogni avvio dell'applicazione
    current_date = date.today()
    if (current_date != dates[1]):
        save_date(current_date, dates)
        count_reset()

def count_reset():

    with open("tick-instances.csv", "r") as file:
        csv_file = csv.reader(file)
        matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                #NB. numbers are converted into string values
        print(matrix)
        print(len(matrix))
        for i in range(len(matrix) -1):
                matrix[i+1][2] = 0 

    with open("tick-instances1.csv", "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix)

count_reset()
    
