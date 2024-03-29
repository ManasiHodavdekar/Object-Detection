import cv2
import numpy as np
import datetime
import time

weights= "yolov3.weights" 
yolo_cfg= "yolov3.cfg"
name=str(datetime.datetime.now().strftime('%d-%b-%Y %H-%H'))

cam= cv2.VideoCapture(0)
time.sleep(2)
ret,frame= cam.read()
img_name="{}.jpg".format(name)
cv2.imwrite(img_name,frame)
print("{} written!".format(img_name))
cam.release()
j = 0 

def get_output_layers(net): # getting the convolution neural networks values from the yolov3.cfg file     
    layer_names = net.getLayerNames()    
    output_layers = [layer_names[i[0] - 1] 
    for i in net.getUnconnectedOutLayers()]     
    return output_layers 

def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h): # drawing shapes on the image after the detection    
    label = str(classes[class_id]) # retrieving all classes that can be detected by the model     
    color = COLORS[class_id] # randomly picking up color from the colors class     
    cv2.rectangle(img, (int(x),int(y)), (int(x_plus_w),int(y_plus_h)), color, 2) # drawing the rectangle around the detected object in image     
    cv2.putText(img, label, (int(x)-10,int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) # selecting font and writing name of object detected on upper left corner of rectangle 
    
image = cv2.imread(img_name) # reading the saved image captured by the camera 
Width = image.shape[1] # calculating the width of image 
Height = image.shape[0] # calculating the height of image 

scale = 0.00392 # this will be used as offset for values or error correction value in the model. this value is achieved by model itself during the training... altering this value will generate errors in prediction 
classes = None # this will be used to read the object name from yolov3.txt file which can be detected 
 
with open("yolov3.txt", 'r') as f: # reading all object name which can be detected by our model
     classes = [line.strip() for line in f.readlines()] 
 
COLORS = np.random.uniform(0, 255, size=(len(classes), 3)) # selecting random color for drawing rectangle 
net = cv2.dnn.readNet(weights, yolo_cfg) # reading weights for model and configuration from yolov3.weights and yolov3.cfg file for deep neutral network 
blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False) # before processing the image, input image will be in 416x416 and will be scaled with offset(scale variable value) will be done according 
net.setInput(blob) # after sampling of image it is been provided to deep neural network for detection 
outs = net.forward(get_output_layers(net)) # runs forward pass to compute outputs of layers listed in output file
class_ids = [] 
confidences = [] 
boxes = [] 
conf_threshold = 0.5 
nms_threshold = 0.4 

 
for out in outs:
      for detection in out:
          scores = detection[5:]
          class_id = np.argmax(scores) #Returns the indices of the maximum values along an axis         
          confidence = scores[class_id]
          if confidence > 0.3: # after detection confidence limit is checked to decide whether the object detected is valid or not
              center_x = int(detection[0] * Width) # if greater than confidence limit then make the calculation for drawing box on the detected part
              center_y = int(detection[1] * Height)             
              w = int(detection[2] * Width)             
              h = int(detection[3] * Height)             
              x = center_x - w / 2             
              y = center_y - h / 2             
              class_ids.append(class_id) # name of the object that is been detected is stored for futher computation             
              confidences.append(float(confidence)) # confidence value if stored for further computation             
              boxes.append([x, y, w, h]) # after calculating the box dimension it is stored for further computation 
 

indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold) # Performs non maximum suppression(post-processing technique for smoothing of surface and avoiding overlap of pixels) given boxes and corresponding scores 
 
for i in indices:     
    i = i[0]
    box = boxes[i]     
    x = box[0]     
    y = box[1]     
    w= box[2]     
    h = box[3]     
    draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h)) # drawing rectangles on the images with stored information from previous computation 
 
count = str(len(indices)) # calculating no of object detected 
cv2.imshow("object detected " + count, image) # image with object detection along with no of detection is displayed on screen 
cv2.imwrite("object-detected " + img_name, image) # detected image is also saved/write on the disk 
cv2.waitKey() # detected image will open and wait for you to press any key to close 
cv2.destroyAllWindows() # this will close any other window  
