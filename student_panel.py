import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. TWOJA MAPA NAZW
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # 2. NAGŁÓWEK (TWÓJ UKŁAD)
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])
    with c_pow:
        pelne_dane = str(wiersz_ucznia.iloc[0, 1])
        imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
        st.subheader(f"👋 {imie}!")

    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 3. TWOJA LOGIKA OSIĄGNIĘĆ (TA CO BYŁA W APP.PY)
    df_temp = wiersz_ucznia.copy()
    nowe_nazwy = []
    for col in df_temp.columns:
        czesci_col = [str(poziom) for poziom in col if "Unnamed" not in str(poziom)]
        if "Działy" in czesci_col: czesci_col.remove("Działy")
        nowe_nazwy.append(" ".join(czesci_col).strip())
    df_temp.columns = nowe_nazwy

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

    zdane_list = list(set(zdane_przetlumaczone))

    # WYŚWIETLANIE OSIĄGNIĘĆ
    if zdane_list:
        st.success(f"🏆 Twoje zdane działy: {', '.join(zdane_list)}")

    # 4. TWOJA TABELA HTML Z REGEXEM
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_tabela = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_tabela.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
