import bluetooth
import RPi.GPIO as GPIO
lock = 18     
sensor = 17 
GPIO.setmode(GPIO.BCM)  
GPIO.setup(lock, GPIO.OUT)   
GPIO.setup(sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
host = ""
port = 1        
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
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

                if data == b"1":
                        GPIO.output(lock, True)
                        print("Safebox ready to open")
                        send_data = "Safebox ready to open"
                        if GPIO.input(sensor) == GPIO.HIGH:
                            print("Please open Safebox")
                            send_data = "Please open Safebox"
                        else:
                            print("Safebox is already open")
                            send_data = "Safebox is already open"
                            
                else:
                        GPIO.output(lock, False)
                        print("Safebox ready to close")
                        send_data = "Safebox ready to close "
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
