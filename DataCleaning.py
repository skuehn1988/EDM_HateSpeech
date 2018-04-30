# -*- coding: utf-8 -*-

import pandas as pd
import string
import numpy as np
import random
import xlrd
import csv
import re

#
# input_file  = pd.read_csv("/Users/banana/Desktop/input.csv", error_bad_lines=False, low_memory=False, skiprows=0, usecols=[3])
# output_file = "output.csv"
#
# #
# # Done repair iterating loop
# # ToDo Writing dataframe to CSV
# # Done Array to String
# # Todo Count False / True lables for small (300-400) and big models
# # Workaround Figure out dataframe -> lamda
#
# # ToDo the Quote Cleaner needs to be accessed first otherwise there will be a massive problem in deleting the actual quote
# # ToDo Problem in data cleaning : lastname schrieb am date time <- works
# # ToDo But : surname lastname schrieb am date time <- does not work. need to find a cleaner work around
# # ToDo Workaround check if after " schrieb am " <- put this first. than comes the cleaning
#
# # 12/14 2.5 s
#
# ###
# # confusion matrix
# # prediction csv
# # preprocessing
# #
#
#
# def getrows(file):
#     end = len(file)
#     return end
#
#
# # open CSV file
#
# def input(file):
#     #try:
#         # skip first line / 0 = index /   3 = content / 4 = deleted
#         content_ = pd.DataFrame(file)
#
#         processing(content_)
#         writeData(content_)
#
#     #except:
#      #   print("error reading data")
#
#
# def processing(data):
#     print(data)
#     nor = len(data)
#     processedData = replaceWords(data, nor)
#     processedData = str(processedData)
#     print (processedData)
#
#
#
# def replaceWords(string, row):
#     blackList = ["greetz", "[quote]", "[/quote]", "edge", "\\n", "\\r", "*", "\""]
#     bl = len(blackList)
#     for x in range(0, row):
#         quoteCleaner(string)
#         dataString = str(string.iloc[x])
#         for y in range (0, bl):
#             dataString = dataString.replace(blackList[y], "")
#         #print(dataString)
#     return(dataString)
#
#
# def dateChecker(string):
#     date = str(string)
#     len(date)
#     if(date.find(".") != -1 and len(date) == 10 ):
#         print("found date")
#         date = ""
#         return date
#
#
#
#
#
# """hurghada schrieb am 23.11.2017 20:49:[quote]Man kommt gar nicht auf die Idee - unter neu"""
# """hurgha da schrieb am 23.11.2017 20:49:[quote]Man kommt gar nicht auf die Idee - unter neuen, veränderten Bedingungen! - das Volk neu zu befragen. Des Volkes Meinung könnte der Demokratie mit ihren bewährten Institutionen - siehe oben! - zuwiderlaufen ...\r\n[/quote]\r\n\r\nDas Volk kann doch gar nicht die wirklichen Umstände beurteilen da man sie ihn vorenthält, selbst Willy Brandt (Pseudonym) war überrascht als er Kanzler wurde wie die wirklichen Machtverhältnisse liegen.\r\n\r\nDiese vermaledeite Volk könnte eine Regierung aus einer Koalition kleinerer Parteien injizieren, das muss auf jeden Fall verhindert werden, den so eine Regierung würde sich nicht an die 'Gott gewollten' Umstände halten und zuviel offen legen was der Pöbel nie verstehen würde."""
#
# def quoteCleaner(comment):
#     print("quotecleaner")
#     containsQuote = False
#     myComment = str(comment)
#     # start & end of quote
#
#
#     # get index of x = :\r\n\r\n[quote]\r\n
#     # get index of y = \r\n[/quote]\r\n\r\n
#     # delete everything between character 0 and y
#     # done
#
#     # later we need to check if the next word is a date + time if so we need to delete the name in front of "schrieb am" if there is still a word left kill that too
#     if(myComment.find(" schrieb am ") != -1):
#         print("entering QuoteCleaner")
#         # find gives me the position of "s"chrieb
#         containsQuote = True
#         myComment = myComment.split(' ')
#         schriebIndex = myComment.index("schrieb")
#         # dd.mm.yyyy HH:MM:SS
#         isDate = myComment[schriebIndex+2] # check if that is date
#         xquote = myComment[schriebIndex+3] # check if that is time
#         print(xquote)
#         try:
#             qstart  = xquote.index('[quote]')
#             qend    = xquote.rindex('[/quote]')
#             print(qstart)
#             print(qend)
#         except:
#             return comment
#
#
#
#
#
#
#         isDate = dateChecker(isDate)
#
#         #if(schriebIndex == (myComment.index("")+1)):
#          #   print("certainly quote that needs to be deleted")
#
#
#
#
#     if(containsQuote == False):
#         return(comment)
#     else:
#         return(myComment)
#
#
#
# def toArrayString(string): # deprecated
#     # if sentence contains "schrieb, am Datum Uhrzeit"
#     stringArray =  string.split(' ')
#     if( stringArray[1] == "schrieb" and stringArray[2] == "am"):
#         stringArray[4] = ""
#         stringArray[3] = ""
#         stringArray[2] = ""
#         stringArray[1] = ""
#         stringArray[0] = ""
#         stringArray = " ".join(stringArray)
#         stringArray = stringArray[5:]
#         print("replacing: x schrieb, am")
#         return stringArray
#     else:
#         stringArray = " ".join(stringArray)
#         return stringArray
#
#
#
#
# # write New CSV file
# def writeData(data):
#     # write new csv file
#     print("Writing to new CSV_file")
#     #print(data)
#     try:
#         data.to_csv(output_file, sep=';')
#     except:
#         print("error Writing CSV FILE")
#     #data.to_csv('output_file.csv')
#     # if column is not empty take next column
#
#
#
#
# input(input_file)
#
# #iterrows(input_file)


input_file = "input_utf8.csv"
output_file = "output_utf8_small.csv"
toxic_counter = 0
nontoxic_counter = 0


def quoteRemover(string):
    #print(" I ", string)
    data = str(string)
    #try:
    #print(data)
    qstart = data.find("[quote]")
    qend = data.find("[/quote]")
    data_tb_replaced = data[qstart:qend+8]
    data = data.replace(data_tb_replaced, "")
    data = quoter(data)
    data = blacklist(data)
    return data

def blacklist(string):
    blacklistedWords = ["greetz", "[quote]", "[/quote]", "edge", "\\n", "\\r", "*", "\""]
    for x in range(len(blacklistedWords)):
        string = str(string).replace(blacklistedWords[x],"")
    return string


def quoter(string):
    if(string.find(" schrieb am ") != -1):
        string = string.split(' ')
        schriebIndex = string.index("schrieb")
        isDate = string[schriebIndex+2] # check if that is date
        if(dateChecker(isDate) == True): #17
            string = " ".join(string)
            start = str(string).find(isDate)
            end = start+17
            string = string[end:]
    return string


def dateChecker(string):
    date = str(string)
    len(date)
    if(date.find(".") != -1 and len(date) == 10 ):
        return True

def writeToFile(writer, id, content, deleted):
    writer.writerow([id, content, deleted])

# def writeToSmallFile(writer, id, content, deleted):
#     global toxic_counter
#     global nontoxic_counter
#     if deleted == "TRUE" and toxic_counter < 500:
#         writer.writerow([id, content, deleted])
#         toxic_counter = toxic_counter + 1
#     if deleted == "FALSE" and nontoxic_counter < 500:
#         writer.writerow([id, content, deleted])
#         nontoxic_counter = nontoxic_counter + 1
#     if nontoxic_counter == 500 and toxic_counter == 500:
#         exit()

with open(input_file, "r", encoding="utf-8") as csvfile:
    output_file = open(output_file, "w", encoding="utf-8")
    writer = csv.writer(output_file)
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]
    id = 0
    for row in data:
        content = row["content"]
        deleted = row["deleted"]
        if(str(content).find("quote")):
            content = quoteRemover(content)
        print([id, content, deleted])
        writeToFile(writer, id, content, deleted)
        id = id +1
    output_file.close()
    exit()

# with open(output_file, "wr") as csvfile_:
#      writer = csv.DictWriter(csvfile_)
#      data = [row for fow in]
#      writer.writerow([content])
#      writer.writerow([deleted])
