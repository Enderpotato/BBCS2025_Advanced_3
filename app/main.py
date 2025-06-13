from flask import Flask, render_template,Response,jsonify
import cv2
import time
import threading
import pygame
import random
from modelmodel import get_the_model, annotate_image

model = get_the_model()

app = Flask(__name__)
cam = cv2.VideoCapture(0)
pygame.init()
pygame.mixer.init()

audios = ["static/wakeup.mp3","static/awesome.mp3","static/doinggreat.mp3","static/giveup.mp3"]

last_played = 0
audio_cooldown = 10 
is_playing_audio = False

def is_distracted(detections, confidence_threshold=0.9):
    class_list = detections.data["class_name"]

    is_distracted = class_list.tolist().count("Distracted") > 0
    eyes_closed = class_list.tolist().count("Eyes closed") > 0

    confidence = detections.confidence.tolist()[0] if len(detections.confidence) > 0 else 0

    #hi enoch put the model logic here or smt return true if distracted | DONE boyy
    return (is_distracted or eyes_closed) and confidence > confidence_threshold

def play_sound_once():
    global last_played, is_playing_audio
    now = time.time()
    if now - last_played > audio_cooldown:
        last_played = now
        is_playing_audio = True
        def play():
            sound = audios[random.randint(0,len(audios) - 1)]
            pygame.mixer.music.load("static/wakeup.mp3")
            pygame.mixer.music.play()
            time.sleep(2)
            global is_playing_audio
            is_playing_audio = False
        threading.Thread(target=play, daemon=True).start()


def gen_frames():
    while True:
        okay, frame = cam.read() #ret is boolean, True if successful
        if not okay:break

        annotated, detections = annotate_image(frame, model)
        
        if is_distracted(detections):
            play_sound_once()

        ret, buffer = cv2.imencode('.jpg',annotated)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    

@app.route("/")
def hi_enoch():
    return render_template('index.html')

@app.route("/video")
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/status")
def status():
    return jsonify({"distracted": is_playing_audio})




if __name__ == "__main__":
    app.run(debug = True)
