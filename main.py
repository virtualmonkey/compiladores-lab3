import sys
import os
from antlr4 import *
from YAPLLexer import YAPLLexer
from YAPLParser import YAPLParser
from YAPLVisitor import YAPLVisitor
from antlr4.tree.Trees import Trees
from MyYAPLVisitor import MyYAPLVisitor
from MyYAPLNewVisitor import MyYAPLNewVisitor
from ThreeAddressCodeVisitor import ThreeAddressCodeVisitor
from MipsCodeGenerator import MipsCodeGenerator
from objects.Error import Error

import tkinter as tk
from tkinter import filedialog as fd

# F5F05C

def grafica():
    gui = tk.Tk()
    gui.geometry("1280x1500")
    button = tk.Frame(gui)
    code = tk.Frame(gui)
    gui['bg'] = '#080808'
    button.pack()
    code.pack(fill = tk.X)
    gui.title("Proyecto Compiladores 2")
    user = tk.Text(code)
    user['bg'] = '#080808'
    user.config(fg="#F5F05C")
    windowThreeAddressCode = tk.Text(code)
    windowThreeAddressCode['bg'] = '#080808'
    windowThreeAddressCode.config(fg="#18C6F5")
    windowErrors = tk.Text(width=200)
    windowErrors['bg'] = '#080808'
    windowErrors.config(fg="#5CF577")
    compile = tk.Button(button, text="Compile", command=lambda: main(user.get("1.0", tk.END), windowErrors, windowThreeAddressCode))
    load = tk.Button(button, text="Load File", command=lambda: loadfile(user))
    compile.pack(side=tk.RIGHT, padx=15, pady=20)
    compile.configure(font=("Comic Sans MS", 11))
    compile.config(fg="#080808")
    load.pack(side=tk.LEFT, padx=15, pady=20)
    load.configure(font=("Comic Sans MS", 11))
    load.config(fg="#080808")
    user.pack(side=tk.LEFT,fill=tk.X)
    windowThreeAddressCode.pack(side=tk.LEFT,fill=tk.X)
    windowErrors.pack(fill=tk.Y)
    gui.mainloop()


def loadfile(userIngui):
    userIngui.delete("1.0", tk.END)
    filename = fd.askopenfilename(initialdir = os.getcwd(), title = "Select a file to upload")
    with open(filename, 'r') as f:
        lines = f.read()
        userIngui.insert(tk.END, lines)


def main(program, windowErrors, windowThreeAddressCode):
    windowErrors.delete("1.0", tk.END)
    windowThreeAddressCode.delete("1.0", tk.END)
    data = InputStream(program)
    #lexer
    lexer = YAPLLexer(data)
    stream = CommonTokenStream(lexer)
    #parser
    parser = YAPLParser(stream)
    tree = parser.program()

    # evaluator
    myYAPLVisitor = MyYAPLVisitor()
    myYAPLVisitor.visit(tree)

    myYAPLNewVisitor = MyYAPLNewVisitor(myYAPLVisitor.table, myYAPLVisitor.errors)
    myYAPLNewVisitor.visit(tree)
    
    stringOfErrors = myYAPLNewVisitor.buildErrorString()

    windowErrors.insert(tk.END, stringOfErrors)

    stringOfThreeAddressCode = ''

    if (len(myYAPLNewVisitor.errors) == 0):
        threeAddressCodeVisitor = ThreeAddressCodeVisitor(myYAPLNewVisitor.table)
        threeAddressCode = threeAddressCodeVisitor.visit(tree)
        stringOfThreeAddressCode = str(threeAddressCode)
    else:
        stringOfThreeAddressCode = 'Compiler Error: Cant generate 3-address code if there are syntax errors in loaded file, please fix them and try again'

    windowThreeAddressCode.insert(tk.END,str(stringOfThreeAddressCode))

    arrayOfThreeAddressCode = stringOfThreeAddressCode.split("\n")
    mipsCodeGenerator = MipsCodeGenerator(arrayOfThreeAddressCode)
    mipsCodeGenerator.generateMipsCode()
    print(str(mipsCodeGenerator))

if __name__ == "__main__":
    grafica()
