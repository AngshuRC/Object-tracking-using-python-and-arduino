import cv2
import numpy as np
import serial
yolo = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
arduino = serial.Serial('COM7',9600,timeout=1)
with open("coco.names", "r") as file:
    classes = [line.strip() for line in file.readlines()]
layer_names = yolo.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo.getUnconnectedOutLayers()]

colorRed = (0, 0, 255)
colorGreen = (0, 255, 0)

# #Loading Images
cap = cv2.VideoCapture(0)
while True:
    _, frame = cap.read()

    name = frame
    img = name
    height, width, channels = img.shape

    # # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    yolo.setInput(blob)
    outputs = yolo.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                # print(classes[class_id])
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            cv2.rectangle(img, (x, y), (x + w, y + h), colorGreen, 3)
            cv2.putText(img, label, (x, y + 10), cv2.FONT_HERSHEY_PLAIN, 8, colorRed, 8)

            #  print(label+" ,"+str(len(boxes)))
            if label == "bottle":
                print(f"x: {x}; y: {y}")
                arduino.write(bytes(str(x), 'utf-8'))
    cv2.imshow("Image", frame)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()