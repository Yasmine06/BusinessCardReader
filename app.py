import os
import sqlite3 as sql
from flask import Flask, render_template, request, g
import random
from ocr_core import ocr_core
import cv2
from capture import capture
# connection = sqlite3.connect("contact.db")
UPLOAD_FOLDER = '/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
videoCaptureObject = cv2.VideoCapture(0)
result = True
app = Flask(__name__)
# print(connection.total_changes)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home_page():
    return render_template('index.html')






@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))

            # call the OCR function on it
            extracted_text = ocr_core(file)
            text_id = str(random.randint(0,22)) + extracted_text[0]

            with sql.connect("contact.db") as con:
                con.execute('CREATE TABLE IF NOT EXISTS contact_data (ID TEXT, info TEXT)')
                cur = con.cursor()
                
                cur.execute("INSERT INTO contact_data (ID,info) VALUES (?,?)",(text_id, extracted_text))
                
                con.commit()
                msg = "Record successfully added"
                print(msg)
            
            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   img_src=UPLOAD_FOLDER + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/list')
def list():
   con = sql.connect("contact.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from contact_data")
   
   rows = cur.fetchall()
   print(rows)
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
    app.run()
