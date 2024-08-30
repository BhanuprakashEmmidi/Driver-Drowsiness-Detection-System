from flask import Flask, render_template, request, url_for, session, redirect, flash, Response
from flask_mysqldb import MySQL
import MySQLdb.cursors
import numpy as np

import os
import cv2
import re

import tensorflow as tf
from tensorflow.keras.models import model_from_json
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from werkzeug.utils import secure_filename

face_haar_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


cap=cv2.VideoCapture(0)
app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

UPLOAD_FOLDER = 'static/tests/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 


model = model_from_json(open("models.json", "r").read())
model.load_weights('model_weight.h5')

def allowed_file(filename):
    """ Checks the file format when file is uploaded"""
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS) 
    
def gen_frames():
    while True:
        ret,frame=cap.read()
        if not ret:
            break
        else:
            gray_img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.32, 5)
            for (x,y,w,h) in faces_detected:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=7)
                roi_gray=gray_img[y:y+w,x:x+h]
                roi_gray=cv2.resize(roi_gray,(48,48))
                img_pixels = image.img_to_array(roi_gray)
                img_pixels = np.expand_dims(img_pixels, axis=0)
                img_pixels = np.repeat(img_pixels, 3, axis=-1)  
                img_pixels /= 255

                predictions = model.predict(img_pixels)
                print("predictions:", predictions)
                max_index = np.argmax(predictions, axis=1)
                print("max_index:", max_index[0])

                drowsy = ('Drowsiness', 'Normal', 'Normal', 'Drowsiness')
                predicted_drowsy = drowsy[max_index[0]]
                cv2.putText(frame, predicted_drowsy, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            resized_img = cv2.resize(frame, (1000, 700))

            ret, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'drowsy'
mysql = MySQL(app)

@app.route('/',methods = ['GET','POST'])
def first():
    return render_template('first.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# @app.route('/camera')
# def camera():
#     return render_template('camera.html')     
 

@app.route('/login', methods = ['GET',"POST"])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM people WHERE username = %s AND password = %s AND status="Approved"' , (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            global Id
            session['Id'] = account['Id']

            Id = session['Id']
            global Username
            session['username'] = account['username']
            Username = session['username']
            return redirect(url_for('index'))
        else:
            flash('Incorrect username/password! Please login with correct credentials')
            return redirect(url_for('login'))

    return render_template('login.html', msg=msg)

@app.route('/register',methods= ['GET',"POST"])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'mobile' in request.form and'loginid' in request.form and 'address' in request.form and 'company' in request.form and 'state' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile = request.form['mobile']
        loginid = request.form['loginid']
        address = request.form['address']
        company = request.form['company']
        state = request.form['state']
        
        
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
        pattern = re.compile(reg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM people WHERE Username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not re.search(pattern,password):
            msg = 'Password should contain atleast one number, one lower case character, one uppercase character,one special symbol and must be between 6 to 10 characters long'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO people VALUES (NULL, %s, %s, %s, %s,%s, %s, %s, %s,"Approved")', (username, password, email, mobile,loginid,address,company,state))
            mysql.connection.commit()
            flash('You have successfully registered! Please proceed for login!')
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
        return msg
    return render_template('register.html', msg=msg)


@app.route("/index", methods=['GET', 'POST'])
def index():
	return render_template("index.html")

def predict_label(img_path):
    test_image = image.load_img(img_path, target_size=(48, 48))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)  # Add batch dimension
    test_image = test_image / 255.0
	# test_image = test_image.reshape(1, 48,48,1)
    predict_x=model.predict(test_image) 
    preds=np.argmax(predict_x, axis=1)
    print("predict_x:", predict_x)
    print("preds:", preds[0])
    drowsy = ('Drowsiness', 'Normal', 'Normal', 'Drowsiness')
    result = drowsy[preds[0]]
    return result, predict_x

@app.route('/uploadimage', methods=['POST'])
def uploadimage():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(img_path)
            print(filename) 
            predict_result, predict_x = predict_label(img_path)
                
            sentence = predict_result
            cur = mysql.connection.cursor()    
            cur.execute("INSERT INTO review(sentence,filename,userid) VALUES ( %s, %s,%s) ", (sentence,filename,Id))
            mysql.connection.commit()
            cur.close()
            return render_template("index.html", prediction = predict_result, img_path = img_path, predict_x=predict_x[0][0])
    return render_template('index.html')         

    
@app.route("/performance", methods=['GET', 'POST'])
def performance():
	return render_template("performance.html") 

@app.route('/chart3')
def chart3():
    legend = "review by sentence"
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("SELECT sentence from review GROUP BY sentence")
        rows = cursor.fetchall()
        labels = list()
        i = 0
        for row in rows:
            labels.append(row[i])
        
        cursor.execute("SELECT COUNT(id) from review GROUP BY sentence")
        rows = cursor.fetchall()
        values = list()
        i = 0
        for row in rows:
            values.append(row[i])
        cursor.close()
    except:
        print ("Error: unable to fetch items")    
    return render_template('chart3.html', values=values, labels = labels, legend=legend)

if __name__ == '__main__':
    app.run()