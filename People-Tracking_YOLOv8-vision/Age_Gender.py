from base64 import b64decode, b64encode
import cv2, PIL, io, html, time
import numpy as np
from PIL import Image, ImageDraw # Load Images & Draw Rectangles.
import torchvision.transforms as transforms # Tensor Transformation.
import torchvision.models as models # ResNet-18 PyTorch Model.
import matplotlib.pyplot as plt # Display Images.

from torch import nn # Neural Network Layers
import torch # YOLO v5 Model
import time # Benchmark extraction
import os

DetectionModel = 'Models/YOLO/Best.onnx'
ClassificationModel1 = 'Models/InceptionResNetV1/Age 0.60 + Gender 91.pt'
ClassificationModel2 = 'Models/ResNet-18/ResNet-18 Age 0.60 + Gender 93.pt'
Classes = 9
Groups = ['00-10', '11-20', '21-30',
          '31-40', '41-50', '51-60',
          '61-70', '71-80', '81-90']

runOn = "cuda:0" if torch.cuda.is_available() else "cpu"

FaceDetector = torch.hub.load('ultralytics/yolov5',
                              'custom',
                              projectPath+'Models/YOLO/Best.onnx',
                              _verbose=False)
FaceDetector.eval()
FaceDetector.to(runOn);

FaceClassifier = models.resnet18(pretrained=True)

FaceClassifier.fc = nn.Linear(512, Classes+2)
FaceClassifier = nn.Sequential(FaceClassifier, nn.Sigmoid())

FaceClassifier.load_state_dict(torch.load(projectPath + ClassificationModel2))

FaceClassifier.eval()
FaceClassifier.to(runOn);

transform = transforms.Compose([transforms.ToTensor()])

def extractFace(IMG, FaceDetector, threshold=0.50, returnFace=True):
    extractedFaces = []
    extractedBoxes = []
    FaceDetections = FaceDetector(IMG).pandas().xyxy[0]
    for detection in FaceDetections.values:
        xmin, ymin, xmax, ymax, confidence = detection[:5]
        if confidence >= threshold:
            bb = [(xmin, ymin), (xmax, ymax)]
            if returnFace:
                w, h = xmax - xmin, ymax - ymin
                currentFace = IMG.crop((xmin, ymin, w+xmin, h+ymin))
                extractedFaces.append(currentFace)
            extractedBoxes.append(bb)

    return extractedFaces, extractedBoxes

def readImage(IMG):
    IMG = IMG.convert('RGB')
    IMG = IMG.resize((200, 200))
    tensorIMG = transform(IMG).unsqueeze(0)
    return tensorIMG

def extractInfo(MyModel, tensorIMG, Verbosity=False):
    tensorIMG = tensorIMG.to(runOn)
    tensorLabels = MyModel(tensorIMG)[0]

    Age = torch.argmax(tensorLabels[:Classes])
    Gender = int(torch.argmax(tensorLabels[Classes:]))
    Gender = 'Male' if Gender == 0 else 'Female'

    C1 = float(torch.max(tensorLabels[:Classes]))
    C2 = float(torch.max(tensorLabels[Classes:]))

    if Verbosity:
        output = [round(float(x), 3) for x in tensorLabels]
        print(output)
    return Groups[Age], Gender, [round(C1, 3), round(C2, 3)]

def returnAnalysis(IMG):
    facesData = []
    IMG = Image.fromarray(IMG)
    faces, bbs = extractFace(IMG, FaceDetector, 0.7)
    for face, bb in zip(faces, bbs):
        tensorIMG = readImage(face)

        Age, Gender, C = extractInfo(FaceClassifier, tensorIMG)

        textBox = f'{Age} {Gender}'
        facesData.append(textBox)

    return bbs, facesData


def draw_label(img, text, pos, bg_color):
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.4
    color = (0, 0, 0)
    thickness = cv2.FILLED
    margin = 2
    txt_size = cv2.getTextSize(text, font_face, scale, thickness)

    end_x = pos[0] + txt_size[0][0] + margin
    end_y = pos[1] - txt_size[0][1] - margin

    cv2.rectangle(img, pos, (end_x, end_y), bg_color, thickness)
    cv2.putText(img, text, pos, font_face, scale, color, 1, cv2.LINE_AA)

videoPath = '/home/sklyvan/Downloads/Act of Rage & Rejecta.mp4'

name, extension = videoPath.split('/')[-1].split('.')
newName = name + ' (FaceDetection)' + '.avi'
newPath = '/'.join(videoPath.split('/')[:-1]) + '/' + newName

output = cv2.VideoWriter(newPath, cv2.VideoWriter_fourcc('M','J','P','G'), 20, (1920, 1080))

print(f"Output to: {newPath}")

videoCapture = cv2.VideoCapture(videoPath)

while videoCapture.isOpened():
    isCorrect, lastFrame = videoCapture.read()
    if isCorrect:
        BoundingBoxes, Labels = returnAnalysis(lastFrame)
        for bb, lbl in zip(BoundingBoxes, Labels):
            (x, y), (w, h) = bb
            print('Face!')
            cv2.rectangle(lastFrame, (int(x), int(y)), (int(w), int(h)), (255, 0, 0), 2)
            draw_label(lastFrame, lbl, (int(x), int(y)), (255, 0, 0))

        output.write(lastFrame)
        cv2.imshow('Frame', lastFrame)
        Key = cv2.waitKey(20)
        if Key == ord('q'): break
    else:
        break
else:
    print("Something went wrong.")

videoCapture.release()
cv2.destroyAllWindows()

