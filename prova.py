import datetime

def is_sameweek_dates(date1, date2): 
    dat1 = date1.isocalendar() # date1 and date2 are supposed to be "date" objects from datetime library
    dat2 = date2.isocalendar()
    return dat1[1] == dat2[1]


#current_date = datetime.now().strftime("%d/%m/%Y")
current_date = datetime.datetime.today()
print(current_date)
#d = datetime.date(2019, 4, 13)
date1 = datetime.date(2021, 5, 29)
print(date1)

print(is_sameweek_dates(current_date, date1))