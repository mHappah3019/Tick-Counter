from datetime import datetime #https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime

import csv
import os

os.chdir("C:/Users/mkcam/Desktop/Tick Counter/Tick-Counter")

current_date = datetime.today()  #for now current_date can be thought as a global variable


def save_daily_counts():
    current_date = datetime.today().strftime("%d/%m/%Y") #getting current_date and formatting it
    fields = [current_date] #"appending" first element to the row (will go under header "Name" in dailies.csv)

    with open("tick-instances1.csv", "r") as f: #ATTENZIONE al nome del file
        csv_reader = csv.reader(f)
        headers = next(csv_reader)      #skipping headers row
        for row in csv_reader:    #for every instance we want to store the daily count
            fields.append(row[2]) #appending every instance's daily count, to be then appended to one single row, correspoding to "current_date"
    
    with open("dailies.csv", "r") as file:
        text = file.read()                 #reading the file so that we can check later if it ends with a newline (\n)...
    with open("dailies.csv", "a", newline='\n') as f1:
        writer = csv.writer(f1)
        if ( not text.endswith("\n") ):    #...checking if file ends with a newline (\n)
            f1.write("\n")                  #adding newline if file doesn't have a newline at the end
        writer.writerow(fields)  #writing as row this corresponding list: [current_date, <count-for-first-instance>, <count-for-second-instance>, <count-for-third-instance>, etc ... ]
                                 #all these counts are just DAILY counts


# function that checks if 2 dates fall in the same week or not
# returns True if the 2 dates fall in the same week
def is_sameweek_dates(date1_object, date2_string):               #"date<>_objects" stands for datetime object coming from the datetime module
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    
    week1 = date1_object.isocalendar()[1] # takes value 1 to 53 (number of the week of the year)
    week2 = date2_object.isocalendar()[1]

    dat1 = trunc_datetime1(date1_object, "week") # makes month and year to be the only worthy "variables" for the later comparison
    dat2 = trunc_datetime1(date2_object, "week")

    #checks both if the 2 dates have the same "week number" (1-53) and if they are in the same month of the same year
    return (week1 == week2) & (dat1==dat2) 
    

# function that checks if 2 dates fall in the same month or not
# returns True if the 2 dates fall in the same month
def is_samemonth_dates(date1_object, date2_string):
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    dat1 = trunc_datetime1(date1_object, "month") # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = trunc_datetime1(date2_object, "month")

    return dat1 == dat2

  
def is_same_date(date1_object, date2_string):
    date2_object = datetime.strptime(date2_string, "%d/%m/%Y")
    dat1 = trunc_datetime1(date1_object, "day") # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = trunc_datetime1(date2_object, "day")

    return dat1 == dat2
    

def check_count_reset(dates):
    # "dates" dovrebbe arrivare con un solo elemento in prima posizione (indice 0)
    # ovvero l'ultima data in "dailies.csv"

    # questa funzione prende in INPUT "dates"
    # FUNZIONALITà: 

    current_date = datetime.today()
    last_saved_date = load_last_date()

    if ( not is_same_date(current_date, last_saved_date) ):        #se current_date e dates[0] (o "ultima data") non coincidono allora dovremmo resettare il daily count di ogni instanza
        save_daily_counts()
        count_reset("day")
    if ( not is_sameweek_dates(current_date, last_saved_date) ): #se current_date e dates[0] (o "ultima data") non sono giorni della stessa settimana allora dovremmo resettare il weekly count di ogni instanza
        count_reset("week")
    if ( not is_samemonth_dates(current_date, last_saved_date) ): #se current_date e dates[0] (o "ultima data") non sono giorni dello stesso mese allora dovremmo resettare il monthly count di ogni instanza
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
def trunc_datetime1(someDate, option):
    if (option == "day"):
        return someDate.replace(hour=0, minute=0, second=0, microsecond=0)
    elif (option == "week"):                                                      # sta robba non funziona
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # sta robba non funziona
    elif (option == "month"):
        return someDate.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
