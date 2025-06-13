from flask import Flask, render_template,Response
import cv2
import time
from playsound import playsound
import threading
import time
import pygame

app = Flask(__name__)
cam = cv2.VideoCapture(0)

last_played = 0
audio_cooldown = 10 

def is_distracted(frame):
    #hi enoch put the model logic here or smt return true if distracted
    return True

def play_sound_once():
    global last_played
    now = time.time()
    if now - last_played > audio_cooldown:
        last_played = now
        threading.Thread(target=pygame.mixer.music.load, args=("static/wakeup.mp3",)).start()
        threading.Thread(target=pygame.mixer.music.play).start()


def gen_frames():
    while True:
        okay, frame = cam.read() #ret is boolean, True if successful
        if not okay:break
        
        if is_distracted(frame):
            play_sound_once()

        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    

@app.route("/")
def hi_enoch():
    return render_template('index.html')

@app.route("/video")
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == "__main__":
    # timeLastAudioPlayed = -audioLength
    pygame.init()
    pygame.mixer.init()
    app.run(debug = True)
