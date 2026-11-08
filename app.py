import streamlit as st
from PIL import Image
from datetime import datetime, date
import datetime as dt
import base64, io
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="RAYSHA WEDDING - Pro", page_icon="💍", layout="centered")

# --- SESSION STATE ---
if 'foto_list' not in st.session_state:
    st.session_state.foto_list = []
if 'lagu_data' not in st.session_state:
    st.session_state.lagu_data = None
if 'tamu_list' not in st.session_state:
    st.session_state.tamu_list = []

st.markdown("""
<style>
.main-title { font-family: 'Great Vibes', cursive; font-size: 55px; color: #d4af37; text-align: center; margin: 0; }
.card { background: #fefaf5; border-radius: 20px; padding: 20px; border: 2px solid #d4af37; }
.countdown-row { display: flex; gap: 8px; justify-content: center; margin: 15px 0; }
.count-box { background: #7a9a7a; color: white; border-radius: 12px; padding: 12px 5px; text-align: center; flex: 1; }
.count-box h2 { margin:0; font-size: 28px; }
.count-box p { margin:0; font-size: 12px; }
.music-top { position: sticky; top: 0; z-index: 999; background: #fefaf5; padding: 10px; border-radius: 15px; border: 1px solid #d4af37; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">RAYSHA WEDDING</p>', unsafe_allow_html=True)

# --- SIDEBAR LENGKAP + WA CLIENT ---
with st.sidebar:
    st.header("⚙️ Setting Undangan")
    nama_pria = st.text_input("Nama Pria", "Imam", key="nama_pria")
    nama_wanita = st.text_input("Nama Wanita", "Raysya", key="nama_wanita")
    wa_client = st.text_input("WA Client (628xxx)", "6281234567890", key="wa_client", help="WA pengantin buat nerima RSVP")
    tgl = st.date_input("Tanggal Acara", date(2026, 12, 20), key="tgl_acara")
    jam = st.time_input("Jam Acara", dt.time(9,0), key="jam_acara")
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna, Jakarta", key="lokasi")
    maps_link = st.text_input("Link Google Maps", "https://maps.google.com", key="maps")

    st.divider()
    fotos = st.file_uploader("Upload 3 Foto (auto slide)", type=["jpg","jpeg","png","webp"], accept_multiple_files=True, key="uploader_foto")
    if fotos:
        st.session_state.foto_list = fotos
        st.success(f"{len(fotos)} foto siap slide!")

    lagu = st.file_uploader("Upload Lagu MP3", type=["mp3","wav"], key="uploader_lagu")
    if lagu:
        st.session_state.lagu_data = lagu
        st.success("Lagu di atas siap!")

    st.divider()
    st.subheader("📋 Daftar Tamu (Admin)")
    if st.session_state.tamu_list:
        df = pd.DataFrame(st.session_state.tamu_list)
        st.dataframe(df, use_container_width=True)
        st.download_button("Download Excel Tamu", df.to_csv(index=False), "daftar_tamu.csv", "text/csv", use_container_width=True)
    else:
        st.caption("Belum ada tamu RSVP")

# --- MUSIK DI ATAS - FIX SESUAI REQUEST LU ---
if st.session_state.lagu_data:
    st.markdown('<div class="music-top">🎵 <b>Wedding Song - Auto Play</b>', unsafe_allow_html=True)
    st.audio(st.session_state.lagu_data, format='audio/mp3', autoplay=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("🎵 Upload lagu di sidebar, nanti muncul di ATAS sini (auto-play)")

# --- CARD UTAMA ---
st.markdown('<div class="card">', unsafe_allow_html=True)

# SLIDER OTOMATIS
foto_to_show = st.session_state.foto_list
if foto_to_show and len(foto_to_show) > 0:
    b64_images = []
    for f in foto_to_show[:5]:
        img = Image.open(f)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        b64_images.append(b64)

    slider_html = f"""
    <html><head><style>
    .slideshow {{ position: relative; width: 100%; height: 380px; border-radius: 20px; overflow: hidden; }}
    .slideshow img {{ width: 100%; height: 380px; object-fit: cover; position: absolute; top:0; left:0; opacity:0; transition: opacity 1s ease-in-out; }}
    .slideshow img.active {{ opacity:1; }}
    .dots {{ text-align:center; margin-top: 10px; }}
    .dot {{ height: 10px; width: 10px; margin: 0 4px; background-color: #ddd; border-radius: 50%; display: inline-block; }}
    .dot.active {{ background-color: #d4af37; }}
    </style></head><body>
    <div class="slideshow" id="slideshow">
        {''.join([f'<img src="data:image/jpeg;base64,{b}" id="img{i}">' for i,b in enumerate(b64_images)])}
    </div>
    <div class="dots">{''.join([f'<span class="dot" id="dot{i}"></span>' for i in range(len(b64_images))])}</div>
    <script>
    let current = 0;
    const imgs = document.querySelectorAll('.slideshow img');
    const dots = document.querySelectorAll('.dot');
    function showSlide(n){{ imgs.forEach(i=>i.classList.remove('active')); dots.forEach(d=>d.classList.remove('active')); imgs[n].classList.add('active'); dots[n].classList.add('active'); }}
    function nextSlide(){{ current = (current+1)%imgs.length; showSlide(current); }}
    showSlide(0); setInterval(nextSlide, 2500);
    </script></body></html>
    """
    components.html(slider_html, height=430)
else:
    st.image("https://images.unsplash.com/photo-1519741497674-611481863552?w=500", width=400)

st.markdown(f'<p class="main-title" style="font-size:42px">{nama_pria} & {nama_wanita}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#5a6d5a;">{tgl.strftime("%A, %d %B %Y")} • {jam.strftime("%H:%M")} WIB<br>{lokasi}</p>', unsafe_allow_html=True)

# --- COUNTDOWN FIX JADI SEJAJAR (GAK NUMPUK KE BAWAH KAYAK SCREENSHOT LU) ---
now = datetime.now()
event_dt = datetime.combine(tgl, jam)
selisih = event_dt - now
if selisih.total_seconds() > 0:
    st.markdown(f"""
    <div class="countdown-row">
        <div class="count-box"><h2>{selisih.days}</h2><p>HARI</p></div>
        <div class="count-box"><h2>{selisih.seconds//3600}</h2><p>JAM</p></div>
        <div class="count-box"><h2>{(selisih.seconds%3600)//60}</h2><p>MENIT</p></div>
        <div class="count-box"><h2>{selisih.seconds%60}</h2><p>DETIK</p></div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# --- RSVP + WA CLIENT + DAFTAR TAMU ---
st.subheader("💌 Konfirmasi Kehadiran")
with st.form("rsvp_form", clear_on_submit=True):
    nama_tamu = st.text_input("Nama Kamu")
    jml = st.selectbox("Jumlah Tamu", [1,2,3,4,5])
    ucapan = st.text_area("Ucapan & Doa")
    hadir = st.radio("Kehadiran", ["Hadir", "Tidak Hadir"], horizontal=True)
    submit = st.form_submit_button("Kirim RSVP", use_container_width=True, type="primary")

    if submit and nama_tamu:
        data_tamu = {"Nama": nama_tamu, "Jumlah": jml, "Hadir": hadir, "Ucapan": ucapan, "Waktu": datetime.now().strftime("%d-%m %H:%M")}
        st.session_state.tamu_list.append(data_tamu)
        st.success(f"Makasih {nama_tamu}! Data masuk daftar tamu.")
        st.balloons()
        # Auto WA ke client
        pesan = f"Halo {nama_pria}&{nama_wanita}, Saya {nama_tamu} ({jml} orang) konfirmasi {hadir} di acara {tgl}. Ucapan: {ucapan}"
        wa_url = f"https://wa.me/{wa_client}?text={pesan.replace(' ','%20')}"
        st.markdown(f"[📲 Kirim WA ke Pengantin {nama_pria}]({wa_url})")

# Tampilkan daftar tamu di public (opsional)
if st.session_state.tamu_list:
    st.divider()
    st.subheader(f"🎉 {len(st.session_state.tamu_list)} Tamu Sudah Konfirmasi")
    for t in st.session_state.tamu_list[-5:][::-1]: # 5 terbaru
        st.markdown(f"**{t['Nama']}** ({t['Jumlah']} org) - {t['Hadir']}  \n_{t['Ucapan']}_")

st.markdown('</div>', unsafe_allow_html=True)

st.link_button("📍 Buka Lokasi di Maps", maps_link, use_container_width=True)
