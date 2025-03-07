# Membuat file README.md dengan format markdown

readme_content = """\
# 🌍 Air Quality Dashboard

Air Quality Dashboard adalah aplikasi berbasis **Streamlit** yang digunakan untuk memvisualisasikan dan menganalisis kualitas udara berdasarkan data **AQI (Air Quality Index)** dari berbagai kota pada repository ini juga terdapat notebook hasil analisa dari dataset yang disediakan.

---
## 🚀 **Cara Menjalankan Notebook**
### **Visual Studio Code**
1. Buka VS Code dan arahkan ke folder proyek.
2. Buka file dashboard.ipynb.
3. Pastikan Kernel Python aktif (Anda bisa memilih environment yang sesuai di bagian atas notebook).
4. Jalankan setiap sel satu per satu atau tekan Run All.

### **Google Colab**
1. Buka Google Drive → Klik New → Pilih Upload file.
2. Upload dashboard.ipynb.
3. Buka file yang diunggah → Klik "Open with" → Google Colaboratory.
4. Jalankan sel satu per satu.

> Catatan: Jika all_df.csv digunakan dalam notebook, pastikan mengunggahnya juga ke Colab atau gunakan Google Drive Mount.

---
## 🚀 **Cara Menjalankan Dashboard Streamlite**
- Buka URL berikut: https://kualitas-udara-jihan-aurelia.streamlit.app/ 

- Jalankan di lokal:
### 1️⃣ Clone Repository
```bash
git clone https://github.com/username/dicoding-analisis-data.git
cd dicoding-analisis-data/dashboard
```

### 2️⃣ Buat Virtual Environment (Opsional)
Utuk menghindari konflik dependencies:
```bash
python -m venv venv
source venv/bin/activate    # Mac/Linux
venv\\Scripts\\activate     # Windows
```

### 3️⃣ Install Dependencies
Pastikan semua library yang dibutuhkan terinstal:
```bash
pip install -r requirements.txt
```

### 4️⃣ Jalankan Dashboard
```bash
streamlit run dashboard.py
```
Setelah menjalankan perintah di atas, dashboard akan terbuka di browser dengan URL: http://localhost:8501

