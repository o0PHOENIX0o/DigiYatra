import cv2
import pickle
import face_recognition
import numpy as np

person_id = 'Elon'

cap = cv2.VideoCapture(0)

cap.set(3,406)
cap.set(4,575)

print("loading encode file")
with open("face_recognition/EncodeFile.p",'rb') as file:
    encodeListKnownWithId = pickle.load(file)


encodeListKnown, ids = encodeListKnownWithId
print(ids)
print("loaded encode file")

bgimg = cv2.imread('face_recognition/resources/frame.png')

while True:
    success, img  = cap.read()

    imgs = cv2.resize(img,(0,0), None, 0.25, 0.25)
    imgs = cv2.cvtColor(imgs,cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgs)
    encodeCurFrame = face_recognition.face_encodings(imgs,faceCurFrame)

    for encodeFace, faceLoc in zip(encodeCurFrame,faceCurFrame):
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        bbox = x1,y1, x2-x1, y2-y1
        color = (0, 0, 255)  # Blue color
        label_text = "Unmatched"
        thickness = 2


        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)

        matchIndex = np.argmin(faceDis)
        print("min value ", matchIndex)
        matched_id = ids[matchIndex]

        if (matched_id == person_id and matches[matchIndex]):
            color = (0, 255, 0)
            label_text = f"Matched: {matched_id}"
            print("face matched")
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        text_x = x1
        text_y = y2 + 20  
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        font_color = color 
        line_type = 2
      
        cv2.putText(img, label_text, (text_x, text_y), font, font_scale, font_color, line_type)

    cv2.imshow("fave recognition", img)
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()