import streamlit as st
import pandas as pd 
import numpy as np

st.set_page_config(page_title="SPK Beasiswa Tidak Mampu", layout="centered")

#=== MENUBAR ===
menu = st.sidebar.selectbox(
    "Menu", 
    ["Beranda", "Input Data", "Hasil Ranking","Analisis Sensitivitas"]
)

# ===== BERANDA =====
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

# ===== INPUT DATA =====
elif menu == "Input Data":
    st.title("📥 Input Data")

    st.subheader("📌 Informasi Kriteria & Skala Penilaian")

    with st.expander("Lihat Penjelasan Kriteria"):
        st.write("""
        Skala 1–3:

        - 3 = Sangat Layak  
        - 2 = Cukup Layak  
        - 1 = Kurang Layak  

        **Tanggungan**
        - ≥ 4 = 3  
        - 2–3 = 2  
        - ≤ 1 = 1  

        **Status**
        - Yatim Piatu = 3  
        - Yatim/Piatu = 2  
        - Lengkap = 1  

        **Penghasilan**
        - < 500.000 = 3  
        - 500.000–900.000 = 2  
        - ≥ 1.000.000 = 1  
        """)

    # --- DATA ALTERNATIF ---
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

    # --- MATRIX ---
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

    # --- SIMPAN ---
    if st.button("Simpan Data"):
        st.session_state.data = edited_data
        st.session_state.matrix = edited_matrix.values
        st.success("Data berhasil disimpan!")
