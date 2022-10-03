# Source Code File for Lab
# Dakota Leslie

# This is for easy and pretty XML output
import xml.etree.ElementTree as ET
from xml.dom import minidom

# This is code I used at my summer internship to get pretty xml output
def write(elem):
    # create a pretty xml string from the xml tree
    xmlstr = minidom.parseString(ET.tostring(elem.getroot())).toprettyxml(indent=" ")
    # write the xml tree to output file
    with open("SquareGameOutput.xml", "w") as f:
        f.write(xmlstr)

# This creates XML elements and makes them subelements of the "Tokens" root
def add(et, str, val):
    # create an xml element with the category of token
    temp = ET.Element(str)
    # add the token to the text of the elelment
    temp.text = " " + val + " "
    # make the element a subelement of the xml tree root
    et.getroot().append(temp)
    return None

# Main method of my code
def driver():
    read = "SquareGame.jack" # File to read
    output = ET.ElementTree(ET.Element("tokens")) # Creates the XML Tree root
    # set of possible keywords
    keywords = {"class", "constructor", "method", "function", "int", "boolean", "char", "void", "var", "static", "field", "let", "do", "if", "else", "while", "return", "true", "flase", "null", "this"}
    # set of possible symbols
    symbols = {'(', ')', '[', ']', '{', '}', ',', ';', '=', '.', '+', '-', '*', '/', '&', '|', '~', '<', '>'}
    # flag for skipping comments
    flag = False
    # counter for moving the iterator of my for-loop
    skip = 0

    # open and read the input file
    with open(read, "r") as f:
        # Read each line of the file
        for line in f:
            # check if we are ignoring comments
            if (flag):
                # Look for the end of comments
                if (line.__contains__("*/")):
                    flag = False
                continue

            # start building a token variable
            token = ''
            # access each character in the line
            for i in range(len(line)):
                # Check for whitespaces (typically at the beginning)
                if (line[i] == "\t"):
                    continue
                # iterate through if we need to skip characters
                if (skip > 0):
                    skip = skip - 1
                    continue
                # check for line comments
                elif (line[i] == '/' and line[i + 1] == '/'):
                    break
                # check for multi-line comments / API Documentation comments
                elif(line[i] == '/' and line[i + 1] == '*'):
                    # see if the comment ends within this line
                    if not (line.__contains__("*/")):
                        flag = True
                    break
                # Look for the start of a string constant
                elif(line[i] == '"'):
                    token = ''
                    j = i + 1
                    # iterate through the string constant
                    while (j < len(line) and line[j] != '"'):
                        token = token + line[j]
                        j = j + 1
                    # add the string constant to the xml otuput
                    add(output, "stringConstant", token)
                    # skip characters based on the size of the string constant
                    skip = len(token) + 1
                    token = ''
                # see if the character is a symbol
                elif (line[i] in symbols):
                    # add the symbol to the output
                    add(output, "symbol", line[i])
                # check if end of token
                elif (line[i] == ' ' or (i + 1) >= len(line) or (line[i + 1] in symbols)):
                    # see if character needs to be added to built token
                    if (line[i] != ' ' and (i + 1 >= len(line) or (line[i + 1] in symbols))):
                        token = token + line[i]
                    if (token == ''):
                        pass
                    # Check if it is a keyword
                    elif (token in keywords):
                        # add the keyword to the output
                        add(output, "keyword", token)
                        token = ''
                    # check if the value is a number
                    elif (token.isnumeric()):
                        # add integer constant to output
                        add(output, "integerConstant", token)
                        token = ''
                    # check if valid identifier
                    elif ((token[0] == '_' or token[0].isalpha()) and (token[1:-1].isalnum() or len(token) == 1 or len(token) == 2)):
                        # add identifier to output
                        add(output, "identifier", token)
                        token = ''
                    token = ''
                # continue buildin the token if it hasn't been added to output
                if (i < len(line) and line[i] != ' ' and line[i] not in symbols):
                    token = token + line[i]
                # clear the token if it has been added to output
                else:
                    token = ''
    # write the file
    write(output)

# line called at runtime, runs the driver function (main body)
driver()