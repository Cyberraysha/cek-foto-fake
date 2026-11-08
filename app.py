import streamlit as st, base64, io, os, urllib.parse
from PIL import Image
from datetime import date
import streamlit.components.v1 as components

st.set_page_config(page_title="RAYSHA 3D FINAL", layout="wide")
st.markdown("<style>.block-container{padding:0 !important} header{visibility:hidden}</style>", unsafe_allow_html=True)

# --- CEK MODE ADMIN ---
query = st.query_params
is_admin = query.get("admin") == "rahasia123"
tamu_nama = query.get("to", "Tamu Undangan")

# Folder simpan permanen (di Streamlit Cloud)
os.makedirs("assets", exist_ok=True)

def save_file(upload, name):
    if upload:
        path = os.path.join("assets", name)
        with open(path, "wb") as f:
            f.write(upload.getvalue())
        return path
    return None

def load_b64(path):
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

# --- SIDEBAR ADMIN ---
if is_admin:
    st.sidebar.markdown("## 🔐 MODE ADMIN RAYSHA")
    st.sidebar.success("Lu lagi di mode admin, semua yang lu upload bakal kesimpen buat tamu!")
    
    st.sidebar.markdown("### 1. 🎵 Musik (Auto ke Tamu)")
    lagu = st.sidebar.file_uploader("Upload MP3", type=["mp3","m4a","wav"])
    if lagu:
        save_file(lagu, "musik.mp3")
        st.sidebar.audio(lagu)
        st.sidebar.success("Musik kesimpen!")
    
    st.sidebar.markdown("### 2. 📸 Foto 3D")
    fc = st.sidebar.file_uploader("5 Foto Cover (Auto Slide)", type=["jpg","png","webp"], accept_multiple_files=True)
    if fc:
        for i,f in enumerate(fc[:5]):
            save_file(f, f"cover_{i}.jpg")
    
    fw = st.sidebar.file_uploader("Foto Wanita", type=["jpg","png","webp"])
    if fw: save_file(fw, "wanita.jpg")
    
    fp = st.sidebar.file_uploader("Foto Pria", type=["jpg","png","webp"])
    if fp: save_file(fp, "pria.jpg")
    
    fg = st.sidebar.file_uploader("Gallery 5 Foto", type=["jpg","png","webp"], accept_multiple_files=True)
    if fg:
        for i,f in enumerate(fg[:5]):
            save_file(f, f"gal_{i}.jpg")
    
    st.sidebar.markdown("### 3. 👨‍👩‍👧 Orang Tua & Data")
    nw = st.sidebar.text_input("Wanita", "PUTRI", key="anw")
    np = st.sidebar.text_input("Pria", "ANDIKA", key="anp")
    ayah_w = st.sidebar.text_input("Ayah Wanita", "Bpk Wahyu", key="aaw")
    ibu_w = st.sidebar.text_input("Ibu Wanita", "Ibu Sri", key="aiw")
    ayah_p = st.sidebar.text_input("Ayah Pria", "Bpk Marno", key="aap")
    ibu_p = st.sidebar.text_input("Ibu Pria", "Ibu Ani", key="aip")
    lokasi = st.sidebar.text_input("Lokasi", "Gedung Serbaguna", key="alok")
    maps = st.sidebar.text_input("Link Maps", "https://maps.app.goo.gl/", key="amaps")
    tgl = st.sidebar.date_input("Tanggal", date(2025,12,28), key="atgl")
    
    # Simpan data teks ke file
    with open("assets/data.txt","w") as f:
        f.write(f"{nw}|{np}|{ayah_w}|{ibu_w}|{ayah_p}|{ibu_p}|{lokasi}|{maps}|{tgl}")
    
    st.sidebar.markdown("### 4. 👥 Daftar Tamu + WA ke Client")
    daftar = st.sidebar.text_area("Tulis nama tamu per baris (Budi, Ani, Siti)", "Budi Santoso\nAni Wijaya\nKeluarga Bpk RT")
    wa_client = st.sidebar.text_input("WA Client (pengantin)", "6281234567890")
    
    if st.sidebar.button("Generate Link Tamu"):
        base_url = "https://cekfotofake.streamlit.app"
        for nama in daftar.split("\n"):
            if nama.strip():
                link = f"{base_url}/?to={urllib.parse.quote(nama.strip())}"
                wa_link = f"https://wa.me/{wa_client}?text=Halo%20{nama.strip()}%20ini%20undangan%20{base_url}/?to={urllib.parse.quote(nama.strip())}"
                st.sidebar.code(link)
                st.sidebar.link_button(f"WA ke {nama.strip()}", wa_link)
    
    st.sidebar.divider()
    if st.sidebar.button("Lihat sebagai Tamu"):
        st.query_params.clear()
        st.rerun()
else:
    # MODE TAMU - Load dari assets
    nw,np,ayah_w,ibu_w,ayah_p,ibu_p,lokasi,maps,tgl_str = "PUTRI","ANDIKA","Bpk Wahyu","Ibu Sri","Bpk Marno","Ibu Ani","Gedung Serbaguna","https://maps.app.goo.gl/","2025-12-28"
    if os.path.exists("assets/data.txt"):
        try:
            with open("assets/data.txt") as f:
                parts = f.read().split("|")
                if len(parts)>=9:
                    nw,np,ayah_w,ibu_w,ayah_p,ibu_p,lokasi,maps,tgl_str = parts[:9]
        except: pass

# LOAD FOTO UNTUK TAMPILAN
def get_img(name, default_url):
    path = os.path.join("assets", name)
    if os.path.exists(path):
        b64 = load_b64(path)
        return f"data:image/jpeg;base64,{b64}"
    return default_url

covers = []
for i in range(5):
    img = get_img(f"cover_{i}.jpg", "https://images.unsplash.com/photo-1519741497674-611481863552?w=800" if i==0 else "")
    if img: covers.append(img)
if not covers: covers = ["https://images.unsplash.com/photo-1519741497674-611481863552?w=800"]

wanita_src = get_img("wanita.jpg", "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400")
pria_src = get_img("pria.jpg", "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400")

gals = []
for i in range(5):
    img = get_img(f"gal_{i}.jpg", "")
    if img.startswith("data:"): gals.append(img)

musik_path = "assets/musik.mp3"
musik_src = ""
if os.path.exists(musik_path):
    musik_src = f"data:audio/mp3;base64,{load_b64(musik_path)}"
else:
    musik_src = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"

slide_html = ""
for i,s in enumerate(covers):
    cls = "active" if i==0 else ""
    slide_html += f'<img src="{s}" class="{cls}">'

gal_html = ""
for g in gals:
    gal_html += f'<div class="g3d"><img src="{g}"></div>'
if not gal_html:
    gal_html = '<div class="g3d"><img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400"></div>'*3

# --- HTML FINAL 3D ---
html = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:#0a0a0a;color:#f5e6d3;font-family:sans-serif;overflow-x:hidden}}
.top{{position:fixed;top:0;left:0;right:0;background:rgba(10,10,10,0.9);backdrop-filter:blur(20px);border-bottom:1px solid #d4af8a;padding:12px 18px;display:flex;justify-content:space-between;z-index:9999}}
.cover{{height:100vh;width:100%;position:fixed;top:0;left:0;z-index:9998;transition:1.2s}} .cover .slides img{{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:1.5s}} .cover .slides img.active{{opacity:1}}
.overlay{{position:absolute;inset:0;background:radial-gradient(rgba(0,0,0,0.1), rgba(0,0,0,0.8));display:flex;align-items:center;justify-content:center}}
.card{{width:360px;background:rgba(255,248,240,0.08);backdrop-filter:blur(30px);border:1px solid #d4af8a;border-radius:28px;padding:14px;transform:rotateY(-10deg);box-shadow:0 40px 100px rgba(0,0,0,0.8)}}
.inner{{border:1.5px solid #d4af8a;border-radius:22px;padding:28px 20px;text-align:center;background:rgba(255,248,240,0.96);color:#5D2E2E}}
.cover.hide{{transform:translateY(-100%)}} #main{{display:none;padding-top:60px}}
.sec{{padding:80px 20px;text-align:center;max-width:700px;margin:0 auto}}
.oval3d{{width:220px;height:310px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:6px solid #d4af8a;box-shadow:0 30px 80px rgba(0,0,0,0.7)}}
.oval3d img{{width:100%;height:100%;object-fit:cover}}
.parent3d{{background:rgba(212,175,138,0.15);border:1px solid #d4af8a;border-radius:12px;padding:12px;margin-top:10px;font-size:12px}}
.gallery3d{{display:flex;gap:16px;overflow-x:auto;padding:20px 0}} .g3d{{min-width:280px;background:rgba(255,255,255,0.06);border:1px solid #d4af8a;border-radius:20px;padding:10px}} .g3d img{{width:100%;height:350px;object-fit:cover;border-radius:16px}}
.btn3d{{background:#d4af8a;color:#1a0f0f;border:none;padding:15px 36px;border-radius:30px;font-weight:800;cursor:pointer}}
</style></head><body>
<div class="top"><div>✨ {nw} & {np} • 3D</div><button id="tbtn" onclick="toggle()" style="background:#d4af8a;border:none;padding:7px 14px;border-radius:20px;font-weight:700">Play</button></div>
<div class="cover" id="cover"><div class="slides" id="slides">{slide_html}</div><div class="overlay"><div class="card"><div class="inner">
<p style="letter-spacing:6px;font-size:11px;color:#8B5E3C">THE WEDDING OF</p>
<div style="width:88px;height:88px;margin:16px auto;border-radius:50%;overflow:hidden;border:3px solid #d4af8a"><img src="{covers[0]}" style="width:100%;height:100%;object-fit:cover"></div>
<div style="font-size:30px;font-weight:900;color:#5D2E2E">{nw} & {np}</div>
<div style="background:white;border-radius:14px;padding:12px;margin:14px 0;border:1px dashed #d4af8a"><p style="font-size:10px">Kepada Yth.</p><p style="font-weight:800;font-size:16px">{tamu_nama}</p><p style="font-size:9px;color:#8B5E3C">di Tempat</p></div>
<button class="btn3d" onclick="buka()">BUKA UNDANGAN 3D</button>
</div></div></div></div>
<div id="main">
<div class="sec"><h1 style="font-size:48px;color:#d4af8a">{nw} & {np}</h1><p>{tgl_str} • {lokasi}</p></div>
<div class="sec" style="display:flex;gap:40px;justify-content:center;flex-wrap:wrap">
<div><div class="oval3d"><img src="{wanita_src}"></div><h3>{nw}</h3><div class="parent3d">Putri dari<br><b>{ayah_w}<br>& {ibu_w}</b></div></div>
<div><div class="oval3d"><img src="{pria_src}"></div><h3>{np}</h3><div class="parent3d">Putra dari<br><b>{ayah_p}<br>& {ibu_p}</b></div></div>
</div>
<div class="sec"><a href="{maps}" target="_blank" class="btn3d" style="text-decoration:none;display:inline-block">📍 Shareloc Maps</a><br><br><div class="gallery3d">{gal_html}</div></div>
</div>
<audio id="aud" loop src="{musik_src}"></audio>
<script>
let cur=0,total={len(covers)},play=false;
function show(n){{document.querySelectorAll('#slides img').forEach(i=>i.classList.remove('active')); let el=document.querySelectorAll('#slides img')[n]; if(el) el.classList.add('active')}}
setInterval(()=>{{cur=(cur+1)%total; show(cur)}},3500);
function buka(){{document.getElementById('cover').classList.add('hide'); setTimeout(()=>{{document.getElementById('main').style.display='block'}},900); let a=document.getElementById('aud'); a.play().then(()=>{{play=true; document.getElementById('tbtn').innerText='Pause'}}).catch(()=>{{}});}}
function toggle(){{let a=document.getElementById('aud'); let t=document.getElementById('tbtn'); if(play){{a.pause(); t.innerText='Play'; play=false}}else{{a.play(); t.innerText='Pause'; play=true}}}}
show(0);
</script>
</body></html>
"""

components.html(html, height=1000, scrolling=True)

if not is_admin:
    st.caption(f"Mode Tamu: {tamu_nama} - Link ini personal buat tamu")
else:
    st.sidebar.info("Admin: Abis upload, copy link tamu di atas buat kirim WA ke client!")
