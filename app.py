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
        Skala yang digunakan merupakan bentuk yang telah di konversi menjadi angka 1-3 dengan keterangan seperti dibawah ini, untuk mempermundah proses perhitungan
        **Kriteria:**
        - 3 = Sangat Layak  
        - 2 = Cukup Layak  
        - 1 = Kurang Layak  

        **Indikator Penilaian:** 
        1. **Penghasilan Orang Tua** 
        - < 500.000 = 3 
        - 500.000 - 900.000 = 2 
        - ≥ 1 juta = 1

        2. **Tanggungan Keluarga** 
        - ≥ 4 orang = 3 
        - 2–3 orang = 2 
        - ≤ 1 orang = 1 

        3. **Status**
        - Yatim Piatu = 3  
        - Yatim/Piatu/Keluarga Tidak utuh = 2  
        - Lengkap = 1  

        4.**Nilai Akademik** 
        - Tinggi = 3 
        - Sedang = 2 
        - Rendah = 1

        5.3. **Motivasi Belajar** 
        - Tinggi = 3 
        - Sedang = 2 
        - Rendah = 1
           **Catatan:** 
            Data yang dimasukkan sudah dalam bentuk angka berdasarkan konversi indikator di atas.
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

# ===== HASIL RANKING =====
elif menu == "Hasil Ranking":
    st.title("🏆 Hasil Ranking")

    if "data" in st.session_state and "matrix" in st.session_state:

        data = st.session_state.data.copy()
        matrix = st.session_state.matrix

        criteria = ["Tanggungan","Status","Akademik","Penghasilan","Motivasi"]
        n = len(criteria)

        # --- MATRIX ---
        st.subheader("Matriks Perbandingan")
        st.dataframe(pd.DataFrame(matrix, columns=criteria, index=criteria))

        # --- JUMLAH ---
        col_sum = matrix.sum(axis=0)
        st.subheader("Jumlah Perbandingan Matriks")
        st.dataframe(pd.DataFrame(col_sum.reshape(1,-1), columns=criteria))

        # --- NORMALISASI ---
        norm_matrix = matrix / col_sum
        st.subheader("Normalisasi Matriks")
        st.dataframe(pd.DataFrame(norm_matrix, columns=criteria, index=criteria))

        # --- BOBOT ---
        weights = norm_matrix.mean(axis=1)
        st.subheader("Bobot Prioritas")
        st.dataframe(pd.DataFrame({
            "Kriteria": criteria,
            "Bobot": weights
        }))

        # --- CI & CR ---
        lambda_max = (col_sum * weights).sum()
        CI = (lambda_max - n) / (n - 1)
        RI = 1.12
        CR = CI / RI

        st.subheader("Uji Konsistensi")
        st.write(f"λ max: {round(lambda_max,4)}")
        st.write(f"CI: {round(CI,4)}")
        st.write(f"CR: {round(CR,4)}")

        if CR < 0.1:
            st.success("Konsisten ✅")
        else:
            st.error("Tidak Konsisten ❌")

        # ===== RANKING =====
        st.subheader("🏆 Ranking Alternatif")

        nilai = data[criteria].values
        skor = np.dot(nilai, weights)

        data["Skor Akhir"] = skor
        data = data.sort_values(by="Skor Akhir", ascending=False)
        data["Ranking"] = range(1, len(data)+1)

        st.dataframe(data)

    else:
        st.warning("Silakan input data terlebih dahulu di menu Input Data")

#===ANALISIS SENSITIVITAS
elif menu == "Analisis Sensitivitas":
    st.title("📈 Analisis Sensitivitas")

    if "data" in st.session_state and "matrix" in st.session_state:

        data = st.session_state.data.copy()
        matrix = st.session_state.matrix

        criteria = ["Tanggungan","Status","Akademik","Penghasilan","Motivasi"]

        # --- HITUNG BOBOT AWAL ---
        col_sum = matrix.sum(axis=0)
        norm_matrix = matrix / col_sum
        weights = norm_matrix.mean(axis=1)

        st.subheader("Bobot Awal")
        st.write(dict(zip(criteria, weights)))

        # --- FUNGSI HITUNG RANKING ---
        def hitung_ranking(bobot):
            nilai = data[criteria].values
            skor = np.dot(nilai, bobot)
            df = data.copy()
            df["Skor"] = skor
            df = df.sort_values(by="Skor", ascending=False)
            df["Ranking"] = range(1, len(df)+1)
            return df

        # --- RANKING AWAL ---
        st.subheader("Ranking Awal")
        ranking_awal = hitung_ranking(weights)
        st.dataframe(ranking_awal)

        # --- SKENARIO ---
        st.subheader("Hasil Sensitivitas")

        for i, k in enumerate(criteria):

            st.markdown(f"### 🔄 Skenario: Bobot {k} dinaikkan")

            bobot_baru = weights.copy()

            # naikkan 20%
            bobot_baru[i] = bobot_baru[i] * 1.2

            # normalisasi ulang biar total = 1
            bobot_baru = bobot_baru / bobot_baru.sum()

            st.write("Bobot Baru:", dict(zip(criteria, bobot_baru)))

            hasil = hitung_ranking(bobot_baru)

            st.dataframe(hasil)
