from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import cv2
import numpy as np
import io
from PIL import Image
import base64
from Helpers import *
import glob
import os
import random

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_img_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	# if 'file[]' not in request.files:
	# 	flash('No file part')
	# 	return redirect(request.url)
	# files = request.files.getlist("file[]")
	# for file1 in files:
	# 	if file1.filename and allowed_img_file(file1.filename):
	# 		filename = secure_filename(file1.filename)
	# 		print(filename)
	# 		filestr = file1.read()
	# 		npimg = np.frombuffer(filestr, np.uint8)
	# 		image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
	# 	print(file1.filename)
	uploads = request.files
	print(uploads)
	for upload in uploads:
		print(upload,type(upload))
	if len(uploads)!=2:
		flash('Select exactly two files - 1 image and another txt annotation file')
		return redirect(request.url)
 
	# for filename, file in request.files.iteritems():
	# 	name = request.files[filename].name
	# 	print(name)
	classes= request.form.getlist('classes')
	print(classes)
	# if file.filename == '':
	# 	flash('No image selected for uploading')
	# 	return redirect(request.url)

	# if file and allowed_file(file.filename):
	# 	flash('Document scan was successful')
	# 	filename = secure_filename(file.filename)
 
		
	filestr = request.files['image'].read()
	npimg = np.frombuffer(filestr, np.uint8)
	image = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
 
	f = request.files['annotation']
	f.save(secure_filename(f.filename))
	f1=open(secure_filename(f.filename),'r')
	lines=f1.readlines()
	f1.close()
	os.remove(secure_filename(f.filename))
	for i in range(len(lines)):
		t=lines[i].strip().split(' ')
		class_type=t[0].split('-')[0]
		if class_type in classes:
			x1=int(t[1].split(',')[0])
			y1=int(t[1].split(',')[1])
			x2=int(t[2].split(',')[0])
			y2=int(t[2].split(',')[1])
			x3=int(t[3].split(',')[0])
			y3=int(t[3].split(',')[1])
			x4=int(t[4].split(',')[0])
			y4=int(t[4].split(',')[1])
			
			bbox = np.array([[[x1, y1], [x2, y2], [x3, y3], [x4,y4]]], np.int32)
			cv2.polylines(image, [bbox], True, (random.randint(10,240),random.randint(10,240),random.randint(10,240)), thickness=2)

	
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	# cv2.imwrite('annotated.png',image)
	file_object = io.BytesIO()
	img= Image.fromarray(Helpers.resize(image,width=600))
	img.save(file_object, 'PNG')
	base64img = "data:image/png;base64,"+base64.b64encode(file_object.getvalue()).decode('ascii')

	return render_template('upload.html', image=base64img )
	# else:
	# 	flash('Allowed image types are -> png, jpg, jpeg')
	# 	return redirect(request.url)

if __name__ == "__main__":
	app.run(debug=True)