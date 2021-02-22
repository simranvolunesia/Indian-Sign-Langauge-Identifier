from flask import Flask, Response, render_template, flash
import cv2
import numpy as np
import tensorflow as tf
import speech_recognition as sr

#mongodb libraries
from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

app = Flask(__name__)
cam = cv2.VideoCapture(0)

image_x, image_y = 64, 64

img_text = ''

app.config['MONGO_URI'] = "mongodb://localhost:27017/SignLanguageIdentification"
mongo = PyMongo(app)

from keras.models import load_model

def auc(y_true, y_pred):
    auc = tf.metrics.auc(y_true, y_pred)[1]
    keras.backend.get_session().run(tf.local_variables_initializer())
    return auc

global graph
graph = tf.get_default_graph()
classifier = load_model('Trained_model.h5', custom_objects={'auc': auc})

def predictor():
    import numpy as np
    from keras.preprocessing import image
    test_image = image.load_img('1.png', target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    with graph.as_default():
        result = classifier.predict(test_image)
    #result = classifier._make_predict_function()

    if result[0][0] == 1:
        return 'A'
    elif result[0][1] == 1:
        return 'B'
    elif result[0][2] == 1:
        return 'C'
    elif result[0][3] == 1:
        return 'D'
    elif result[0][4] == 1:
        return 'E'
    elif result[0][5] == 1:
        return 'F'
    elif result[0][6] == 1:
        return 'G'
    elif result[0][7] == 1:
        return 'H'
    elif result[0][8] == 1:
        return 'I'
    elif result[0][9] == 1:
        return 'J'
    elif result[0][10] == 1:
        return 'K'
    elif result[0][11] == 1:
        return 'L'
    elif result[0][12] == 1:
        return 'M'
    elif result[0][13] == 1:
        return 'N'
    elif result[0][14] == 1:
        return 'O'
    elif result[0][15] == 1:
        return 'P'
    elif result[0][16] == 1:
        return 'Q'
    elif result[0][17] == 1:
        return 'R'
    elif result[0][18] == 1:
        return 'S'
    elif result[0][19] == 1:
        return 'T'
    elif result[0][20] == 1:
        return 'U'
    elif result[0][21] == 1:
        return 'V'
    elif result[0][22] == 1:
        return 'W'
    elif result[0][23] == 1:
        return 'X'
    elif result[0][24] == 1:
        return 'Y'
    elif result[0][25] == 1:
        return 'Z'
    else:
        return ''

def gen(cam):
    while True:
        global img_text
        success, frame = cam.read()
        frame = cv2.flip(frame, 1)
        img = cv2.rectangle(frame, (425, 100), (625, 300), (0, 255, 0), thickness=2, lineType=8, shift=0)
        cv2.putText(img, img_text, (30, 400), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        ret, jpeg = cv2.imencode('.jpg', img)

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        lower_blue = np.array([0, 58, 30])
        upper_blue = np.array([33, 255, 255])
        imcrop = img[102:298, 427:623]
        hsv = cv2.cvtColor(imcrop, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        mask = cv2.GaussianBlur(mask, (3, 3), 0)

        img_name = "1.png"
        global image_x,image_y
        save_img = cv2.resize(mask, (image_x, image_y))
        cv2.imwrite(img_name, save_img)
        print("{} written!".format(img_name))
        img_text = predictor()
        print(img_text)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/index2.html')
def index2():
    return render_template("index2.html")

@app.route('/login.html', methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route('/loginsli', methods=['POST'])
def loginsli():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            flash("You are logged in as "+session['username'])
            return redirect(url_for('welcome'))

    flash('Invalid username or password')
    return redirect(url_for('login'))

@app.route('/signupsli', methods=['POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})
        existing_email = users.find_one({'email': request.form['email']})

        if existing_email is None:
            if existing_user is None:
                hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                users.insert({'name': request.form['username'], 'password': hashpass, 'email':request.form['email']})
                session['username'] = request.form['username']
                flash("Account created successfully")
                return redirect(url_for('login'))
            else:
                flash('This username is already taken')
                return redirect(url_for('signup'))
        else:
                flash('There is an account registered for this email!!')
                return redirect(url_for('signup'))

@app.route('/feedbacksli',methods=['POST'])
def feedbacksli():
    if request.method == 'POST':
        feedback = mongo.db.feedback
        isEmptyComment = request.form['Submit!!']
        if isEmptyComment == "":
            return redirect(url_for('welcome'))
        else:
            feedback.insert({'Feedback': request.form['Submit!!']})
            flash('Thank you for the feedback!')
            return redirect(url_for('welcome'))

@app.route("/signup.html")
def signup():
    return render_template("signup.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/welcome.html")
def welcome():
    return render_template("welcome.html")

@app.route("/feedback.html")
def feedback():
    return render_template("feedback.html")

@app.route("/ISLtoTextService.html")
def isltotext():
    return render_template("ISLtoTextService.html")

@app.route("/AlternateSpeechToISL.html")
def AlternateSpeechToISL():
    return render_template("AlternateSpeechToISL.html")

@app.route("/video_feed")
def video_feed():
    global cam
    return Response(gen(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/SpeechToISLService.html")
def func():
    return render_template("SpeechToISLService.html")

@app.route("/SpeechToISL.html")
def function():
    return render_template("SpeechToISL.html")

@app.route("/speechtoisl")
def speechtoisl():
        r = sr.Recognizer()
        isl_gif = ['all the best', 'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick',
                   'be careful',
                   'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office',
                   'do you have money',
                   'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry',
                   'flower is beautiful',
                   'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch',
                   'happy journey',
                   'hello what is your name', 'how many people are there in your family', 'i am a clerk',
                   'i am bore doing nothing',
                   'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything',
                   'i go to a theatre', 'i love to shop',
                   'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur',
                   'lets go for lunch', 'my mother is a homemaker',
                   'my name is john', 'nice to meet you', 'no smoking please', 'open the door',
                   'please call an ambulance', 'please call me later',
                   'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage',
                   'please wait for sometime', 'shall I help you',
                   'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care',
                   'there was traffic jam', 'wait I am thinking',
                   'what are you doing', 'what is the problem', 'what is todays date', 'what is your age',
                   'what is your father do', 'what is your job',
                   'what is your mobile number', 'what is your name', 'whats up', 'when is your interview',
                   'when we will go', 'where do you stay',
                   'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra',
                   'ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras',
                   'banglore',
                   'bihar', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic',
                   'coconut', 'crocodile', 'dasara',
                   'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass',
                   'grapes', 'gujrat', 'hello',
                   'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala',
                   'krishna', 'litre', 'mango',
                   'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan',
                   'pass', 'police station',
                   'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop',
                   'sleep', 'southafrica',
                   'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town',
                   'tuesday', 'usa', 'village',
                   'voice', 'wednesday', 'weight']
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            i=0
            while True:
                    print('Say something')
                    audio = r.listen(source)
                    try:
                        a=r.recognize_google(audio)
                        print("You said " + a.lower())
                        if a.lower() in isl_gif:
                            temp1 = a.lower()
                            temp2 = a.lower() + '.gif'
                            return render_template("SpeechToISL.html",VAR1=temp1,VAR2=temp2)
                        else:
                            temp1 = a.lower()
                            temp2 = ''
                            for i in range(len(temp1)):
                                if temp1[i] == " ":
                                    temp2 = temp2 + '$'
                                else:
                                    temp2 = temp2 + temp1[i]
                            return render_template("AlternateSpeechToISL.html",VAR1=temp1,VAR2=temp2)
                    except:
                        print("Couldn't listen")
        return "hello"

if __name__ == '__main__':
    app.secret_key = 'slisecret'
    app.run(debug=True)