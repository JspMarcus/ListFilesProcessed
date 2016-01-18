import os
import shutil

#import datetime
#import re
#from string import Template
#import fnmatch

#Definizioni
##pathDB = '..\Test\pathDB'
pathDB = os.path.join('..','Test','pathDB')
##pathUpdate = '..\Test\pathUpdate'
pathUpdate = os.path.join('..','Test','pathUpdate')
pathReport = os.path.join('..','Test')
reportListFile_Name = 'report_FilesList.txt'
reportListFile = os.path.join(pathReport,reportListFile_Name)
print (reportListFile)
listapathDB = []
listapathUpdate = []

#GUI -----------------------------------


#GUI end -----------------------------------





# Open a file
#fo = open(reportListFile, "w")
fo = open(reportListFile, "r+")

#os.chdir(pathDB)
print ("Lunghezza stringa pathDB: ",(len(pathDB)))
for dirname, dirnames, filenames in os.walk(pathDB):
    print("\n-- dirname -- : ",dirname)
    print("---subdirname")
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print(os.path.join(dirname, subdirname))

    print("---filename")
    # print path to all filenames.
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
        dirCorto          = "."+dirname[len(pathDB):len(dirname)]
        print("  * dirCorto: ",dirCorto)
        pathCompleto = os.path.join(dirname, filename)
        pathCompletoCorto = "."+pathCompleto[len(pathDB):len(pathCompleto)]
        #listapathDB.append("[ ]"+"\t"+filename+"\t"+dirname+"\t"+os.path.join(dirname, filename)+"\n")
        listapathDB.append("[ ]"+"\t"+filename+"\t"+dirCorto+"\t"+pathCompletoCorto+"\n")
        

#os.chdir("..")
#os.chdir("..")
##os.chdir(pathUpdate)
for dirname, dirnames, filenames in os.walk(pathUpdate):
    print(" ")
    print("----------------")
    print("------ B -------")
    print(dirname)
    print("---subdirname")
    # print path to all subdirectories first.
    for subdirname in dirnames:
        print(os.path.join(dirname, subdirname))

    print("---filename")
    # print path to all filenames.
    for filename in filenames:
        pathCompleto = os.path.join(dirname, filename)
        print(pathCompleto)
        dirCorto          = "."+dirname[len(pathUpdate):len(dirname)]
        pathCompletoCorto = "."+pathCompleto[len(pathUpdate):len(pathCompleto)]
        elemento = "[ ]"+"\t"+filename+"\t"+dirCorto+"\t"+pathCompletoCorto+"\n"
        #listapathUpdate.append("[ ]"+"\t"+filename+"\t"+dirCorto+"\t"+pathCompletoCorto+"\n")
        listapathUpdate.append(elemento)

        
        
        if elemento in listapathDB:
            print("PRESENTE: *"+pathCompletoCorto)
        else:
            print("ASSENTE: *"+pathCompletoCorto)
            shutil.copy2(os.path.join(pathUpdate,pathCompletoCorto), os.path.join(pathDB,pathCompletoCorto))


fo.writelines(listapathDB)
fo.writelines(listapathUpdate)
#fo.writelines("GIUSEPPE")




#The close() Method
#The close() method of a file object flushes any unwritten information and
#closes the file object, after which no more writing can be done.
#Python automatically closes a file when the reference object of a file is
#reassigned to another file.
#It is a good practice to use the close() method to close a file.
fo.close();

i=1
for a in listapathDB:
    print (str(i) +"\t"+a)
    i=i+1
    if a==a:
        print("uguali")

i=1
for a in listapathUpdate:
    print (str(i) +"\t"+a)
    i=i+1
    if a==a:
        print("uguali")
#dirIn
#dirOut
        
