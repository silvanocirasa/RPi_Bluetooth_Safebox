import bluetooth
import RPi.GPIO as GPIO
lock = 18 #Magnetschlösser 1+2
sensor = 17 #Endschalter
GPIO.setmode(GPIO.BCM)  
#definiere Magnetschlösser als Output
GPIO.setup(lock, GPIO.OUT)    
#definiere Endschalter als Pull-Down Input
GPIO.setup(sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
host = ""
port = 1        
#definiere Bluetooth-Service
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM) 
print('Bluetooth Socket Created')
#versuche mit bluetooth service zu verbinden
try: 
        server.bind((host, port))
        print("Bluetooth Binding Completed")
except:
        print("Bluetooth Binding Failed")
server.listen(1) 
client, address = server.accept()
print("Connected To", address)
print("Client:", client)
try:
        while True:

                data = client.recv(1024)
                print(data)
        #Anforderung von App zum Öffnen 
                if data == b"1":
                #setze Magnetschlösser auf 1 (öffnen)
                        GPIO.output(lock, True) 
                        print("Safebox ready to open")
                        #sende Nachricht an App
                        send_data = "Safebox ready to open" 
                #Abfrage Endschalter (offen/geschlossen)
                        if GPIO.input(sensor) == GPIO.HIGH: 
                            print("Please open Safebox")
                            send_data = "Please open Safebox"
                        else:
                            print("Safebox is already open")
                            send_data = "Safebox is already open"
        #Anforderung von App zum Schliessen
                else:
                        #setze Magnetschlösser auf 0 (schliessen)
                        GPIO.output(lock, False) 
                        print("Safebox ready to close")
                        #sende Nachricht an App
                        send_data = "Safebox ready to close " 
                #Abfrage Endschalter (offen/geschlossen)
                        if GPIO.input(sensor) == GPIO.HIGH:
                            print("Safebox Closed")
                            send_data = "Safebox Closed"
                        else:
                            print("Please close Safebox")
                            send_data = "Please close Safebox"
                client.send(send_data)
except:
        GPIO.cleanup()
        client.close()
        server.close()
