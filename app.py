import streamlit as st
from PIL import Image
import datetime as dt
from datetime import date, datetime
import time

st.set_page_config(page_title="Undangan 2 Foto", page_icon="💍", layout="centered")

st.markdown("""
<style>
.main-title { font-family: cursive; font-size: 50px; color: #d4af37; text-align: center; }
.card { background: #eef4ee; border-radius: 20px; padding: 20px; border: 2px solid #d4af37; text-align:center; }
.count-box { background: #7a9a7a; color: white; border-radius: 10px; padding: 10px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">Undangan 2 Foto</p>', unsafe_allow_html=True)
st.caption("Basic - 2 Foto Slide Otomatis")

with st.sidebar:
    st.header("⚙️ Admin")
    mode = st.radio("Pilih:", ["1 Foto", "2 Foto Slide (Basic)"])
    nama1 = st.text_input("Nama Pria", "Imam")
    nama2 = st.text_input("Nama Wanita", "Aisyah")
    tgl = st.date_input("Tanggal", date(2026, 12, 20))
    lokasi = st.text_input("Lokasi", "Gedung Al-Hikmah, Jakarta")
    
    if mode == "1 Foto":
        f1 = st.file_uploader("Foto 1", type=["jpg","png","jpeg"])
        f2 = None
    else:
        f1 = st.file_uploader("Foto 1 (Prewedding)", type=["jpg","png","jpeg"])
        f2 = st.file_uploader("Foto 2 (Prewedding)", type=["jpg","png","jpeg"])

st.markdown('<div class="card">', unsafe_allow_html=True)

if mode == "1 Foto":
    st.write("MODE: 1 FOTO")
    if f1:
        st.image(Image.open(f1), width=320)
    else:
        st.image("https://images.unsplash.com/photo-1519741497674-611481863552?w=400", width=320)
else:
    st.write("MODE: 2 FOTO SLIDE - OTOMATIS GANTI")
    if f1 and f2:
        box = st.empty()
        for i in range(2): # loop 2x biar keliatan slide
            for idx, file in enumerate([f1,f2]):
                box.image(Image.open(file), width=320, caption=f"Foto {idx+1}/2 - {nama1} & {nama2}")
                time.sleep(3)
    elif f1:
        st.image(Image.open(f1), width=320, caption="Foto 1/2 - Upload foto ke-2 di sidebar")
    else:
        st.info("Upload 2 foto di sidebar kiri")

st.markdown(f'<p class="main-title" style="font-size:40px">{nama1} & {nama2}</p>', unsafe_allow_html=True)
st.write(f"📅 {tgl.strftime('%d %B %Y')} • 📍 {lokasi}")

# countdown simple
selisih = datetime.combine(tgl, dt.time(9,0)) - datetime.now()
if selisih.days >=0:
    c1,c2 = st.columns(2)
    c1.markdown(f'<div class="count-box"><b>{selisih.days}</b><br>HARI LAGI</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="count-box"><b>{selisih.seconds//3600}</b><br>JAM LAGI</div>', unsafe_allow_html=True)

st.write("")
st.button("✅ RSVP Hadir", type="primary", use_container_width=True)
st.link_button("📍 Buka Maps", f"https://maps.google.com/?q={lokasi}", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
st.divider()
st.success("Basic 2 foto = lu bisa jual 200rb. Bikinnya 1 menit!")
