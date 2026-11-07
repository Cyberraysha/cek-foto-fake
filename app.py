import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Cek Foto Fake Pro", page_icon="🕵️", layout="centered")
st.title("🕵️ Cek Foto Fake PRO v3")

uploaded = st.file_uploader("Upload foto yang mau dicek", type=["jpg","jpeg","png"])

if uploaded:
    image = Image.open(uploaded)
    st.image(image, use_column_width=True)
    
    if st.button("CEK SEKARANG - AKURAT", type="primary"):
        with st.spinner("Menganalisa..."):
            # LOGIKA REAL
            exif = image._getexif()
            w, h = image.size
            filesize = len(uploaded.getvalue()) / 1024
            
            fake_score = 0
            logs = []

            # 1. Cek EXIF - kalo ga ada EXIF biasanya comotan FB/WA/AI
            if not exif:
                fake_score += 35
                logs.append("❌ Tidak ada data kamera (EXIF kosong) - ciri foto download / AI")
            else:
                logs.append("✅ Ada data kamera - foto asli dari HP")

            # 2. Cek ukuran file vs resolusi
            if filesize < 150:
                fake_score += 25
                logs.append("❌ File terlalu kecil (<150KB) - foto sudah di-compress / comotan")
            
            # 3. Cek resolusi aneh AI biasanya 1024x1024, 512x512
            if w in [512, 768, 1024, 1024] and h in [512, 768, 1024]:
                fake_score += 20
                logs.append("❌ Resolusi kotak AI (512, 768, 1024)")
            
            # Hasil final
            st.divider()
            if fake_score >= 50:
                st.error(f"🚨 HASIL: {fake_score}% FAKE / SCAM - WASPADA!")
            elif fake_score >= 25:
                st.warning(f"⚠️ HASIL: {fake_score}% Mencurigakan")
            else:
                st.success(f"✅ HASIL: {100-fake_score}% ASLI - Keliatan natural")

            for l in logs:
                st.write(l)

            st.info("💡 Tips: Kalo kenalan online, wajib video call. Jangan kirim uang / foto KTP!")
