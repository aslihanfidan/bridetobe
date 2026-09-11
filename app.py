import time
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
# ─────────────────────────────────────────────────────────────
BILGILER = [
    "Üniversitede okuduğu bölümle hiç alakasız bir işte çalışıyor",
    "İlk işi bir çağrı merkezindeydi",
    "Çocukken pilot olmak istiyordu",
    "Evde üçten fazla hayvanı var",
    "Hiç yurt dışına çıkmadı",
    "Bir enstrüman çalabiliyor",
    "Ehliyeti var ama hiç araba kullanmıyor",
    "Sabah 6'dan önce kalkıyor",
    "Aynı diziyi beşten fazla kez baştan izledi",
]

SURE = 15  # saniye

# ─────────────────────────────────────────────────────────────

st.set_page_config(page_title="Bu Kim?", page_icon="🎀", layout="centered")


@st.cache_resource
def ortak():
    return {
        "aktif": None,        # aktif soru indeksi
        "baslangic": None,    # soru başlama zamanı
        "oylar": {},          # {soru_index: {isim: secim}}
        "bitenler": set(),
    }


V = ortak()

st.markdown(
    """
    <style>
    .soru { font-size: 1.6rem; font-weight: 700; text-align: center;
            padding: 1.4rem 1rem; border-radius: 16px; background: #fff3f8;
            margin-bottom: 1rem; }
    .sayac { font-size: 4rem; font-weight: 800; text-align: center; margin: .5rem 0; }
    .kazanan { font-size: 2.6rem; font-weight: 800; text-align: center;
               padding: 1.6rem; border-radius: 20px; background: #ffeef4; }
    </style>
    """,
    unsafe_allow_html=True,
)


def kalan():
    if V["baslangic"] is None:
        return 0
    return max(0, SURE - int(time.time() - V["baslangic"]))


mod = st.sidebar.radio("Ekran", ["Oyuncu", "Sunum ekranı"])

# ══════════════════════════════ OYUNCU ══════════════════════════════
if mod == "Oyuncu":
    st.markdown("### 🎀 Bu Kim?")

    isim = st.selectbox("Sen kimsin?", ["— seç —"] + KATILIMCILAR)
    if isim == "— seç —":
        st.info("Başlamak için ismini seç.")
        st.stop()

    @st.fragment(run_every="1s")
    def oyuncu_ekrani():
        i = V["aktif"]
        if i is None:
            st.info("⏳ Sunucunun soruyu başlatmasını bekle…")
            return

        k = kalan()
        st.markdown(f'<div class="soru">{BILGILER[i]}</div>', unsafe_allow_html=True)

        if k == 0:
            st.warning("⏱️ Süre doldu! Sonuç ekranda.")
            return

        st.markdown(f'<div class="sayac">{k}</div>', unsafe_allow_html=True)
        st.progress(k / SURE)

        mevcut = V["oylar"].get(i, {}).get(isim)
        if mevcut:
            st.success(f"Cevabın: **{mevcut}** — değiştirmek için başka bir isme bas")

        kolonlar = st.columns(2)
        for n, ad in enumerate(KATILIMCILAR):
            if kolonlar[n % 2].button(ad, key=f"o{i}_{ad}", use_container_width=True):
                V["oylar"].setdefault(i, {})[isim] = ad
                st.rerun(scope="fragment")

    oyuncu_ekrani()

# ══════════════════════════ SUNUM EKRANI ══════════════════════════
else:
    st.markdown("### 🎤 Sunum ekranı")

    secim = st.selectbox(
        "Soru seç",
        range(len(BILGILER)),
        format_func=lambda x: f"{x+1}. {BILGILER[x]}",
    )

    c1, c2 = st.columns(2)
    if c1.button("▶️ Soruyu başlat", type="primary", use_container_width=True):
        V["aktif"] = secim
        V["baslangic"] = time.time()
        V["oylar"].pop(secim, None)
        st.rerun()
    if c2.button("🔄 Oyunu sıfırla", use_container_width=True):
        V["aktif"] = None
        V["baslangic"] = None
        V["oylar"].clear()
        st.rerun()

    st.divider()

    @st.fragment(run_every="1s")
    def sunum():
        i = V["aktif"]
        if i is None:
            st.info("Bir soru seçip başlat.")
            return

        st.markdown(f'<div class="soru">{BILGILER[i]}</div>', unsafe_allow_html=True)
        k = kalan()
        oylar = list(V["oylar"].get(i, {}).values())

        if k > 0:
            st.markdown(f'<div class="sayac">{k}</div>', unsafe_allow_html=True)
            st.progress(k / SURE)
            st.caption(f"Cevaplayan: {len(oylar)} kişi")
            return

        if not oylar:
            st.warning("Kimse cevaplamadı 😅")
            return

        sayim = {}
        for o in oylar:
            sayim[o] = sayim.get(o, 0) + 1
        en_yuksek = max(sayim.values())
        kazananlar = [ad for ad, s in sayim.items() if s == en_yuksek]

        st.markdown(
            f'<div class="kazanan">🏆 {" & ".join(kazananlar)} 🎉<br>'
            f'<span style="font-size:1.1rem;font-weight:500">'
            f"en çok seçilen isim — {en_yuksek}/{len(oylar)} oy</span></div>",
            unsafe_allow_html=True,
        )

        if i not in V["bitenler"]:
            V["bitenler"].add(i)
            st.balloons()

        st.write("")
        for ad, s in sorted(sayim.items(), key=lambda x: -x[1]):
            st.progress(s / len(oylar), text=f"{ad} — {s} oy")

    sunum()
