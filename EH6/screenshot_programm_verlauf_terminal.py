epr@raspberrypi:~ $ cd Desktop/
epr@raspberrypi:~/Desktop $ sudo python3 lies_tds_raspi.py 
Traceback (most recent call last):
  File "/home/epr/Desktop/lies_tds_raspi.py", line 7, in <module>
    dateiobjekt = open(dateiname, "wb")
FileNotFoundError: [Errno 2] No such file or directory: '/home/pi/Desktop/EPR_TDS_20231121100534.bmp'
epr@raspberrypi:~/Desktop $ sudo python3 lies_tds_fenster.py 
epr@raspberrypi:~/Desktop $ lsusb
Bus 001 Device 005: ID 0a81:0205 Chesen Electronics Corp. PS/2 Keyboard+Mouse Adapter
Bus 001 Device 007: ID 0699:0363 Tektronix, Inc. Tektronix TDS1002B
Bus 001 Device 004: ID 05e3:0608 Genesys Logic, Inc. Hub
Bus 001 Device 003: ID 0424:ec00 Microchip Technology, Inc. (formerly SMSC) SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Microchip Technology, Inc. (formerly SMSC) SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
epr@raspberrypi:~/Desktop $ sudo python3 lies_tds_fenster.py 
Traceback (most recent call last):
  File "/home/epr/Desktop/lies_tds_fenster.py", line 53, in <module>
    dateiobjekt = open(dateiname, "wb")
FileNotFoundError: [Errno 2] No such file or directory: '/home/epr5-tuer/Schreibtisch/EPR_TDS_20231121100641.bmp'
epr@raspberrypi:~/Desktop $ sudo python3 lies_tds_fenster.py 
epr@raspberrypi:~/Desktop $ 

