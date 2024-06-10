import serial
import paho.mqtt.client as mqtt

broker = "192.168.0.201" #mqtt broker address
port = 1883              #mqtt port

idTopic = 'idTopic'      #msg topic to publish the msg read by barcode scanner

def connectToMqtt():
    client.connect(broker, port=port)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        
    else:
        print("not Connected to MQTT Broker")
        connectToMqtt();


client = mqtt.Client("RaspberryPiClient") 
client.on_connect = on_connect


connectToMqtt();


client.loop_start()

#serial_port = '/dev/tty1'
serial_port = '/dev/ttyUSB0'
baud_rate = 9600  
ser = serial.Serial(serial_port, baud_rate, timeout=5)

barcode_data = ""

while True:
    if ser.in_waiting > 0:
        incoming_char = ser.read().decode('utf-8')
        print(incoming_char, end='')  # Print each character as it comes in
        barcode_data += incoming_char

            # Check for the end of the barcode message (newline or carriage return)
        if incoming_char == '\n' or incoming_char == '\r':
            print("Complete Barcode:", barcode_data)
            person_id = str(barcode_data.strip())
            client.publish(idTopic, barcode_data)
            barcode_data = ""  
