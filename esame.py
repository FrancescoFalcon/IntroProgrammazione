#Codice di Falcon Francesco, esame 20/06/23
import csv

class CSVFile:

    def __init__(self, name):
        self.name = name

    def get_data(self):
        pass

class CSVTimeSeriesFile(CSVFile):

    def get_data(self):
        try:
            with open(self.name, 'r') as csvfile:                                           
                my_file = csv.reader(csvfile)                                                   #Leggo il file e salto l'intestazione
                next(my_file)
                time_series = []
                for row in my_file:
                    date, passengers = row
                    try:
                        if int(passengers) <= 0:                                                #Se i passeggeri sono <0 ignoro la riga
                            continue
                        time_series.append([str(date), int(passengers)])
                    except ValueError:                                                          #Se i dati inseriti non sono convertibili in stringa e int ignoro la riga
                        continue

                year0_month1 = []                                                               #Creo una lista dividendo anni da mesi
                for i in range(len(time_series)-1):
                    elements = time_series[i][0].split('-')                                                    
                    if elements[0] != 'date':                                                  
                        year0_month1.append(elements)

                for i in range(0,len(year0_month1) - 1):                                        #Controllo che gli anni siano in ordine
                    if year0_month1[i+1][0] < year0_month1[i][0]:
                        raise ExamException("Gli anni del file csv non sono in ordine")
                    
                    if int(year0_month1[i][1]) > 12:                                            #Controllo che il numero del mese non superi 12
                        raise ExamException("Non esiste un tredicesimo mese")
                    
                    for j in range(1,len(year0_month1) - 1 - i):                                #Controllo se ci sono duplicati
                        if time_series[i][0] == time_series[i+j][0]:
                            raise ExamException("Ci sono dei timestamp duplicati")

                #print(time_series)
        except FileNotFoundError:                                                               #Se il file non viene trovato alzo un eccezione
            raise ExamException("File non trovato")

        return time_series

class ExamException(Exception):
    pass

def compute_avg_monthly_difference(time_series, first_year, last_year):

    if not time_series:                                                                         #Controllo che time_series non sia vuota
        raise ExamException("time_series vuota")
    
    try:
        first_year = int(first_year)                                                            #Se gli anni non sono convertibili in int alzo un eccezione
        last_year = int(last_year)
    except ValueError:
        raise ExamException("Gli anni inseriti non sono numerici interi")

    if first_year > last_year:                                                                  #Se l'intervallo degli anni non è in ordine alzo un eccezione
        raise ExamException("Il primo anno deve essere minore dell'ultimo")
    
    monthly_diffs = []                                                                          #Creo una lista vuota di 12 elementi 
    for i in range(12): 
        monthly_diffs.append([])

    for i in range(len(time_series) -1):
        date = time_series[i][0]
        year, month = [int(line) for line in date.split('-')]
        try:
            if first_year <= year < last_year:
                diff = abs(time_series[i + 12][1] - time_series[i][1])                          #Calcolo le differenze parziali dei mesi
                monthly_diffs[month - 1].append(diff)
        except IndexError:                                                                      #Se l'indice non è valido alzo un eccezione
            raise ExamException("L'intervallo di anni inseriti non è presente nel dataset")


    result = []
    for diffs in monthly_diffs:
        if diffs:
            avg = sum(diffs) / len(diffs)                                                       #Effettuo il calcolo dell'incremento medio
        else:
            avg = 0
        result.append(avg)                                                                      #Se non ci sono dati in diffs metto 0

    return result

#time_series_file = CSVTimeSeriesFile(name='C:/Users/User/Desktop/data.csv')
#time_series = time_series_file.get_data()
#result = compute_avg_monthly_difference(time_series, "1949", "1951")
#print(result)