import cv2
import pickle
import face_recognition
import numpy as np
import paho.mqtt.client as mqtt

broker = "192.168.0.201"  # Broker address
port = 1883
person_id = ''
idTopic = 'idTopic'  # Topic for receiving MQTT messages from reader.py

def connectToMqtt():
    client.connect(broker, port=port)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(idTopic)
    else:
        print("Failed to connect, return code %d\n", rc)
        connectToMqtt()

def on_message(client, userdata, message):
    global person_id
    person_id = message.payload.decode()
    Topic = message.topic
    print(f"Received message '{person_id}' on topic '{Topic}'")

client = mqtt.Client("digiYatra")
client.on_connect = on_connect
client.on_message = on_message

connectToMqtt()

print("Loading encoded faces file")
with open("DigiYatra/DigiYatra Rasp/controller/EncodeFile.p", 'rb') as file:
    encodeListKnownWithId = pickle.load(file)

encodeListKnown, ids = encodeListKnownWithId
print("Loaded encoded faces file")

client.loop_start()

# Initialize webcam
cap = cv2.VideoCapture(0)  # '0' is the ID for the default camera, change if you have multiple cameras

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs, faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        bbox = x1, y1, x2 - x1, y2 - y1
        color = (0, 0, 255)
        label_text = "Unmatched"
        thickness = 2

        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        matchIndex = np.argmin(faceDis)
        matched_id = ids[matchIndex]

        if not person_id:
            label_text = "Scan the QR"

        if matches[matchIndex] and (matched_id == person_id.strip()):
            if count == 15:
                person_id = ''
                count = 0
            else:
                color = (0, 255, 0)
                label_text = f"Matched: {matched_id}"
                count += 1

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
        text_x = x1
        text_y = y2 + 20
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_color = color
        line_type = 2

        cv2.putText(frame, label_text, (text_x, text_y), font, font_scale, font_color, line_type)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
client.loop_stop()
