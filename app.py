import streamlit as st, base64, io
import streamlit.components.v1 as components
from PIL import Image
from datetime import datetime, date

st.set_page_config(page_title="PUTRI & ANDIKA - Final", layout="wide")
st.markdown("<style>.block-container{padding:0 !important;} header{visibility:hidden;}</style>", unsafe_allow_html=True)

if 'lagu_b64' not in st.session_state:
    st.session_state.lagu_b64 = None

with st.sidebar:
    st.markdown("## 🎵 1. MUSIK DI ATAS (WAJIB)")
    lagu = st.file_uploader("Upload MP3 sesuai keinginan", type=["mp3","m4a","wav","ogg"], key="musik_top")
    if lagu:
        st.session_state.lagu_b64 = base64.b64encode(lagu.getvalue()).decode()
        st.success(f"✅ LAGU {lagu.name} AKTIF DI ATAS!")
        st.audio(lagu)
    
    st.divider()
    st.header("👰🤵 Data Pasangan")
    nw = st.text_input("Panggilan Wanita", "PUTRI")
    np = st.text_input("Panggilan Pria", "ANDIKA")
    nlw = st.text_input("Nama Lengkap Wanita", "Putri Cantika Sari")
    nlp = st.text_input("Nama Lengkap Pria", "Putra Andika Pratama")
    
    st.subheader("👨‍👩‍👧 Nama Orang Tua Sesuai Keinginan")
    ayah_w = st.text_input("Ayah Wanita", "Bapak H. Wahyu Widodo")
    ibu_w = st.text_input("Ibu Wanita", "Ibu Hj. Sri Mulyani")
    ayah_p = st.text_input("Ayah Pria", "Bapak H. Marno")
    ibu_p = st.text_input("Ibu Pria", "Ibu Hj. Siti Halimah")
    
    tgl = st.date_input("Tanggal", date(2025,12,28))
    jam = st.time_input("Jam", datetime.strptime("08:00","%H:%M").time())
    lokasi = st.text_input("Nama Gedung", "Gedung Serbaguna, Bekasi")
    
    st.subheader("📍 Shareloc (Google Maps)")
    link_maps = st.text_input("Link Google Maps", "https://maps.app.goo.gl/xyz123")
    embed_maps = st.text_area("Embed Maps (iframe src)", placeholder="https://www.google.com/maps/embed?pb=...")
    
    st.divider()
    st.header("📸 Foto Auto Slide")
    st.caption("5 Foto atas = auto slide pas client kirim ke tamu")
    fc = st.file_uploader("5 Foto Cover Atas (Auto Slide)", type=["jpg","png","webp"], accept_multiple_files=True, key="fc")
    fw = st.file_uploader("Foto Wanita Oval", type=["jpg","png","webp"], key="fw")
    fp = st.file_uploader("Foto Pria Oval", type=["jpg","png","webp"], key="fp")
    fg = st.file_uploader("5 Foto Gallery Bawah", type=["jpg","png","webp"], accept_multiple_files=True, key="fg")
    wa = st.text_input("WA Mimin", "6281234567890")

def to_b64(f):
    if not f: return ""
    try:
        img = Image.open(f)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()
    except: return ""

cover_list = [to_b64(f) for f in (fc[:5] if fc else [])]
if not cover_list:
    cover_list = ["https://images.unsplash.com/photo-1519741497674-611481863552?w=800"]
wanita_b64 = to_b64(fw)
pria_b64 = to_b64(fp)
gallery_list = [to_b64(f) for f in (fg[:5] if fg else [])]

musik_src = f"data:audio/mp3;base64,{st.session_state.lagu_b64}" if st.session_state.lagu_b64 else "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
musik_label = "LAGU CUSTOM" if st.session_state.lagu_b64 else "LAGU DEFAULT"

slide_html = ""
for i, b in enumerate(cover_list):
    src = b if b.startswith("http") else f"data:image/jpeg;base64,{b}"
    active = "active" if i==0 else ""
    slide_html += f'<img src="{src}" class="{active}">'

gallery_html = ""
for b in gallery_list:
    gallery_html += f'<img src="data:image/jpeg;base64,{b}"><img src="data:image/jpeg;base64,{b}">' if False else f'<div class="g-item"><img src="data:image/jpeg;base64,{b}"></div>'
if not gallery_list:
    gallery_html = '<div class="g-item"><img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400"></div>'*3

html_code = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Great+Vibes&family=Poppins:wght@300;400&family=Playfair+Display:ital@0;1&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{font-family:'Poppins',sans-serif;background:#fdf2f2;overflow-x:hidden}}
/* MUSIC DI ATAS */
.music-top{{position:fixed;top:0;left:0;right:0;background:rgba(93,46,46,0.95);color:#f5e6d3;padding:10px 15px;display:flex;justify-content:space-between;align-items:center;z-index:10000;backdrop-filter:blur(10px)}}
.music-top .info{{font-size:11px}} .music-top button{{background:#d4af8a;border:none;color:#5D2E2E;padding:6px 12px;border-radius:20px;font-weight:700;cursor:pointer}}

/* COVER */
.cover{{height:100vh;width:100%;position:fixed;top:0;left:0;z-index:9999;transition:transform 1.2s cubic-bezier(0.77,0,0.175,1);overflow:hidden}}
.cover .slideshow{{width:100%;height:100%;position:relative}} .cover .slideshow img{{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:opacity 1.2s}} .cover .slideshow img.active{{opacity:1}}
.cover-overlay{{position:absolute;inset:0;background:linear-gradient(to bottom,rgba(0,0,0,0.1),rgba(0,0,0,0.4));display:flex;align-items:center;justify-content:center;padding:20px}}
.card{{background:rgba(255,248,240,0.96);border-radius:28px;padding:0;overflow:hidden;max-width:380px;width:92%;box-shadow:0 25px 80px rgba(0,0,0,0.4);border:8px solid #fff}}
.card-inner{{border:2px solid #d4af8a;margin:8px;border-radius:20px;padding:25px 20px;text-align:center;background: url('https://i.ibb.co/0jZ3QYp/floral-border.png')}}
.cover.hide{{transform:translateY(-100%)}}

/* PARALLAX GAZEBO + KUDA PERSIS VIDEO */
.parallax{{height:85vh;background: linear-gradient(to bottom, #fdf2f2 0%, transparent 20%, transparent 80%, #fdf2f2 100%), url('https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200'); background-size:cover; background-position:center; background-attachment:fixed; position:relative; display:flex; align-items:center; justify-content:center;}}
.parallax::before{{content:'🏛️';font-size:180px;position:absolute;opacity:0.9;filter:drop-shadow(0 10px 20px rgba(0,0,0,0.2))}}
.parallax::after{{content:'🐎';font-size:80px;position:absolute;bottom:20%;left:15%;opacity:0.8}}

.sec{{padding:70px 20px;text-align:center;max-width:520px;margin:0 auto;position:relative}}
.sec.cream{{background:#fdf2f2 url('https://www.transparenttextures.com/patterns/floral.png'); color:#5D2E2E}}
.sec.maroon{{background:#5D2E2E; color:#f5e6d3}}
.floral-frame{{border:12px solid transparent; border-image: url('https://i.imgur.com/Qb6s6yK.png') 30 stretch;}}
.title-script{{font-family:'Great Vibes',cursive;font-size:42px;color:#d4af8a}}
.title-serif{{font-family:'Cormorant Garamond',serif;font-size:36px;font-weight:600;letter-spacing:2px}}
.oval{{width:210px;height:300px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:7px solid #d4af8a;box-shadow:0 15px 40px rgba(0,0,0,0.3)}}
.oval img{{width:100%;height:100%;object-fit:cover}}
.parent-box{{background:rgba(255,255,255,0.08);border:1px solid #d4af8a;border-radius:15px;padding:12px;margin-top:10px}}
.count-box{{display:flex;gap:10px;justify-content:center;margin:20px 0}} .count-item{{background:rgba(255,255,255,0.1);border:1px solid #d4af8a;border-radius:15px;padding:14px 10px;min-width:72px}} .count-item h2{{font-size:30px;font-family:'Cormorant Garamond'}}
.g-slider{{display:flex;gap:10px;overflow-x:auto;scroll-snap-type:x mandatory;padding:10px 0;scroll-behavior:smooth}} .g-slider::-webkit-scrollbar{{display:none}} .g-item{{min-width:75%;scroll-snap-align:center}} .g-item img{{width:100%;height:260px;object-fit:cover;border-radius:18px;border:4px solid #d4af8a}}
.map-btn{{background:#f5e6d3;color:#5D2E2E;padding:12px 24px;border-radius:30px;text-decoration:none;font-weight:700;display:inline-block;margin-top:15px}}
.float-music{{position:fixed;bottom:25px;right:20px;background:#5D2E2E;color:#f5e6d3;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:100;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,0.4);border:2px solid #d4af8a;animation:spin 4s linear infinite}}
@keyframes spin{{0%{{transform:rotate(0)}} 100%{{transform:rotate(360deg)}}}} .float-music.paused{{animation:none}}
</style></head><body>

<div class="music-top" id="musicTop">
  <div class="info">🎵 {musik_label} • {nw} & {np} • Auto Slide Aktif</div>
  <button id="topBtn" onclick="toggleM()">⏸️ Pause</button>
</div>

<div class="cover" id="cover">
  <div class="slideshow" id="slide">{slide_html}</div>
  <div class="cover-overlay">
    <div class="card">
      <div class="card-inner">
        <p style="letter-spacing:5px;font-size:11px;color:#8B5E3C;font-family:'Cormorant Garamond'">THE WEDDING OF</p>
        <div style="width:80px;height:80px;margin:15px auto;border-radius:50%;overflow:hidden;border:3px solid #d4af8a"><img src="{cover_list[0] if cover_list[0].startswith('http') else f"data:image/jpeg;base64,{cover_list[0]}"}" style="width:100%;height:100%;object-fit:cover"></div>
        <div style="font-family:'Playfair Display';font-size:30px;font-weight:600;color:#5D2E2E;line-height:1.1">{nw} &<br>{np}</div>
        <div style="background:white;border-radius:12px;padding:10px;margin:15px 0;border:1px dashed #d4af8a">
          <p style="font-size:10px;color:#8B5E3C">Kepada Yth.</p><p style="font-weight:700;font-size:14px">Tamu Undangan</p><p style="font-size:9px;color:#8B5E3C">di Tempat</p>
        </div>
        <button style="background:#5D2E2E;color:white;border:none;padding:13px 32px;border-radius:30px;font-weight:600;cursor:pointer" onclick="buka()">Buka Undangan</button>
      </div>
    </div>
  </div>
</div>

<div id="main" style="display:none;padding-top:44px">
  <div class="parallax"></div>
  
  <div class="sec cream">
    <p style="font-family:'Great Vibes';font-size:38px;color:#d4af8a">The Wedding Of</p>
    <h1 style="font-family:'Cormorant Garamond';font-size:40px;line-height:1">{nw}<br><span style="font-family:'Great Vibes';font-size:32px;color:#d4af8a">&</span><br>{np}</h1>
    <p style="margin-top:12px;font-size:13px;letter-spacing:2px">{tgl.strftime('%A, %d %B %Y')}</p>
  </div>

  <div class="sec cream">
    <div style="font-size:90px">🤵👰</div>
    <p style="font-size:13px;line-height:1.8;color:#8B5E3C;margin-top:20px">"Dan di antara tanda-tanda kekuasaan-Nya ialah Dia menciptakan untukmu isteri-isteri dari jenismu sendiri, supaya kamu cenderung dan merasa tenteram kepadanya"<br><br><b>QS. Ar-Rum: 21</b></p>
  </div>

  <div class="sec maroon">
    <p style="font-family:'Great Vibes';font-size:36px">Bride & Groom</p>
    <div style="margin:35px 0">
      <div class="oval"><img src="{f"data:image/jpeg;base64,{wanita_b64}" if wanita_b64 else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"}"></div>
      <h3 style="font-family:'Cormorant Garamond';font-size:28px">{nlw}</h3>
      <div class="parent-box"><p style="font-size:11px;opacity:0.8">Putri Tercinta dari</p><p style="font-weight:600;font-size:13px">{ayah_w}<br>& {ibu_w}</p></div>
    </div>
    <p style="font-family:'Great Vibes';font-size:60px;color:#d4af8a">&</p>
    <div style="margin:35px 0">
      <div class="oval"><img src="{f"data:image/jpeg;base64,{pria_b64}" if pria_b64 else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"}"></div>
      <h3 style="font-family:'Cormorant Garamond';font-size:28px">{nlp}</h3>
      <div class="parent-box"><p style="font-size:11px;opacity:0.8">Putra Tercinta dari</p><p style="font-weight:600;font-size:13px">{ayah_p}<br>& {ibu_p}</p></div>
    </div>
  </div>

  <div class="sec maroon" style="border-top:1px solid #d4af8a">
    <p style="font-family:'Great Vibes';font-size:32px">Menuju Hari Bahagia</p>
    <div class="count-box" id="count">
      <div class="count-item"><h2 id="d">46</h2><p style="font-size:10px">HARI</p></div>
      <div class="count-item"><h2 id="h">20</h2><p style="font-size:10px">JAM</p></div>
      <div class="count-item"><h2 id="m">09</h2><p style="font-size:10px">MENIT</p></div>
      <div class="count-item"><h2 id="s">17</h2><p style="font-size:10px">DETIK</p></div>
    </div>
    <p style="font-size:12px;margin-top:15px">{tgl.strftime('%A, %d %B %Y')} • {jam.strftime('%H:%M')} WIB<br>{lokasi}</p>
    <a href="{link_maps}" target="_blank" class="map-btn">📍 Lihat Lokasi (Shareloc)</a>
    {f'<div style="margin-top:15px;border-radius:15px;overflow:hidden;border:3px solid #d4af8a"><iframe src="{embed_maps}" width="100%" height="200" style="border:0" loading="lazy"></iframe></div>' if embed_maps else ''}
  </div>

  <div class="sec cream">
    <p style="font-family:'Great Vibes';font-size:36px;color:#d4af8a">Our Gallery</p>
    <p style="font-size:11px;color:#8B5E3C;margin-bottom:10px">Auto Slide • Geser untuk lihat</p>
    <div class="g-slider" id="gSlider">{gallery_html if gallery_list else '<div class="g-item"><img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400"></div><div class="g-item"><img src="https://images.unsplash.com/photo-1511285560929-80b456fea0bc?w=400"></div>'}</div>
  </div>

  <div class="sec maroon"><p style="font-size:10px;opacity:0.6">Made with ❤️ by RAYSHA WEDDING • {musik_label} • Auto Slide Aktif</p></div>
</div>

<div class="float-music" id="floatBtn" onclick="toggleM()">🎵</div>
<audio id="aud" loop src="{musik_src}"></audio>

<script>
var cur=0; var play=false;
function show(n){{ var imgs=document.querySelectorAll('#slide img'); imgs.forEach(i=>i.classList.remove('active')); if(imgs[n]) imgs[n].classList.add('active'); }}
function next(){{ cur=(cur+1)%{len(cover_list)}; show(cur); }}
var slideInt=setInterval(next, 3500);

function buka(){{
  document.getElementById('cover').classList.add('hide');
  setTimeout(()=>{{document.getElementById('main').style.display='block'; window.scrollTo(0,0)}}, 900);
  var a=document.getElementById('aud'); a.play().then(()=>{{play=true; document.getElementById('topBtn').innerHTML='⏸️ Pause'; document.getElementById('floatBtn').innerHTML='⏸️'; document.getElementById('floatBtn').classList.remove('paused');}}).catch(()=>{{}});
  clearInterval(slideInt); slideInt=setInterval(next, 3500);
  // Auto slide gallery juga
  var g=document.getElementById('gSlider'); var gx=0; setInterval(()=>{{ gx+=280; if(gx>=g.scrollWidth) gx=0; g.scrollTo({{left:gx, behavior:'smooth'}}); }}, 4000);
}}
function toggleM(){{
  var a=document.getElementById('aud'); var t=document.getElementById('topBtn'); var f=document.getElementById('floatBtn');
  if(play){{a.pause(); t.innerHTML='▶️ Play'; f.innerHTML='🎵'; f.classList.add('paused'); play=false;}} else {{a.play(); t.innerHTML='⏸️ Pause'; f.innerHTML='⏸️'; f.classList.remove('paused'); play=true;}}
}}
// Countdown
var target=new Date("{tgl} {jam}").getTime();
setInterval(function(){{ var now=new Date().getTime(); var diff=target-now; if(diff>0){{ document.getElementById('d').innerHTML=Math.floor(diff/(1000*60*60*24)); document.getElementById('h').innerHTML=Math.floor((diff%(1000*60*60*24))/(1000*60*60)); document.getElementById('m').innerHTML=Math.floor((diff%(1000*60*60))/(1000*60)); document.getElementById('s').innerHTML=Math.floor((diff%(1000*60))/1000); }}}},1000);
show(0);
</script>
</body></html>
"""

components.html(html_code, height=1000, scrolling=True)
st.caption("✅ Musik di ATAS, Orang Tua sesuai keinginan, Shareloc aktif, Auto Slide pas client kirim ke tamu")
