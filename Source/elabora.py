import os
import shutil
import filecmp
import logging
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
#logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

#import datetime
#import re
#from string import Template
#import fnmatch

#Definizioni
pathDB     = os.path.join('..','Test','Test_01','CartellaTest_DB')
pathUpdate = os.path.join('..','Test','Test_01','CartellaTest_Update')
pathReport = os.path.join('..','Test','Test_01','CartellaReport')
reportListFile_Name = 'report_FilesList.txt'
reportListFile = os.path.join(pathReport,reportListFile_Name)
print (reportListFile)
listapathDB = []
listapathUpdate = []

#GUI -----------------------------------

#GUI end -----------------------------------

def getLabelFromRiga(riga):
	indiceTab0  = riga.find("\t")
	return riga[0 : indiceTab0]

def get_Path_e_Filename_FromRiga(riga):
	#indiceTab1 = riga.find(sub[, start[, end]]) 
	indiceTab0  = riga.find("\t" )
	indiceTab1  = riga.find("\t", indiceTab0+1)
	indiceTab2  = riga.find("\n", indiceTab1+1)
		
	path = riga[6 : indiceTab1]
	fileName = riga[indiceTab1+1 : indiceTab2]
	print ("**path:     "+path)
	print ("**fileName: "+fileName)
	return (path, fileName)
	
def getInfoFromReport():
    a = dict()
    fo = open(reportListFile, "r")
    for riga in fo:
        label = getLabelFromRiga(riga)
        coppia = get_Path_e_Filename_FromRiga(riga)
        a[coppia] = label
        print("1) Coppia: "+coppia[0]+"\t"+coppia[1])
        print("2) label : "+label)
    fo.close();
    return a


def getListaDaPath(path):
    listapath = []
    listaCoppie = []
    print ("\nLunghezza stringa path: ",(len(path)),"---------------------")
    for dirname, dirnames, filenames in os.walk(path):
        print("\n-- dirname -- : ",dirname)
        print("---subdirname")
        # print path to all subdirectories first.
        for subdirname in dirnames:
            print(os.path.join(dirname, subdirname))

        print("---filename")
        # print path to all filenames.
        for filename in filenames:
            pathCompleto = os.path.join(dirname, filename)
            print(pathCompleto)
	
            dirCorto          = "."+dirname[len(path):len(dirname)]
            print("  * dirCorto: ",dirCorto)
	
            pathCompletoCorto = "."+pathCompleto[len(path):len(pathCompleto)]
            elemento = "[ ]"+"\t"+filename+"\t"+dirCorto+"\t"+pathCompletoCorto+"\n"
            listapath.append(elemento)

            coppia = ( dirCorto, filename)
            listaCoppie.append( coppia )            
    #return listapath VEDREMO!!!

            
    return listaCoppie
#END  getListaDaPath ------------------------------




elementiReport = getInfoFromReport()
for el in elementiReport:
    logging.info("-Righe Report- "+el[0]+el[1]+elementiReport[el])

logging.info("\n------ path DB ------------")
listapathDB = getListaDaPath(pathDB)

for path in listapathDB:
	if path in elementiReport:
		logging.info ("path in elementiReport "+path[1])
	else:
		logging.info ("path is NOT in elementiReport "+path[1])
		elementiReport[path]="[ABS]"

for path in elementiReport:
    if path in listapathDB:
        logging.info("path is in listapathDB     : "+path[1])
    else:
        logging.info("path is NOT in listapathDB : "+path[1])
        elementiReport[path]="[Unc]"

		
logging.info("*** POST Elaborazione ***")
for el in elementiReport:
    logging.info("-Righe Report- "+el[0]+el[1]+elementiReport[el])


logging.info("\n------ path Update --------")
listapathUpdate = getListaDaPath(pathUpdate)

def getNew_PathFileName(e1, e2):
    elemento = (e1, e2+"_N")
    return elemento
        
for elemento in listapathUpdate:        
    path_FileNameDB      = os.path.join(pathDB,    elemento[0])
    path_FileNameUpdate  = os.path.join(pathUpdate,elemento[0])
    logging.info("path_FileNameDB     : "+path_FileNameDB)
    logging.info("path_FileNameUpdate : "+path_FileNameUpdate)
	
    if not elemento in listapathDB:
        logging.info("ASSENTE: "+elemento[0]+"\t"+elemento[1])
		#CAPIRE perché non COPIA se il path destinatazione NON eiste!!!
        if not os.path.exists(path_FileNameDB):
            shutil.copytree(path_FileNameUpdate, path_FileNameDB)
        #shutil.copy2(os.path.join(pathUpdate,elemento[0], elemento[1]), os.path.join(pathDB,elemento[0], elemento[1]))
        shutil.copyfile(os.path.join(path_FileNameUpdate, elemento[1]), os.path.join(path_FileNameDB, elemento[1]))
        elementiReport[elemento]="[New]"
    else:
        logging.info("PRESENTE: "+elemento[0]+"\t"+elemento[1])
        #for match, mismatch, errors in filecmp.cmpfiles(pathDB, pathUPD, elemento[1], True) 
        #m = filecmp.cmpfiles(pathDB, pathUpdate, elemento[1], True)
        #match, mismatch, errors = filecmp.cmpfiles(path_FileNameDB, path_FileNameUpdate, elemento[1], True)
        if filecmp.cmp(os.path.join(path_FileNameDB,elemento[1]) , os.path.join(path_FileNameUpdate, elemento[1]), True):
            logging.info("  -- UGUALI -- : "+elemento[1])
        else:
            logging.info("  -- DIVERSI - : "+elemento[1])
            if elementiReport[elemento]=="[APr]": #Already Processed
                logging.info("     -- RIMPIAZZARE - : ",elemento[1])
                #IMPL: RIMPIAZZA FILE
                shutil.copy2(os.path.join(pathUpdate,elemento[0], elemento[1]), os.path.join(pathDB,elemento[0], elemento[1]))
                #IMPL: diventa [TBP] #To Be Processed
                elementiReport[elemento]="[TBP]"
            else:
                logging.info("     -- CREA NUOVO NOME - : "+elemento[1])
                #IMPL: Crea nuovo con ugual nome + contatore
                nuovoElem = getNew_PathFileName(elemento[0], elemento[1])
                logging.info ("nuovoElem: "+nuovoElem[1])
                logging.warning('Watch out!') # will print a message to the console
                shutil.copy2(os.path.join(pathUpdate,elemento[0], elemento[1]), os.path.join(pathDB,elemento[0], nuovoElem[1]))
                #IMPL: lo crea con [TBP] #To Be Processed
                elementiReport[nuovoElem]="[TBP]"
				

	
lista = []
fo = open(reportListFile, "w")#"r+")
logging.info ("-- Scrive nel ReportFile ---")	
for coppia in elementiReport:
    lista.append(coppia)
    #fo.writelines(elementiReport[coppia]+"\t"+coppia[0]+"\t"+coppia[1]+"\n")
lista.sort()

for el in lista:
    logging.info(elementiReport[el]+"\t"+el[0]+"\t"+el[1])
    fo.writelines(elementiReport[el]+"\t"+el[0]+"\t"+el[1]+"\n")

fo.close();


