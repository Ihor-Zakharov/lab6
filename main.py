import tkinter as tk
import customtkinter as ctk 
from abc import ABC, abstractmethod
from datetime import datetime
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
class SingletonMeta(type):
    # static field (_ - static, __ - private)
    _instances = {}

    # "*" allows to take n arguments, the same can be atchieved with a spread operator in JS (...)
    def __call__(cls, *args, **kwargs):
        print(cls._instances)
        if cls not in cls._instances:
            #super class is type, type defines how classes work in python (similar to constructor)
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    
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
class BL(metaclass=SingletonMeta):
    @staticmethod
    def countDigitsSum(dateStr: str) -> int:
      #check the format properly

      # if re.match(r'^\d{2}\.\d{2}\.\d{4}$', dateStr):
        # raise ValueError("The format of date should be DD.MM.YYYY")
      # in JS for (const c of str) { sum += Numbere(c) }
      return sum(int(char) for char in dateStr if char.isdigit())
      
    @staticmethod
    def getAgeVerb(age: int) -> str:
        ageVerbSecondCondition = age == 0 or age % 100 == 12 or age % 100 == 13 or age % 100 == 14 or (age % 10 != 2 and age % 10 != 3 and age % 10 != 4)

        if age == 1:
            return ageVerb["1"]
        elif ageVerbSecondCondition:
            return ageVerb["rest"]
        else:
            return ageVerb["2-4"]

#endregion

#region UI

class UI(metaclass=SingletonMeta):
    def __init__(self, app):
        self.__app = app

        self.nameForm = ctk.CTkEntry(self.__app, height=40, width=350, placeholder_text=verbiage["enterName"])
        
        self.dateForm = ctk.CTkEntry(self.__app, height=40, width=350, placeholder_text=verbiage["enterBirthDate"])

        self.buttomSubmit = ctk.CTkButton(self.__app, height=40, width=350, text=verbiage["submit"], command=self.onSubmit)

        self.msg = ctk.CTkLabel(self.__app, text="")

        self.mountElements()
    
    def mountElements(self):
        self.nameForm.pack(pady=20)
        self.dateForm.pack(pady=20)
        self.buttomSubmit.pack(pady=20)
        self.msg.pack()


    def onSubmit(self):
        try:
            date_obj: datetime = datetime.strptime(self.dateForm.get(), "%d.%m.%Y")

            #code below works like arr1.every((e, i) => e < arr2[i]) in JS
            hadNoBirthdayThisYear = (datetime.today().day, datetime.today().month) < (date_obj.day, date_obj.month)
            #bool var hadNoBirthdayThisYear is being converted to either 1 or 0
            age = datetime.today().year - date_obj.year - hadNoBirthdayThisYear

            message = (f"{msgVerb["0"]}{self.nameForm.get()}{msgVerb["1"]}{str(age)} {BL.getAgeVerb(age)}{msgVerb["2"]}{BL.countDigitsSum(self.dateForm.get())}{msgVerb["3"]}")

            print(message)
            
            self.msg.configure(text=message)
        except ValueError:
            self.msg.configure(text="Дата має бути у форматі DD.MM.YYYY")

#endregion

# Run app

ui = UI(app)

app.mainloop()