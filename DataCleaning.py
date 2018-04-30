# -*- coding: utf-8 -*-


import csv



input_file = "/Users/banana/Desktop/input_utf8.csv"
output_file = "/Users/banana/Desktop/output_utf8_small.csv"
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
    # TODO Links https<- kill
    # " <-
    blacklistedWords = ["greetz", "[quote]", "[/quote]", "edge", "\\n", "\\r", "*", "\"", "\\", "//", "/", "[i]", ":-D", ":D", ":)", ";)", ":-)", ";-)", ":(", ":-(", "[b]", ">", "<"]
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

