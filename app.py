import streamlit as st
import pandas as pd 
import numpy as np
import os

file_excel = "DATA_ALTERNATIF.xlsx"

if os.path.exists(file_excel):
    data_excel = pd.read_excel(file_excel)
else:
    data_excel = pd.DataFrame({
        "Nama": ["Siswa 1"],
        "Kelas": ["X"],
        "Penghasilan": [1],
        "Tanggungan": [1],
        "Status": [1],
        "Akademik": [1],
        "Motivasi": [1],
    })

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

        5. **Motivasi Belajar** 
        - Tinggi = 3 
        - Sedang = 2 
        - Rendah = 1
           **Catatan:** 
            Data yang dimasukkan sudah dalam bentuk angka berdasarkan konversi indikator di atas.
        """)

    # --- DATA ALTERNATIF ---
    st.subheader("Input Data Alternatif")

    edited_data = st.data_editor(data_excel, num_rows="dynamic")

    if st.button("Gunakan Data Ini"):
        st.session_state.data = edited_data
        st.success("Data berhasil digunakan!")

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
    
    criteria = ["Penghasilan","Tanggungan","Status","Akademik","Motivasi"]
    
    # inisialisasi pertama kali
    if "matrix" not in st.session_state:
        st.session_state.matrix = pd.DataFrame(
            np.ones((5,5)),
            columns=criteria,
            index=criteria
        )
    
    # tampilkan matrix (HANYA SEKALI)
    edited_matrix = st.data_editor(st.session_state.matrix)
    
    # --- AUTO RECIPROCAL ---
    matrix = edited_matrix.copy()
    
    for i in range(len(criteria)):
        for j in range(len(criteria)):
            if i != j:
                try:
                    matrix.iloc[j, i] = 1 / float(matrix.iloc[i, j])
                except:
                    matrix.iloc[j, i] = 1
    
    # simpan hasil
    st.session_state.matrix = matrix
    
    st.caption("Isi satu sisi matriks saja, sistem akan otomatis mengisi kebalikannya (1/n)")
    


# ===== HASIL RANKING =====
elif menu == "Hasil Ranking":
    st.title("🏆 Hasil Ranking")

    if "data" in st.session_state and "matrix" in st.session_state:

        data = st.session_state.data.copy()
        matrix = st.session_state.matrix.values

        criteria = ["Penghasilan","Tanggungan","Status","Akademik","Motivasi"]
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

        # --- URUTAN PRIORITAS KRITERIA ---
        st.subheader("Urutan Prioritas Kriteria")
        
        df_urut = pd.DataFrame({
            "Kriteria": criteria,
            "Bobot": weights
        })
        df_urut = df_urut.sort_values(by="Bobot", ascending=False)
        df_urut["Ranking"] = range(1, len(df_urut)+1)
        
        st.dataframe(df_urut)
        
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
        matrix = st.session_state.matrix.values
        criteria = ["Penghasilan","Tanggungan","Status","Akademik","Motivasi"]

        # --- BOBOT AWAL ---
        col_sum = matrix.sum(axis=0)
        norm_matrix = matrix / col_sum
        weights = norm_matrix.mean(axis=1)

        # fungsi ranking
        def hitung_ranking(bobot):
            nilai = data[criteria].values
            skor = np.dot(nilai, bobot)
            df = data.copy()
            df["Skor"] = skor
            df = df.sort_values(by="Skor", ascending=False)
            df["Ranking"] = range(1, len(df)+1)
            return df

        # ranking awal
        ranking_awal = hitung_ranking(weights)
        st.subheader("Ranking Awal")
        st.dataframe(ranking_awal)

        perubahan_kriteria = []

        st.subheader("Hasil Sensitivitas")

        for i, k in enumerate(criteria):

            st.markdown(f"### 🔄 Skenario: {k} dinaikkan")

            bobot_baru = weights.copy()
            bobot_baru[i] = bobot_baru[i] * 1.2
            bobot_baru = bobot_baru / bobot_baru.sum()

            hasil = hitung_ranking(bobot_baru)

            # CEK PERUBAHAN RANKING
            berubah = not ranking_awal["Nama"].equals(hasil["Nama"])

            if berubah:
                st.error("Ranking BERUBAH ❗ (Sensitif)")
                perubahan_kriteria.append((k, True))
            else:
                st.success("Ranking TIDAK berubah (Stabil)")
                perubahan_kriteria.append((k, False))

            st.dataframe(hasil)

        # --- KESIMPULAN ---
        st.subheader("Kesimpulan Sensitivitas")

        df_sens = pd.DataFrame(perubahan_kriteria, columns=["Kriteria","Sensitif"])

        # ubah ke label
        df_sens["Status"] = df_sens["Sensitif"].apply(lambda x: "Sensitif" if x else "Stabil")

        st.dataframe(df_sens)

        # kriteria paling sensitif
        sensitif_only = df_sens[df_sens["Sensitif"] == True]

        if not sensitif_only.empty:
            st.warning("Kriteria yang paling mempengaruhi perubahan ranking:")
            st.write(sensitif_only["Kriteria"].tolist())
        else:
            st.success("Semua kriteria stabil (tidak ada perubahan ranking)")
