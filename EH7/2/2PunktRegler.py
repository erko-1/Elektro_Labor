import PySimpleGUI as sg
import time
import threading

# der Einfachheit halber verwenden wir hier globale Variablen.
# ist zwar nicht best practise, aber funktioniert


hysterese=1
tist=60
tsoll=0
runthread=0
graphx=0
# code für die Regelung. Dieser läuft nach Start unabhängig vom Fenster in einem eigenen thread

def regelung_thread(window):
    global tsoll
    global tist
    global hysterese
    global runthread
    # hier den code für die Regelung einfügen (innerhalb der while Scheife )
    # Messung der Spannung am NTC
    # Umrechnung der Spannung in den Widerstandswert
    # Umrechnung Widerstand in Temperatur
    # Lampe schalten
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    while(runthread==1):
        print('spannung am NTC:',0)
        print('Widerstand des NTC:',0)
        print('Isttemperatur:',tist)
        tsoll=tsoll+1
        tist=tist+1
        time.sleep(3)
        window.write_event_value('-UPDATE-',tist) # schreibe nach jedem Durchlauf ein Update-event, um die
        #ist-Temperatur in Fenster anzuzeigen
        
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    window.write_event_value('-THREAD DONE-', '')
    
# mit dieser Funktion wird der thread zur Regelung gestartet

def regelung():
    threading.Thread(target=regelung_thread, args=(window,), daemon=True).start()

# Fensterlayout
graph = sg.Graph(canvas_size=(400, 200),
                 graph_bottom_left=(0, 0),
                 graph_top_right=(400, 200),
                 background_color='white',
                 key='graph')

layout = [[sg.Output(size=(80,10))],
          [graph],
          [sg.Text("Tsoll         "),sg.Slider(range=(20,70), orientation='h', default_value=30, key = '-TSOLL-'),sg.Text("Tist: "),sg.Text(size=(8,1),key='-TIST-')],
          [sg.Text("Hysterese"),sg.Slider(range=(0.5,2), orientation='h', default_value=1, resolution=0.1, key = '-HYSTERESE-')],
          [sg.Button('Start'), sg.Button('Stop'),sg.Button('Apply'), sg.Button('Exit')]  ]

window = sg.Window('2-Punkt-Regler', layout)

while True:             # Event Loop ++++++++++++++++++++++++++++++++++++++++
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break # hier auch die Lampe ausschalten
    
    if event == 'Start':
        print('Regelung gestartet')
        runthread=1
        graphx=0
        graph.erase()
        regelung() #start des Regelungs-threads
    
    elif event== 'Stop':
        runthread=0
    
    elif event == 'Apply': # erst durch apply werden die Werte der Slider in die Variablen übertragen
        tsoll=(values['-TSOLL-'])
        hysterese=(values['-HYSTERESE-'])
        
    elif event == '-UPDATE-': # wenn von Regelthread ein 'update' gesendet wird, kann man die Isttemperatur updaten
        window['-TIST-'].update(str(tist))  
        graph.draw_point([graphx,tist*2], size=2,color="black")
        graphx=graphx+1
        if graphx>400:
            graphx=0
            graph.erase()
    elif event == '-THREAD DONE-':
        print('Regelung gestoppt')
    
    print(event, values)
window.close()
