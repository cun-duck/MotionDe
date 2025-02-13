# Object Counting System

## Overview
Proyek ini merupakan implementasi sistem object detection, tracking, dan people counting untuk memantau jumlah orang yang berada pada area high risk (berbentuk polygon) dalam video feed (misalnya, CCTV). Sistem ini menggunakan model YOLOv8 untuk deteksi objek dan centroid tracking untuk melacak pergerakan orang, sehingga dapat menghitung berapa kali seseorang memasuki atau keluar dari area polygon. Selain itu, sistem menyediakan API dan dashboard web interaktif untuk monitoring secara real-time, termasuk live video processed, feedback deteksi, dan grafik tren.

---

## Challenge List & Checklist Fitur

### Challenge 1: Desain Database (SQL/NoSQL)
- **Fitur:**
  - Menyimpan data objek/orang yang terdeteksi (waktu deteksi, detail deteksi, dll).
  - Menyimpan data counting (jumlah orang yang masuk dan keluar area polygon).
  - Menyimpan data konfigurasi area (koordinat polygon, nama area, dll).
- **Implementasi:**
  - File: `src/config/models.py`
  - Tabel: `detection_data`, `count_data`, `config_area`
- **Status:** **Done**
- **Catatan:** Diagram database dan diagram desain sistem dilampirkan pada README (gambar diagram dapat ditambahkan ke repositori).

### Challenge 2: Pengumpulan Dataset
- **Fitur:**
  - Menggunakan file video sebagai sumber data.
  - Contoh video: *Malioboro_10_Kepatihan.stream*, *Malioboro_30_Pasar_Beringharjo.stream*, *NolKm_Utara.stream*
- **Implementasi:**
  - Dataset diambil dari sumber video CCTV Jogja atau dataset open source (jika live streaming sulit didapatkan).
- **Status:** **Done**
- **Catatan:** Sumber dataset dijelaskan di README.

### Challenge 3: Object Detection & Tracking
- **Fitur:**
  - Deteksi objek menggunakan pre-trained YOLOv8 untuk mendeteksi multi objek (terutama orang, tetapi juga sepeda, mobil, motor, traffic light).
  - Tracking khusus untuk objek 'person' dengan metode centroid tracking untuk menghitung "people in" dan "people out" ketika objek masuk/keluar area polygon.
  - Sistem menghitung jumlah objek per class (misalnya, 0: person, 1: bicycle, 2: car, 3: motorcycle, 9: traffic light) untuk ditampilkan sebagai feedback.
  - Polygon area deteksi awal ditetapkan secara hard-coded, namun dapat diubah secara dinamis melalui API/dashboard.
- **Implementasi:**
  - Modul deteksi: `src/detection/yolo_detector.py`
  - Modul tracking & counting: `src/tracking/people_counter.py` dan `src/tracking/centroid_tracker.py`
- **Status:** **Done**
- **Catatan:** Diagram alur sistem (video frame → deteksi bounding box → cek apakah bounding box masuk/keluar polygon → update counter) dijelaskan di README.

### Challenge 5: Integrasi Sistem (API & Dashboard)
- **Fitur:**
  - Menampilkan hasil deteksi, counting, dan (opsional) prediksi melalui API.
  - Endpoint minimal:
    - `GET /api/stats/` – Menampilkan history jumlah orang yang masuk/keluar area polygon.
    - `GET /api/stats/live` – Menampilkan data live counting (people in/out).
    - `(Opsional) POST /api/config/area` – Mengatur konfigurasi area polygon secara dinamis.
    - `GET /api/detections` – Mengembalikan data deteksi (object counts per class).
    - `GET /video_feed` – Menyajikan stream video processed (overlay bounding box) dalam format MJPEG.
  - Dashboard web interaktif yang menampilkan:
    - **Live Video Processed** di bagian atas.
    - **Feedback Deteksi** di sidebar (jumlah Orang, Mobil, Motor, People In, People Out).
    - **Graph Prediksi** (grafik tren) di bawah feedback detection.
    - **Kontrol Sumber Video** (opsi default, custom URL, atau file upload) di bagian bawah.
- **Implementasi:**
  - File API & Dashboard: `src/api/app.py`
  - Template Dashboard: `src/api/templates/dashboard.html`
- **Status:** **Done**
- **Catatan:**  
  - Dashboard menggunakan polling AJAX untuk update data live dan Chart.js untuk grafik tren.
  - Fitur file upload untuk input video juga diimplementasikan.

### Challenge 6: Deployment
- **Fitur (Opsional):**
  - Containerization menggunakan Docker untuk mempermudah reviewer menjalankan sistem.
  - Penjelasan cara menjalankan aplikasi secara lokal (jika Docker tidak digunakan).
- **Implementasi:**
  - (Opsional: Dockerfile dan docker-compose.yml)
- **Status:** **X**
- **Catatan:** Deployment menggunakan Docker belum diimplementasikan.

---

## Struktur Proyek

