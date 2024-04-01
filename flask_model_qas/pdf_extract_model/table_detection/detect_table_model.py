import cv2
import numpy as np

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers

def detect_table_coords(imgfname):
    net = cv2.dnn.readNetFromDarknet(r"C://yolov4_test.cfg",r"C://yolov4_train_best_LO.weights")
    image = cv2.imread(imgfname)
    
    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392
    classes = ['table']
    
    blob = cv2.dnn.blobFromImage(image, 1/255, (608,608), (0,0,0), True, crop=False)
    
    net.setInput(blob)
        # run inference through the network
    # and gather predictions from output layers
    outs = net.forward(get_output_layers(net))
    
    
    # initialization
    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4
    
    # for each detetion from each output layer 
    # get the confidence, class id, bounding box params
    # and ignore weak detections (confidence < 0.5)

    x = 0
    y = 0
    w = 0
    h = 0

    for out in outs:
        for detection in out:
            scores = detection[5:]
            
            
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])
    # apply non-max suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
    
    # go through the detections remaining
    # after nms and draw bounding box
    for i in indices:
        print(i)
      

        i = i[0]
        box = boxes[i]
        
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]

    print("Table has been detected..............................100%")    
        
    return round(x), round(y), round(x + w), round(y + h)
    # print("Detection function===================================")
    # print(x,y,x+w,y+h)
