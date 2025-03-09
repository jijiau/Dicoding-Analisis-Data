import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ================== LOAD DATA ==================
csv_path = os.path.join(os.path.dirname(__file__), "all_df.csv")
all_df = pd.read_csv(csv_path)

# Konversi tanggal jika tersedia
if 'year' in all_df.columns and 'month' in all_df.columns:
    all_df['date'] = pd.to_datetime(all_df[['year', 'month']].assign(day=1))

# ================== SIDEBAR (FILTER) ==================
with st.sidebar:
    st.markdown("### **Jihan Aurelia**")
    st.markdown("📚 Cohort: MC002D5X2442")
    st.markdown("📚 Group: MC - 19")
    st.write("---")
    
    st.header("🗂 Filter Data")
    
    selected_years = st.multiselect("📆 Pilih Tahun:", all_df['year'].unique(), default=all_df['year'].unique())
    selected_months = st.multiselect("📅 Pilih Bulan:", all_df['month'].unique(), default=all_df['month'].unique())
    selected_cities = st.multiselect("🏙️ Pilih Kota:", all_df['station'].unique(), default=all_df['station'].unique())

    # Filter AQI Range
    min_aqi, max_aqi = st.slider("⚠️ Filter AQI Range:", int(all_df["AQI_Dominant"].min()), int(all_df["AQI_Dominant"].max()), (int(all_df["AQI_Dominant"].min()), int(all_df["AQI_Dominant"].max())))

# Filter dataset berdasarkan pilihan user
filtered_df = all_df[
    (all_df['year'].isin(selected_years)) & 
    (all_df['month'].isin(selected_months)) & 
    (all_df['station'].isin(selected_cities)) &
    (all_df['AQI_Dominant'].between(min_aqi, max_aqi))
]

# ================== HEADER & METRICS ==================
st.title("📊 Air Quality Dashboard")

st.header("1. Bagaimana Tren Kualitas Udara Berubah Seiring Waktu di Berbagai Kota?")
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

# ================== VISUALISASI 1: TREND AQI PER KOTA ==================
st.subheader("📈 Tren Perubahan Kualitas Udara per Kota")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=filtered_df, x='year', y='AQI_Dominant', hue='station', marker="o", ax=ax, linewidth=2)
ax.set_xlabel("Tahun")
ax.set_ylabel("AQI Dominant")
plt.legend(title="Kota", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)

st.write("""
💡 **Interpretasi:**  
- Secara umum, **terdapat penurunan AQI dari 2014 hingga 2017**, yang berarti **kualitas udara mengalami perbaikan**.  
- Kota seperti `changping` menunjukkan **penurunan AQI lebih signifikan**, yang kemungkinan disebabkan oleh kebijakan pengurangan emisi dan regulasi lingkungan.  
""")

# ================== VISUALISASI 2: POLA MUSIMAN AQI ==================
st.subheader("📆 Pola Musiman dalam Perubahan Kualitas Udara")
fig, ax = plt.subplots(figsize=(12, 5))
sns.boxplot(data=filtered_df, x='month', y='AQI_Dominant', palette="coolwarm", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("AQI Dominant")
ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"])
st.pyplot(fig)

st.write("""
💡 **Interpretasi:**  
- **AQI cenderung lebih tinggi di musim dingin**, terutama di bulan Desember dan Januari.  
- Ini mungkin disebabkan oleh **pemanasan rumah tangga dan inversi suhu**, yang memperburuk polusi udara.  
""")

st.header("2. Bagaimana Kualitas Udara di Setiap Kota Memengaruhi Risiko Kesehatan Penduduk?")
# ================== VISUALISASI 3: HARI DENGAN AQI "TIDAK SEHAT" ==================
st.subheader("🔴 Jumlah Hari dengan AQI Tidak Sehat atau Lebih")
aqi_unhealthy_days = filtered_df[filtered_df["AQI_Dominant"] > 100].groupby("year").size()
max_unhealthy_year = aqi_unhealthy_days.idxmax()

# Membuat palet warna dinamis (default abu-abu, tahun dengan jumlah tertinggi merah terang)
colors = ["#D3D3D3" if year != max_unhealthy_year else "#FF5733" for year in aqi_unhealthy_days.index]

# Plot dengan highlight
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=aqi_unhealthy_days.index, y=aqi_unhealthy_days.values, palette=colors, ax=ax)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Jumlah Hari dengan AQI Tidak Sehat", fontsize=12)
ax.set_title("Highlight Tahun dengan Jumlah Hari Tidak Sehat Terbanyak", fontsize=14, fontweight="bold")

# anotasi untuk tahun dengan jumlah tertinggi
ax.annotate(
    f"{max_unhealthy_year}: {aqi_unhealthy_days[max_unhealthy_year]} hari",
    xy=(max_unhealthy_year, aqi_unhealthy_days[max_unhealthy_year]),
    xytext=(max_unhealthy_year, aqi_unhealthy_days.max() + 5),
    fontsize=12, fontweight="bold",
    ha="center", arrowprops=dict(arrowstyle="->", color="black")
)

st.pyplot(fig)


st.write("""
💡 **Interpretasi:**  
- **Beberapa tahun memiliki lebih banyak hari dengan AQI buruk**, terutama di kota industri atau dengan kendaraan bermotor tinggi.  
- **Dampaknya:** Risiko kesehatan meningkat bagi penduduk kota-kota ini.  
""")

# ================== VISUALISASI 4: KORELASI POLUSI CO & O3 DENGAN AQI ==================
st.subheader("🌫️ Korelasi antara Polutan dan IQR AQI")
# menghitung IQR
def calculate_iqr(series):
    return np.percentile(series, 75) - np.percentile(series, 25)

iqr_data = all_df.groupby(["month", "station"]).agg(
    IQR_AQI=("AQI_Dominant", calculate_iqr),
    PM2_5=("PM2.5", "mean"),
    PM10=("PM10", "mean"),
    NO2=("NO2", "mean"),
    SO2=("SO2", "mean"),
    CO=("CO", "mean"),
    O3=("O3", "mean")
).reset_index()

corr_matrix = iqr_data[["IQR_AQI", "PM2_5", "PM10", "NO2", "SO2", "CO", "O3"]].corr()

# Visualisasi heatmap
fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Korelasi antara Polutan dan IQR AQI", fontsize=14, fontweight="bold")

st.pyplot(fig)

st.write("""
💡 **Interpretasi:**  
- **Polusi CO dan O3 memiliki korelasi yang signifikan dengan AQI**, menunjukkan bahwa mereka adalah kontributor utama polusi udara.  
- CO sering berasal dari kendaraan bermotor, sedangkan O3 sering terbentuk dari reaksi kimia di atmosfer akibat polutan lainnya.  
""")

# ================== FOOTER ==================
st.caption("© 2024 Air Quality Monitoring Dashboard")
