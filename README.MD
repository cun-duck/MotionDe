People Counting System
Overview
Proyek ini merupakan implementasi sistem object detection, tracking, dan people counting yang digunakan untuk memantau jumlah orang di area high risk berbentuk polygon pada video feed (CCTV). Sistem menggunakan model YOLOv8 untuk deteksi objek dan centroid tracking untuk melacak pergerakan orang, serta menyediakan dashboard web untuk menampilkan live video processed, data feedback (jumlah objek) dan grafik tren.

Challenge List
Challenge 1: Desain Database (SQL/NoSQL)
Fitur:
Menyimpan data objek/orang yang terdeteksi (waktu deteksi, detail deteksi, dsb)
Menyimpan data counting (jumlah orang yang masuk dan keluar area polygon)
Menyimpan data konfigurasi area (koordinat polygon, nama area, dsb)
Implementasi:
File: src/config/models.py
Tabel:
detection_data: Menyimpan data deteksi
count_data: Menyimpan data counting
config_area: Menyimpan konfigurasi area polygon
Status: Done
Catatan: Diagram database dan diagram desain sistem disertakan pada README (gambar dapat dilampirkan)
Challenge 2: Pengumpulan Dataset
Fitur:
Menggunakan file video sebagai sumber data.
Contoh video: Malioboro_10_Kepatihan.stream, Malioboro_30_Pasar_Beringharjo.stream, NolKm_Utara.stream
Implementasi:
Dataset diambil dari sumber video CCTV Jogja (atau dataset open source jika real-time sulit didapatkan)
Status: Done
Catatan: Sumber video/dataset dijelaskan pada README.
Challenge 3: Object Detection & Tracking
Fitur:
Deteksi objek (terutama orang, tetapi juga objek lain seperti sepeda, mobil, motor, dan traffic light) menggunakan model pre-trained YOLOv8.
Tracking objek 'person' dengan metode centroid tracking untuk menghitung berapa kali seseorang memasuki atau keluar dari area polygon.
Penghitungan objek untuk kelas tertentu (0: person, 1: bicycle, 2: car, 3: motorcycle, 9: traffic light) sebagai data feedback.
Konfigurasi polygon area yang awalnya hard-coded namun dapat diubah secara dinamis melalui API/dashboard.
Implementasi:
Modul Deteksi: src/detection/yolo_detector.py
Modul Tracking & Counting: src/tracking/people_counter.py dan src/tracking/centroid_tracker.py
Status: Done
Catatan: Diagram alur sistem (video frame → deteksi bounding box → cek apakah bounding box masuk/keluar polygon → update counter) dijelaskan di README.
Challenge 5: Integrasi Sistem (API & Dashboard)
Fitur:
Menyediakan API endpoint untuk menampilkan hasil deteksi dan counting:
GET /api/stats/: Menampilkan history jumlah orang masuk/keluar (dapat dikembangkan dengan filter/pagination)
GET /api/stats/live: Menampilkan data live counting (people in/out)
(Opsional) POST /api/config/area: Untuk mengatur konfigurasi area polygon secara dinamis
GET /api/detections: Mengembalikan data deteksi (jumlah objek per class)
GET /video_feed: Menyajikan stream video processed (dengan overlay bounding box) dalam format MJPEG.
Dashboard web yang menampilkan:
Live Video Processed di bagian atas
Feedback Deteksi (jumlah orang, mobil, motor, people tracking) di sidebar
Graph Prediksi (grafik tren) di bawah feedback detection
Kontrol Sumber Video di bagian bawah, dengan opsi: default streaming (radio button), custom URL, atau file upload.
Implementasi:
API dan Dashboard: src/api/app.py
Template Dashboard: src/api/templates/dashboard.html
Status: Done
Catatan:
Dashboard dilengkapi dengan polling AJAX untuk update live feedback dan grafik tren menggunakan Chart.js.
Fitur file upload untuk input video juga diimplementasikan.
Challenge 6: Deployment
Fitur (Opsional):
Containerization menggunakan Docker untuk mempermudah reviewer menjalankan sistem.
Penjelasan cara menjalankan aplikasi secara lokal (jika Docker tidak digunakan).
Implementasi:
Belum diimplementasikan containerization secara penuh.
Status: X
Kendala:
Deployment menggunakan Docker dapat ditambahkan jika waktu memungkinkan.
