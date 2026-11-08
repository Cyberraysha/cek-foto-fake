import streamlit as st
import base64, io
from PIL import Image
from datetime import date
import streamlit.components.v1 as components

st.set_page_config(page_title="RAYSHA 3D BRUTAL", layout="wide")
st.markdown("<style>.block-container{padding:0 !important} header{visibility:hidden}</style>", unsafe_allow_html=True)

if 'lagu' not in st.session_state:
    st.session_state.lagu = None

with st.sidebar:
    st.markdown("## 🎵 MUSIK DI ATAS")
    f = st.file_uploader("MP3 Custom", type=["mp3","m4a","wav"])
    if f:
        st.session_state.lagu = base64.b64encode(f.getvalue()).decode()
        st.audio(f)
    st.divider()
    nw = st.text_input("Wanita", "PUTRI")
    np = st.text_input("Pria", "ANDIKA")
    ayah_w = st.text_input("Ayah Wanita", "Bpk H. Wahyu")
    ibu_w = st.text_input("Ibu Wanita", "Ibu Hj. Sri")
    ayah_p = st.text_input("Ayah Pria", "Bpk H. Marno")
    ibu_p = st.text_input("Ibu Pria", "Ibu Hj. Ani")
    tgl = st.date_input("Tanggal", date(2025,12,28))
    lokasi = st.text_input("Lokasi", "Gedung Serbaguna Bekasi")
    maps = st.text_input("Link Shareloc", "https://maps.app.goo.gl/")
    c1 = st.file_uploader("5 Foto Cover 3D", type=["jpg","png","webp"], accept_multiple_files=True)
    c2 = st.file_uploader("Foto Wanita", type=["jpg","png","webp"])
    c3 = st.file_uploader("Foto Pria", type=["jpg","png","webp"])
    c4 = st.file_uploader("5 Foto Gallery 3D", type=["jpg","png","webp"], accept_multiple_files=True)

def b64(file):
    if not file: return ""
    i = Image.open(file)
    buf = io.BytesIO()
    i.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode()

covers = [b64(x) for x in (c1[:5] if c1 else [])]
if not covers:
    covers = ["https://images.unsplash.com/photo-1519741497674-611481863552?w=800"]
wanita = b64(c2)
pria = b64(c3)
gals = [b64(x) for x in (c4[:5] if c4 else [])]

musik_src = f"data:audio/mp3;base64,{st.session_state.lagu}" if st.session_state.lagu else ""
slide = ""
for i,b in enumerate(covers):
    s = b if b.startswith("http") else f"data:image/jpeg;base64,{b}"
    a = "active" if i==0 else ""
    slide += f'<img src="{s}" class="{a}">'

gallery = ""
for b in gals:
    gallery += f'<div class="g3d"><img src="data:image/jpeg;base64,{b}"></div>'
if not gals:
    gallery = '<div class="g3d"><img src="https://images.unsplash.com/photo-1519741497674-611481863552?w=400"></div>'*4

wanita_src = f"data:image/jpeg;base64,{wanita}" if wanita else "https://images.unsplash.com/photo-1531123897727-8f129e1688ce?w=400"
pria_src = f"data:image/jpeg;base64,{pria}" if pria else "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400"
cover_first = covers[0] if covers[0].startswith("http") else f"data:image/jpeg;base64,{covers[0]}"

# HTML brutal 3D
html = f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1.0">
<script type="importmap">{{"imports":{{"three":"https://unpkg.com/three@0.160.0/build/three.module.js"}}}}</script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}} body{{background:#050505;color:#f5e6d3;font-family:sans-serif;overflow-x:hidden}}
#canvas3d{{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0}}
.top{{position:fixed;top:0;left:0;right:0;background:rgba(10,10,10,0.85);backdrop-filter:blur(20px);border-bottom:1px solid #d4af8a;padding:12px 18px;display:flex;justify-content:space-between;z-index:9999}}
.cover{{height:100vh;width:100%;position:fixed;top:0;left:0;z-index:9998;transition:1.2s cubic-bezier(.77,0,.175,1)}}
.cover .slides img{{width:100%;height:100%;object-fit:cover;position:absolute;top:0;left:0;opacity:0;transition:1.5s;transform:scale(1.15)}}
.cover .slides img.active{{opacity:1;transform:scale(1)}}
.overlay{{position:absolute;inset:0;background:radial-gradient(ellipse at center, rgba(0,0,0,0.1), rgba(0,0,0,0.8));display:flex;align-items:center;justify-content:center;z-index:2}}
.card-wrap{{perspective:1200px;transform-style:preserve-3d}}
.card{{width:360px;background:linear-gradient(145deg, rgba(255,248,240,0.12), rgba(255,240,220,0.08));backdrop-filter:blur(30px);border:1px solid rgba(212,175,138,0.5);border-radius:28px;padding:14px;transform:rotateY(-12deg) rotateX(8deg);box-shadow:0 40px 100px rgba(0,0,0,0.8), 0 0 0 1px rgba(212,175,138,0.2) inset;transition:0.8s;cursor:grab}}
.card:active{{cursor:grabbing}}
.inner{{border:1.5px solid #d4af8a;border-radius:22px;padding:28px 20px;text-align:center;background:radial-gradient(ellipse at top, rgba(255,248,240,0.98), rgba(253,242,230,0.92));color:#5D2E2E;transform:translateZ(30px)}}
.cover.hide{{transform:translateY(-100%) rotateX(25deg) scale(0.9)}}
#main{{display:none;position:relative;z-index:1;padding-top:60px}}
.sec{{padding:90px 20px;text-align:center;max-width:700px;margin:0 auto;position:relative}}
.oval3d{{width:230px;height:330px;border-radius:50% / 60%;overflow:hidden;margin:20px auto;border:7px solid #d4af8a;transform:rotateY(-15deg) translateZ(20px);box-shadow:0 30px 80px rgba(0,0,0,0.7);transition:0.6s}}
.oval3d:hover{{transform:rotateY(0) translateZ(50px) scale(1.05)}}
.oval3d img{{width:100%;height:100%;object-fit:cover}}
.parent3d{{background:linear-gradient(145deg, rgba(212,175,138,0.15), rgba(93,46,46,0.15));border:1px solid #d4af8a;border-radius:14px;padding:12px;margin-top:12px;transform:translateZ(15px)}}
.gallery3d{{display:flex;gap:20px;overflow-x:auto;padding:30px 10px;scroll-snap-type:x mandatory;perspective:1200px}}
.g3d{{min-width:300px;scroll-snap-align:center;background:rgba(255,255,255,0.06);border:1px solid rgba(212,175,138,0.3);border-radius:20px;padding:10px;transform:rotateY(-10deg) translateZ(0);transition:0.6s;box-shadow:0 20px 60px rgba(0,0,0,0.6)}}
.g3d:hover{{transform:rotateY(0) translateZ(60px) scale(1.05);box-shadow:0 40px 100px rgba(212,175,138,0.4)}}
.g3d img{{width:100%;height:380px;object-fit:cover;border-radius:16px}}
.btn3d{{background:linear-gradient(145deg,#d4af8a,#8B5E3C);color:#1a0f0f;border:none;padding:15px 36px;border-radius:30px;font-weight:800;cursor:pointer;box-shadow:0 15px 40px rgba(212,175,138,0.4), inset 0 1px 1px rgba(255,255,255,0.6);transform:translateZ(20px);transition:0.3s}}
.btn3d:hover{{transform:translateZ(40px) scale(1.08)}}
.float3d{{position:fixed;bottom:28px;right:22px;width:62px;height:62px;background:radial-gradient(circle at 30% 30%, #d4af8a, #5D2E2E);border-radius:50%;display:flex;align-items:center;justify-content:center;z-index:100;cursor:pointer;box-shadow:0 15px 40px rgba(0,0,0,0.6), 0 0 0 2px #d4af8a;animation:float3d 3s ease-in-out infinite;transform:translateZ(20px)}}
@keyframes float3d{{0%,100%{{transform:translateY(0) translateZ(20px)}} 50%{{transform:translateY(-10px) translateZ(40px)}}}}
.count3d{{display:flex;gap:14px;justify-content:center;margin:25px 0}}
.count3d div{{background:linear-gradient(145deg, rgba(255,255,255,0.08), rgba(0,0,0,0.2));border:1px solid #d4af8a;border-radius:18px;padding:18px 14px;min-width:86px;transform:rotateY(-8deg);box-shadow:0 10px 30px rgba(0,0,0,0.4);transition:0.4s}}
.count3d div:hover{{transform:rotateY(0) translateZ(20px)}}
</style></head><body>
<canvas id="canvas3d"></canvas>
<div class="top"><div>✨ 3D BRUTAL • {nw} & {np}</div><button id="tbtn" onclick="toggle()" style="background:#d4af8a;border:none;padding:7px 14px;border-radius:20px;font-weight:700;cursor:pointer">Play</button></div>
<div class="cover" id="cover"><div class="slides" id="slides">{slide}</div><div class="overlay"><div class="card-wrap"><div class="card" id="mainCard"><div class="inner">
<p style="letter-spacing:6px;font-size:11px;color:#8B5E3C">THE WEDDING OF</p>
<div style="width:88px;height:88px;margin:16px auto;border-radius:50%;overflow:hidden;border:3px solid #d4af8a;box-shadow:0 10px 30px rgba(0,0,0,0.3)"><img src="{cover_first}" style="width:100%;height:100%;object-fit:cover"></div>
<div style="font-size:32px;font-weight:900;line-height:1;color:#5D2E2E">{nw}<br>&<br>{np}</div>
<p style="font-size:12px;color:#8B5E3C;margin:14px 0">{tgl.strftime('%d %B %Y')} • Auto 3D Slide</p>
<div style="background:white;border-radius:14px;padding:12px;border:1px dashed #d4af8a"><p style="font-size:10px">Kepada Yth.</p><p style="font-weight:800;font-size:15px">Tamu Undangan</p><p style="font-size:9px;color:#8B5E3C">Drag kartu 3D ini 👆</p></div><br>
<button class="btn3d" onclick="buka()">✨ BUKA UNDANGAN 3D</button>
</div></div></div></div></div>
<div id="main">
<div class="sec"><h1 style="font-size:52px;font-weight:900;color:#d4af8a;text-shadow:0 0 30px rgba(212,175,138,0.5)">{nw} & {np}</h1><p style="letter-spacing:3px;margin-top:15px">{tgl.strftime('%A, %d %B %Y')} • {lokasi}</p></div>
<div class="sec" style="display:flex;gap:40px;justify-content:center;flex-wrap:wrap">
<div><div class="oval3d"><img src="{wanita_src}"></div><h3>{nw}</h3><div class="parent3d">Putri dari<br><b>{ayah_w}<br>& {ibu_w}</b></div></div>
<div><div class="oval3d"><img src="{pria_src}"></div><h3>{np}</h3><div class="parent3d">Putra dari<br><b>{ayah_p}<br>& {ibu_p}</b></div></div>
</div>
<div class="sec"><h2 style="font-size:36px">Menuju Hari Bahagia</h2><div class="count3d"><div><h2 id="d">46</h2><p>HARI</p></div><div><h2 id="h">20</h2><p>JAM</p></div><div><h2 id="m">30</h2><p>MENIT</p></div><div><h2 id="s">10</h2><p>DETIK</p></div></div><p>{lokasi}</p><br><a href="{maps}" target="_blank" class="btn3d" style="text-decoration:none;display:inline-block">📍 Shareloc Maps 3D</a></div>
<div class="sec"><h2 style="font-size:32px">Gallery 3D - Drag & Swipe</h2><p style="font-size:12px;opacity:0.6">Efek 3D asli - geser kiri kanan</p><div class="gallery3d" id="gal">{gallery}</div></div>
</div>
<div class="float3d" id="fbtn" onclick="toggle()">🎵</div>
<audio id="aud" loop src="{musik_src}"></audio>
<script type="module">
import * as THREE from 'three';
let scene, camera, renderer, hearts=[], particles;
let mouseX=0, mouseY=0;
function init3D(){{
  scene=new THREE.Scene();
  camera=new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
  camera.position.z=6;
  renderer=new THREE.WebGLRenderer({{canvas:document.getElementById('canvas3d'), alpha:true, antialias:true}});
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  // Hearts 3D
  for(let i=0;i<18;i++){{
    let g=new THREE.SphereGeometry(0.08, 8, 8);
    let m=new THREE.MeshPhongMaterial({{color: i%2==0 ? 0xd4af8a : 0x5D2E2E, emissive:0x331111, transparent:true, opacity:0.8}});
    let mesh=new THREE.Mesh(g,m);
    mesh.position.set((Math.random()-0.5)*12, (Math.random()-0.5)*10, (Math.random()-0.5)*5);
    mesh.userData={{speed:0.002+Math.random()*0.008, rot:Math.random()*0.02}};
    hearts.push(mesh); scene.add(mesh);
  }}
  // Lights
  let light=new THREE.PointLight(0xd4af8a, 2, 20); light.position.set(2,2,4); scene.add(light);
  let amb=new THREE.AmbientLight(0xffffff, 0.6); scene.add(amb);
  // Particles gold dust
  let geo=new THREE.BufferGeometry(); let pos=[]; for(let i=0;i<600;i++){{pos.push((Math.random()-0.5)*15, (Math.random()-0.5)*15, (Math.random()-0.5)*10)}} geo.setAttribute('position', new THREE.Float32BufferAttribute(pos,3));
  let mat=new THREE.PointsMaterial({{color:0xd4af8a, size:0.02, transparent:true, opacity:0.6}}); particles=new THREE.Points(geo, mat); scene.add(particles);
  animate();
}}
function animate(){{
  requestAnimationFrame(animate);
  hearts.forEach(h=>{{h.position.y+=h.userData.speed; h.rotation.y+=h.userData.rot; if(h.position.y>6) h.position.y=-6;}});
  if(particles) particles.rotation.y+=0.0005;
  camera.position.x+=(mouseX*0.5 - camera.position.x)*0.05;
  camera.position.y+=(-mouseY*0.5 - camera.position.y)*0.05;
  camera.lookAt(0,0,0);
  renderer.render(scene,camera);
}}
window.addEventListener('mousemove', e=>{{mouseX=(e.clientX/window.innerWidth)*2-1; mouseY=-(e.clientY/window.innerHeight)*2+1;}});
window.addEventListener('resize', ()=>{{camera.aspect=window.innerWidth/window.innerHeight; camera.updateProjectionMatrix(); renderer.setSize(window.innerWidth, window.innerHeight);}});
init3D();

// 3D Card drag
let card=document.getElementById('mainCard'); let isDrag=false, startX, startY, rotY=-12, rotX=8;
card.addEventListener('mousedown', e=>{{isDrag=true; startX=e.clientX; startY=e.clientY; card.style.cursor='grabbing';}});
window.addEventListener('mouseup', ()=>{{isDrag=false; card.style.cursor='grab'; card.style.transition='0.8s'; setTimeout(()=>{{card.style.transform=`rotateY(${{rotY}}deg) rotateX(${{rotX}}deg)`}},100);}});
window.addEventListener('mousemove', e=>{{if(!isDrag) return; card.style.transition='0s'; let dx=(e.clientX-startX)*0.3; let dy=(e.clientY-startY)*0.3; card.style.transform=`rotateY(${{rotY+dx}}deg) rotateX(${{rotX-dy}}deg) translateZ(40px)`;}});
// Touch for mobile
card.addEventListener('touchstart', e=>{{isDrag=true; startX=e.touches[0].clientX; startY=e.touches[0].clientY;}});
window.addEventListener('touchend', ()=>{{isDrag=false;}});
window.addEventListener('touchmove', e=>{{if(!isDrag) return; let dx=(e.touches[0].clientX-startX)*0.3; let dy=(e.touches[0].clientY-startY)*0.3; card.style.transform=`rotateY(${{rotY+dx}}deg) rotateX(${{rotX-dy}}deg) translateZ(40px)`;}});

// Slide logic
let cur=0, total={len(covers)}, play=false;
function show(n){{document.querySelectorAll('#slides img').forEach(i=>i.classList.remove('active')); let el=document.querySelectorAll('#slides img')[n]; if(el) el.classList.add('active')}}
function next(){{cur=(cur+1)%total; show(cur)}}
setInterval(next, 3800);
window.buka=function(){{document.getElementById('cover').classList.add('hide'); setTimeout(()=>{{document.getElementById('main').style.display='block'}},1000); let a=document.getElementById('aud'); if(a.src){{a.play().then(()=>{{play=true; document.getElementById('tbtn').innerText='Pause'; document.getElementById('fbtn').innerText='⏸️';}})}}}}
window.toggle=function(){{let a=document.getElementById('aud'); let t=document.getElementById('tbtn'); let f=document.getElementById('fbtn'); if(play){{a.pause(); t.innerText='Play'; f.innerText='🎵'; play=false}}else{{if(a.src) a.play(); t.innerText='Pause'; f.innerText='⏸️'; play=true}}}}
show(0);
let target=new Date("{tgl}").getTime(); setInterval(()=>{{let diff=target-Date.now(); if(diff>0){{document.getElementById('d').innerText=Math.floor(diff/(1000*60*60*24)); document.getElementById('h').innerText=Math.floor((diff%(1000*60*60*24))/(1000*60*60)); document.getElementById('m').innerText=Math.floor((diff%(1000*60*60))/(1000*60)); document.getElementById('s').innerText=Math.floor((diff%(1000*60))/1000);}}}},1000);
</script>
</body></html>
"""

components.html(html, height=1000, scrolling=True)
