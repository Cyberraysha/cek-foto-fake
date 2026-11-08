import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date
import base64, io
from PIL import Image

st.set_page_config(page_title="The Wedding of Putri & Andika - RAYSHA", page_icon="💍", layout="wide")

st.markdown("<style>header, footer, .stSidebar {display:block;} .block-container{padding:0 !important;}</style>", unsafe_allow_html=True)

# --- SETTING DI SIDEBAR (BIAR LU BISA JUALAN GANTI NAMA CEPET) ---
with st.sidebar:
    st.header("⚙️ Setting Premium")
    nama_wanita = st.text_input("Nama Wanita", "PUTRI", key="w")
    nama_pria = st.text_input("Nama Pria", "ANDIKA", key="p")
    nama_lengkap_w = st.text_input("Nama Lengkap Wanita", "Putri Cantika Sari", key="lw")
    nama_lengkap_p = st.text_input("Nama Lengkap Pria", "Putra Andika Pratama", key="lp")
    tgl_acara = st.date_input("Tanggal Acara", date(2025, 12, 28), key="tgl")
    jam_akad = st.time_input("Jam Akad", datetime.strptime("08:00", "%H:%M").time(), key="jam")
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna", key="lok")
    wa_mimin = st.text_input("WA Mimin", "6281234567890", key="wa")
    
    st.divider()
    st.caption("Upload foto: 1 Cover + 2 Pengantin + 3 Gallery")
    foto_cover = st.file_uploader("Foto Cover (Berdua)", type=["jpg","png","webp"], key="fc")
    foto_wanita = st.file_uploader("Foto Wanita (Oval)", type=["jpg","png","webp"], key="fw")
    foto_pria = st.file_uploader("Foto Pria (Oval)", type=["jpg","png","webp"], key="fp")
    fotos_gallery = st.file_uploader("Gallery 5 Foto", type=["jpg","png","webp"], accept_multiple_files=True, key="fg")

def img_to_base64(file):
    if not file: return ""
    img = Image.open(file)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

cover_b64 = img_to_base64(foto_cover)
wanita_b64 = img_to_base64(foto_wanita)
pria_b64 = img_to_base64(foto_pria)
gallery_b64 = [img_to_base64(f) for f in (fotos_gallery[:5] if fotos_gallery else [])]

# Default image jika belum upload (pakai placeholder premium)
if not cover_b64:
    cover_b64 = "https://images.unsplash.com/photo-1519741497674-611481863552?w=800"
    is_cover_url = True
else:
    is_cover_url = False

# HTML PREMIUM PERSIS VIDEO
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Great+Vibes&family=Poppins:wght@300;400&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Poppins',sans-serif; background:#fdf6f0; overflow-x:hidden;}}
.cover{{height:100vh; width:100%; background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url('{"data:image/jpeg;base64,"+cover_b64 if not is_cover_url else cover_b64}'); background-size:cover; background-position:center; display:flex; align-items:center; justify-content:center; position:fixed; top:0; left:0; z-index:9999; transition: transform 1.2s cubic-bezier(0.77,0,0.175,1);}}
.cover.hide{{transform: translateY(-100%);}}
.cover-card{{background: rgba(255,250,245,0.92); border: 3px solid #d4af8a; border-radius: 25px; padding: 30px 20px; text-align:center; max-width:350px; width:90%; box-shadow: 0 20px 60px rgba(0,0,0,0.3); backdrop-filter: blur(10px);}}
.cover-card h4{{font-family:'Cormorant Garamond',serif; letter-spacing:4px; font-size:12px; color:#8B5E3C;}}
.cover-card h1{{font-family:'Great Vibes',cursive; font-size:42px; color:#5D2E2E; margin:10px 0;}}
.cover-card .names{{font-family:'Cormorant Garamond',serif; font-size:32px; font-weight:600; color:#5D2E2E; line-height:1;}}
.cover-card .tamu{{background:white; border-radius:15px; padding:12px; margin:15px 0; border:1px dashed #d4af8a;}}
.btn-buka{{background:#5D2E2E; color:white; border:none; padding:14px 35px; border-radius:30px; font-weight:600; letter-spacing:1px; cursor:pointer; margin-top:10px; box-shadow:0 5px 15px rgba(93,46,46,0.4);}}

#main{{display:none;}}
.parallax{{height:70vh; background: url('https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'); background-attachment:fixed; background-size:cover; background-position:center; position:relative; display:flex; align-items:center; justify-content:center;}}
.parallax-overlay{{position:absolute; inset:0; background: linear-gradient(to bottom, rgba(253,246,240,0.2), rgba(253,246,240,0.8));}}
.parallax-content{{position:relative; z-index:2; text-align:center;}}
.gazebo{{width:200px; height:200px; background: white; border-radius:50% 50% 0 0; box-shadow:0 10px 30px rgba(0,0,0,0.2); display:flex; align-items:center; justify-content:center; font-size:80px;}}

.section{{padding:60px 20px; text-align:center; max-width:500px; margin:0 auto;}}
.section.maroon{{background:#5D2E2E; color:#f5e6d3;}}
.section.cream{{background:#fdf6f0; color:#5D2E2E;}}
.floral-border{{border:12px solid transparent; border-image: url('https://www.pngall.com/wp-content/uploads/13/Floral-Border-PNG-Photo.png') 30 stretch; padding:20px;}}
.title-script{{font-family:'Great Vibes',cursive; font-size:38px; color:#d4af8a;}}
.title-serif{{font-family:'Cormorant Garamond',serif; font-size:34px; font-weight:600; letter-spacing:2px;}}
.oval-frame{{width:200px; height:280px; border-radius:50% / 60%; overflow:hidden; margin:20px auto; border:6px solid #d4af8a; box-shadow:0 10px 30px rgba(0,0,0,0.2);}}
.oval-frame img{{width:100%; height:100%; object-fit:cover;}}
.count-grid{{display:flex; gap:10px; justify-content:center; margin:20px 0;}}
.count-item{{background: rgba(255,255,255,0.1); border:1px solid #d4af8a; border-radius:15px; padding:15px 10px; min-width:70px;}}
.count-item h2{{font-size:28px;}}
.gallery-grid{{display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:20px;}}
.gallery-grid img{{width:100%; height:180px; object-fit:cover; border-radius:15px;}}

@keyframes fadeUp{{from{{opacity:0; transform:translateY(30px);}} to{{opacity:1; transform:translateY(0);}}}}
.fade{{animation: fadeUp 1s ease forwards;}}
</style>
</head>
<body>

<!-- COVER PERSIS VIDEO 0-1 DETIK -->
<div class="cover" id="cover">
  <div class="cover-card">
    <h4>THE WEDDING OF</h4>
    <div class="names">{nama_wanita} & {nama_pria}</div>
    <p style="font-size:12px; margin-top:5px; color:#8B5E3C;">{tgl_acara.strftime('%A, %d %B %Y')}</p>
    <div class="tamu">
      <p style="font-size:11px; color:#8B5E3C;">Kepada Yth.</p>
      <p style="font-weight:600; color:#5D2E2E;">Tamu Undangan</p>
      <p style="font-size:10px; color:#8B5E3C;">di Tempat</p>
    </div>
    <button class="btn-buka" onclick="bukaUndangan()">💌 Buka Undangan</button>
  </div>
</div>

<!-- MAIN CONTENT - SCROLL KAYA VIDEO LU -->
<div id="main">
  <!-- PARALLAX HUTAN + GAZEBO + KUDA - PERSIS 2-9 DETIK VIDEO -->
  <div class="parallax">
    <div class="parallax-overlay"></div>
    <div class="parallax-content fade">
      <div style="background: rgba(255,255,255,0.9); padding:20px; border-radius:20px; border:3px solid #d4af8a;">
        <p style="font-family:'Great Vibes'; font-size:28px; color:#5D2E2E;">Welcome to</p>
        <p style="font-family:'Cormorant Garamond'; font-size:18px; letter-spacing:3px;">THE WEDDING</p>
        <div style="font-size:60px;">🏛️</div>
        <p style="font-size:12px; color:#8B5E3C;">Scroll ke bawah ↓</p>
      </div>
    </div>
  </div>

  <!-- SECTION NAMA - 10 DETIK VIDEO -->
  <div class="section cream">
    <p class="title-script">The Wedding Of</p>
    <h1 class="title-serif">{nama_wanita}<br>&<br>{nama_pria}</h1>
    <p style="margin-top:10px; letter-spacing:2px; font-size:12px;">{tgl_acara.strftime('%A, %d %B %Y')}</p>
    <p style="margin-top:30px; font-size:13px; line-height:1.8; color:#8B5E3C;">
      "Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu isteri-isteri dari jenismu sendiri, supaya kamu cenderung dan merasa tenteram kepadanya"
      <br><br><b>QS. Ar-Rum: 21</b>
    </p>
  </div>

  <!-- FOTO BERDUA - 12-14 DETIK VIDEO -->
  <div class="section maroon">
    <div class="oval-frame" style="width:280px; height:350px;">
      <img src="{"data:image/jpeg;base64,"+cover_b64 if not is_cover_url else cover_b64}" />
    </div>
    <p style="font-family:'Great Vibes'; font-size:32px; margin-top:15px;">{nama_wanita} & {nama_pria}</p>
  </div>

  <!-- BRIDE & GROOM - 15-18 DETIK VIDEO -->
  <div class="section cream">
    <p class="title-script">Bride & Groom</p>
    <div style="margin:30px 0;">
      <div class="oval-frame">
        <img src="{f"data:image/jpeg;base64,{wanita_b64}" if wanita_b64 else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"}" />
      </div>
      <h3 class="title-serif" style="font-size:26px;">{nama_wanita}</h3>
      <p style="font-size:13px; color:#8B5E3C;">{nama_lengkap_w}</p>
      <p style="font-size:11px; margin-top:5px;">Putri Pertama Bapak H. Ahmad & Ibu Siti</p>
    </div>
    
    <p style="font-family:'Great Vibes'; font-size:50px; color:#d4af8a;">&</p>
    
    <div style="margin:30px 0;">
      <div class="oval-frame">
        <img src="{f"data:image/jpeg;base64,{pria_b64}" if pria_b64 else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"}" />
      </div>
      <h3 class="title-serif" style="font-size:26px;">{nama_pria}</h3>
      <p style="font-size:13px; color:#8B5E3C;">{nama_lengkap_p}</p>
      <p style="font-size:11px; margin-top:5px;">Putra Pertama Bapak H. Budi & Ibu Ani</p>
    </div>
  </div>

  <!-- COUNTDOWN - 19-21 DETIK VIDEO -->
  <div class="section maroon">
    <p class="title-script" style="color:#f5e6d3;">Menuju Hari Bahagia</p>
    <div class="count-grid" id="countdown">
      <div class="count-item"><h2 id="d">46</h2><p>HARI</p></div>
      <div class="count-item"><h2 id="h">20</h2><p>JAM</p></div>
      <div class="count-item"><h2 id="m">09</h2><p>MENIT</p></div>
      <div class="count-item"><h2 id="s">17</h2><p>DETIK</p></div>
    </div>
    <p style="font-size:12px; margin-top:15px; opacity:0.8;">{tgl_acara.strftime('%A, %d %B %Y')} • {jam_akad.strftime('%H:%M')} WIB<br>{lokasi}</p>
    <a href="https://maps.google.com" target="_blank" style="display:inline-block; margin-top:15px; background:#f5e6d3; color:#5D2E2E; padding:10px 20px; border-radius:20px; text-decoration:none; font-size:12px; font-weight:600;">📍 Lihat Lokasi</a>
  </div>

  <!-- GALLERY -->
  <div class="section cream">
    <p class="title-script">Our Gallery</p>
    <div class="gallery-grid">
      {"".join([f'<img src="data:image/jpeg;base64,{b}" />' for b in gallery_b64]) if gallery_b64 else '<img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400" /><img src="https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400" /><img src="https://images.unsplash.com/photo-1520854221256-17451ccdf07b?w=400" /><img src="https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?w=400" />'}
    </div>
  </div>

  <!-- RSVP -->
  <div class="section maroon">
    <p class="title-script" style="color:#f5e6d3;">RSVP & Ucapan</p>
    <p style="font-size:12px; margin:10px 0;">Konfirmasi kehadiran & beri doa terbaik</p>
    <a href="https://wa.me/{wa_mimin}?text=Halo%20{nama_wanita}%20%26%20{nama_pria}%20Saya%20akan%20hadir%20di%20acara%20{tgl_acara}" target="_blank" style="display:block; background:#25D366; color:white; padding:14px; border-radius:30px; text-decoration:none; font-weight:700; margin-top:20px;">💬 Konfirmasi via WhatsApp</a>
    <p style="font-size:10px; margin-top:30px; opacity:0.6;">Made with ❤️ by RAYSHA WEDDING</p>
  </div>
</div>

<script>
function bukaUndangan(){{
  document.getElementById('cover').classList.add('hide');
  setTimeout(()=>{{ document.getElementById('main').style.display='block'; window.scrollTo(0,0); }}, 800);
  // Play music
  var audio = new Audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3');
  audio.loop = true;
  audio.play().catch(()=>{{}});
}}
// Countdown live
var target = new Date("{tgl_acara} {jam_akad}").getTime();
setInterval(function(){{
  var now = new Date().getTime();
  var diff = target - now;
  if(diff>0){{
    document.getElementById('d').innerHTML = Math.floor(diff/(1000*60*60*24));
    document.getElementById('h').innerHTML = Math.floor((diff%(1000*60*60*24))/(1000*60*60));
    document.getElementById('m').innerHTML = Math.floor((diff%(1000*60*60))/(1000*60));
    document.getElementById('s').innerHTML = Math.floor((diff%(1000*60))/1000);
  }}
}},1000);
</script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)

st.caption("✅ Upload foto di sidebar biar jadi kayak video PUTRI & ANDIKA. Tombol Buka Undangan → scroll ada efek gazebo + kuda kayak video lu.")
