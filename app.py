import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="SPK Beasiswa Tidak Mampu", layout="centered")

#===MENUBAR
menu = st.sidebar.selectbox(
    "Menu", 
    ["Beranda", "Perhitungan", "Hasil Ranking","Analisis Sensitivitas"]
)

# ===== HALAMAN AWAL =====
if menu == "Beranda":
    st.title("🎓 Sistem Pendukung Keputusan Beasiswa")

    st.write("""
    Sistem ini digunakan untuk membantu menentukan penerima beasiswa tidak mampu 
    menggunakan metode **Analytical Hierarchy Process (AHP)**.
    """)

    st.subheader("🎯 Tujuan")
    st.write("""
    - Menentukan prioritas penerima beasiswa
    - Menghasilkan peringkat alternatif
    - Menganalisis sensitivitas bobot kriteria
    """)

    st.subheader("📊 Kriteria Penilaian")
    st.write("""
    1. Tanggungan Keluarga  
    2. Status Anak  
    3. Nilai Akademik  
    4. Penghasilan Orang Tua  
    5. Motivasi Belajar  
    """)

    st.info("Metode yang digunakan: AHP")
    st.write("Gunakan Menu Sidebar untuk Melanjutkan Perhitungan")
    st.markdown("---")

# ===== PERHITUNGAN =====
elif menu == "Perhitungan":
    st.title("📊 Perhitungan")
    st.subheader("Input Data Alternatif")

    data = pd.DataFrame({
        "Nama": ["Siswa 1", "Siswa 2"],
        "Kelas dan Jurusan": ["X TKJ 1", "XI TOT"],
        "Tanggungan": [2,3],
        "Status": [1,2],
        "Akademik": [3,2],
        "Penghasilan": [2,1],
        "Motivasi": [3,3],
    })

    edited_data = st.data_editor(data, num_rows="dynamic")

    st.subheader("Pairwise Comparison Kriteria")

    criteria = ["Tanggungan","Status","Akademik","Penghasilan","Motivasi"]
    n = len(criteria)
    
    matrix = np.ones((n,n))
    
    for i in range(n):
        for j in range(i+1, n):
            nilai = st.number_input(
                f"{criteria[i]} dibanding {criteria[j]}",
                min_value=1.0,
                max_value=9.0,
                value=1.0,
                key=f"{i}{j}"
            )
            matrix[i][j] = nilai
            matrix[j][i] = 1 / nilai
            
    if st.button("Hitung Bobot"):

    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum
    weights = norm_matrix.mean(axis=1)

    st.subheader("Bobot Kriteria")

    for i, c in enumerate(criteria):
        st.write(f"{c}: {round(weights[i],4)}")
