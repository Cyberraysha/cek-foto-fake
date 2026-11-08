import streamlit as st
from PIL import Image
from datetime import datetime, date
import datetime as dt
import base64, io, time
import streamlit.components.v1 as components

st.set_page_config(page_title="RAYSHA WEDDING - Auto Slide", page_icon="💍", layout="centered")

if 'foto_list' not in st.session_state:
    st.session_state.foto_list = []
if 'lagu_data' not in st.session_state:
    st.session_state.lagu_data = None
if 'slide_idx' not in st.session_state:
    st.session_state.slide_idx = 0

st.markdown("""
<style>
.main-title { font-family: 'Great Vibes', cursive; font-size: 60px; color: #d4af37; text-align: center; }
.card { background: #fefaf5; border-radius: 20px; padding: 25px; border: 2px solid #d4af37; text-align: center; }
.count-box { background: #7a9a7a; color: white; border-radius: 10px; padding: 12px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">RAYSHA WEDDING</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Setting Undangan")
    nama_pria = st.text_input("Nama Pria", "Imam", key="nama_pria")
    nama_wanita = st.text_input("Nama Wanita", "Raysya", key="nama_wanita")
    tgl = st.date_input("Tanggal Acara", date(2026, 12, 20), key="tgl_acara")
    jam = st.time_input("Jam Acara", dt.time(9,0), key="jam_acara")
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna, Jakarta", key="lokasi")

    st.divider()
    fotos = st.file_uploader("Upload 3 Foto Prewedding (auto slide)", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, key="uploader_foto")
    if fotos:
        st.session_state.foto_list = fotos

    lagu = st.file_uploader("Upload Lagu MP3", type=["mp3","wav"], key="uploader_lagu")
    if lagu:
        st.session_state.lagu_data = lagu

# --- PREVIEW CARD ---
st.markdown('<div class="card">', unsafe_allow_html=True)

# --- FIX AUTO SLIDE YANG BENERAN JALAN ---
foto_to_show = st.session_state.foto_list

if foto_to_show and len(foto_to_show) > 0:
    # Bikin base64 semua foto
    b64_images = []
    for f in foto_to_show[:5]:
        img = Image.open(f)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        b64_images.append(b64)

    # Ini HTML slider yang jalan otomatis - pake components.html biar JS nya gak ke-block
    b64_js_array = str(b64_images) # jadi list string
    slider_html = f"""
    <html>
    <head>
    <style>
    .slideshow {{ position: relative; width: 100%; height: 400px; border-radius: 20px; overflow: hidden; }}
    .slideshow img {{ width: 100%; height: 400px; object-fit: cover; position: absolute; top:0; left:0; opacity:0; transition: opacity 1s ease-in-out; border-radius: 20px; }}
    .slideshow img.active {{ opacity:1; }}
    .dots {{ text-align:center; margin-top: 10px; }}
    .dot {{ height: 10px; width: 10px; margin: 0 4px; background-color: #ddd; border-radius: 50%; display: inline-block; transition: background-color 0.6s ease; }}
    .dot.active {{ background-color: #d4af37; }}
    </style>
    </head>
    <body>
    <div class="slideshow" id="slideshow">
        {''.join([f'<img src="data:image/jpeg;base64,{b}" id="img{i}">' for i,b in enumerate(b64_images)])}
    </div>
    <div class="dots" id="dots">
        {''.join([f'<span class="dot" id="dot{i}"></span>' for i in range(len(b64_images))])}
    </div>
    <script>
    let current = 0;
    const imgs = document.querySelectorAll('.slideshow img');
    const dots = document.querySelectorAll('.dot');
    function showSlide(n) {{
        imgs.forEach(img => img.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        imgs[n].classList.add('active');
        dots[n].classList.add('active');
    }}
    function nextSlide() {{
        current = (current + 1) % imgs.length;
        showSlide(current);
    }}
    showSlide(0);
    setInterval(nextSlide, 2500); // AUTO GANTI TIAP 2.5 DETIK BRO!
    </script>
    </body>
    </html>
    """
    components.html(slider_html, height=450)
    st.caption(f"✨ Auto slide {len(b64_images)} foto - jalan tiap 2.5 detik (siap jual)")
else:
    st.image("https://images.unsplash.com/photo-1519741497674-611481863552?w=500", width=400)
    st.caption("Upload 3 foto di sidebar biar jadi slide otomatis")

st.markdown(f'<p class="main-title" style="font-size:45px">{nama_pria} & {nama_wanita}</p>', unsafe_allow_html=True)
st.markdown(f'<h3 style="text-align:center; color:#5a6d5a;">{tgl.strftime("%A, %d %B %Y")} • {jam.strftime("%H:%M")} WIB</h3>', unsafe_allow_html=True)

# Countdown
now = datetime.now()
event_dt = datetime.combine(tgl, jam)
selisih = event_dt - now
if selisih.total_seconds() > 0:
    c1,c2,c3,c4 = st.columns(4)
    c1.markdown(f'<div class="count-box"><h2>{selisih.days}</h2>HARI</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="count-box"><h2>{selisih.seconds//3600}</h2>JAM</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="count-box"><h2>{(selisih.seconds%3600)//60}</h2>MENIT</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="count-box"><h2>{selisih.seconds%60}</h2>DETIK</div>', unsafe_allow_html=True)

if st.session_state.lagu_data:
    st.audio(st.session_state.lagu_data, format='audio/mp3', autoplay=True)

st.markdown('</div>', unsafe_allow_html=True)
st.link_button("📍 Buka Maps", f"https://www.google.com/maps/search/{lokasi}", use_container_width=True)
