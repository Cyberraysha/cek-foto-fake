import streamlit as st, base64, io
import streamlit.components.v1 as components
from PIL import Image
from datetime import datetime, date

st.set_page_config(page_title="Wedding Putri & Andika", layout="wide")
st.markdown("<style>.block-container{padding:0 !important;}</style>", unsafe_allow_html=True)

if 'lagu_b64' not in st.session_state:
    st.session_state.lagu_b64 = None

with st.sidebar:
    st.markdown("## 🎵 UPLOAD MUSIK DI SINI")
    st.warning("SCROLL PALING ATAS - INI TEMPAT UPLOAD MUSIK")
    lagu = st.file_uploader("Pilih MP3", type=["mp3","m4a","wav","ogg"], key="musik_top")
    if lagu:
        st.session_state.lagu_b64 = base64.b64encode(lagu.getvalue()).decode()
        st.success(f"LAGU {lagu.name} AKTIF!")
        st.audio(lagu)
    
    st.divider()
    st.header("Data Pengantin")
    nw = st.text_input("Nama Wanita", "PUTRI")
    np = st.text_input("Nama Pria", "ANDIKA")
    nlw = st.text_input("Nama Lengkap Wanita", "Putri Cantika Sari")
    nlp = st.text_input("Nama Lengkap Pria", "Putra Andika Pratama")
    tgl = st.date_input("Tanggal", date(2025,12,28))
    jam = st.time_input("Jam", datetime.strptime("08:00","%H:%M").time())
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna")
    wa = st.text_input("WA Mimin", "6281234567890")
    
    st.divider()
    fc = st.file_uploader("Foto Cover Berdua", type=["jpg","png","webp"])
    fw = st.file_uploader("Foto Wanita Oval", type=["jpg","png","webp"])
    fp = st.file_uploader("Foto Pria Oval", type=["jpg","png","webp"])
    fg = st.file_uploader("Gallery 5 Foto", type=["jpg","png","webp"], accept_multiple_files=True)

def to_b64(f):
    if not f: return ""
    img = Image.open(f)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

cover_b64 = to_b64(fc)
wanita_b64 = to_b64(fw)
pria_b64 = to_b64(fp)
gallery_b64 = [to_b64(f) for f in (fg[:5] if fg else [])]

cover_src = f"data:image/jpeg;base64,{cover_b64}" if cover_b64 else "https://images.unsplash.com/photo-1519741497674-611481863552?w=800"
musik_src = f"data:audio/mp3;base64,{st.session_state.lagu_b64}" if st.session_state.lagu_b64 else "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
musik_label = "✅ LAGU CUSTOM AKTIF" if st.session_state.lagu_b64 else "⚠️ PAKAI LAGU DEFAULT - UPLOAD DI ATAS"

html = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&family=Great+Vibes&family=Poppins&display=swap" rel="stylesheet">
<style>*{{margin:0;padding:0;box-sizing:border-box}} body{{font-family:Poppins}} .cover{{height:100vh;width:100%;background:linear-gradient(rgba(0,0,0,0.3),rgba(0,0,0,0.3)),url('{cover_src}');background-size:cover;background-position:center;display:flex;align-items:center;justify-content:center;position:fixed;top:0;left:0;z-index:9999;transition:1.2s}} .cover.hide{{transform:translateY(-100%)}} .card{{background:rgba(255,250,245,0.92);border:3px solid #d4af8a;border-radius:25px;padding:30px 20px;text-align:center;max-width:350px;width:90%}} .btn{{background:#5D2E2E;color:white;border:none;padding:14px 35px;border-radius:30px;font-weight:600;cursor:pointer}} #main{{display:none}} .sec{{padding:60px 20px;text-align:center;max-width:500px;margin:0 auto}} .maroon{{background:#5D2E2E;color:#f5e6d3}} .cream{{background:#fdf6f0;color:#5D2E2E}} .oval{{width:200px;height:280px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:6px solid #d4af8a}} .oval img{{width:100%;height:100%;object-fit:cover}} .float{{position:fixed;bottom:20px;right:20px;background:#5D2E2E;color:white;width:50px;height:50px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:100;cursor:pointer}}</style></head><body>
<div class="cover" id="cover"><div class="card">
<h4 style="letter-spacing:4px;font-size:12px;color:#8B5E3C">THE WEDDING OF</h4>
<div style="font-family:'Cormorant Garamond';font-size:32px;font-weight:600;color:#5D2E2E;margin:10px 0">{nw} & {np}</div>
<p style="font-size:11px;color:#8B5E3C">{tgl.strftime('%A, %d %B %Y')}</p>
<div style="background:white;border-radius:15px;padding:12px;margin:15px 0;border:1px dashed #d4af8a"><p style="font-size:11px">Kepada Yth.</p><p style="font-weight:600">Tamu Undangan</p><p style="font-size:9px;color:#d4af8a">{musik_label}</p></div>
<button class="btn" onclick="buka()">💌 Buka Undangan</button>
</div></div>
<div id="main">
<div style="height:70vh;background:url('https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200');background-size:cover;background-position:center;display:flex;align-items:center;justify-content:center"><div style="background:rgba(255,255,255,0.9);padding:20px;border-radius:20px;text-align:center"><p style="font-family:'Great Vibes';font-size:28px;color:#5D2E2E">Welcome</p><p>The Wedding</p></div></div>
<div class="sec cream"><p style="font-family:'Great Vibes';font-size:38px;color:#d4af8a">The Wedding Of</p><h1 style="font-family:'Cormorant Garamond';font-size:34px">{nw}<br>&<br>{np}</h1><p>{tgl}</p></div>
<div class="sec maroon"><div class="oval" style="width:280px;height:350px"><img src="{cover_src}"></div><p style="font-family:'Great Vibes';font-size:32px">{nw} & {np}</p></div>
<div class="sec cream"><p style="font-family:'Great Vibes';font-size:38px;color:#d4af8a">Bride & Groom</p><div class="oval"><img src="{f"data:image/jpeg;base64,{wanita_b64}" if wanita_b64 else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"}"></div><h3>{nw}</h3><p>{nlw}</p><p style="font-family:'Great Vibes';font-size:50px;color:#d4af8a">&</p><div class="oval"><img src="{f"data:image/jpeg;base64,{pria_b64}" if pria_b64 else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"}"></div><h3>{np}</h3><p>{nlp}</p></div>
<div class="sec maroon"><p>Acara: {tgl} {jam} WIB<br>{lokasi}</p><a href="https://wa.me/{wa}" target="_blank" style="display:block;background:#25D366;color:white;padding:14px;border-radius:30px;text-decoration:none;font-weight:700;margin-top:20px">💬 Chat Mimin</a></div>
</div>
<div class="float" id="mBtn" onclick="toggleM()">🎵</div>
<audio id="aud" loop src="{musik_src}"></audio>
<script>
var play=false;
function buka(){{
document.getElementById('cover').classList.add('hide');
setTimeout(()=>{{document.getElementById('main').style.display='block'}},800);
var a=document.getElementById('aud'); a.play().then(()=>{{play=true;document.getElementById('mBtn').innerHTML='⏸️'}}).catch(()=>{{}});
}}
function toggleM(){{
var a=document.getElementById('aud'); var b=document.getElementById('mBtn');
if(play){{a.pause();b.innerHTML='🎵';play=false}} else {{a.play();b.innerHTML='⏸️';play=true}}
}}
</script>
</body></html>
"""
components.html(html, height=900, scrolling=True)
