import time
import streamlit as st

# ═════════════════════════════════════════════════════════════
# 1) KATILIMCILAR
# ═════════════════════════════════════════════════════════════
KATILIMCILAR = [
    "Güliz", "Pınar", "Aslı", "Sümeyra", "Gizem", "Necdet",
    "Aleyna", "Tülay", "Elif", "Oğuz", "Demet", "Pars",
    "Çağatay", "Ezgi", "Huriye", "Zehra", "Aysun",
]

# ═════════════════════════════════════════════════════════════
# 2) SORULAR
# ═════════════════════════════════════════════════════════════
BILGILER = [
    {"soru": "Üniversitede okuduğu bölümle hiç alakasız bir işte çalışıyor",
     "adaylar": ["Güliz", "Necdet", "Elif", "Aysun"]},
    {"soru": "İlk işi bir çağrı merkezindeydi",
     "adaylar": ["Pınar", "Aleyna", "Oğuz", "Zehra"]},
    {"soru": "Çocukken pilot olmak istiyordu",
     "adaylar": ["Aslı", "Pars", "Tülay", "Çağatay"]},
    {"soru": "Evde üçten fazla hayvanı var",
     "adaylar": ["Sümeyra", "Demet", "Gizem", "Huriye"]},
    {"soru": "Hiç yurt dışına çıkmadı",
     "adaylar": ["Gizem", "Necdet", "Zehra", "Ezgi"]},
    {"soru": "Bir enstrüman çalabiliyor",
     "adaylar": ["Çağatay", "Elif", "Aysun", "Pars"]},
    {"soru": "Ehliyeti var ama hiç araba kullanmıyor",
     "adaylar": ["Tülay", "Aleyna", "Pınar", "Demet"]},
    {"soru": "Sabah 6'dan önce kalkıyor",
     "adaylar": ["Huriye", "Oğuz", "Güliz", "Sümeyra"]},
    {"soru": "Aynı diziyi beşten fazla kez baştan izledi",
     "adaylar": ["Ezgi", "Aslı", "Zehra", "Aleyna"]},
]

SURE = 15
OYUN_ADI = "Bu Kim?"
ALT_BASLIK = "Bakalım birbirimizi ne kadar tanıyoruz"

# ═════════════════════════════════════════════════════════════

st.set_page_config(page_title=OYUN_ADI, page_icon="🎀", layout="centered")

RENKLER = ["#E8547C", "#7B5EA7", "#E8A33D", "#3DA9A0", "#D45D79",
           "#5C7AEA", "#C96EA8", "#4FA35C", "#E07B39", "#8A6BBF",
           "#2E8B9E", "#B8496B", "#6A8F3C", "#A85CC4", "#D9793E",
           "#3F7FB5", "#C2477D"]


@st.cache_resource
def ortak():
    return {"aktif": None, "baslangic": None, "oylar": {}, "puan": {}, "islenen": set()}


V = ortak()

st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(160deg,#fdf2f8 0%,#f6efff 55%,#fff7ed 100%); }
    section[data-testid="stSidebar"] { background:#fdf2f8; }

    .marka { text-align:center; margin-bottom:1.2rem; }
    .marka h1 { font-size:2.4rem; font-weight:800; margin:0;
        background:linear-gradient(90deg,#E8547C,#7B5EA7);
        -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
    .marka p { color:#8b7a94; margin:.2rem 0 0; font-size:.95rem; }

    .soru-kart { background:#fff; border-radius:24px; padding:1.8rem 1.4rem;
        text-align:center; font-size:1.5rem; font-weight:700; color:#3d2d45;
        box-shadow:0 10px 30px rgba(180,120,180,.18); margin-bottom:1.2rem;
        border:2px solid rgba(232,84,124,.15); }

    .halka { width:130px; height:130px; margin:0 auto 1rem; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:3rem; font-weight:800; color:#fff;
        box-shadow:0 8px 24px rgba(232,84,124,.35); }
    .halka.normal { background:linear-gradient(135deg,#E8547C,#7B5EA7); }
    .halka.acil { background:linear-gradient(135deg,#e63946,#f77f00);
        animation:zipla .6s infinite; }
    @keyframes zipla { 0%,100%{transform:scale(1)} 50%{transform:scale(1.12)} }

    div.stButton > button { border-radius:18px; border:none; color:#fff !important;
        font-weight:700; font-size:1.05rem; padding:.9rem .5rem; width:100%;
        box-shadow:0 6px 16px rgba(0,0,0,.13); transition:transform .12s; }
    div.stButton > button:hover { transform:translateY(-3px); color:#fff !important; }
    div.stButton > button:active { transform:scale(.96); }

    .kazanan { background:linear-gradient(135deg,#fff0f6,#f3ecff);
        border-radius:26px; padding:2rem 1.2rem; text-align:center;
        border:3px solid #E8547C; box-shadow:0 14px 36px rgba(232,84,124,.28); }
    .kazanan .ad { font-size:2.8rem; font-weight:800; color:#E8547C; margin:0; }
    .kazanan .alt { font-size:1rem; color:#8b7a94; margin-top:.4rem; }

    .cubuk-sar { background:#fff; border-radius:14px; padding:.7rem .9rem;
        margin-bottom:.5rem; box-shadow:0 3px 10px rgba(180,120,180,.12); }
    .cubuk-ad { font-weight:700; color:#3d2d45; font-size:.95rem; }
    .cubuk-dis { background:#f1e7f5; border-radius:8px; height:12px; margin-top:.35rem; }
    .cubuk-ic { height:12px; border-radius:8px; }

    .madalya { background:#fff; border-radius:16px; padding:.8rem 1rem;
        margin-bottom:.5rem; display:flex; justify-content:space-between;
        box-shadow:0 3px 10px rgba(180,120,180,.12); font-weight:700; color:#3d2d45; }
    .bekleme { text-align:center; padding:2.5rem 1rem; color:#8b7a94; font-size:1.1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


def renk(ad):
    return RENKLER[KATILIMCILAR.index(ad) % len(RENKLER)]


def kalan():
    if V["baslangic"] is None:
        return 0
    return max(0, SURE - int(time.time() - V["baslangic"]))


def puanlari_isle(i):
    """Çoğunluğa katılanlara hız bonuslu puan ver."""
    if i in V["islenen"]:
        return
    kayitlar = V["oylar"].get(i, {})
    if not kayitlar:
        V["islenen"].add(i)
        return
    sayim = {}
    for secim, _ in kayitlar.values():
        sayim[secim] = sayim.get(secim, 0) + 1
    en_yuksek = max(sayim.values())
    kazanan_secimler = {s for s, a in sayim.items() if a == en_yuksek}
    for oyuncu, (secim, sn) in kayitlar.items():
        if secim in kazanan_secimler:
            bonus = int(500 + 500 * max(0, (SURE - sn)) / SURE)
            V["puan"][oyuncu] = V["puan"].get(oyuncu, 0) + bonus
        else:
            V["puan"].setdefault(oyuncu, 0)
    V["islenen"].add(i)


st.markdown(
    f'<div class="marka"><h1>🎀 {OYUN_ADI}</h1><p>{ALT_BASLIK}</p></div>',
    unsafe_allow_html=True,
)

mod = st.sidebar.radio("Ekran", ["Oyuncu", "Sunum ekranı"])

# ══════════════════════════ OYUNCU ══════════════════════════
if mod == "Oyuncu":
    isim = st.selectbox("Sen kimsin?", ["— seç —"] + KATILIMCILAR)
    if isim == "— seç —":
        st.markdown('<div class="bekleme">👋 Başlamak için ismini seç</div>',
                    unsafe_allow_html=True)
        st.stop()

    @st.fragment(run_every="1s")
    def oyuncu():
        i = V["aktif"]
        if i is None:
            st.markdown('<div class="bekleme">⏳ Sunucunun soruyu başlatmasını bekle…</div>',
                        unsafe_allow_html=True)
            return

        st.markdown(f'<div class="soru-kart">{BILGILER[i]['soru']}</div>', unsafe_allow_html=True)
        k = kalan()

        if k == 0:
            puanlari_isle(i)
            st.markdown('<div class="bekleme">⏱️ Süre doldu — sonuç büyük ekranda!</div>',
                        unsafe_allow_html=True)
            p = V["puan"].get(isim, 0)
            st.markdown(f'<div class="madalya"><span>Puanın</span><span>{p}</span></div>',
                        unsafe_allow_html=True)
            return

        sinif = "acil" if k <= 5 else "normal"
        st.markdown(f'<div class="halka {sinif}">{k}</div>', unsafe_allow_html=True)

        mevcut = V["oylar"].get(i, {}).get(isim)
        if mevcut:
            st.markdown(
                f'<div class="madalya"><span>Cevabın</span><span>{mevcut[0]}</span></div>',
                unsafe_allow_html=True)

        adaylar = BILGILER[i]["adaylar"]
        kol = st.columns(2)
        for n, ad in enumerate(adaylar):
            with kol[n % 2]:
                st.markdown(
                    f"<style>div[data-testid='stVerticalBlock'] div.stButton "
                    f"button[kind][aria-label], .b{n} {{}}</style>",
                    unsafe_allow_html=True)
                if st.button(ad, key=f"o{i}_{ad}", use_container_width=True):
                    gecen = SURE - k
                    V["oylar"].setdefault(i, {})[isim] = (ad, gecen)
                    st.rerun(scope="fragment")

    oyuncu()

    st.markdown(
        "<style>"
        + "".join(
            f"div.stButton > button[key='o{V['aktif']}_{ad}'] {{background:{renk(ad)};}}"
            for ad in KATILIMCILAR
        )
        + "</style>",
        unsafe_allow_html=True,
    )

# ══════════════════════ SUNUM EKRANI ══════════════════════
else:
    secim = st.selectbox("Soru seç", range(len(BILGILER)),
                         format_func=lambda x: f"{x+1}. {BILGILER[x]['soru']}")

    c1, c2 = st.columns(2)
    if c1.button("▶️ Soruyu başlat", use_container_width=True):
        V["aktif"] = secim
        V["baslangic"] = time.time()
        V["oylar"].pop(secim, None)
        V["islenen"].discard(secim)
        st.rerun()
    if c2.button("🔄 Sıfırla", use_container_width=True):
        V.update({"aktif": None, "baslangic": None})
        V["oylar"].clear(); V["puan"].clear(); V["islenen"].clear()
        st.rerun()

    st.divider()

    @st.fragment(run_every="1s")
    def sunum():
        i = V["aktif"]
        if i is None:
            st.markdown('<div class="bekleme">Bir soru seçip başlat 🎬</div>',
                        unsafe_allow_html=True)
            return

        st.markdown(f'<div class="soru-kart">{BILGILER[i]['soru']}</div>', unsafe_allow_html=True)
        k = kalan()
        kayitlar = V["oylar"].get(i, {})

        if k > 0:
            sinif = "acil" if k <= 5 else "normal"
            st.markdown(f'<div class="halka {sinif}">{k}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="bekleme">✋ {len(kayitlar)} kişi cevapladı</div>',
                unsafe_allow_html=True)
            return

        if not kayitlar:
            st.markdown('<div class="bekleme">Kimse cevaplamadı 😅</div>',
                        unsafe_allow_html=True)
            return

        puanlari_isle(i)

        sayim = {}
        for secim_ad, _ in kayitlar.values():
            sayim[secim_ad] = sayim.get(secim_ad, 0) + 1
        en_yuksek = max(sayim.values())
        kazananlar = [a for a, s in sayim.items() if s == en_yuksek]
        toplam = len(kayitlar)

        st.markdown(
            f'<div class="kazanan">🏆<p class="ad">{" & ".join(kazananlar)}</p>'
            f'<p class="alt">en çok seçilen isim — {en_yuksek}/{toplam} oy 🎉</p></div>',
            unsafe_allow_html=True)
        st.write("")

        for ad, s in sorted(sayim.items(), key=lambda x: -x[1]):
            yuzde = int(s / toplam * 100)
            st.markdown(
                f'<div class="cubuk-sar"><div class="cubuk-ad">{ad} — {s} oy</div>'
                f'<div class="cubuk-dis"><div class="cubuk-ic" '
                f'style="width:{yuzde}%;background:{renk(ad)}"></div></div></div>',
                unsafe_allow_html=True)

        if V["puan"]:
            st.write("")
            st.markdown("#### 🥇 Liderlik tablosu")
            madalyalar = ["🥇", "🥈", "🥉"]
            for n, (ad, p) in enumerate(sorted(V["puan"].items(), key=lambda x: -x[1])):
                isaret = madalyalar[n] if n < 3 else f"{n+1}."
                st.markdown(
                    f'<div class="madalya"><span>{isaret} {ad}</span><span>{p}</span></div>',
                    unsafe_allow_html=True)

    sunum()
