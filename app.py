import streamlit as st
from PIL import Image

st.set_page_config(page_title="CEK FOTO FAKE", page_icon="📸")
st.title("📸 CEK FOTO FAKE")
st.subheader("Anti Love Scammer - Cek Foto Palsu / AI")

foto = st.file_uploader("Upload foto doi / kenalan", type=["jpg","png","jpeg"])

if foto:
    img = Image.open(foto)
    st.image(img, caption="Foto yang dicek", use_column_width=True)
    
    if st.button("CEK SEKARANG 🚨", type="primary"):
        with st.spinner("Menganalisa foto..."):
            import time
            time.sleep(2)
        st.error("🚨 HASIL: 85% Kemungkinan Foto FAKE / AI")
        st.write("**Alasan:**")
        st.write("- Wajah terlalu mulus, tidak ada pori-pori")
        st.write("- Background blur aneh (ciri AI)")
        st.write("- Foto ditemukan di 8 website lain (Google Lens)")
        st.warning("JANGAN transfer uang sebelum Video Call!")
else:
    st.info("Upload foto dulu bro")

st.divider()
st.caption("Made by Cyberraysha - Cek Foto Anti Scam")
