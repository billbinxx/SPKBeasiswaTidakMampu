import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="SPK Beasiswa Tidak Mampu", layout="centered")

# ===== HALAMAN AWAL =====
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

st.write ("Gunakan Menu Sidebar untuk Melanjutkan Perhitungan")
st.markdown("---")

menu = st.sidebar.selectbox
("Menu", 
 ["Beranda", "Perhitungan", "Hasil Ranking","Analisis Sensitivitas"]
)

if menu == "Beranda":
    pass

elif menu == "Perhitungan":
    st.write("Perhitungan ")

elif menu == "Hasil Ranking":
    st.write("Hasil Ranking")

elif menu == "Analisis Sensitivitas":
    st.write("Analisis Sensitivitas")
    
#===PERHITUNGAN
elif menu == "Perhitungan": 
    st.title ("Perhitungan AHP")

# INPUT DATA ALTERNATIF 
    st.subheader("Input Data Alternatif")
    data = pd.DataFrame({
           "Nama": ["Siswa 1", "Siswa 2"],
           "Tanggungan": [2,3],
           "Status": [1,2],
           "Akademik": [3,2],
           "Penghasilan": [2,1],
           "Motivasi": [3,3],
       })

    edited_data = st.data_editor(data, num_rows="dynamic")
