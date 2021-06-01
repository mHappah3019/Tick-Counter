#from datetime import date
from collections import deque
from datetime import datetime

import csv
import os

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

current_date = datetime.today()  # for now current_date can be thought as a global variable



def save_daily_counts():
    
    current_date = datetime.today().strftime("%d/%m/%Y") #getting current_date and formatting it
    fields = [current_date]

    with open("tick-instances1.csv", "r") as f: #TODO: ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)   #skipping headers row
        for row in csv_reader:    #for every instance we want to store the daily count
            fields.append(row[2]) #appending every instance daily count, to be then appended to one single row, correspoding to "current_date"
    
    with open("dailies.csv", "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)
    with open("dailies.csv", "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #checking if file ends with a newline (\n)
            f1.write("\n")                 #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [current_date, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just DAILY counts


# function that checks if 2 dates fall in the same week or not
# returns True if the 2 dates fall in the same week
def is_sameweek_dates(date1, date2): 
    dat1 = date1.isocalendar() # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = date2.isocalendar()
    return dat1[1] == dat2[1]


# function that checks if 2 dates fall in the same month or not
# returns True if the 2 dates fall in the same month

def is_samemonth_dates(date1, date2):
    dat1 = trunc_datetime(date1) # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = trunc_datetime(date2)

    return dat1 == dat2


# TODO: modificare funzione in modo da poter comparare le stringhe delle date, in quanto datetime.today() rende informazioni ulteriori su ore:minuti:secondi che non permettono un confronto rispetto al solo giorno
# o altrimenti usare lo stesso formato usato per  is_samewek_dates e is_samemonth_dates
def is_same_date(date1_object, date2):
    date2_object = datetime.strptime(date2, "%d/%m/%Y")
    
    dat1 = date1_object.isocalendar()
    dat2 = date2_object.isocalendar()

    return dat1[2] == dat2[2]

    #TODO: pensare che a distanza di una settimana potrebbe riscontrarsi un bug, in quanto due lunedì diversi sarebbero considerati una stessa data
    #      aggiungere quindi logica per verificare successivamente se fanno parte della stessa settimana
    
    

def check_count_reset(dates):
    # "dates" dovrebbe arrivare con un solo elemento in prima posizione (indice 0)
    # ovvero l'ultima data in "dailies.csv"

    # questa funzione prende in INPUT "dates"
    # FUNZIONALITà: 

    current_date = datetime.today()
    last_saved_date = load_last_date()
    

    #TODO: capire se gli if statements messi così sono funzionali a quello che voglio fare o meno
    # sto infatti pensando che probabilmente in python se il controllo entra nel primo if, ad esempio, non potrà rientrare nei successivi elif

    if ( not is_same_date(current_date, last_saved_date) ):        #se current_date e dates[0] (o "ultima data") non coincidono allora dovremmo resettare il daily count di ogni instanza
        #save_date(current_date, dates)  TODO: capire che cazzo ci fa questa chiamata qua
        count_reset("day")
    elif ( not is_sameweek_dates(current_date, last_saved_date) ): #se current_date e dates[0] (o "ultima data") non sono giorni della stessa settimana allora dovremmo resettare il weekly count di ogni instanza
        count_reset("week")
    elif( not is_samemonth_dates(current_date, last_saved_date) ): #se current_date e dates[0] (o "ultima data") non sono giorni dello stesso mese allora dovremmo resettare il monthly count di ogni instanza
        count_reset("month")


def count_reset(info):

    with open("tick-instances1.csv", "r") as file:
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
                matrix[i+1][option] = 0 #RESETTING...

    with open("tick-instances1.csv", "w", newline="") as file1:
        csv_file1 = csv.writer(file1)
        csv_file1.writerows(matrix)
 

def load_last_date():
    with open("dailies.csv", "r") as file:
        csv_reader = csv.reader(file)
        matrix = list(csv_reader)

        print(matrix)

        last_date = matrix[-1][0]
        return last_date


print(load_last_date())
#print(dates)

# funzione che presa una qualsiasi data "someDate" tiene il valore "originale" di mese e anno
# ma rende un valore "univoco" al resto delle specifiche, quali: giorno, ora, minuto, secondo, etc...
# usata perchè prese 2 date qualsiasi, ci permette di verificare se queste sono nello stesso mese o meno
def trunc_datetime(someDate):
    return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)