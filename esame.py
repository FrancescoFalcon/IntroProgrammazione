#Codice di Falcon Francesco

class CSVFile:

    def _init_(self, name):
        self.name = name

    def get_data(self):
        pass


class CSVTimeSeriesFile(CSVFile):

    def get_data(self): 

        if isinstance(self.name, str) != True:                                               #controllo che il nome del file sia utilizzabile
            raise ExamException('Filename: {} non è una stringa...'.format(self.name))

        leggibile = True 
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
            time_series = []
            my_file = open(self.name, 'r')
            for line in my_file:
                elements = line.split(',')                                                   #divido in 2 liste: una contentente la data, una contentente i passeggeri       
                if elements[0] != 'date':                                                    #non riporto l'intestazione
                    time_series.append(elements)
        except ExamException as e: 
            leggibile = False
            print('Il file non è leggibile: "{}"'.format(e))                                 #se non è utilizzabile alzo un eccezione
            return None

        for line in my_file:
            try:
                time_series.append([str(line[0]), int(line[1])])                             #controllo che i dati siano di tipo valido, in caso contrario elimino
            except ValueError:
                pass

        my_file.close()

        for line in time_series:                                                             #controllo che il numero dei mesi non superi il 12
            if time_series[line][1] > 12:
                raise ExamException("Non esiste nessun tredicesimo mese")

        for line in time_series:                                                             #se una riga è vuota la elimino
            if time_series[line][1] == None:
                time_series.remove(line)

        for line in time_series:
            if time_series[line][0] == None:
                time_series.remove(line)

        for line in time_series:                                                             #se una riga contiene valori negativi la elimino
            if time_series[line][1] < 0:
                time_series.remove(line)               

        anni_zero_mesi_uno = []
        for line in time_series[line][0]:                                                    #separo anni dai mesi
            anni_zero_mesi_uno = line.split('-',1)

        for line in anni_zero_mesi_uno:                                                      #se ci sono mesi o anni negatibi elimino la riga
            if anni_zero_mesi_uno[line][0] < 0:
                time_series.remove(line)

        for line in anni_zero_mesi_uno:
            if anni_zero_mesi_uno[line][1] < 0:
                time_series.remove(line)

        for line in range(len(anni_zero_mesi_uno)-1):                                        #controllo che gli anni siano in ordine crescente
            if anni_zero_mesi_uno[line+1][0] <= anni_zero_mesi_uno[line][0]:
                raise ValueError("Anni fuori ordine")

        tmp = 1
        for line in range(len(anni_zero_mesi_uno)-1):                                        #controllo che non ci siano mesi duplicati
            while anni_zero_mesi_uno[line][0] == anni_zero_mesi_uno[line+1][0]:
                tmp +=1
            if tmp > 12:
                raise ExamException("Ci sono mesi duplicati")
            tmp = 1

        for line in anni_zero_mesi_uno:                                                      #controllo che i mesi siano in ordine crescente
            if anni_zero_mesi_uno[line][0] == anni_zero_mesi_uno[line+1][0]:
                if anni_zero_mesi_uno[line+1][1] > anni_zero_mesi_uno[line][1]:
                    raise ExamException("I mesi non sono in ordine")

        return time_series


class ExamException(Exception):
    pass


def detect_similar_monthly_variations(time_series, years):

    if type(years) != list:                                                                 #controllo che years sia una lista
        raise ExamException('Years deve essere una lista')

    if len(years) < 2:                                                                      #controllo che ci siano almeno 2 anni
        raise ExamException("Gli anni inseriti devono essere almeno 2")

    for item in years:                                                                      #controllo che gli anni siano interi
        try:
            years[item] = int(years[item])
        except:
            raise ExamException("Gli anni inseriti devono essere interi")

    if abs(years[0]-years[1]) != 1:                                                         #controllo che gli anni siano consecutivi
        raise ExamException("I due anni non sono consecutivi")

    anni_zero_mesi_uno = []
    for line in time_series[line][0]:
        anni_zero_mesi_uno = line.split('-',1)
    
    count1= anni_zero_mesi_uno.count(years[0])                                          #controllo che gli anni richiesti siano presenti in time_series
    count2= anni_zero_mesi_uno.count(years[1])

    if count1 or count2 == 0:
        raise ExamException("Gli anni inseriti non sono presenti nella timeseries")

    conta1 = 1
    conta2 = 1
    for line in anni_zero_mesi_uno:                                                         #conto quanti elementi deve avere il risultato, in caso ci siano meno di 12 mesi
        if line == years[0]:
            if anni_zero_mesi_uno[line][0] == anni_zero_mesi_uno[line + 1][0]:
                conta1 +=1

    for line in anni_zero_mesi_uno:
        if line == years[1]:
            if anni_zero_mesi_uno[line][0] == anni_zero_mesi_uno[line + 1][0]:
                conta2 +=1

    membro1 = []
    membro2 = []
    for line in anni_zero_mesi_uno[0]:                                                      #creo una lista con i passeggeri del primo anno
        if years[0] == line:
            for item in range(0, len(min(conta1,conta2))-2):
                membro1.append(time_series[item][1])
            break

    for line in anni_zero_mesi_uno[0]:                                                      #creo una lista con i passeggeri del secondo anno
        if years[1] == line:
            for item in range(0,len(min(conta1,conta2))-2):
                membro2.append(time_series[item][1])
            break   

    differenza_passeggeri1 = []
    differenza_passeggeri2 = []
 
    for element in range (0,len(membro1)-2):                                                 #inserisco nella lista la differenza tra i passeggeri
            differenza_passeggeri1.append(abs(membro1[element]-membro1[element+1]))

    for element in range (0,len(membro2)-1):
            differenza_passeggeri2.append(abs(membro2[element]-membro2[element+1]))

    result = []
    for element in membro1:                                                                 #se uno dei membri considerati è none o la differenza è maggiore di 2 metto false
        if (abs(membro1[element] - membro2[element]) >= 2):
            result.append(False)
        else:
            result.append(True)            
    
    return result