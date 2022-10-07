from audioop import bias
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch import optim
import torch.nn.functional as F





nr=420 #numero di righe
i=0
epoche=50
ds = pd.read_csv("C:/Users/User/Desktop/Training_fibre.data")

x = ds.iloc[0:nr, [2,3,4,5]].values     #fisso variabili fibra
#x=np.where(x=="Monomodale",1,-1)        #a monomodale assegno 1 e a multimodale assegno -1

y = ds.iloc[0:nr,[6]].values            #attenuazione campione


#Conversione array Numpy in tensori Pytorch
tensore_PYTC_X=torch.empty(x.shape[1])                                   
tensore_PYTC_Y=torch.empty([1]) 
tensore_dati=torch.from_numpy(x).float() + tensore_PYTC_X                
tensore_uscita=torch.from_numpy(y).float() + tensore_PYTC_Y
 #print("Tensore_dati",tensore_dati)
 #print("Tensore_uscita ",tensore_uscita)


#Creazione rete neurale con 1 layer
class PyTorchNN(nn.Module):
    def __init__(self):
        super(PyTorchNN, self).__init__()
        self.layer1 = nn.Linear(in_features=4, out_features=1,bias=True)
    def forward(self, x1):
        x2 = nn.Sequential(self.layer1
                          )(x1)
        return x2

RETE_NEURALE=PyTorchNN()
loss=torch.nn.MSELoss()                                                 #definisco funzione LOSS
OTTIMIZZATORE=optim.SGD(params=RETE_NEURALE.parameters(),lr=0.000001)     #definizione dell'ottimizzatore, in questo caso uno che sfrutta i gradienti per cambiare pio i pesi



for i in range(epoche):                     
    OTTIMIZZATORE.zero_grad()                                           #azzero i gradienti precedenti
    Attenuazione=RETE_NEURALE(tensore_dati)                         #calcolo l'uscita della rete neurale
    params = list(RETE_NEURALE.parameters())                                               
  #  print(params)                                                      #stampo i parametri della rete, pesi e bias per ogni layer  
  #  print("Attenuazione = ",Attenuazione,"\n")                       #stampo l'uscita della rete per ogni riga di dati
    errore =loss(Attenuazione,tensore_uscita)                       #calcolo la loss funcion dell'uscita rispetto all'uscita target del dataset
    errore.backward()                                                   #applico la backpropagation
    OTTIMIZZATORE.step()                                                #ottimizzo i pesi e i bias con l'ottimizzatore  
    
    if np.mod(i,5)==0:
        print("errore ",errore,"\n")                                    #stampo l'errore commesso ogni tot epoche, in questo caso 50
        
print("Attenuazione = ",Attenuazione,"\n")

Errore2=abs(Attenuazione-tensore_uscita)
print("Errore2 ",Errore2)

#Variabili per l'input

#print("Inserisci i parametri della casa: \n")
#print("Numero camere: ")
#camere=float(input())
#print("Numero bagni: ")
#bagni=float(input())
#print("Metri quadri vivibili: ")
#mtliving=float(input())
#print("Metri quadri terreno: ")
#mtlot=float(input())
"""""
tensore_in=torch.empty(4)
tensore_in[0]=camere
tensore_in[1]=bagni
tensore_in[2]=mtliving
tensore_in[3]=mtlot     
prezzo=int(RETE_NEURALE(tensore_in))
print("Questa casa costa: ",prezzo,"€")

"""