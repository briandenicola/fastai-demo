#https://www.roytuts.com/upload-and-display-image-using-python-flask/

import os
import uuid
import urllib.request
from fastai2.learner import load_learner
from flask import Flask, flash, request, redirect, url_for, render_template

app = Flask(__name__) 
learner_inference = load_learner('../models/coins.pkl')
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		return redirect(request.url)
	
	file = request.files['file']

	if file.filename == '':
		return redirect(request.url)

	if file:
		filename = str(uuid.uuid4())
		filepath = os.path.join('./static/uploads', filename)
		file.save(filepath)
		pred,pred_idx,prob = learner_inference.predict(filepath)
		
		confident_level = f'{prob[pred_idx]:.04f}'

		return render_template('upload.html', coin_type=pred, filename=filename, confident_level=(confident_level))
	else:
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)