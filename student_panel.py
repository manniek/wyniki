import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. DANE (Indeksy 1, 15, 16 - Twoja żelazna logika)
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    kol_info = wiersz_clean.columns

    imie = str(dane[1]).split()[1] if len(str(dane[1]).split()) > 1 else str(dane[1])
    suma_total = float(dane[15])
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""

    # 2. NAGŁÓWEK KOMPUTEROWY (Drabinka z wczoraj)
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])
    with c_pow:
        st.subheader(f"👋 {imie}!")
    with c_progi:
        p = st.columns(6)
        s = 'display:block; color:white; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold;'
        kolory = [("#FF0000", "2"), ("#92D050", "3"), ("#00B050", "3.5"), ("#00B0F0", "4"), ("#0070C0", "4.5"), ("#FFC000", "5")]
        for i, (kolor, oc) in enumerate(kolory):
            text_color = "black" if oc in ["3", "5"] else "white"
            p[i].markdown(f'<div style="{s} background-color:{kolor}; color:{text_color};">Ocena {oc}</div>', unsafe_allow_html=True)
    with c_btn:
        if st.button("Wyloguj"):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 3. TWOJA TABELA
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. LOGIKA DZIAŁÓW (Twoja pętla range 3-14)
    zdane, do_zrobienia = [], []
    for i in range(3, 14, 2):
        try:
            nazwa = str(kol_info[i][1])
            if "Unnamed" in nazwa: continue
            suma_pary = float(dane[i]) + float(dane[i+1])
            if suma_pary >= 4.5: zdane.append(nazwa)
            else: do_zrobienia.append(nazwa)
        except: continue

    # 5. STATUSY (To co było "super")
    st.write("")
    cl, cp = st.columns(2)
    with cl:
        st.info("**✅ Zdane:** " + (", ".join(zdane) if zdane else "Brak"))
        if ocena: st.success(f"### 🎓 Twoja ocena: {ocena}")
        else: st.metric("Suma punktów", f"{suma_total:.1f} pkt")
    with cp:
        st.warning("**🚀 Do poprawy:** " + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if not ocena and suma_total < 40.5:
            st.error(f"📉 Brakuje Ci: {40.5 - suma_total:.1f} pkt")
