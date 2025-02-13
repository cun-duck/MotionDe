# Object Counting System

## Overview
Proyek ini merupakan implementasi sistem object detection, tracking, dan people counting untuk memantau jumlah orang yang berada pada area high risk (berbentuk polygon) dalam video feed (misalnya, CCTV). Sistem ini menggunakan model YOLOv8 untuk deteksi objek dan centroid tracking untuk melacak pergerakan orang, sehingga dapat menghitung berapa kali seseorang memasuki atau keluar dari area polygon. Selain itu, sistem menyediakan API dan dashboard web interaktif untuk monitoring secara real-time, termasuk live video processed, feedback deteksi, dan grafik tren.

---

## List & Checklist Fitur

### Desain Database (SQL/NoSQL)
- **Fitur:**
  - Menyimpan data objek/orang yang terdeteksi (waktu deteksi, detail deteksi, dll).
  - Menyimpan data counting (jumlah orang yang masuk dan keluar area polygon).
  - Menyimpan data konfigurasi area (koordinat polygon, nama area, dll).
- **Implementasi:**
  - File: `src/config/models.py`
  - Tabel: `detection_data`, `count_data`, `config_area`
### Pengumpulan Dataset
- **Fitur:**
  - Menggunakan file video sebagai sumber data.
  - Contoh video: *Malioboro_10_Kepatihan.stream*, *Malioboro_30_Pasar_Beringharjo.stream*, *NolKm_Utara.stream*
- **Implementasi:**
  - Dataset diambil dari sumber video CCTV Jogja atau dataset open source (jika live streaming sulit didapatkan).
###  Object Detection & Tracking
- **Fitur:**
  - Deteksi objek menggunakan pre-trained YOLOv8 untuk mendeteksi multi objek (terutama orang, tetapi juga sepeda, mobil, motor, dan traffic light).
  - Tracking khusus untuk objek 'person' dengan metode centroid tracking untuk menghitung "people in" dan "people out" ketika objek masuk/keluar area polygon.
  - Sistem menghitung jumlah objek per class (misalnya, 0: person, 1: bicycle, 2: car, 3: motorcycle, 9: traffic light) untuk ditampilkan sebagai feedback.
  - Polygon area deteksi awal ditetapkan secara hard-coded, namun dapat diubah secara dinamis melalui API/dashboard.
- **Implementasi:**
  - Modul deteksi: `src/detection/yolo_detector.py`
  - Modul tracking & counting: `src/tracking/people_counter.py` dan `src/tracking/centroid_tracker.py`
### Integrasi Sistem (API & Dashboard)
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
###  Deployment
- **Fitur (Opsional):**
  - Containerization menggunakan Docker untuk mempermudah reviewer menjalankan sistem.
  - Penjelasan cara menjalankan aplikasi secara lokal (jika Docker tidak digunakan).
- **Implementasi:**
  - (Opsional: Dockerfile dan docker-compose.yml)
---

## Struktur Proyek

```
MotionDe/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py           # Konfigurasi polygon awal
│   │   └── models.py           # Struktur database: detection_data, count_data, config_area
│   ├── detection/
│   │   ├── __init__.py
│   │   └── yolo_detector.py    # Modul deteksi menggunakan YOLOv8
│   ├── tracking/
│   │   ├── __init__.py
│   │   ├── centroid_tracker.py # Centroid tracking untuk objek
│   │   └── people_counter.py   # Mengintegrasikan deteksi, tracking, dan counting
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py              # API endpoints, streaming video, dan dashboard
│   │   └── templates/
│   │       └── dashboard.html  # Dashboard web interaktif
├── Dockerfile                 # (Opsional) Untuk containerization
├── docker-compose.yml         # (Opsional) Untuk deployment dengan Docker Compose
├── README.md                  # Dokumentasi lengkap (ini file README.md)
├── requirements.txt           # Daftar dependency: flask, sqlalchemy, opencv-python, numpy, ultralytics
└── .gitignore
```
---
## Cara Menjalankan Aplikasi
### Setup Lokal
1. **Clone Repository:**
   ```bash
   git clone https://github.com/username/people-counting-system.git
   cd people-counting-system
   ```
2. **Buat dan Aktifkan Virtual Environment:**
   ```bash
   python -m venv env
   # Aktifkan:
   # Windows:
   .\env\Scripts\activate
   # macOS/Linux:
   source env/bin/activate
   ```
3. **Install Dependency:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Jalankan Aplikasi:**
   ```bash
   python -m src.api.app
   ```
5. **Akses Dashboard:**
   Buka browser dan akses [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Penggunaan File Upload
- Di halaman dashboard, terdapat opsi untuk:
  - Memilih sumber video melalui radio button (default streaming URL atau webcam).
  - Memasukkan custom URL.
  - Meng-upload file video.
- File video yang di-upload akan disimpan di folder `uploads/` dan digunakan sebagai sumber video.

---

## Diagram Desain
*(Lampirkan diagram database dan diagram alur sistem di sini atau sebagai file gambar terpisah di repositori.)*

---

## Pengumpulan Dataset
Dataset video diambil dari contoh video CCTV Jogja, antara lain:
- *Malioboro_10_Kepatihan.stream*
- *Malioboro_30_Pasar_Beringharjo.stream*
- *NolKm_Utara.stream*  
Jika video live tidak tersedia, digunakan video statis atau dataset open source.

---
## Catatan Deployment
- **Deployment (Opsional):**  
  Containerization menggunakan Docker belum diimplementasikan.  
  Jika diperlukan, sertakan file `Dockerfile` dan `docker-compose.yml` beserta petunjuk penggunaan dalam README.
---
## Penutup
Proyek ini mengimplementasikan sistem deteksi, tracking, dan counting untuk memonitor area high risk menggunakan video feed. Fitur utama telah diselesaikan, termasuk desain database, object detection & tracking, integrasi API & dashboard, serta opsi file upload.  
---
## Checklist Fitur
✔️ **Desain Database**:  
  *Diagram dan struktur tabel sudah dibuat di `src/config/models.py`.*
✔️ **Pengumpulan Dataset**:  
  *Dataset video dari contoh CCTV Jogja / open source.*
✔️ **Object Detection & Tracking**:   
  *Tidak ada kendala dalam mendeteksi objek yang sangat berdekatan.*
✔️ **Counting & Polygon Area**:  
  *People in/out dihitung, dan polygon dapat diubah melalui API/dashboard.*
✔️ **Prediksi (Forecasting)**:  
  *Grafik tren prediksi telah ditampilkan di dashboard menggunakan Chart.js.*
✔️ **Integrasi API (API/Front End)**:   
  *Endpoint API dan dashboard web interaktif telah diimplementasikan (`src/api/app.py`, `src/api/templates/dashboard.html`).*
❌ **Deployment**:   
  *Containerization dengan Docker belum diimplementasikan.*


