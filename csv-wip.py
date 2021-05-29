from datetime import date
from collections import deque

import csv
import os

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

dates = deque(maxlen=3) # contains 3 dates (even though I might have settled for 2 since I just need to know what was the date for yesterday, and not one day before yesterday too)

# function that checks if 2 dates fall in the same week or not
# returns True if the 2 dates fall in the same week
def is_sameweek_dates(date1, date2): 
    
    dat1 = date1.isocalendar() # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = date2.isocalendar()

    return dat1[1] == dat2[1]


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
    # TODO: gestire le prime esecuzioni di questa funzione, in quanto l'array "dates" sarà necessariamente vuoto
    current_date = date.today()
    if (current_date != dates[1]):
        save_date(current_date, dates)
        count_reset("day")
    elif ( not is_sameweek_dates(current_date, dates[1]) ):
        count_reset("week")


def count_reset(info):

    with open("tick-instances.csv", "r") as file:
        csv_file = csv.reader(file)
        matrix = list(csv_file) #stores data locally in the form of a matrix where every row represents one single instance and the columns represent different parameters
                                #NB. numbers are converted into string values
        if (info == "day"):
            option = 2
        elif (info == "week"):
            option = 3
        elif (info == "month"):
            option = 4

        print(matrix)
        print(len(matrix))
        for i in range(len(matrix) -1):
                matrix[i+1][option] = 0 

    with open("tick-instances1.csv", "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix) 


""" def count_reset():

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
        csv_file1.writerows(matrix) """
 

count_reset("week")
count_reset("day")
    
