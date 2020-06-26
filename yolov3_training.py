# -*- coding: utf-8 -*-
"""yolov3-training.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pdOJ7VonoprdcNvSrsC7wqfxVtd3_3EA
"""

import os.path
import shutil
from google.colab import drive
drive.mount('/content/drive')

!wget http://www.iapr-tc11.org/dataset/ICDAR_SignatureVerification/SigComp2009/SigComp2009-training.zip

!unzip -P 'I hereby accept the SigComp 2009 disclaimer.' '/content/SigComp2009-training.zip'

!tar xvzf '/content/NISDCC-offline-all-001-051-6g.tgz'

import os
os.chdir('/content/NISDCC-offline-all-001-051-6g')
!ls -1 | wc -l

os.chdir('/content')
!wget http://image.ntua.gr/iva/datasets/flickr_logos/flickr_logos_27_dataset.tar.gz

!tar xvzf '/content/flickr_logos_27_dataset.tar.gz'

!tar xvzf '/content/flickr_logos_27_dataset/flickr_logos_27_dataset_images.tar.gz'

os.chdir('/content/flickr_logos_27_dataset_images')
!ls -1 | wc -l

!du -sh '/content/NISDCC-offline-all-001-051-6g'

!du -sh '/content/flickr_logos_27_dataset_images'

os.chdir('/content')
!wget 'http://93.174.95.29/main/1309000/90db32d070cfb70ca617e655d5c35529/Alfred%20V.%20Aho%2C%20Monica%20S.%20Lam%2C%20Ravi%20Sethi%2C%20Jeffrey%20D.%20Ullman%20-%20Compilers%20-%20Principles%2C%20Techniques%2C%20and%20Tools-Pearson_Addison%20Wesley%20%282006%29.pdf'

!python back_rem.py '/content/NISDCC-offline-all-001-051-6g'

!python back_rem.py '/content/flickr_logos_27_dataset_images'

os.chdir('/content/NISDCC-offline-all-001-051-6g')
!rm *.PNG
os.chdir('/content/flickr_logos_27_dataset_images')
!rm *.jpg

os.chdir('/content')
!cp -r '/content/NISDCC-offline-all-001-051-6g' '/content/drive/My Drive/yolov3/'
!cp -r '/content/flickr_logos_27_dataset_images' '/content/drive/My Drive/yolov3/'

!pip install PyMuPDF

os.chdir('/content')
!python generate_ebook_patching.py '/content/Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman - Compilers - Principles, Techniques, and Tools-Pearson_Addison Wesley (2006).pdf' 4 600 '/content/drive/My Drive/yolov3/invoice/'

!du -sh '/content/drive/My Drive/yolov3/invoice'

!cp -r '/content/drive/My Drive/Jio-AI/stamp' '/content/drive/My Drive/yolov3/'

!rm -r '/content/drive/My Drive/yolov3/invoice_multiple_dataset'

os.chdir('/content/drive/My Drive/yolov3')
!python patching_multiple.py invoice sign stamp logo invoice_multiple_dataset

os.chdir('/content/drive/My Drive/yolov3')
!python partition_dataset.py -x -i "/content/drive/My Drive/yolov3/invoice_multiple_dataset" -r 0.1

os.chdir('/content/drive/My Drive/yolov3/invoice_multiple_dataset')
!rm *.png *.xml

os.chdir('/content/drive/My Drive/yolov3')
!python convert_voc_to_yolo.py '/content/drive/My Drive/yolov3/invoice_multiple_dataset/valid' sign stamp logo

os.chdir('/content/drive/My Drive/yolov3')
!python convert_voc_to_yolo.py '/content/drive/My Drive/yolov3/invoice_multiple_dataset/train' sign stamp logo

"""# Prepration

- In order to train the Yolo v3 model, we will need to compile `darknet` which is an open source neural network framework written in C and CUDA. 
- Once the `darknet` is compiled, we will download the exported data set from HyperLabel


**Note**: Before starting to work, change the runtime to use the GPU.

If you don't have any dataset or pretrained model (weight) for that dataset, you can use our demo data set and trained weight.

Copy the following files to your Google drive (create a new folder called `ml` in your Google drive and put the files in there)

- [Dataset](https://drive.google.com/file/d/1wxHNFR2xXx6wJMJR2ey2NP_rWFJNs8-I/view?usp=sharing)
- [Pre trained weight](https://drive.google.com/file/d/1-5iEJhBgwRGBZ_ZBfO6Juo2tF6lGa4b6/view?usp=sharing)


### Clone darknet
"""

!cp '/content/drive/My Drive/yolov3/train.txt' '/content/darknet/data/'
!cp '/content/drive/My Drive/yolov3/valid.txt' '/content/darknet/data/'

os.chdir('/content')
!git clone https://github.com/AlexeyAB/darknet

"""### Compile darknet"""

os.chdir('/content/darknet')
!sed -i 's/GPU=0/GPU=1/g' Makefile
!cat Makefile
!make

"""### Download the data set exported from HyperLabel"""

import os.path
import shutil
from google.colab import drive

if not os.path.exists('/content/gdrive'):
  drive.mount('/content/gdrive')
  
DOWNLOAD_LOCATION = '/content/darknet/data/'
DRIVE_DATASET_FILE = '/content/gdrive/My Drive/yolo-dataset.zip' #adjust path/name of dataset which is in your G-drive

shutil.copy(DRIVE_DATASET_FILE, DOWNLOAD_LOCATION)

print('Successfully downloaded the dataset')

"""### Unzip the dataset"""

!unzip data/yolo-dataset.zip -d data/ # adjust the dataset filename which you have downloaded from Google drive

"""##Training the model

- Download the initial weight
- Train the model

### Download initial pre-trained weights for the convolutional layers (If you have already trained and saved the weights to your Google drive, you can skip this)
"""

!wget https://pjreddie.com/media/files/darknet53.conv.74

"""### Set Yolo configurations

We need to set configurations for Yolo in order to properly train. There are few settings which we need to change in the default yolov3.cfg file.

- batch
- subdivisions (if you get memory out error, increase this 16, 32 or 64)
- max_batches (it should be classes*2000)
- steps (it should be 80%, 90% of max_batches)
- classes (the number of classes which you are going to train)
- filters (the value for filters can be calculated using (classes + 5)x3 )

Change the values below as per your requirement
"""

!sed -i 's/batch=1/batch=64/g' cfg/yolov3.cfg
!sed -i 's/subdivisions=1/subdivisions=32/g' cfg/yolov3.cfg
!sed -i 's/max_batches = 500200/max_batches = 6000/g' cfg/yolov3.cfg
!sed -i 's/steps=400000,450000/steps=4000,5000/g' cfg/yolov3.cfg
!sed -i 's/classes=80/classes=3/g' cfg/yolov3.cfg
!sed -i 's/filters=255/filters=24/g' cfg/yolov3.cfg
!cat cfg/yolov3.cfg

"""**Now we are moving forward with the training part. If you have already trained the model, you can fetch them from Google drive and skip the training part.**"""

# Only run this cell, if you have already trained the model and have weights and backup files in your Google drive
# (Optional) Download the pretrained weight from Google drive


  
BACKUP_FOLDER = '/content/darknet/backup'
DRIVE_YOLO_BACKUP = '/content/gdrive/My Drive/yolov3/yolov3_last.weights'

shutil.copy(DRIVE_YOLO_BACKUP, BACKUP_FOLDER)

print('Successfully fetched the pretrained files for Yolo from Google drive')

"""### Start the training

It will take a long time to complete, so sit back and relax

Note: If during training you see nan values for avg (loss) field - then training goes wrong, but if nan is in some other lines - then training goes well.

- file yolo-obj_last.weights will be saved to the darknet/backup for each 100 iterations
- file yolo-obj_xxxx.weights will be saved to the darknet/backup for each 1000 iterations
- After each 100 iterations if you want, you can stop and later start training from this point. For example, after 2000 iterations you can stop training, and later just start training using: darknet detector train data/obj.data yolov3.cfg backup/yolo-obj_2000.weights
"""

# use the line below to train a fresh model
os.chdir('/content/darknet')
# !./darknet detector train data/obj.data cfg/yolov3.cfg darknet53.conv.74

# use the line below to retrain your previous saved weight
!./darknet detector train data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights

# Once you have trained your model, you can save them to your Google drive. So that next time, you don't need to retrain
# This step is optional, you can skip it if you want
import os.path
import shutil
from google.colab import drive

# if not os.path.exists('/content/gdrive'):
#   drive.mount('/content/gdrive')
  
YOLO_BACKUP = '/content/darknet/backup/yolov3_last.weights' #adjust the backup file name or keep it default
DRIVE_DIR = '/content/drive/My Drive/yolov3/trained_weights/' #adjust path in your Google drive, or keep it default

shutil.copy(YOLO_BACKUP, DRIVE_DIR)

print('Saved training data to drive at: ' + DRIVE_DIR)

"""## Running predictions"""

os.chdir('/content/darknet')
!./darknet detector test data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights '/content/drive/My Drive/yolov3/invoice_multiple_dataset/valid/78.png' -thresh 0.05

"""### Display result"""

def display_image(file_path = '/content/darknet/predictions.jpg'):
    import cv2
    import matplotlib.pyplot as plt
    import os.path

    if os.path.exists(file_path):
      img = cv2.imread(file_path)
      show_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
      plt.imshow(show_img)
    else:
      print('failed to open file')
    
display_image()

!wget https://southeastasia1-mediap.svc.ms/transform/zip?cs=fFNQTw
