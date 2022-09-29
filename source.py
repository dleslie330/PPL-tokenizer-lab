# Source Code File for Lab
# Dakota Leslie

import xml.etree.ElementTree as ET
from xml.dom import minidom

def write(elem):
    xmlstr = minidom.parseString(ET.tostring(elem.getroot())).toprettyxml(indent=" ")
    with open("SquareGameOutput.xml", "w") as f:
        f.write(xmlstr)

def driver():
    read = "SquareGame.jack"
    output = ET.ElementTree(ET.Element("tokens"))

    with open("SquareGame.jack") as f:
        while (True):
            line = f.readline()

            if not line:
                break

            token = ''
            for i in range(len(line)):
                if (line[i] == '(' or line[i] == ')' or line[i] == '[' or line[i] == ']' or line[i] == '{' or line[i] =='}' or line[i] == ',' or line[i] == ';' or line[i] == '=' or line[i] == '.' or line[i] == '+' or line[i] == '-' or line[i] == '*' or line[i] == '/' or line[i] == '&' or line[i] == '|' or line[i] == '~' or line[i] == '<' or line[i] == '>'):
                    token = line[i]
                    temp = ET.Element("symbol")
                    temp.text = token
                    output.getroot().append(temp)
                elif (line[i] == ' '):
                    token = ''
    write(output)

driver()