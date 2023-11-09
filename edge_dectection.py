import cv2
import numpy as np
import os
import json
import base64,io
import math

def edge2labelme(classes,points):
    initial_shape = {
        "label":None,
        "points":[],
        "group_id":"null",
        "shape_type": "polygon",
        "flags": {}
    }
    if points:
        if initial["shapes"] == []:
            gate = False
        else:
            for i in initial["shapes"]:           
                if i["label"] == str(classes):
                    i["points"].append(points)
                    gate = True
                    
                    break
                else:
                    gate =False
                   
                    continue

        if gate == False:
            
            initial_shape["label"]=str(classes)
            initial_shape["points"].append(points)
            initial["shapes"].append(initial_shape)


def convolve2D(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        
    else:
        imagePadded = image

    # Iterate through image
    for y in range(1,imagePadded.shape[1]):
        # Exit Convolution
        if y > image.shape[1] - yKernShape:
            break
        # Only Convolve if y has gone down by the specified Strides
        if y % strides == 0:
            for x in range(1,imagePadded.shape[0]):
                # Go to next row once kernel is out of bounds
                if x > image.shape[0] - xKernShape:
                    break
                try:
                    # Only Convolve if x has moved by the specified Strides
                    if x % strides == 0:
                        
                        checked_kernel = (kernel * imagePadded[x-1: x +2, y-1: y + 2])
                        
                        if len(np.unique(checked_kernel))>1:
                            output[x,y] = imagePadded[x,y]
                            if imagePadded[x,y] !=0:
                                edge2labelme(imagePadded[x,y],[y,x])

                        else:
                            output[x,y] = 0
                except:
                    break

    return output


def sort_points(json):
    
    shape = json["shapes"]
    for classes in shape:
        points = classes["points"]
        print(classes['label'])
        print(len(points))
        center = [sum(x[0] for x in points) / len(points), sum(x[1] for x in points) / len(points)]
        def polar_angle(point):
            return math.atan2(point[1] - center[1], point[0] - center[0])
        sorted_coordinate = sorted(points,key=polar_angle)
        k = 0
        true_coordinate = []
        for i in range(int(len(sorted_coordinate))//2):
            try:
                tmp_coordinate =[ sorted_coordinate[i+k] ]+ [sorted_coordinate[i+k+10]]
            except IndexError:
                continue
            true_coordinate = true_coordinate+ tmp_coordinate
            k = k+30
        classes["points"] =  true_coordinate
        print(len( classes["points"]))
if __name__ =="__main__":
    
    path = os.path.join("0000111.png")
    JEPG_path = os.path.join("000011.jpg")
    json_path = os.path.join("000011.json")
    initial = {
        "version": "5.1.1",
        "flags": {},
        "shapes":[],
        "imagePath":f"{JEPG_path}",
        "imageData":None,
        "imageHeight":720,
        "imageWidth":1280
    
    }
    img = cv2.imread(path)
    # print(np.unique(img)) # unique list
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    kernel = np.ones((3,3))
    b64_string = base64.b64encode(open(JEPG_path,'rb').read())
    # print(b64_string[0:10])
    initial["imageData"] = str(b64_string)[2:]
    out = convolve2D(img,kernel,padding=1)
    sort_points(initial)
    with open(json_path,"w") as file:
        json.dump(initial,file,indent=1)
    cv2.imwrite("test.png",out+100)