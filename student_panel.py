import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. POBIERANIE DANYCH (Logika z Twojego mobile_panel.py)
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    kol_info = wiersz_clean.columns

    pelne_dane = str(dane[1])
    imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
    suma_total = float(dane[15])
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""

    # 2. NAGŁÓWEK (Układ na komputer)
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])
    
    with c_pow:
        st.subheader(f"👋 {imie}!")

    with c_progi:
        # Twoja drabinka ocen (kolory standardowe, układ poziomy)
        p = st.columns(6)
        s_w = 'display:block; color:white; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        s_b = 'display:block; color:black; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        
        p[0].markdown(f'<div style="{s_w} background-color:#FF0000;">2<br>(0-40]</div>', unsafe_allow_html=True)
        p[1].markdown(f'<div style="{s_b} background-color:#92D050;">3<br>(40-52]</div>', unsafe_allow_html=True)
        p[2].markdown(f'<div style="{s_w} background-color:#00B050;">3.5<br>(52-64]</div>', unsafe_allow_html=True)
        p[3].markdown(f'<div style="{s_w} background-color:#00B0F0;">4<br>(64-76]</div>', unsafe_allow_html=True)
        p[4].markdown(f'<div style="{s_w} background-color:#0070C0;">4.5<br>(76-88]</div>', unsafe_allow_html=True)
        p[5].markdown(f'<div style="{s_b} background-color:#FFC000;">5<br>(88-100]</div>', unsafe_allow_html=True)

    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 3. TABELA (Twoja oryginalna metoda)
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_tabela = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_tabela.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 4. LOGIKA OSIĄGNIĘĆ (Z mobile_panel.py)
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    zdane = []
    do_zrobienia = []

    for i in range(3, 14, 2):
        try:
            raw_name = str(kol_info[i][1])
            if "Unnamed" in raw_name: continue
            clean_key = raw_name.split(" ")[0]
            nazwa_finalna = mapa_nazw.get(clean_key, raw_name)
            suma_pary = float(dane[i]) + float(dane[i+1])
            if suma_pary >= 4.5:
                zdane.append(nazwa_finalna)
            else:
                do_zrobienia.append(nazwa_finalna)
        except: continue

    # 5. WYNIKI POD TABELĄ (Dwie kolumny, logika z mobile)
    st.write("")
    col_l, col_p = st.columns(2)

    with col_l:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if ocena:
            st.success(f"### 🎓 Twoja ocena: {ocena}")
        else:
            st.metric("Suma punktów", f"{suma_total:.1f} pkt")

    with col_p:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if not ocena:
            if suma_total < 40.5:
                brak = 40.5 - suma_total
                st.error(f"📉 Brakuje Ci: {brak:.1f} pkt do zaliczenia")
            else:
                st.success("Masz punkty na zaliczenie!")
