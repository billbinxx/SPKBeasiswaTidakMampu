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

st.markdown("---")

if st.button("➡️ Mulai Perhitungan"):
    st.success("Silakan lanjut ke menu perhitungan di sidebar")
if menu == "Beranda":
    # isi halaman awal

elif menu == "Perhitungan":
    # input data & bobot

elif menu == "Ranking":
    # hasil ranking

elif menu == "Sensitivitas":
    # analisis
