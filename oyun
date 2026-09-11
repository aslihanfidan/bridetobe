import streamlit as st

# ─────────────────────────────────────────────────────────────
# 1) KATILIMCI İSİMLERİ — şıklar bu listeden gelir
# ─────────────────────────────────────────────────────────────
KATILIMCILAR = [
    "Aslı", "Büşra", "Sümeyra", "Pınar", "Güliz",
    "Ezgi", "Deniz", "Merve", "Can", "Elif",
]

# ─────────────────────────────────────────────────────────────
# 2) BİLGİLER — "bu kim?" soruları
#    "dogru": bilginin sahibi. Bilerek gizli tutmak istersen None bırak,
#    o zaman sadece çoğunluğun tahmini gösterilir.
# ─────────────────────────────────────────────────────────────
BILGILER = [
    {"bilgi": "Üniversitede okuduğu bölümle hiç alakasız bir işte çalışıyor", "dogru": None},
    {"bilgi": "İlk işi bir çağrı merkezindeydi", "dogru": None},
    {"bilgi": "Çocukken pilot olmak istiyordu", "dogru": None},
    {"bilgi": "Evde üçten fazla hayvanı var", "dogru": None},
    {"bilgi": "Hiç yurt dışına çıkmadı", "dogru": None},
    {"bilgi": "Bir enstrüman çalabiliyor", "dogru": None},
    {"bilgi": "Ehliyeti var ama hiç araba kullanmıyor", "dogru": None},
    {"bilgi": "Sabah 6'dan önce kalkıyor", "dogru": None},
    {"bilgi": "Aynı diziyi beşten fazla kez baştan izledi", "dogru": None},
]

BASLIK = "Bu Kim?"
ALT_BASLIK = "Her bilgi birimizle ilgili. Bakalım birbirimizi ne kadar tanıyoruz?"

# ─────────────────────────────────────────────────────────────

st.set_page_config(page_title=BASLIK, page_icon="🎀", layout="centered")


@st.cache_resource
def ortak_veri():
    """Tüm oyuncular arasında paylaşılan hafıza."""
    return {"cevaplar": {}, "acilan": set()}


VERI = ortak_veri()

st.markdown(
    """
    <style>
    .baslik { font-size: 2rem; font-weight: 700; margin-bottom: 0; }
    .altbaslik { color: #6b6b6b; margin-top: .2rem; }
    .sonuc { font-size: 2.2rem; font-weight: 800; text-align: center;
             padding: 1.1rem; border-radius: 16px; background: #ffeef4; }
    </style>
    """,
    unsafe_allow_html=True,
)

mod = st.sidebar.radio("Ekran", ["Oyuncu", "Sunum ekranı"])

# ══════════════════════════════ OYUNCU ══════════════════════════════
if mod == "Oyuncu":
    st.markdown(f'<p class="baslik">🎀 {BASLIK}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="altbaslik">{ALT_BASLIK}</p>', unsafe_allow_html=True)

    isim = st.selectbox("Sen kimsin?", ["— seç —"] + KATILIMCILAR)

    if isim == "— seç —":
        st.info("Başlamak için ismini seç.")
        st.stop()

    if isim in VERI["cevaplar"]:
        st.success("Kartın kaydedildi. Sonuçlar sunum ekranında 🎉")
        if st.button("Cevaplarımı değiştir"):
            del VERI["cevaplar"][isim]
            st.rerun()
        st.stop()

    secimler = []
    for i, b in enumerate(BILGILER):
        secim = st.radio(f"**{i+1}. {b['bilgi']}**", KATILIMCILAR, index=None,
                         key=f"q{i}", horizontal=False)
        secimler.append(secim)
        st.divider()

    if st.button("Kartı gönder", type="primary", use_container_width=True):
        if None in secimler:
            st.warning("Tüm kutucukları doldurman gerekiyor.")
        else:
            VERI["cevaplar"][isim] = secimler
            st.balloons()
            st.rerun()

# ══════════════════════════ SUNUM EKRANI ══════════════════════════
else:
    st.markdown('<p class="baslik">🎤 Sunum ekranı</p>', unsafe_allow_html=True)
    st.caption(f"Kartını gönderen: {len(VERI['cevaplar'])} kişi")

    if not VERI["cevaplar"]:
        st.info("Henüz kimse kart göndermedi.")
        st.stop()

    st.write("**Oynayanlar:** " + ", ".join(VERI["cevaplar"].keys()))
    st.divider()

    for i, b in enumerate(BILGILER):
        st.markdown(f"**{i+1}. {b['bilgi']}**")

        oylar = [c[i] for c in VERI["cevaplar"].values()]
        sayim = {ad: oylar.count(ad) for ad in KATILIMCILAR if oylar.count(ad) > 0}
        toplam = max(len(oylar), 1)

        if i in VERI["acilan"]:
            for ad, adet in sorted(sayim.items(), key=lambda x: -x[1]):
                etiket = f"{ad} — {adet} oy"
                if b["dogru"] and ad == b["dogru"]:
                    etiket = f"✅ {etiket}  (doğru)"
                st.progress(adet / toplam, text=etiket)

            en_cok = max(sayim, key=sayim.get)
            st.markdown(
                f'<div class="sonuc">👉 {en_cok}<br>'
                f'<span style="font-size:1rem;font-weight:500">en çok oyu alan isim '
                f'({sayim[en_cok]}/{toplam})</span></div>',
                unsafe_allow_html=True,
            )
            if b["dogru"]:
                st.caption(f"Gerçek cevap: **{b['dogru']}**")
        else:
            if st.button("Oyları göster", key=f"ac{i}"):
                VERI["acilan"].add(i)
                st.rerun()

        st.divider()

    # Doğru cevaplar girildiyse sıralama tablosu
    if all(b["dogru"] for b in BILGILER) and len(VERI["acilan"]) == len(BILGILER):
        puanlar = {
            ad: sum(1 for i, b in enumerate(BILGILER) if c[i] == b["dogru"])
            for ad, c in VERI["cevaplar"].items()
        }
        st.subheader("🏆 Sıralama")
        for ad, p in sorted(puanlar.items(), key=lambda x: -x[1]):
            st.write(f"{ad} — {p}/{len(BILGILER)}")
        st.balloons()

    if st.button("Oyunu sıfırla"):
        VERI["cevaplar"].clear()
        VERI["acilan"].clear()
        st.rerun()
