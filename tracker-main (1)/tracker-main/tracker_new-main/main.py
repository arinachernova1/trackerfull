# from tracker import *
#
# import sys
#
# app = QtWidgets.QApplication(sys.argv)
# MainWindow = QtWidgets.QMainWindow()
# ui = Ui_MainWindow()
# ui.setupUi(MainWindow)
# MainWindow.show()
#
# ui.label.setText("SFHGS%GNTRERGA$#")
#
# sys.exit(app.exec_())

import pickle #библиотека позволяет работать с файлами
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication #код из документаци модуля
import os
import sqlite3 as sq

with sq.connect("tracker.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        day DATE,
        place TEXT,
        ivent TEXT
        )""")
    cur.execute("SELECT * FROM users WHERE day > 2023-06-17 ORDER BY day DESC LIMIT 5")
    for result in cur:
        print(result)
        

print(os.path.realpath(__file__))
dirname, filename = os.path.split(os.path.realpath(__file__))
print(dirname)
Form, Window = uic.loadUiType(dirname + "\\tracker.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def save_to_file():
    global start_date, calc_date, description, dirname
    # start_date = QDate(2020, 12, 1)
    data_to_save = {"start": start_date, "end": calc_date, "desc": description} #структура данных
    file1 = open(dirname + "\\config.txt", "wb")
    pickle.dump(data_to_save, file1) #используя модуль сохраним объект в файл
    file1.close()
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Трекер события" /sc MINUTE /mo 120 /ed 31/12/2020 /F"""
    task = """schtasks /create /tr "python """ + os.path.realpath(
        __file__) + """" /tn "Трекер события" /sc MINUTE /mo 120 /ed """ + calc_date.toString("dd/MM/yyyy") + """ /F"""
    print(task)
    os.system('chcp 65001')
    os.system(task)


def read_from_file():
    global start_date, calc_date, description, now_date, dirname
    try:
        file1 = open(dirname + "\\config.txt", "rb") #открываем файл на чтение
        data_to_load = pickle.load(file1) #читаем файл
        file1.close()
        start_date = data_to_load["start"]
        calc_date = data_to_load["end"]
        description = data_to_load["desc"]
        print(start_date.toString('dd-MM-yyyy'), calc_date.toString('dd-MM-yyyy'), description)
        form.calendarWidget.setSelectedDate(calc_date)
        form.dateEdit.setDate(calc_date)
        form.plainTextEdit.setPlainText(description) #отображаем считанные ранее данные
        delta_days_left = start_date.daysTo(now_date)  # прошло дней
        delta_days_right = now_date.daysTo(calc_date)  # осталось дней
        days_total = start_date.daysTo(calc_date)  # всего дней
        print("$$$$: ", delta_days_left, delta_days_right, days_total)
        procent = int(delta_days_left * 100 / days_total)
        print(procent)
        form.progressBar.setProperty("value", procent)
    except:
        print("Не могу прочитать файл конфигурации (Может его нет )))!)")


def on_click():
    global calc_date, description, start_date
    start_date = now_date
    calc_date = form.calendarWidget.selectedDate() #считаем дату из календаря
    description = form.plainTextEdit.toPlainText() #cчитаем описание из текст поля
    # print(form.plainTextEdit.toPlainText())
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    print("Clicked!!!")
    save_to_file()
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    # date = QDate(2022, 9, 17)
    # form.calendarWidget.setSelectedDate(date)


def on_click_calendar():
    global start_date, calc_date #текущая и выбранная даты глобальные переменные
    # print(form.calendarWidget.selectedDate().toString('dd-MM-yyyy'))
    form.dateEdit.setDate(form.calendarWidget.selectedDate()) #изменение даты в edit на ту которая выбрана в календаре
    calc_date = form.calendarWidget.selectedDate() #та дата которую мы выбрали на календаре
    delta_days = start_date.daysTo(calc_date)#определяем сколько дней осталось от текущей до выбранной даты
    print(delta_days)
    form.label_3.setText("До наступления события осталось: %s дней )))" % delta_days)


def on_dateedit_change():
    global start_date, calc_date
    # print(form.dateEdit.dateTime().toString('dd-MM-yyyy'))
    form.calendarWidget.setSelectedDate(form.dateEdit.date()) #выбрав дату в edit она так же меняется в календаре
    calc_date = form.dateEdit.date()#выбранная дата это та которую выбрали в edit
    delta_days = start_date.daysTo(calc_date)#определяем сколько дней осталось от текущей до выбранной даты
    print(delta_days)
    form.label_3.setText("До наступления события осталось: %s дней )))" % delta_days)




#def save_file():
 #       text_event = text_edit.toPlainText()
  #      with open("event.txt", "w") as f:
   #         f.write(text_event)
#def save_to_file_event():


def save_information(self):
    #fname = QFileDialog.getSaveFileName(self)[0]
    #try:
         f = open("event.txt", 'w')
        # text = self.plainTextEdit.toPlainText()
         f.write("Это мое важное событие")
         f.close()
    #except FileNotFoundError:
     #   print("Нет такого файла")
  #  print(text_info)

form.pushButton.clicked.connect(on_click) # нажимая кнопку "Отслеживать" выполняется функция
form.calendarWidget.clicked.connect(on_click_calendar) #функция выбора даты в календаре
form.dateEdit.dateChanged.connect(on_dateedit_change) #при выборе даты в edit выполняется функция
form.pushButton_2.clicked.connect(save_information)
#form.pushButton_2.clicked.connect(save_to_file_event)
#form.pushButton_2.clicked.connect(create_file)



start_date = form.calendarWidget.selectedDate()
now_date = form.calendarWidget.selectedDate()
calc_date = form.calendarWidget.selectedDate()
description = form.plainTextEdit.toPlainText()
#text_info = form.plainTextEdit.toPlainText()  #пересчитываются данные
read_from_file() #пересчитываются данные




form.label.setText("Трекер события от %s" % start_date.toString('dd-MM-yyyy'))
on_click_calendar() #вызываем еще раз для синхронизации дат

app.exec_()