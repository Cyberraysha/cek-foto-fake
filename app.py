import streamlit as st
import base64
import io
from PIL import Image
from datetime import datetime, date
import streamlit.components.v1 as components

st.set_page_config(page_title="PUTRI ANDIKA Final", layout="wide")
st.markdown("<style>.block-container{padding:0 !important;} header{visibility:hidden;}</style>", unsafe_allow_html=True)

if 'lagu_b64' not in st.session_state:
    st.session_state.lagu_b64 = None

with st.sidebar:
    st.markdown("## MUSIK DI ATAS (WAJIB)")
    lagu = st.file_uploader("Upload MP3 sesuai keinginan", type=["mp3","m4a","wav","ogg"])
    if lagu:
        st.session_state.lagu_b64 = base64.b64encode(lagu.getvalue()).decode()
        st.success("Lagu Aktif!")
        st.audio(lagu)
    st.divider()
    nw = st.text_input("Panggilan Wanita", "PUTRI")
    np = st.text_input("Panggilan Pria", "ANDIKA")
    nlw = st.text_input("Nama Lengkap Wanita", "Putri Cantika Sari")
    nlp = st.text_input("Nama Lengkap Pria", "Putra Andika Pratama")
    ayah_w = st.text_input("Ayah Wanita", "Bapak H. Wahyu Widodo")
    ibu_w = st.text_input("Ibu Wanita", "Ibu Hj. Sri Mulyani")
    ayah_p = st.text_input("Ayah Pria", "Bapak H. Marno")
    ibu_p = st.text_input("Ibu Pria", "Ibu Hj. Siti Halimah")
    tgl = st.date_input("Tanggal", date(2025,12,28))
    jam = st.time_input("Jam", datetime.strptime("08:00","%H:%M").time())
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna, Bekasi")
    link_maps = st.text_input("Link Shareloc Maps", "https://maps.app.goo.gl/")
    fc = st.file_uploader("5 Foto Cover Auto Slide", type=["jpg","png","webp"], accept_multiple_files=True)
    fw = st.file_uploader("Foto Wanita Oval", type=["jpg","png","webp"])
    fp = st.file_uploader("Foto Pria Oval", type=["jpg","png","webp"])
    fg = st.file_uploader("5 Foto Gallery Bawah", type=["jpg","png","webp"], accept_multiple_files=True)
    wa = st.text_input("WA Mimin", "6281234567890")

def to_b64(f):
    if not f:
        return ""
    try:
        img = Image.open(f)
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode()
    except:
        return ""

covers = [to_b64(f) for f in (fc[:5] if fc else [])]
if not covers:
    covers = ["https://images.unsplash.com/photo-1519741497674-611481863552?w=800"]
wanita_b64 = to_b64(fw)
pria_b64 = to_b64(fp)
gals = [to_b64(f) for f in (fg[:5] if fg else [])]

musik_src = "data:audio/mp3;base64," + st.session_state.lagu_b64 if st.session_state.lagu_b64 else "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
musik_label = "LAGU CUSTOM" if st.session_state.lagu_b64 else "LAGU DEFAULT"

slide_imgs = ""
for i,b in enumerate(covers):
    src = b if b.startswith("http") else "data:image/jpeg;base64," + b
    cls = "active" if i==0 else ""
    slide_imgs += f'<img src="{src}" class="{cls}">'

gallery_html = ""
for b in gals:
    gallery_html += f'<div class="g-item"><img src="data:image/jpeg;base64,{b}"></div>'
if not gals:
    gallery_html = '<div class="g-item"><img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400"></div>'

cover_first = covers[0] if covers[0].startswith("http") else "data:image/jpeg;base64," + covers[0]
wanita_src = "data:image/jpeg;base64," + wanita_b64 if wanita_b64 else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"
pria_src = "data:image/jpeg;base64," + pria_b64 if pria_b64 else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"

html_template = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{margin:0;padding:0;box-sizing:border-box} body{font-family:sans-serif;background:#fdf2f2}
.music-top{position:fixed;top:0;left:0;right:0;background:#5D2E2E;color:#f5e6d3;padding:10px 15px;display:flex;justify-content:space-between;z-index:10000}
.cover{height:100vh;width:100%;position:fixed;top:0;left:0;z-index:9999;transition:1.2s;overflow:hidden}
.cover .slideshow{width:100%;height:100%;position:relative}
.cover .slideshow img{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:1.2s}
.cover .slideshow img.active{opacity:1}
.cover-overlay{position:absolute;inset:0;background:linear-gradient(rgba(0,0,0,0.1),rgba(0,0,0,0.5));display:flex;align-items:center;justify-content:center}
.card{background:rgba(255,248,240,0.96);border-radius:28px;padding:8px;max-width:380px;width:92%}
.card-inner{border:2px solid #d4af8a;border-radius:20px;padding:25px 20px;text-align:center}
.cover.hide{transform:translateY(-100%)}
.parallax{height:85vh;background:linear-gradient(to bottom,#fdf2f2,transparent,#fdf2f2),url(https://images.unsplash.com/photo-1519225421980-715cb0215aed?w=1200);background-size:cover;background-position:center;background-attachment:fixed}
.sec{padding:70px 20px;text-align:center;max-width:520px;margin:0 auto}
.maroon{background:#5D2E2E;color:#f5e6d3} .cream{background:#fdf2f2;color:#5D2E2E}
.oval{width:210px;height:300px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:7px solid #d4af8a}
.oval img{width:100%;height:100%;object-fit:cover}
.parent-box{background:rgba(255,255,255,0.08);border:1px solid #d4af8a;border-radius:15px;padding:12px;margin-top:10px}
.count-box{display:flex;gap:10px;justify-content:center;margin:20px 0} .count-item{background:rgba(255,255,255,0.1);border:1px solid #d4af8a;border-radius:15px;padding:14px 10px;min-width:72px}
.g-slider{display:flex;gap:10px;overflow-x:auto;padding:10px 0} .g-item{min-width:75%} .g-item img{width:100%;height:260px;object-fit:cover;border-radius:18px;border:4px solid #d4af8a}
.map-btn{background:#f5e6d3;color:#5D2E2E;padding:12px 24px;border-radius:30px;text-decoration:none;font-weight:700;display:inline-block;margin-top:15px}
.float-music{position:fixed;bottom:25px;right:20px;background:#5D2E2E;color:#f5e6d3;width:54px;height:54px;border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:100;cursor:pointer;border:2px solid #d4af8a}
</style></head><body>
<div class="music-top"><div>LAGU_LABEL - NAMA_PASANGAN - Auto Slide</div><button id="topBtn" onclick="toggleM()">Pause</button></div>
<div class="cover" id="cover"><div class="slideshow" id="slide">SLIDE_IMGS</div><div class="cover-overlay"><div class="card"><div class="card-inner"><p>THE WEDDING OF</p><div style="width:80px;height:80px;margin:15px auto;border-radius:50%;overflow:hidden;border:3px solid #d4af8a"><img src="COVER_FIRST" style="width:100%;height:100%;object-fit:cover"></div><div style="font-size:30px;font-weight:600;color:#5D2E2E">NAMA_PASANGAN</div><div style="background:white;border-radius:12px;padding:10px;margin:15px 0;border:1px dashed #d4af8a"><p>Kepada Yth.</p><p style="font-weight:700">Tamu Undangan</p></div><button style="background:#5D2E2E;color:white;border:none;padding:13px 32px;border-radius:30px;font-weight:600;cursor:pointer" onclick="buka()">Buka Undangan</button></div></div></div></div>
<div id="main" style="display:none;padding-top:44px">
<div class="parallax"></div>
<div class="sec cream"><h1>NAMA_PASANGAN2</h1><p>TGL_TXT</p></div>
<div class="sec maroon"><p>Bride & Groom</p>
<div style="margin:35px 0"><div class="oval"><img src="WANITA_SRC"></div><h3>NAMA_LENGKAP_W</h3><div class="parent-box"><p>Putri dari</p><p><b>AYAH_W<br>& IBU_W</b></p></div></div>
<p style="font-size:60px">&</p>
<div style="margin:35px 0"><div class="oval"><img src="PRIA_SRC"></div><h3>NAMA_LENGKAP_P</h3><div class="parent-box"><p>Putra dari</p><p><b>AYAH_P<br>& IBU_P</b></p></div></div></div>
<div class="sec maroon"><p>Menuju Hari Bahagia</p><div class="count-box"><div class="count-item"><h2 id="d">46</h2><p>HARI</p></div><div class="count-item"><h2 id="h">20</h2><p>JAM</p></div><div class="count-item"><h2 id="m">09</h2><p>MENIT</p></div><div class="count-item"><h2 id="s">17</h2><p>DETIK</p></div></div><p>TGL2<br>LOKASI_TXT</p><a href="MAPS_LINK" target="_blank" class="map-btn">Lihat Lokasi (Shareloc)</a></div>
<div class="sec cream"><p>Our Gallery - Auto Slide</p><div class="g-slider" id="gSlider">GALLERY_HTML</div></div>
</div>
<div class="float-music" id="floatBtn" onclick="toggleM()">MUSIK</div>
<audio id="aud" loop src="MUSIK_SRC"></audio>
<script>
var cur=0, play=false, total=TOTAL_NUM;
function show(n){var imgs=document.querySelectorAll('#slide img');imgs.forEach(i=>i.classList.remove('active'));if(imgs[n])imgs[n].classList.add('active')}
function next(){cur=(cur+1)%total;show(cur)}
var slideInt=setInterval(next,3500);
function buka(){document.getElementById('cover').classList.add('hide');setTimeout(()=>{document.getElementById('main').style.display='block'},900);var a=document.getElementById('aud');a.play().then(()=>{play=true;document.getElementById('topBtn').innerHTML='Pause';document.getElementById('floatBtn').innerHTML='Pause'}).catch(()=>{}); var g=document.getElementById('gSlider'); var gx=0; setInterval(()=>{gx+=280; if(gx>=g.scrollWidth) gx=0; g.scrollTo({left:gx, behavior:'smooth'})},4000)}
function toggleM(){var a=document.getElementById('aud');var t=document.getElementById('topBtn');var f=document.getElementById('floatBtn');if(play){a.pause();t.innerHTML='Play';f.innerHTML='Music';play=false}else{a.play();t.innerHTML='Pause';f.innerHTML='Pause';play=true}}
var target=new Date("TGL_JS").getTime(); setInterval(function(){var now=new Date().getTime();var diff=target-now;if(diff>0){document.getElementById('d').innerHTML=Math.floor(diff/(1000*60*60*24));document.getElementById('h').innerHTML=Math.floor((diff%(1000*60*60*24))/(1000*60*60));document.getElementById('m').innerHTML=Math.floor((diff%(1000*60*60))/(1000*60));document.getElementById('s').innerHTML=Math.floor((diff%(1000*60))/1000)}},1000);
show(0);
</script>
</body></html>
"""

html = html_template.replace("LAGU_LABEL", musik_label)
html = html.replace("NAMA_PASANGAN", f"{nw} & {np}")
html = html.replace("NAMA_PASANGAN2", f"{nw} & {np}")
html = html.replace("SLIDE_IMGS", slide_imgs)
html = html.replace("COVER_FIRST", cover_first)
html = html.replace("WANITA_SRC", wanita_src)
html = html.replace("PRIA_SRC", pria_src)
html = html.replace("NAMA_LENGKAP_W", nlw)
html = html.replace("NAMA_LENGKAP_P", nlp)
html = html.replace("AYAH_W", ayah_w)
html = html.replace("IBU_W", ibu_w)
html = html.replace("AYAH_P", ayah_p)
html = html.replace("IBU_P", ibu_p)
html = html.replace("TGL_TXT", tgl.strftime("%A, %d %B %Y"))
html = html.replace("TGL2", f"{tgl.strftime('%A, %d %B %Y')} - {jam.strftime('%H:%M')} WIB")
html = html.replace("TGL_JS", f"{tgl} {jam}")
html = html.replace("LOKASI_TXT", lokasi)
html = html.replace("MAPS_LINK", link_maps)
html = html.replace("GALLERY_HTML", gallery_html)
html = html.replace("MUSIK_SRC", musik_src)
html = html.replace("TOTAL_NUM", str(len(covers)))

components.html(html, height=1000, scrolling=True)
