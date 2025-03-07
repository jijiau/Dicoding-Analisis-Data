import os 
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
csv_path = os.path.join(os.path.dirname(__file__), "all_df.csv")
all_df = pd.read_csv(csv_path)

# Konversi tanggal jika tersedia
if 'year' in all_df.columns and 'month' in all_df.columns:
    all_df['date'] = pd.to_datetime(all_df[['year', 'month']].assign(day=1))

# ================== NAVBAR KIRI (Sidebar) ==================
with st.sidebar:
    # --- Menampilkan Foto, Nama, dan Cohort ---
    st.image("https://drive.google.com/file/d/1xidwg5K3cvJdzGIy9YaB4ah7IXN1tzzz/view?usp=sharing", width=150)  # Ganti URL dengan foto Anda
    st.markdown("### **Jihan Aurelia**")
    st.markdown("📚 Cohort: MC002D5X2442")
    st.markdown("📚 Group: MC - 19")
    st.write("---")  # Garis pembatas
    
    # --- Sidebar untuk Filter Waktu ---
    st.header("🗂 Filter Data")
    selected_years = st.multiselect("📆 Pilih Tahun:", all_df['year'].unique(), default=all_df['year'].unique())
    selected_months = st.multiselect("📅 Pilih Bulan:", all_df['month'].unique(), default=all_df['month'].unique())

# Filter dataset berdasarkan pilihan user
filtered_df = all_df[(all_df['year'].isin(selected_years)) & (all_df['month'].isin(selected_months))]

# ================== HEADER & METRICS ==================
st.title("📊 Air Quality Dashboard")
st.subheader("Ringkasan Kualitas Udara")

col1, col2, col3 = st.columns(3)

with col1:
    avg_aqi = round(filtered_df["AQI_Dominant"].mean(), 2)
    st.metric("🌍 Rata-rata AQI", value=avg_aqi)

with col2:
    dominant_pollutant = filtered_df[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean().idxmax()
    st.metric("⚠️ Polutan Dominan", value=dominant_pollutant)

with col3:
    avg_temp = round(filtered_df['TEMP'].mean(), 2)
    st.metric("🌡️ Rata-rata Suhu (°C)", value=avg_temp)

# ================== VISUALISASI 1: TREND AQI DOMINANT ==================
st.subheader("📈 Tren AQI Dominant per Bulan")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered_df, x='month', y='AQI_Dominant', hue='year', marker="o", ax=ax, linewidth=2)
ax.set_xlabel("Bulan")
ax.set_ylabel("AQI Dominant")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
plt.legend(title="Tahun")
st.pyplot(fig)

# ================== VISUALISASI 2: VARIASI AQI BERDASARKAN KONDISI CUACA ==================
st.subheader("🌤️ Variasi AQI Berdasarkan Kondisi Cuaca")
fig, ax = plt.subplots(figsize=(12, 5))
sns.violinplot(data=filtered_df, x='AQI_Dominant', y='wd', palette='coolwarm', ax=ax, inner='quartile')
ax.set_xlabel("AQI Dominant")
ax.set_ylabel("Arah Angin")
st.pyplot(fig)

# ================== VISUALISASI 3: HEATMAP KORELASI ==================
st.subheader("🔍 Korelasi antara Parameter Cuaca dan AQI")
corr_matrix = filtered_df[['AQI_Dominant', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
st.pyplot(fig)

# ================== VISUALISASI 4: KATEGORISASI AQI ==================
st.subheader("🌍 Distribusi Kualitas Udara berdasarkan Kategori AQI")
labels = ['Baik', 'Sedang', 'Tidak Sehat', 'Sangat Tidak Sehat', 'Berbahaya']
bins = [0, 50, 100, 150, 200, 500]
filtered_df['AQI_Category'] = pd.cut(filtered_df['AQI_Dominant'], bins=bins, labels=labels)
aqi_counts = filtered_df['AQI_Category'].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=aqi_counts.index, y=aqi_counts.values, palette='Reds', ax=ax)
ax.set_xlabel("Kategori AQI")
ax.set_ylabel("Jumlah Observasi")
st.pyplot(fig)

# ================== FOOTER ==================
st.caption("© 2024 Air Quality Monitoring Dashboard")

