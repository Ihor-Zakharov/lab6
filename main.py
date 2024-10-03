import tkinter as tk
import customtkinter as ctk 
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

import re

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("720x480")

app.bind_all("<Button-1>", lambda event: event.widget.focus_set())

class Operations(Enum):
    Undefined = 0,
    Add = 1,
    Sub = 2,
    Mul = 3,
    Div = 4,
    Pow = 5
    
#endregion
    
#region Verbige

#endregion

#region BL

#add getters and setters
class BL():
    def __init__(self):
        self.firstArgStr = ctk.StringVar(value="0")
        self.secondArgStr = ctk.StringVar(value="0")
        self.operation = Operations.Undefined


    @staticmethod
    def concatArg(arg: str, char: int | str):
        if (float(arg) == 0):
            if (int(char) == 0):
                return 0
            else: 
                return char
            
        if char == "." and "." in arg:
            return arg 
        
        return arg + char
    
    @staticmethod
    def isValidArg(arg: str):
        if arg == "0":
            return arg
        
        return bool(re.fullmatch(r'\d+(\.\d+)?', arg))
    
    #rec method (O(logn))
    @staticmethod
    def recursionPow(number: int, pow: int):
        if (pow == 1):
            return number
        
        if (pow % 2 == 0):
            value = BL.recursionPow(number, pow / 2)
            return value * value
        return number * BL.recursionPow(number, pow - 1)
        

    
    def concatFirstArg(self, char: int | str):
        self.firstArgStr.set(BL.concatArg(self.firstArgStr.get(), char))
        print(self.firstArgStr.get())
    
    def concatSecondArg(self, char: int | str):
        self.secondArgStr.set(BL.concatArg(self.secondArgStr.get(), char)) 
    
    def concatCurrentArg(self, char: int | str):
        if self.operation.value == Operations.Undefined.value:
            self.concatFirstArg(char)
            return
        
        self.concatSecondArg(char)

    def setOperation(self, operation: Operations):
        self.operation = operation
    
    def add(self):
        self.firstArgStr.set(str(float(self.firstArgStr.get()) + float(self.secondArgStr.get())))
        self.secondArgStr.set("0")

    def sub(self):
        self.firstArgStr.set(str(float(self.firstArgStr.get()) - float(self.secondArgStr.get())))
        self.secondArgStr.set("0")

    def div(self):
        if float(self.secondArgStr.get()) == 0:
            raise ValueError("0 division is not defined")
         
        self.firstArgStr.set(str(float(self.firstArgStr.get()) / float(self.secondArgStr.get())))
        self.secondArgStr.set("0")

    def mul(self):
        self.firstArgStr.set(str(float(self.firstArgStr.get()) * float(self.secondArgStr.get())))
        self.secondArgStr.set("0")

    #recursion
    def pow(self):
        self.firstArgStr.set(str(BL.recursionPow(float(self.firstArgStr.get()), int(self.secondArgStr.get()))))
        self.secondArgStr.set("0")

    def fireResult(self):
        if (self.operation == Operations.Add):
            self.add()
        elif (self.operation == Operations.Sub):
            self.sub()
        elif (self.operation == Operations.Mul):
            self.mul()
        elif (self.operation == Operations.Div):
            self.div()
        elif (self.operation == Operations.Pow):
            self.pow()
    
    # @property 
    # def firstArgStr(self):
    #     return self.__firstArgStr
    
    # @property 
    # def secondArgStr(self):
    #     return self.__secondArgStr
    
    # @secondArgStr.setter
    # def secondArgStr(self, newValue: str):
    #     if (BL.isValidArg(newValue)):
    #         self.secondArgStr = newValue

    # @firstArgStr.setter
    # def firstArgStr(self, newValue: str):
    #     if (BL.isValidArg(newValue)):
    #         self.secondArgStr = newValue
        
#endregion

#region UI

#Add type to handler
class CharButton():
    def __init__(self, app, value: str, handler):
        if (not BL.isValidArg(value) and value != "."):
            raise ValueError(f"Wrong value has been binded to char button: {value}")
        
        self.__app = app

        self.element = ctk.CTkButton(self.__app, height=40, width=40, text=value, command=lambda: handler(value))

    def pack(self):
        self.element.pack()

class UI():
    def __init__(self, app):
        self.__app = app

        self.bl = BL()

        self.displayedStr = ctk.StringVar(value=(self.bl.firstArgStr.get() + " " + self.bl.secondArgStr.get()))
        self.mountArgControls()
        self.mountForm()
        self.mountOperationsControls()

    def mountForm(self):
        self.msg1 = ctk.CTkLabel(self.__app, textvariable=self.bl.firstArgStr)
        self.msg12 = ctk.CTkLabel(self.__app, textvariable=self.bl.secondArgStr)
        self.msg1.pack()
        self.msg12.pack()

    def mountOperationsControls(self):
        buttonAdd = ctk.CTkButton(self.__app, height=40, width=40, text="+", command=lambda: self.bl.setOperation(Operations.Add))
        buttonSub = ctk.CTkButton(self.__app, height=40, width=40, text="-", command=lambda: self.bl.setOperation(Operations.Sub))
        buttonMul = ctk.CTkButton(self.__app, height=40, width=40, text="*", command=lambda: self.bl.setOperation(Operations.Mul))
        buttonDiv = ctk.CTkButton(self.__app, height=40, width=40, text="/", command=lambda: self.bl.setOperation(Operations.Div))
        buttonPow = ctk.CTkButton(self.__app, height=40, width=40, text="**", command=lambda: self.bl.setOperation(Operations.Pow))
        buttonEquals = ctk.CTkButton(self.__app, height=40, width=40, text="=", command=self.bl.fireResult)

        buttonAdd.pack()
        buttonSub.pack()
        buttonMul.pack()
        buttonDiv.pack()
        buttonPow.pack()
        buttonEquals.pack()

    def mountArgControls(self):
        for i in range(0, 10):
            valueStr = str(i)

            button = CharButton(self.__app, valueStr, handler=self.bl.concatCurrentArg)
            button.pack()

        button = CharButton(self.__app, ".", handler=self.bl.concatCurrentArg)
        button.pack()

ui = UI(app)
app.mainloop()