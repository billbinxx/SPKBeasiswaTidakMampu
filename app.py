import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="SPK Beasiswa Tidak Mampu", layout="centered")

#===MENUBAR
menu = st.sidebar.selectbox(
    "Menu", 
    ["Beranda", "Input Data", "Hasil Ranking","Analisis Sensitivitas"]
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
    1. Penghasilan Orang Tua 
    2. Tanggungan Keluarga 
    3. Status Anak   
    4. Nilai Akademik
    5. Motivasi Belajar  
    """)

    st.info("Metode yang digunakan: AHP")
    st.write("Gunakan Menu Sidebar untuk Melanjutkan Perhitungan")
    st.markdown("---")

# ===== PERHITUNGAN =====
elif menu == "Perhitungan":
    st.title("Perhitungan")
    st.subheader("📌 Informasi Kriteria & Skala Penilaian")

    with st.expander("Lihat Penjelasan Kriteria"):
        st.write("""
        **Skala yang digunakan merupakan bentuk yang telah di konversi menjadi angka 1-3 dengan keterangan seperti dibawah ini, untuk mempermundah proses perhitungan**
        
        Keterangan:
        - 3 = Sangat Layak / Prioritas Tinggi  
        - 2 = Cukup Layak  
        - 1 = Kurang Layak  
    
        **Indikator Penilaian:**
        1. **Tanggungan Keluarga**
           - ≥ 4 orang = 3   
           - 2–3 orang = 2  
           - ≤ 1 orang = 1  

    
        2. **Status Anak**
           - Yatim Piatu = 3  
           - Yatim / Piatu / Tidak Utuh = 2  
           - Orang Tua Lengkap = 1  

    
        3. **Nilai Akademik**
           - Tinggi = 3  
           - Sedang = 2  
           - Rendah = 1  

    
        4. **Penghasilan Orang Tua**
           - < 500.000 = 3  
           - 500.000 – 900.000 = 2  
           - ≥ 1.000.000 = 1  

    
        5. **Motivasi Belajar**
           - Tinggi = 3  
           - Sedang = 2  
           - Rendah = 1  
        **Catatan:**
        Data yang dimasukkan sudah dalam bentuk angka berdasarkan konversi indikator di atas.
        """)

    #INPUT DATA ALTERNATIF
    elif menu == "Input Data":
    st.title("Input Data")

    # INPUT DATA ALTERNATIF
    st.subheader("Input Data Alternatif")

    data = pd.DataFrame({
        "Nama": ["Siswa 1", "Siswa 2"],
        "Kelas": ["X TKJ 1", "XI TOT"],
        "Tanggungan": [2,3],
        "Status": [1,2],
        "Akademik": [3,2],
        "Penghasilan": [2,1],
        "Motivasi": [3,3],
    })

    edited_data = st.data_editor(data, num_rows="dynamic")

    # ===== MATRIX INPUT =====
    st.subheader("Input Matriks Perbandingan Kriteria")

    with st.expander("📌 Skala Saaty (1–9)"):
        st.write("""
        1 = Sama penting  
        3 = Sedikit lebih penting  
        5 = Lebih penting  
        7 = Sangat penting  
        9 = Mutlak  
        """)

    criteria = ["Tanggungan","Status","Akademik","Penghasilan","Motivasi"]

    matrix_df = pd.DataFrame(
        np.ones((5,5)),
        columns=criteria,
        index=criteria
    )

    edited_matrix = st.data_editor(matrix_df)

    # SIMPAN KE SESSION
    if st.button("Simpan Data"):
        st.session_state.data = edited_data
        st.session_state.matrix = edited_matrix.values
        st.success("Data berhasil disimpan! Lanjut ke menu Hasil Perhitungan")
