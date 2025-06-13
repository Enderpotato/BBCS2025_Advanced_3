from flask import Flask, render_template,Response
import cv2

app = Flask(__name__)
cam = cv2.VideoCapture(0)

def gen_frames():
    while True:
        okay, frame = cam.read() #okay is boolean, True if successful
        if not okay:break
        
        ret, buffer = cv2.imencode('.jpg',frame)
        frame = buffer.tobytes()
        
        yield(b'--frame\r\n'
              b'Content-Type: image')


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    

@app.route("/")
def hi_enoch():
    return render_template('index.html')

@app.route("/video")
def video():
    return Response(gen_frames)


if __name__ == "__main__":
    app.run(debug = True)
