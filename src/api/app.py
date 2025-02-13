from flask import Flask, jsonify, request, render_template, redirect, url_for, Response
import json
import numpy as np
import time
import cv2
import os
from werkzeug.utils import secure_filename

from src.config.models import SessionLocal, CountData, ConfigArea, init_db
from src.tracking.people_counter import PeopleCounter
from src.config.config import INITIAL_POLYGON

app = Flask(__name__, template_folder="templates")


init_db()
db_session = SessionLocal()


UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


people_counter = None


DEFAULT_STREAMS = [
    "https://cctvjss.jogjakota.go.id/malioboro/Malioboro_10_Kepatihan.stream/playlist.m3u8",
    "https://cctvjss.jogjakota.go.id/malioboro/Malioboro_30_Pasar_Beringharjo.stream/playlist.m3u8",
    "https://cctvjss.jogjakota.go.id/malioboro/NolKm_Utara.stream/playlist.m3u8",
    "webcam"
]

@app.route("/api/stats/", methods=["GET"])
def get_stats():
    records = db_session.query(CountData).order_by(CountData.timestamp.desc()).limit(10).all()
    data = []
    for rec in records:
        data.append({
            "timestamp": rec.timestamp.isoformat(),
            "count_in": rec.count_in,
            "count_out": rec.count_out
        })
    return jsonify(data)

@app.route("/api/stats/live", methods=["GET"])
def get_live_stats():
    global people_counter
    if people_counter:
        data = {
            "count_in": people_counter.count_in,
            "count_out": people_counter.count_out
        }
    else:
        data = {"message": "PeopleCounter not running."}
    return jsonify(data)

@app.route("/api/config/area", methods=["POST"])
def update_config_area():
    req_data = request.get_json()
    if not req_data or "polygon" not in req_data:
        return jsonify({"error": "Polygon data is required"}), 400
    polygon = req_data["polygon"]
    if not isinstance(polygon, list) or not all(isinstance(point, list) and len(point) == 2 for point in polygon):
        return jsonify({"error": "Polygon must be a list of [x, y] pairs"}), 400
    config = db_session.query(ConfigArea).first()
    if not config:
        config = ConfigArea(name="Default Area", polygon=json.dumps(polygon))
        db_session.add(config)
    else:
        config.polygon = json.dumps(polygon)
    db_session.commit()
    if people_counter:
        people_counter.polygon = np.array(polygon, dtype=np.int32)
    return jsonify({"message": "Polygon updated", "polygon": polygon})

@app.route("/api/detections", methods=["GET"])
def get_detections():
    global people_counter
    if people_counter and hasattr(people_counter, 'last_counts'):
        return jsonify(people_counter.last_counts)
    else:
        return jsonify({})

def gen_frames():
    while True:
        if people_counter and people_counter.last_frame is not None:
            ret, buffer = cv2.imencode('.jpg', people_counter.last_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    global people_counter
    message = None
    selected_option = None

    if request.method == "POST":
        # Cek jika file video di-upload
        if 'video_file' in request.files:
            file = request.files['video_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                file.save(filepath)
                selected_option = filepath
                message = f"Video file uploaded: {filename}"
        
        if not selected_option:
            selected_option = request.form.get("streaming_option")
            custom_link = request.form.get("custom_link", "").strip()
            if custom_link:
                selected_option = custom_link
            if not selected_option:
                message = "Please select a streaming option, enter a custom URL, or upload a video file."
        
        if selected_option:
            if people_counter:
                people_counter.stop()
                time.sleep(1)
            if selected_option == "webcam":
                video_source = 0
            else:
                video_source = selected_option
            people_counter = PeopleCounter(video_source=video_source, polygon=INITIAL_POLYGON)
            people_counter.start()
            message = f"Streaming source updated to: {selected_option}"
    if not selected_option and people_counter:
        if isinstance(people_counter.video_source, str):
            selected_option = people_counter.video_source
        elif people_counter.video_source == 0:
            selected_option = "webcam"
    return render_template("dashboard.html",
                           default_streams=DEFAULT_STREAMS,
                           message=message,
                           selected_option=selected_option,
                           people_counter=people_counter)

@app.route("/")
def index():
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
