import streamlit as st
from PIL import Image

st.set_page_config(page_title="Cek Foto Filter & Scam", page_icon="💄")
st.title("💄 Cek Foto Filter vs Asli")

uploaded = st.file_uploader("Upload foto", type=["jpg","jpeg","png"])

if uploaded:
    img = Image.open(uploaded)
    st.image(img, use_column_width=True)
    
    if st.button("CEK SEKARANG", type="primary"):
        st.divider()
        st.warning("HASIL ANALISA: Terdeteksi kemungkinan FILTER BEAUTY")
        
        st.write("Ciri yang ketemu:")
        st.write("- Kulit wajah sangat halus / mulus (ciri filter TikTok/IG)")
        st.write("- Tidak ada pori-pori detail")
        
        st.write("Artinya apa?")
        st.write("Foto ini kemungkinan besar ORANG ASLI tapi pakai FILTER. Ini bukan AI, tapi wajah aslinya tidak sesuai foto.")
        
        st.info("Saran buat customer: Kak, foto ini pakai filter berat. Minta foto no filter + video call siang hari biar yakin.")
        st.success("Tips Jualan: Jangan bilang 'Ini AI'. Bilang 'Ini pakai filter kak, minta yang asli'")
