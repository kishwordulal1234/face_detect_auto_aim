from flask import Flask, Response, render_template
import cv2
import numpy as np
from fer import FER
from deepface import DeepFace

app = Flask(__name__)

# Load the pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize emotion detector
emotion_detector = FER()

def analyze_face(face_image):
    try:
        analysis = DeepFace.analyze(face_image, actions=['age', 'gender'])
        age = analysis[0]['age']
        gender = analysis[0]['gender']
    except Exception as e:
        age = "Unknown"
        gender = "Unknown"
    
    # Emotion detection
    emotions = emotion_detector.detect_emotions(face_image)
    if emotions:
        emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
    else:
        emotion = "Unknown"
    
    return age, gender, emotion

def generate_frames():
    camera_index = 0
    video_capture = cv2.VideoCapture(camera_index)

    if not video_capture.isOpened():
        raise RuntimeError(f"Error: Camera with index {camera_index} could not be opened.")

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, y, w, h = faces[0]
            face_image = frame[y:y+h, x:x+w]
            age, gender, emotion = analyze_face(face_image)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # Red square
            distance = 1 / (w / 100)

            fps = 30
            suspicion = "High" if emotion in ["angry", "fear"] else "Normal"
            surroundings = "Crowded"

            # Use this data to update the second box (you'll integrate this into script.js)
        else:
            distance = "N/A"
            suspicion = "Normal"
            fps = "N/A"
            surroundings = "Clear"

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
