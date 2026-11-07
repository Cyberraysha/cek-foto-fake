import streamlit as st
from PIL import Image
from datetime import date, datetime
import datetime as dt

st.set_page_config(page_title="Undangan Wedding 3&6", page_icon="💍", layout="centered")

st.markdown("""
<style>
.main-title { font-family: cursive; font-size: 48px; color: #d4af37; text-align: center; font-weight: bold; }
.card { background: linear-gradient(180deg, #eef4ee 0%, #ffffff 100%); border-radius: 20px; padding: 20px; border: 2px solid #d4af37; }
.count-box { background: #7a9a7a; color: white; border-radius: 12px; padding: 12px; text-align: center; }
</style>
""", unsafe_allow_html=True)

if 'slide_idx' not in st.session_state:
    st.session_state.slide_idx = 0

st.markdown('<p class="main-title">Undangan Digital</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Admin Jualan")
    paket = st.radio("Pilih Paket Jualan:", ["BASIC - 3 Foto (200rb)", "PRO - 6 Foto (450rb)"])
    nama1 = st.text_input("Nama Pria", "Imam")
    nama2 = st.text_input("Nama Wanita", "Aisyah")
    tgl = st.date_input("Tanggal", date(2026, 12, 20))
    lokasi = st.text_input("Lokasi", "Gedung Al-Hikmah, Jakarta")
    
    max_foto = 3 if "BASIC" in paket else 6
    st.info(f"Upload {max_foto} foto untuk paket ini")
    fotos = st.file_uploader(f"Upload {max_foto} Foto Prewedding", type=["jpg","png","jpeg"], accept_multiple_files=True)
    if fotos and len(fotos) > max_foto:
        st.warning(f"Kepotong jadi {max_foto} foto ya bro, sesuai paket")
        fotos = fotos[:max_foto]
    
    if st.button("Reset Slide"):
        st.session_state.slide_idx = 0

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; color:#7a9a7a; font-weight:bold'>{paket}</p>", unsafe_allow_html=True)

# SLIDE LOGIC - ANTI LAG
if fotos and len(fotos) > 0:
    total = len(fotos)
    idx = st.session_state.slide_idx % total
    img = Image.open(fotos[idx])
    st.image(img, use_container_width=True, caption=f"Foto {idx+1}/{total} - {nama1} & {nama2}")
    
    col1, col2, col3 = st.columns([1,2,1])
    if col1.button("⬅️ Prev"):
        st.session_state.slide_idx = (idx - 1) % total
        st.rerun()
    col2.markdown(f"<p style='text-align:center'>Slide {idx+1}/{total}</p>", unsafe_allow_html=True)
    if col3.button("Next ➡️"):
        st.session_state.slide_idx = (idx + 1) % total
        st.rerun()
    
    st.progress((idx+1)/total)
    if paket.startswith("PRO"):
        st.success(f"PRO: {total} foto = Video {total*3} detik, bisa export MP4")
    else:
        st.caption(f"BASIC: {total} foto = Video {total*3} detik")
else:
    st.warning(f"Upload {max_foto} foto di sidebar kiri (>>)")
    st.image("https://images.unsplash.com/photo-1519741497674-611481863552?w=600", use_container_width=True)

st.markdown(f'<p class="main-title" style="font-size:42px">{nama1} & {nama2}</p>', unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'>📅 {tgl.strftime('%d %B %Y')} • 📍 {lokasi}</p>", unsafe_allow_html=True)

selisih = datetime.combine(tgl, dt.time(9,0)) - datetime.now()
if selisih.days >=0:
    c1,c2 = st.columns(2)
    c1.markdown(f'<div class="count-box"><b>{selisih.days}</b><br>HARI LAGI</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="count-box"><b>{selisih.seconds//3600}</b><br>JAM LAGI</div>', unsafe_allow_html=True)

st.write("")
st.button("✅ RSVP Hadir", type="primary", use_container_width=True)
st.link_button("📍 Buka Google Maps", f"https://maps.google.com/?q={lokasi}", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
