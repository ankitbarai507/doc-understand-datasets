import image_bbox_slicer as ibs
im_src = r'C:\Users\Ankit Khushal Barai\Documents\JIO AI COE\Invoice Generator\tiling'.replace('\\', '/')
an_src = r'C:\Users\Ankit Khushal Barai\Documents\JIO AI COE\Invoice Generator\tiling'.replace('\\', '/')
im_dst = r'C:\Users\Ankit Khushal Barai\Documents\JIO AI COE\Invoice Generator\tiling\tiling_op'.replace('\\', '/')
an_dst = r'C:\Users\Ankit Khushal Barai\Documents\JIO AI COE\Invoice Generator\tiling\tiling_op'.replace('\\', '/')

slicer = ibs.Slicer()
slicer.config_dirs(img_src=im_src, ann_src=an_src, 
                   img_dst=im_dst, ann_dst=an_dst)

slicer.keep_partial_labels = True
slicer.ignore_empty_tiles = True

# slicer.slice_by_number(number_tiles=4)
# slicer.visualize_sliced_random()

slicer.slice_by_size(tile_size=(512,512), tile_overlap=0.5)





# import cv2
# import os
# import xml.etree.ElementTree as ET
# import math
# import sys
# import glob

# folder1=sys.argv[1]

# count=0

# def slice(image, xml, size=(2, 2), path='', suffix=''):
#     global count
#     print(image.shape)

#     height, width = image.shape[:2]
#     wSize = int(math.ceil(float(height) / size[0]))
    
#     count+=1
    
#     for r in range(0, height, wSize):
#         window = image[r:r+wSize]
#         wHeight, wWidth = window.shape[:2]
#         tSize = int(math.ceil(float(wWidth) / size[1]))
#         for c in range(0, wWidth, tSize):
#             tile = image[r:r + wSize, c:c + tSize]

#             annotation = ET.Element('annotation')
#             ET.SubElement(annotation, 'folder').text = 'images'
#             ET.SubElement(annotation, 'filename').text = str(
#                 r) + '_' + str(c) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + suffix + '.jpg'
#             ET.SubElement(annotation, 'path').text = 'images/' + str(r) + '_' + \
#                 str(c) + '_' + str(size[0]) + '_' + \
#                 str(size[1]) + '_' + suffix + '.jpg'

#             source = ET.SubElement(annotation, 'source')
#             ET.SubElement(source, 'database').text = 'Unknown'

#             imageSize = ET.SubElement(annotation, 'size')
#             ET.SubElement(imageSize, 'width').text = str(tile.shape[0])
#             ET.SubElement(imageSize, 'height').text = str(tile.shape[1])
#             ET.SubElement(imageSize, 'depth').text = str(tile.shape[2])

#             ET.SubElement(annotation, 'segmented').text = '0'

#             y = r
#             x = c
#             xx = r + wSize
#             yy = c + tSize

#             for member in xml.findall('object'):
#                 xmin = int(member[4][0].text)
#                 ymin = int(member[4][1].text)
#                 xmax = int(member[4][2].text)
#                 ymax = int(member[4][3].text)

#                 if(
#                     xmin > x and xmax > x and
#                     ymin > y and ymax > y and
#                     xmin < yy and xmax < yy and
#                     ymin < xx and ymax < xx
#                 ):
#                     obj = ET.SubElement(annotation, 'object')
#                     ET.SubElement(obj, 'name').text = member[0].text
#                     ET.SubElement(obj, 'pose').text = member[1].text
#                     ET.SubElement(obj, 'truncated').text = member[2].text
#                     ET.SubElement(obj, 'difficult').text = member[3].text

#                     bndbox = ET.SubElement(obj, 'bndbox')
#                     ET.SubElement(bndbox, 'xmin').text = str(xmin - x)
#                     ET.SubElement(bndbox, 'ymin').text = str(ymin - y)
#                     ET.SubElement(bndbox, 'xmax').text = str(xmax - x)
#                     ET.SubElement(bndbox, 'ymax').text = str(ymax - y)

#             tree = ET.ElementTree(annotation)

#             if tree.find('object') != None:

#                 tree.write(path + '/{}.xml'.format(str(count)+'_'+str(r) + '_' + str(c) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + suffix))

#                 # tile = cv2.cvtColor(tile, cv2.COLOR_BGR2RGB)

#                 cv2.imwrite(path + '/{}.jpg'.format(str(count)+'_'+str(r) + '_' + str(c) + '_' + str(size[0]) + '_' + str(size[1]) + '_' + suffix), tile, [cv2.IMWRITE_JPEG_QUALITY, 95])


# for filename in glob.glob(folder1+'/*.PNG'):  # assuming png
#     im = cv2.imread(filename)
#     path=folder1
#     tree = ET.parse(os.path.splitext(filename)[0]+'.xml')
#     slice(image=im,xml=tree,size=(3,3),path=path)
#     print(filename,'done')
    