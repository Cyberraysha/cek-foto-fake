import streamlit as st, base64, io
import streamlit.components.v1 as components
from PIL import Image
from datetime import datetime, date

st.set_page_config(page_title="Wedding Putri & Andika - Final", layout="wide")
st.markdown("<style>.block-container{padding:0 !important;}</style>", unsafe_allow_html=True)

if 'lagu_b64' not in st.session_state:
    st.session_state.lagu_b64 = None

with st.sidebar:
    st.markdown("## 🎵 UPLOAD MUSIK DI SINI")
    lagu = st.file_uploader("Pilih MP3 (max 5MB)", type=["mp3","m4a","wav","ogg"], key="musik_top")
    if lagu:
        st.session_state.lagu_b64 = base64.b64encode(lagu.getvalue()).decode()
        st.success(f"✅ {lagu.name} AKTIF!")
        st.audio(lagu)
    
    st.divider()
    st.header("Data Pengantin")
    nw = st.text_input("Nama Wanita", "PUTRI")
    np = st.text_input("Nama Pria", "ANDIKA")
    nlw = st.text_input("Nama Lengkap Wanita", "Putri Cantika Sari")
    nlp = st.text_input("Nama Lengkap Pria", "Putra Andika Pratama")
    
    # FIX 1: TAMBAH NAMA ORANG TUA
    st.markdown("### 👨‍👩‍👧 Orang Tua Wanita")
    ayah_w = st.text_input("Ayah Wanita", "Bapak H. Ahmad Sutrisno")
    ibu_w = st.text_input("Ibu Wanita", "Ibu Hj. Siti Aminah")
    st.markdown("### 👨‍👩‍👦 Orang Tua Pria")
    ayah_p = st.text_input("Ayah Pria", "Bapak H. Budi Santoso")
    ibu_p = st.text_input("Ibu Pria", "Ibu Hj. Ani Wijaya")
    
    tgl = st.date_input("Tanggal", date(2025,12,28))
    jam = st.time_input("Jam", datetime.strptime("08:00","%H:%M").time())
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna, Jakarta")
    wa = st.text_input("WA Mimin", "6281234567890")
    
    st.divider()
    st.header("Foto")
    st.caption("Upload 5 foto buat SLIDE atas, 5 lagi buat GALLERY bawah")
    fc = st.file_uploader("Foto Cover Berdua (5 foto = auto slide)", type=["jpg","png","webp"], accept_multiple_files=True, key="fc_multi")
    fw = st.file_uploader("Foto Wanita Oval", type=["jpg","png","webp"], key="fw")
    fp = st.file_uploader("Foto Pria Oval", type=["jpg","png","webp"], key="fp")
    fg = st.file_uploader("Gallery Bawah (5 Foto Terakhir)", type=["jpg","png","webp"], accept_multiple_files=True, key="fg_multi")

def to_b64(f):
    if not f: return ""
    try:
        img = Image.open(f)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()
    except: return ""

# Proses foto
cover_list = []
if fc:
    for f in fc[:5]: # 5 foto pertama buat slide
        cover_list.append(to_b64(f))
if not cover_list:
    cover_list = ["https://images.unsplash.com/photo-1519741497674-611481863552?w=800"]

wanita_b64 = to_b64(fw)
pria_b64 = to_b64(fp)
gallery_list = []
if fg:
    for f in fg[:5]:
        gallery_list.append(to_b64(f))

# Musik
musik_src = f"data:audio/mp3;base64,{st.session_state.lagu_b64}" if st.session_state.lagu_b64 else "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
musik_label = "✅ LAGU CUSTOM" if st.session_state.lagu_b64 else "LAGU DEFAULT"

# Buat HTML slide cover
slide_imgs_html = ""
dots_html = ""
for i, b64 in enumerate(cover_list):
    if b64.startswith("http"):
        src = b64
    else:
        src = f"data:image/jpeg;base64,{b64}"
    active = "active" if i==0 else ""
    slide_imgs_html += f'<img src="{src}" class="{active}">'
    dots_html += f'<span class="dot {active}"></span>'

gallery_html = ""
if gallery_list:
    for b64 in gallery_list:
        gallery_html += f'<img src="data:image/jpeg;base64,{b64}">'
else:
    gallery_html = '<p style="color:#8B5E3C; font-size:12px;">Upload 5 foto di "Gallery Bawah" biar muncul di sini</p>'

html = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Great+Vibes&family=Poppins:wght@300;400&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{font-family:Poppins,sans-serif; background:#fdf6f0}}
.cover{{height:100vh;width:100%;position:fixed;top:0;left:0;z-index:9999;transition:1.2s;overflow:hidden}}
.cover .slideshow{{width:100%;height:100%;position:relative}}
.cover .slideshow img{{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:opacity 1s ease-in-out}}
.cover .slideshow img.active{{opacity:1}}
.cover-overlay{{position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,0.3),rgba(0,0,0,0.5));display:flex;align-items:center;justify-content:center}}
.card{{background:rgba(255,250,245,0.95);border:3px solid #d4af8a;border-radius:25px;padding:30px 20px;text-align:center;max-width:350px;width:90%;backdrop-filter:blur(10px)}}
.btn{{background:#5D2E2E;color:white;border:none;padding:14px 35px;border-radius:30px;font-weight:600;cursor:pointer;box-shadow:0 5px 15px rgba(93,46,46,0.4)}}
.cover.hide{{transform:translateY(-100%)}}
.dots{{position:absolute;bottom:100px;left:50%;transform:translateX(-50%);display:flex;gap:8px;z-index:10}}
.dot{{width:10px;height:10px;background:rgba(255,255,255,0.5);border-radius:50%;transition:0.3s}}
.dot.active{{background:#d4af8a; width:24px; border-radius:5px}}
#main{{display:none}}
.sec{{padding:60px 20px;text-align:center;max-width:500px;margin:0 auto}}
.maroon{{background:#5D2E2E;color:#f5e6d3}} .cream{{background:#fdf6f0;color:#5D2E2E}}
.oval{{width:200px;height:280px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:6px solid #d4af8a;box-shadow:0 10px 30px rgba(0,0,0,0.2)}}
.oval img{{width:100%;height:100%;object-fit:cover}}
.parent{{font-size:11px; color:#8B5E3C; margin-top:8px; line-height:1.4}}
.gallery-grid{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:20px}}
.gallery-grid img{{width:100%;height:180px;object-fit:cover;border-radius:15px;border:3px solid #d4af8a}}
.float{{position:fixed;bottom:20px;right:20px;background:#5D2E2E;color:white;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:100;cursor:pointer;box-shadow:0 4px 15px rgba(0,0,0,0.3)}}
</style></head><body>

<div class="cover" id="cover">
  <div class="slideshow" id="slide">{slide_imgs_html}</div>
  <div class="dots" id="dots">{dots_html}</div>
  <div class="cover-overlay">
    <div class="card">
      <h4 style="letter-spacing:4px;font-size:12px;color:#8B5E3C">THE WEDDING OF</h4>
      <div style="font-family:'Cormorant Garamond';font-size:32px;font-weight:600;color:#5D2E2E;margin:10px 0">{nw} & {np}</div>
      <p style="font-size:11px;color:#8B5E3C">{tgl.strftime('%A, %d %B %Y')}</p>
      <div style="background:white;border-radius:15px;padding:12px;margin:15px 0;border:1px dashed #d4af8a">
        <p style="font-size:11px">Kepada Yth.</p><p style="font-weight:600">Tamu Undangan</p><p style="font-size:9px;color:#d4af8a">{musik_label} • {len(cover_list)} Foto Slide</p>
      </div>
      <button class="btn" onclick="buka()">💌 Buka Undangan</button>
    </div>
  </div>
</div>

<div id="main">
  <div class="sec cream">
    <p style="font-family:'Great Vibes';font-size:38px;color:#d4af8a">The Wedding Of</p>
    <h1 style="font-family:'Cormorant Garamond';font-size:34px">{nw}<br>&<br>{np}</h1>
    <p style="letter-spacing:2px;font-size:12px;margin-top:10px">{tgl.strftime('%A, %d %B %Y')} • {jam.strftime('%H:%M')} WIB</p>
  </div>

  <div class="sec cream">
    <p style="font-family:'Great Vibes';font-size:32px;color:#d4af8a">Bride & Groom</p>
    
    <div style="margin:30px 0">
      <div class="oval"><img src="{f"data:image/jpeg;base64,{wanita_b64}" if wanita_b64 else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"}"></div>
      <h3 style="font-family:'Cormorant Garamond';font-size:26px">{nw}</h3>
      <p style="font-size:13px;font-weight:600">{nlw}</p>
      <div class="parent">Putri dari<br><b>{ayah_w}<br>& {ibu_w}</b></div>
    </div>

    <p style="font-family:'Great Vibes';font-size:60px;color:#d4af8a">&</p>

    <div style="margin:30px 0">
      <div class="oval"><img src="{f"data:image/jpeg;base64,{pria_b64}" if pria_b64 else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"}"></div>
      <h3 style="font-family:'Cormorant Garamond';font-size:26px">{np}</h3>
      <p style="font-size:13px;font-weight:600">{nlp}</p>
      <div class="parent">Putra dari<br><b>{ayah_p}<br>& {ibu_p}</b></div>
    </div>
  </div>

  <div class="sec maroon">
    <p style="font-family:'Great Vibes';font-size:28px">Menuju Hari Bahagia</p>
    <p style="font-size:12px;margin-top:15px">{tgl.strftime('%A, %d %B %Y')} • {jam.strftime('%H:%M')} WIB<br>{lokasi}</p>
    <a href="https://wa.me/{wa}?text=Halo%20{nw}%20%26%20{np}" target="_blank" style="display:block;background:#25D366;color:white;padding:14px;border-radius:30px;text-decoration:none;font-weight:700;margin-top:20px">💬 Chat Mimin</a>
  </div>

  <div class="sec cream">
    <p style="font-family:'Great Vibes';font-size:32px;color:#d4af8a">Our Gallery</p>
    <p style="font-size:11px;color:#8B5E3C">5 Foto Terakhir - Momen Bahagia</p>
    <div class="gallery-grid">
      {gallery_html}
    </div>
  </div>

  <div class="sec maroon">
    <p style="font-size:10px;opacity:0.6">Made with ❤️ by RAYSHA WEDDING • {len(cover_list)} slide + {len(gallery_list)} gallery</p>
  </div>
</div>

<div class="float" id="mBtn" onclick="toggleM()">🎵</div>
<audio id="aud" loop src="{musik_src}"></audio>

<script>
var cur=0; var play=false;
function showSlide(n){{
  var imgs=document.querySelectorAll('#slide img'); var dots=document.querySelectorAll('.dot');
  imgs.forEach(i=>i.classList.remove('active')); dots.forEach(d=>d.classList.remove('active'));
  if(imgs[n]){{ imgs[n].classList.add('active'); dots[n].classList.add('active'); }}
}}
function nextSlide(){{ cur=(cur+1)%{len(cover_list)}; showSlide(cur); }}
var slideInterval = setInterval(nextSlide, 3000);

function buka(){{
  document.getElementById('cover').classList.add('hide');
  clearInterval(slideInterval);
  setTimeout(()=>{{document.getElementById('main').style.display='block'}},800);
  var a=document.getElementById('aud'); a.play().then(()=>{{play=true;document.getElementById('mBtn').innerHTML='⏸️'}}).catch(()=>{{}});
}}
function toggleM(){{
  var a=document.getElementById('aud'); var b=document.getElementById('mBtn');
  if(play){{a.pause();b.innerHTML='🎵';play=false}} else {{a.play();b.innerHTML='⏸️';play=true}}
}}
showSlide(0);
</script>
</body></html>
"""

components.html(html, height=950, scrolling=True)
