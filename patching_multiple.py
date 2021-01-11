# git ls-tree -r master --name-only  LIST files currently being tracked
#
from PIL import Image
import numpy as np
import glob
import sys
import xml.etree.ElementTree as ET
import os
import random

print("Assuming Images in .png format inside each of folders (Paste folder 2 images on Folder 1 images)")

if len(sys.argv) < 4:
    print("Use the command python patching_image.py background_folder to_patch_folder_1 to_patch_folder_2 ... to_patch_folder_N Output_folder ")
    exit(True)


folder1 = sys.argv[1]
# folder2=sys.argv[2]
folder3 = sys.argv[len(sys.argv)-1]  # output folder

to_paste_list = []
print('To patch : ')
for i in range(2, len(sys.argv)-1):
    temp = [ ]
    # putting all folders(stamp,signature,logo) in to_paste_list
    print(sys.argv[i])
    for filename in glob.glob(sys.argv[i]+'/*.png'):
        im = Image.open(filename)
        temp.append(im)
    to_paste_list.append(temp)

if not os.path.exists(folder3):  # Create output folder
    os.makedirs(folder3)

background_list = []
for filename in glob.glob(folder1+'/*.png'):  # assuming png
    im = Image.open(filename)
    background_list.append(im)


count = 1
for img1 in background_list:
    back_im = img1.copy()

    text_img = Image.new('RGBA', back_im.size, (0, 0, 0, 0))
    text_img.paste(back_im, (0, 0))
    back_im = text_img.copy()

    bg_width, bg_height = back_im.size

    # This is the parent (root) tag
    # onto which other tags would be
    # created
    data = ET.Element('annotation')

    # Adding a subtag named `Opening`
    # inside our root tag
    element1 = ET.SubElement(data, 'folder')
    element1.text = "images"

    element2 = ET.SubElement(data, 'filename')
    element2.text = str(count)+'.png'

    element3 = ET.SubElement(data, 'path')
    element3.text = os.path.abspath(folder3+'/'+str(count)+'.png')

    element4 = ET.SubElement(data, 'source')
    element4_1 = ET.SubElement(element4, 'database')
    element4_1.text = "Unknown"

    element5 = ET.SubElement(data, 'size')
    element5_1 = ET.SubElement(element5, 'width')
    element5_1.text = str(bg_width)
    element5_2 = ET.SubElement(element5, 'height')
    element5_2.text = str(bg_height)
    element5_3 = ET.SubElement(element5, 'depth')
    element5_3.text = str(3)

    element6 = ET.SubElement(data, 'segmented')
    element6.text = str(0)

    temp = random.randint(0, 6)  # temp multiple signatures to be patched

    for _ in range(1, temp+1):
        
        obj_type_index=random.choice(range(len(to_paste_list)))
        obj_type=sys.argv[obj_type_index+2]

        img2 = random.choice(to_paste_list[obj_type_index]) # select random image of that object type
        

        to_paste_img = img2.copy()
        to_paste_img = to_paste_img.resize(
            (round(bg_width*0.15), round(bg_height*0.10)), Image.ANTIALIAS)

        to_paste_width, to_paste_height = to_paste_img.size

        tempx = random.randint(2, 8)/10
        tempy = random.randint(2, 8)/10

        back_im.paste(to_paste_img, (round(bg_width*(tempx)), round(bg_height*(tempy))), mask=to_paste_img)  # random.randint(2,8)/10)

        element7 = ET.SubElement(data, 'object')
        element7_1 = ET.SubElement(element7, 'name')
        element7_1.text = obj_type  # 'sign'
        element7_2 = ET.SubElement(element7, 'pose')
        element7_2.text = 'Unspecified'
        element7_3 = ET.SubElement(element7, 'truncated')
        element7_3.text = str(0)
        element7_4 = ET.SubElement(element7, 'difficult')
        element7_4.text = str(0)
        element7_5 = ET.SubElement(element7, 'bndbox')
        element7_5_1 = ET.SubElement(element7_5, 'xmin')
        element7_5_1.text = str(round(bg_width*(tempx)))
        element7_5_2 = ET.SubElement(element7_5, 'ymin')
        element7_5_2.text = str(round(bg_height*(tempy)))
        element7_5_3 = ET.SubElement(element7_5, 'xmax')
        element7_5_3.text = str(round(bg_width*(tempx))+to_paste_width)
        element7_5_4 = ET.SubElement(element7_5, 'ymax')
        element7_5_4.text = str(round(bg_height*(tempy))+to_paste_height)

    back_im.save(folder3+'/'+str(count)+'.png')

    b_xml = ET.tostring(data)

    # Opening a file under the name `items2.xml`,
    # with operation mode `wb` (write + binary)
    with open(folder3+'/'+str(count)+".xml", "wb") as f:
        f.write(b_xml)

    count += 1
