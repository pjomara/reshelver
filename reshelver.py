#! usr/bin/python34

'''
Reshelver  aids in reshelving of library books.  User scans barcode of book
to be reshelved; book call number, user name, and date/time stamp are recorded.
Copyright (C) 2017  Parker O'Mara (pomar001@plattsburgh.edu)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.'''

import sys
import sqlite3
import datetime

def main():

    user= userName()
    barcode= eval(input("Scan the barcode: "))
    if barcode == 1:
        stopScanning(barcode, user)
    else:    
        firstCall(barcode, user)
    
    while barcode != 1:
        barcode= eval(input("Scan the barcode: "))
        call, description = callRetriever(barcode)
        cleanCall = callCleanup(call)
        recorder(user, cleanCall, description)
    else:
        stopScanning(barcode, user)

#Acquires user's name for log file.
def userName():
    user= input("Enter your first name and last initial. ")
    return user

#Acquires, parses, and records first scanned barcode/book.
def firstCall(barcode, user):
    if barcode == 1:
        sys.exit()
    else:
        call, description = callRetriever(barcode)
        cleanCall = callCleanup(call)
        recorder(user, cleanCall, description) 

#Acquires, parses, and records subsequent scanned barcodes/books.
def callRetriever(barcode):
    call= ''
    description= ''
    conn= sqlite3.connect('gcCatalog.sqlite')
    try:
        c = conn.cursor()

        try:
            c.execute("select call, description from items where barcode = ?", (barcode,))

            row = c.fetchone()
            if row:
                call= row[0]
                description= row[1]
            else:
                call = None

        finally:
            c.close()

    finally:
        conn.close()

    return call, description

#Records book's call number (including, if applicable, description),
#user, and date/time stamp.
def recorder(user, cleanCall, description):
    record= open("reshelveLog.csv", "a")
    dateTime= datetime.datetime.now().replace(microsecond=0)
    format= "%a %b %d %H:%M:%S %Y"
    print(cleanCall,",",description, ",", user, ",",dateTime, file= record)
    record.close()

#Removes extraneous characters from call number.
def callCleanup(call):
    if call == None:
        return ("Call not found")
    
    else:
        call= call.rstrip()
        call= call.replace('0','',1)
        call= call.replace(' ','',1)
        if '"' in call:
            call= call.replace('"', ' ', 1)
        if '#' in call:
            call= call.replace('#', ' ', 1)
        if '!' in call:
            call= call.replace('!', ' ', 1)
        return call

#Records "stopped scanning" message in log and quits script if user
#enters 1 for barcode.
def stopScanning(barcode, user):
    record= open("reshelveLog.csv", "a")
    dateTime= datetime.datetime.now().replace(microsecond=0)
    format= "%a %b %d %H:%M:%S %Y"
    print("Stopped scanning",","," ",",", user, ",",dateTime, file= record)
    record.close()
    sys.exit()
main()


                
                
