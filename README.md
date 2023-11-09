# Automatic segment fo labelme

This code is only for who need to generate new data set from sementic segmentation model

## Method

* Step1
  * Using convolutoin to find edge points from each image
    * input
    ![image](./images/0000111.png)
    * visulize
    ![image](./images/vis.png)
    * output(edge_detection)
    ![image](./images/test.png)

* Step2
    * We finding the polygen of output from model and track each center,then use tangent to find points routes

## Run
What you need to do is change file_dir

```bash
python edge_dectection.py
```

##Output in labelme
![image](./images/labelme.png)
