# Source Code File for Lab
# Dakota Leslie

import xml.etree.ElementTree as ET
from xml.dom import minidom

def write(elem):
    xmlstr = minidom.parseString(ET.tostring(elem.getroot())).toprettyxml(indent=" ")
    with open("MainOutput.xml", "w") as f:
        f.write(xmlstr)

def add(et, str, val):
    temp = ET.Element(str)
    temp.text = " " + val + " "
    et.getroot().append(temp)
    return None

def driver():
    read = "Main.jack"
    output = ET.ElementTree(ET.Element("tokens"))
    keywords = {"class", "constructor", "method", "function", "int", "boolean", "char", "void", "var", "static", "field", "let", "do", "if", "else", "while", "return", "true", "flase", "null", "this"}
    symbols = {'(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', '/', '&', '|', '~', '<', '>'}
    flag = False
    skip = 0

    with open(read) as f:
            lines = f.readlines()
            for line in lines:
                if (flag):
                    if (line[-2] == '*' and line[-1] == '/'):
                        flag = False
                    continue

                token = ''
                for i in range(len(line)):
                    if (skip > 0):
                        skip = skip - 1
                        continue
                    elif (line[i] == '/' and line[i + 1] == '/'):
                        break
                    elif(line[i] == '/' and line[i + 1] == '*'):
                        #flag = True
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
                        token = line[i]
                        add(output, "symbol", token)
                        token = ''
                    elif (line[i] == ' ' or (i + 1) >= len(line) or (line[i + 1] in symbols)):
                        if (i + 1 >= len(line) or (line[i + 1] in symbols)):
                            token = token + line[i]
                        if (token == ''):
                            pass
                        elif (token in keywords):
                            add(output, "keyword", token)
                        elif (token.isnumeric()):
                            add(output, "integerConstant", token)
                        elif ((token[0] == '_' or token[0].isalpha()) and (token[1:-1].isalnum() or len(token) == 1)):
                            add(output, "identifier", token)
                        token = ''
                    if (i < len(line) and line[i] != ' '):
                        token = token + line[i]
                    else:
                        token = ''
    write(output)

driver()