from flask import Flask, render_template,Response
import cv2
import time

app = Flask(__name__)
cam = cv2.VideoCapture(0)

def gen_frames():
    while True:
    #iteratively write the current frame to the output file
        okay, frame = cam.read() #ret is boolean, True if successful
        if not okay:break
        
        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n  ')

audioLength = 10
timeLastAudioPlayed = -audioLength
    

@app.route("/")
def hi_enoch():
    global timeLastAudioPlayed
    isDistracted = True
    playingAudio = True

    startAudio = False
    print(audioLength)
    if time.time() - timeLastAudioPlayed > audioLength:
        playingAudio = False

    if isDistracted and not playingAudio:
        startAudio = True
        playingAudio = True
        timeLastAudioPlayed = time.time()

    return render_template('index.html', startAudio = isDistracted)

@app.route("/video")
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == "__main__":
    timeLastAudioPlayed = -audioLength
    app.run(debug = True)

