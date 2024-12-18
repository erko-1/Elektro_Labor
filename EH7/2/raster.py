import PySimpleGUI as sg
SPALTEN = 2
REIHEN = 4

#layout = [[sg.Button(f'{row}bl, {col}') for col in range(SPALTEN)] for row in range(REIHEN)]
layout = [[sg.Button(f'{row}bl, {col}') for col in range(SPALTEN)] for row in range(REIHEN)]

#event, values = sg.Window('List Comprehensions', layout).read(close=True)
event, values = sg.Window('List Comprehensions', layout).read()
