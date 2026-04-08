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

st.write ("Gunakan Menu Sidebar untuk Melanjutkan Perhitungan")
st.markdown("---")

elif menu == "Perhitungan":
    st.write("Perhitungan ")
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

elif menu == "Hasil Ranking":
    st.write("Hasil Ranking")

elif menu == "Analisis Sensitivitas":
    st.write("Analisis Sensitivitas")
    
