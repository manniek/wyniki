import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # --- 1. TWOJA MAPA NAZW (Z TWOJEGO KODU) ---
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # --- 2. NAGŁÓWEK (TWÓJ UKŁAD 2.5, 5.5, 2) ---
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])
    with c_pow:
        pelne_dane = str(wiersz_ucznia.iloc[0, 1])
        czesci = pelne_dane.split()
        imie = czesci[1] if len(czesci) > 1 else pelne_dane
        st.subheader(f"👋 {imie}!")

    with c_progi:
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        s_w = 'display:block; color:white; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        s_b = 'display:block; color:black; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        p1.markdown(f'<div style="{s_w} background-color:#FF0000;">ocena 2:<br>(0-40]</div>', unsafe_allow_html=True)
        p2.markdown(f'<div style="{s_b} background-color:#92D050;">ocena 3:<br>(40-52]</div>', unsafe_allow_html=True)
        p3.markdown(f'<div style="{s_w} background-color:#00B050;">ocena 3.5:<br>(52-64]</div>', unsafe_allow_html=True)
        p4.markdown(f'<div style="{s_w} background-color:#00B0F0;">ocena 4:<br>(64-76]</div>', unsafe_allow_html=True)
        p5.markdown(f'<div style="{s_w} background-color:#0070C0;">ocena 4.5:<br>(76-88]</div>', unsafe_allow_html=True)
        p6.markdown(f'<div style="{s_b} background-color:#FFC000;">ocena 5:<br>(88-100]</div>', unsafe_allow_html=True)

    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # --- 3. TWOJA LOGIKA PRZETWARZANIA (DOKŁADNIE TAK JAK MIAŁEŚ W APP.PY) ---
    df_temp = wiersz_ucznia.copy()
    
    # Spłaszczanie nazw kolumn (Twoja pętla)
    nowe_nazwy = []
    for col in df_temp.columns:
        czesci_col = [str(poziom) for poziom in col if "Unnamed" not in str(poziom)]
        if "Działy" in czesci_col: czesci_col.remove("Działy")
        nowe_nazwy.append(" ".join(czesci_col).strip())
    df_temp.columns = nowe_nazwy

    # Wykrywanie zdanych (Twoja logika z "zal", "1", "x")
    wiersz_danych = df_temp.iloc[0]
    zdane_przetlumaczone = []

    for col_name in df_temp.columns:
        wartosc = str(wiersz_danych[col_name]).lower()
        if wartosc in ["zal", "1", "1.0", "x"]:
            znaleziono = False
            for klucz, tlumaczenie in mapa_nazw.items():
                if klucz.lower() in col_name.lower():
                    zdane_przetlumaczone.append(tlumaczenie)
                    znaleziono = True
                    break
            if not znaleziono and col_name not in ["Lp.", "NAZWISKO I IMIĘ", "Pkt", "Ocena"]:
                zdane_przetlumaczone.append(col_name)

    # Usuwanie duplikatów (Twoje set)
    zdane_list = list(set(zdane_przetlumaczone))

    # --- 4. WYŚWIETLANIE OSIĄGNIĘĆ (TWOJE SUCCESS) ---
    if zdane_list:
        st.success(f"🏆 Twoje zdane działy: {', '.join(zdane_list)}")
    else:
        st.info("Brak odnotowanych zaliczeń działów.")

    st.write("---")

    # --- 5. TWOJA TABELA HTML (Z REGEXEM) ---
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_tabela = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_tabela.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
