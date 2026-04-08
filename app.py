import streamlit as st

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

st.write ("Pergi ke Menu Sidebar untuk Melanjutkan Perhitungan")
st.markdown("---")

menu = st.sidebar.selectbox("Menu", 
                            ["Beranda", "Perhitungan", "Hasil Ranking","Analisis Sensitivitas"]
                           )
if menu == "Beranda":
    st.write("Halaman Beranda")

elif menu == "Perhitungan":
    st.write("Perhitungan ")

elif menu == "Hasil Ranking":
    st.write("Hasil Ranking")

elif menu == "Analisis Sensitivitas":
    st.write("Analisis Sensitivitas")
