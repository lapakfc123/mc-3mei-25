import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Customer Dashboard", page_icon="👥", layout="wide")
st.title("👥 Customers Analytics Dashboard")

# Load data
def load_data():
    df = pd.read_csv("customers.csv")
    return df

df = load_data()

# Sidebar - Filter
st.sidebar.header("🔍 Filter Data")
departments = st.sidebar.multiselect("Pilih Department:", df["Department"].dropna().unique(), default=df["Department"].dropna().unique())
countries = st.sidebar.multiselect("Pilih Country:", df["Country"].dropna().unique(), default=df["Country"].dropna().unique())
genders = st.sidebar.multiselect("Pilih Gender:", df["Gender"].dropna().unique(), default=df["Gender"].dropna().unique())

# Filter usia
st.sidebar.subheader("Filter Rentang Usia")
age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
age_range = st.sidebar.slider("Usia:", min_value=age_min, max_value=age_max, value=(age_min, age_max))

# Filter dataframe
df_filtered = df[
    (df["Department"].isin(departments)) &
    (df["Country"].isin(countries)) &
    (df["Gender"].isin(genders)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

# Tab navigasi
tab1, tab2 = st.tabs(["📊 Ringkasan", "📄 Tabel"])

with tab1:
    st.subheader("📌 Statistik Pelanggan")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", df_filtered["EEID"].nunique())
    col2.metric("Rata-rata Gaji", f"${df_filtered['AnnualSalary'].mean():,.0f}")
    col3.metric("Total Bonus", f"${df_filtered['Bonus'].sum():,.0f}")

    st.success(f"Gaji Tertinggi: ${df_filtered['AnnualSalary'].max():,.0f}")
    st.warning(f"Gaji Terendah: ${df_filtered['AnnualSalary'].min():,.0f}")
    st.info(f"Median Gaji: ${df_filtered['AnnualSalary'].median():,.0f}")

    # Pie chart
    st.subheader("📌 Distribusi Gender")
    fig_pie = px.pie(df_filtered, names="Gender", title="Gender Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Bar chart
    st.subheader("📌 Gaji Rata-Rata per Department")
    salary_by_dept = df_filtered.groupby("Department")["AnnualSalary"].mean().reset_index()
    fig_bar = px.bar(salary_by_dept, x="Department", y="AnnualSalary", title="Average Salary by Department")
    st.plotly_chart(fig_bar, use_container_width=True)

    # Visualisasi baru dengan 2 kolom: Line Chart & Histogram Bonus
    st.subheader("📊 Analisis Gaji dan Bonus")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Rata-rata Gaji Berdasarkan Usia")
        avg_salary_age = df_filtered.groupby("Age")["AnnualSalary"].mean().reset_index()
        fig_line = px.line(avg_salary_age, x="Age", y="AnnualSalary", markers=True, title="Average Salary by Age")
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.markdown("#### 📊 Distribusi Bonus")
        fig_bonus = px.histogram(df_filtered, x="Bonus", nbins=30, title="Distribusi Bonus Customer")
        st.plotly_chart(fig_bonus, use_container_width=True)


with tab2:
    st.subheader("📄 Data Lengkap")
    st.dataframe(df_filtered, use_container_width=True)
