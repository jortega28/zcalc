'''
Title: zcalc
Authors: Justin Ortega, Zachary D'Alessandro, Benjamin Kratz
Date: July 2016
Version: 1.3
Availability: https://github.com/jortega28/zcalc
'''

import sys
import math
import csv
import os

programName = "zcalc"
version = "1.3"
commandlist = ["zsing", "exit", "commands", "help", "zmulti", "credits", "zbasic"]
commandlist.sort()
startypes = ["ab", "c", "rrab", "rrc"]

def help():
    helplist = []
    helplist.append("exit - Application will exit.")
    helplist.append("help - Displays detailed description of command usage.")
    helplist.append("credits - Displays authors and project information.")
    helplist.append("zmulti - Specify a directory to calculate metallicity of files in the given directory.")
    helplist.append("zsing - Specify a single file and calculate metallicity of the given file.")
    helplist.append("zbasic - Specify all the variables manually without specifying a file and have metallicity calculated.")
    helplist.sort()
    for line in helplist:
        print(line)

def exit():
    credits()
    print("Thank you for using " + programName + "!")
    sys.exit(0)

def commands():
    if len(commandlist) % 2 != 0:
        commandlist.append(" ")

    split = len(commandlist)/2
    c1 = commandlist[0:split]
    c2 = commandlist[split:]
    for key, value in zip(c1,c2):
        print('%-20s %s' % (key, value))

def credits():
    print(programName + " was developed in Konkoly Observatory located in Budapest, Hungary.")
    print("The application was developed by group of students from SUNY Oswego located in Oswego, New York.")
    print("Title: " + programName)
    print("Authors: Justin Ortega, Zachary D'Alessandro, Benjamin Kratz")
    print("Date: July 2016")
    print("Version: " + version)
    print("Availability: https://github.com/jortega28/zcalc")

def zsing():
    stype = ""
    while stype not in startypes:
        stype = raw_input("What is the type of the stars? (ab or c)\n")

    filedir = raw_input("What is the name of the file?\n")
    if filedir[0] == "'" and filedir[len(filedir)-1] == "'":
        filedir = filedir[1:len(filedir)-1]
    elif filedir[0] == '"' and filedir[len(filedir)-1] == '"':
        filedir = filedir[1:len(filedir)-1]

    if os.path.isfile(filedir) is False:
        print("File Error: File was not found. Make sure that the file exist and that it is spelled correctly.")
        print("Operation Cancelled!")
        return

    try:
        fcolumn = raw_input("What column are the frequencies located?\n")
        fcolumn = int(fcolumn)
        pcolumn = raw_input("What column are the phases located?\n")
        pcolumn = int(pcolumn)
        startrow = raw_input("What row does the data start?\n")
        startrow = int(startrow)
    except ValueError as e:
        print("Value Error: Value entered was not a number.")
        print("Here's the full error...")
        print(e)
        print("Operation Cancelled!")
        return
    fo = 0.0
    p1 = 0.0
    p3 = 0.0
    i = 0
    print("Calculating metallicity...")
    with open(filedir) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            if i == startrow-1:
                #print("Starting row:\n"+str(line))
                #print(str(line[fcolumn-1]) + " " + str(line[pcolumn-1]))
                fo = float(line[fcolumn-1])
                p1 = float(line[pcolumn-1])
            if i == startrow-1+2:
                p3 = float(line[pcolumn-1])
                break
            i += 1
    z = calcZ(fouCombo(p1,p3), fo, stype)
    print("The metallicity of the given data is:")
    print(str(z))

def zmulti():
    dir = raw_input("What is the path to the directory? (Additional directories will be ignored but all files will be parsed)\n")
    if dir[0] == "'" and dir[len(dir)-1] == "'":
        dir = dir[1:len(dir)-1]
    elif dir[0] == '"' and dir[len(dir)-1] == '"':
        dir = dir[1:len(dir)-1]
    if os.path.isdir(dir) is False:
        print("Directory Error: Could not look through given directory. Check to make sure the name of the directory is correct and that you have \nappropriate permissions to access the given directory.")
        print("Operation Cancelled!")
        return
    if dir[len(dir)-1] != "/":
        dir = dir+"/"
    key = raw_input("Do you want to only parse files that contain a keyword? If yes type it in now otherwise leave blank.\n")

    stype = ""
    while stype not in startypes:
        stype = raw_input("What is the type of the stars? (ab or c)\n")

    try:
        fcolumn = raw_input("What column are the frequencies located?\n")
        fcolumn = int(fcolumn)
        pcolumn = raw_input("What column are the phases located?\n")
        pcolumn = int(pcolumn)
        startrow = raw_input("What row does the data start?\n")
        startrow = int(startrow)
    except ValueError as e:
        print("Value Error: Value entered was not a number.")
        print("Here's the full error...")
        print(e)
        print("Operation Cancelled!")
        return
    savefile = raw_input("Would you like to save the results to a file in the same directory? If yes specify the file name otherwise leave blank.\n")
    filetosaveto = ""
    if savefile != "":
        for root, dirs, files in os.walk(dir):
            for file in files:
                if file == savefile:
                    overwrite = ""
                    while overwrite != "yes" or overwrite != "no":
                        overwrite = raw_input("That file name already exist. Do you wish to overwrite that file? (yes or no)\n")
                        if overwrite == "yes":
                            print("Ok. File will be overwritten.")
                            try:
                                filetosaveto = open(dir+savefile, "w")
                                break
                            except IOError as e:
                                print("IOError: Unable to overwrite file...")
                                print("Here's the full error...")
                                print(e)
                                print("Operation cancelled!")
                                return
                        elif overwrite == "no":
                            print("Operation cancelled!")
                            return
            try:
                filetosaveto = open(dir+savefile, "w")
            except IOError as e:
                print("IOError: Unable to create file...")
                print("Here's the full error...")
                print(e)
                print("Operation cancelled!")
                return

    validfiles = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            if key != "":
                if key in file:
                    validfiles.append(file)
            else:
                validfiles.append(file)

    validfiles.sort()

    print("Calculating metallicities...")
    fo = 0.0
    p1 = 0.0
    p3 = 0.0
    i = 0
    j = 0

    while j < len(validfiles):
        try:
            with open(dir+validfiles[j]) as tsv:
                for line in csv.reader(tsv, dialect="excel-tab"):
                    if i == startrow-1:
                        fo = float(line[fcolumn-1])
                        p1 = float(line[pcolumn-1])
                    if i == startrow-1+2:
                        p3 = float(line[pcolumn-1])
                        break
                    i += 1

            z = calcZ(fouCombo(p1,p3), fo, stype)
            if filetosaveto != "":
                filetosaveto.write("The metallicity of the file " + validfiles[j] + " is:\n")
                filetosaveto.write(str(z)+"\n")
            print("The metallicity of the file " + validfiles[j] + " is:")
            print(str(z))
        except (ValueError, IOError, IndexError) as e:
            print("Read Error: Either the file " + validfiles[j] + " could not be opened or the data is not located where specified.")
            print("Here's the full error...")
            print(e)
            if filetosaveto != "":
                filetosaveto.write("Skipping " + validfiles[j])
            print("Skipping " + validfiles[j])
        i = 0
        j += 1
    if filetosaveto != "":
        filetosaveto.close()

def zbasic():
    stype = ""
    while stype not in startypes:
        stype = raw_input("What is the type of the stars? (ab or c)\n")
    try:
        #Ask for phase 1
        p1 = raw_input("What is the value of phase 1 in radians?\n")
        p1 = float(p1)
        #Ask for phase 3
        p3 = raw_input("What is the value of phase 3 in radians?\n")
        p3 = float(p3)
        #Ask for the fundamental freq
        fo = raw_input("What is the value of the fundamental frequency in Hertz?\n")
        fo = float(fo)
    except ValueError as e:
        print("Value Error: Value entered was not a number.")
        print("Here's the full error...")
        print(e)
        print("Operation Cancelled!")
        return
    print("Calculating metallicity...")
    z = calcZ(fouCombo(p1,p3), fo, stype)
    print("The metallicity using the given values is:")
    print(str(z))

def fouCombo(p1, p3):
    #Fourier combination(31) calculation below
    fc = p3-(3.0*p1)
    pi2 = 2.0*math.pi
    while fc < 0 or fc >= pi2:
        if fc >= pi2:
            fc -= pi2
        else:
            fc += pi2
    #print(str(fc))
    return fc

def calcZ(fc, fo, stype):
    z = 0.0
    P = 1.0/fo
    #print(str(P))
    #Calculation of metallicity
    if stype == "ab" or stype == "rrab":
        b0 = -8.65
        b1 = -40.12
        b2 = 5.96
        b3 = 6.27
        b4 = -0.72
        z = b0 + (b1*P) + (b2*fc) + (b3*fc*P) + (b4*(fc*fc))
    elif stype == "c" or stype == "rrc":
        b0 = 1.70
        b1 = -15.67
        b2 = 0.20
        b3 = -2.41
        b4 = 18.00
        b5 = 0.17
        fcc = fc - math.pi
        z = b0 + (b1*P) + (b2*fc) + (b3*fc*P) + (b4*(P*P)) + (b5*(fc*fc))
    return z

def detectCommand():
    command = raw_input("--> ")
    if command == "exit":
        exit()
    while True:
        if command in commandlist:
            if command == "help":
                help()
            elif command == "commands":
                commands()
            elif command == "credits":
                credits()
            elif command == "zsing":
                zsing()
            elif command == "zmulti":
                zmulti()
            elif command == "zbasic":
                zbasic()
        else:
            print("Unknown command... Use 'help' for a list of commands and usage or "
                  "'commands' for just a list of commands.")
        command = raw_input("--> ")
        if command == "exit":
            exit()

if __name__ == '__main__':
    print("Welcome to " + programName + "! " + "All usable commands are listed below. "
          + "For a full description of commands use the 'help' command.")
    commands()
    detectCommand()