import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. TWOJA MAPA (tylko do ładnego wyświetlania pod tabelą)
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # 2. NAGŁÓWEK
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

    # 3. TABELA (NIENARUSZONY MULTIINDEX)
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    # Wyświetlamy wszystko poza ostatnimi 4 kolumnami technicznymi
    widok_tabela = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_tabela.to_html(index=False, classes='tales-table', border=0)
    # Usuwamy tylko techniczne napisy "Unnamed", żeby nagłówek był czysty
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # 4. TWOJE OSIĄGNIĘCIA (Logika sumowania punktów a + b)
    st.write("### 🏆 Twoje wyniki w działach:")
    
    # Zamieniamy braki na 0, żeby matematyka działała
    dane_num = wiersz_ucznia.fillna(0)
    
    zdane = []
    niezdane = []

    # Iterujemy po kolumnach działów (pary kolumn a i b)
    # Zakładając, że działy zaczynają się od kolumny 3
    for i in range(3, 27, 2):
        try:
            # Pobieramy nazwę działu z drugiego poziomu nagłówka MultiIndex
            raw_name = wiersz_ucznia.columns[i][1]
            nazwa_ladna = mapa_nazw.get(raw_name, raw_name)
            
            # Sumujemy wartości z pary kolumn
            suma = float(dane_num.iloc[0, i]) + float(dane_num.iloc[0, i+1])
            
            if suma >= 4.5:
                zdane.append(f"{nazwa_ladna} ({suma} pkt)")
            else:
                niezdane.append(f"{nazwa_ladna} (brak zaliczenia: {suma}/10 pkt)")
        except:
            continue

    col1, col2 = st.columns(2)
    with col1:
        st.success("**✅ ZALICZONE:**")
        if zdane:
            for z in zdane: st.write(f"✔️ {z}")
        else: st.write("Jeszcze nic.")

    with col2:
        st.warning("**🚀 DO ZDOBYCIA/POPRAWY:**")
        if niezdane:
            for n in niezdane: st.write(f"❌ {n}")
        else: st.write("Wszystko zaliczone!")

    # 5. PODSUMOWANIE OGÓLNE (Pkt / Ocena)
    st.write("---")
    try:
        pkt_suma = wiersz_ucznia.iloc[0, -4]
        ocena = wiersz_ucznia.iloc[0, -3]
        st.info(f"📊 **Suma punktów:** {pkt_suma} | **Aktualna ocena:** {ocena}")
    except:
        pass
