import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Basic Streamlit", page_icon="📊", layout="wide")

# Judul
st.title("📊 Mini Dashboard Streamlit Dasar")
st.markdown("Contoh elemen dasar penggunaan Streamlit dan visualisasi data.")

# Input teks
nama = st.text_input("Masukkan nama Anda:", "Fahmi")
st.write(f"Halo, {nama}! 👋")

# Buat data sederhana
data = {
    "Bulan": ["Jan", "Feb", "Mar", "Apr"],
    "Penjualan": [100, 150, 200, 130]
}
df = pd.DataFrame(data)

# Tampilkan tabel
st.subheader("📄 Data Penjualan")
st.dataframe(df)

# Visualisasi line chart
st.subheader("📈 Grafik Penjualan (Line)")
fig_line = px.line(df, x="Bulan", y="Penjualan", markers=True, title="Trend Penjualan per Bulan")
st.plotly_chart(fig_line, use_container_width=True)

# Visualisasi bar chart
st.subheader("📊 Grafik Penjualan (Bar)")
fig_bar = px.bar(df, x="Bulan", y="Penjualan", title="Bar Chart Penjualan")
st.plotly_chart(fig_bar, use_container_width=True)

# Checkbox
if st.checkbox("Tampilkan statistik data"):
    st.write(df.describe())
