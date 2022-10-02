# Source Code File for Lab
# Dakota Leslie

import xml.etree.ElementTree as ET
from xml.dom import minidom

def write(elem):
    xmlstr = minidom.parseString(ET.tostring(elem.getroot())).toprettyxml(indent=" ")
    with open("SquareGameOutput.xml", "w") as f:
        f.write(xmlstr)

def add(et, str, val):
    temp = ET.Element(str)
    temp.text = " " + val + " "
    et.getroot().append(temp)
    return None

def driver():
    read = "SquareGame.jack"
    output = ET.ElementTree(ET.Element("tokens"))
    keywords = {"class", "constructor", "method", "function", "int", "boolean", "char", "void", "var", "static", "field", "let", "do", "if", "else", "while", "return", "true", "flase", "null", "this"}
    symbols = {'(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', '/', '&', '|', '~', '<', '>'}
    flag = False
    skip = 0

    with open(read, "r") as f:
        for line in f:
            if (flag):
                if (line.__contains__("*/")):
                    flag = False
                continue

            token = ''
            for i in range(len(line)):
                if (line[i] == "\t"):
                    continue
                if (skip > 0):
                    skip = skip - 1
                    continue
                elif (line[i] == '/' and line[i + 1] == '/'):
                    break
                elif(line[i] == '/' and line[i + 1] == '*'):
                    if not (line.__contains__("*/")):
                        flag = True
                    break
                elif(line[i] == '"'):
                    token = ''
                    j = i + 1
                    while (j < len(line) and line[j] != '"'):
                        token = token + line[j]
                        j = j + 1
                    add(output, "stringConstant", token)
                    skip = len(token) + 1
                    token = ''
                elif (line[i] in symbols):
                    add(output, "symbol", line[i])
                elif (line[i] == ' ' or (i + 1) >= len(line) or (line[i + 1] in symbols)):
                    if (line[i] != ' ' and (i + 1 >= len(line) or (line[i + 1] in symbols))):
                        token = token + line[i]
                    if (token == ''):
                        pass
                    elif (token in keywords):
                        add(output, "keyword", token)
                        token = ''
                    elif (token.isnumeric()):
                        add(output, "integerConstant", token)
                        token = ''
                    elif ((token[0] == '_' or token[0].isalpha()) and (token[1:-1].isalnum() or len(token) == 1 or len(token) == 2)):
                        add(output, "identifier", token)
                        token = ''
                    token = ''
                if (i < len(line) and line[i] != ' ' and line[i] not in symbols):
                    token = token + line[i]
                else:
                    token = ''
    write(output)

driver()