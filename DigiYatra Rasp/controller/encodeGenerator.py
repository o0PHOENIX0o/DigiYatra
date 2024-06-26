import cv2
import face_recognition
import os
import pickle

folderPath = 'DigiYatra/DigiYatra Rasp/controller/Images'

PathList = os.listdir(folderPath)
print("PathList --> ",PathList)
imgList = []
ids = []
for path in PathList:
    # print(os.path.join(folderPath,path))
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    ids.append(os.path.splitext(path)[0])

print(ids)


def findEncodeings(imagesList):
    encodeList=[]
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    
    return encodeList


print("start encoding...")
encodeListKnown = findEncodeings(imgList)
encodeListKnownWithId = [encodeListKnown, ids]
print("done encoding/n")
# print(encodeListKnown)

file = open("DigiYatra/DigiYatra Rasp/controller/EncodeFile.p", 'wb')

pickle.dump(encodeListKnownWithId,file)
file.close()

print("file saved")