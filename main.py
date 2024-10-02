import tkinter as tk
import customtkinter as ctk 
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# re is meant to be used to check date format in BL method(s)
import re


#region System setting

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#endregion

#region App frame

app = ctk.CTk()
app.geometry("720x480")

# bind method has nothing to do with function propotype bind in JS. It is an equivalent to element.addEventListener
app.bind_all("<Button-1>", lambda event: event.widget.focus_set())
# lambda is an equivalent for () => {} (anon func) in JS

#endregion

#region Core helpers

# metaclasses essentially work like decorators, but for classes, i.e., some sort of fabric pattern is being used
class Operations(Enum):
    Undefined = 0,
    Add = 1,
    
#endregion
    
#region Verbige
    
ageVerb = {
    "1": "рік",
    "2-4": "роки",
    "rest": "років"
}

msgVerb = {
    "0": "Вітаю, ",
    "1": ", вам ",
    "2": ". Сума цифр дати народження: ",
    "3": ". Слава Україні!"
}

verbiage = {
  "enterName": "Введіть своє ім'я",
  "enterBirthDate": "Введіть дату народження (у форматі 11.11.1990)",
  "submit": "зберегти"
} 
    
#endregion

#region BL

#add getters and setters
class BL():
    def __init__(self):
        self.firstArgStr = ctk.StringVar(value="0")
        self.secondArgStr = "0"
        self.operation = Operations.Undefined


    @staticmethod
    def concatArg(arg: str, char: int | str):
        if (float(arg) == 0):
            if (int(char) == 0):
                return
            else: 
                return char
        
        if not BL.isValidArg(char):
            raise ValueError(f"A character other than '.' ({char}) has been added") 
        
        return arg + char
    
    @staticmethod
    def isValidArg(arg: str):
        return bool(re.fullmatch(r'\d+(\.\d+)?', arg))
    
    def concatFirstArg(self, char: int | str):
        self.firstArgStr.set(BL.concatArg(self.firstArgStr.get(), char))
        print(self.firstArgStr.get())
    
    def concatSecondArg(self, char: int | str):
        self.secondArgStr = BL.concatArg(self.secondArgStr, char)
    
    def concatCurrentArg(self, char: int | str):
        if self.operation.value == Operations.Undefined.value:
            self.concatFirstArg(char)
            return
        
        self.concatSecondArg(char)

    def setOperation(self, operation: Operations):
        self.operation = operation

    def fireResult(self):
        if (self.operation == Operations.Add):
            self.firstArgStr.set(str(float(self.firstArgStr.get()) + float(self.secondArgStr)))
            self.secondArgStr = "0"
    
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
        if (not BL.isValidArg(value)):
            raise ValueError(f"Wrong value has been binded to char button: {value}")
        
        self.__app = app

        self.element = ctk.CTkButton(self.__app, height=40, width=40, text=value, command=lambda: handler(value))

    def pack(self):
        self.element.pack()

class UI():
    def __init__(self, app):
        self.__app = app

        self.bl = BL()

        self.mountArgControls()
        self.mountForm()
        self.mountOperationsControls()

    def mountForm(self):
        self.msg = ctk.CTkLabel(self.__app, textvariable=self.bl.firstArgStr)
        self.msg.pack()

    def mountOperationsControls(self):
        buttonAdd = ctk.CTkButton(self.__app, height=40, width=40, text="+", command=lambda: self.bl.setOperation(Operations.Add))
        buttonEquals = ctk.CTkButton(self.__app, height=40, width=40, text="=", command=self.bl.fireResult)

        buttonAdd.pack()
        buttonEquals.pack()

    def mountArgControls(self):
        for i in range(0, 10):
            valueStr = str(i)

            button = CharButton(self.__app, valueStr, handler=self.bl.concatCurrentArg)
            button.pack()

ui = UI(app)
app.mainloop()