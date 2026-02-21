import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # 1. MAPA NAZW (Tłumaczymy skróty z Excela na ładne nazwy)
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # Nagłówek w Twoim stylu: [Powitanie, Drabinka, Przycisk]
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

    # TWOJA ORYGINALNA TABELA WYNIKÓW
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("---")

    # 2. LOGIKA OSIĄGNIĘĆ (POD TABELĄ)
    st.write("### 🏆 Twoje osiągnięcia:")
    
    # Pobieramy dane z wiersza (zamieniamy na float, braki na 0)
    dane_numeryczne = wiersz_ucznia.fillna(0)
    
    zdane = []
    do_zrobienia = []

    # Pętla po kolumnach działów (od 3 kolumny, skok co 2 - sprawdzamy pary a i b)
    # Zakładam, że działy zaczynają się od kolumny 3 (indeks 3)
    for i in range(3, 27, 2):
        try:
            # Nazwa działu z pierwszego poziomu nagłówka
            raw_name = wiersz_ucznia.columns[i][1] 
            nazwa_ladna = mapa_nazw.get(raw_name, raw_name)
            
            # Sumujemy punkty z kolumny 'a' i 'b' dla danego działu
            pkt_a = float(dane_numeryczne.iloc[0, i])
            pkt_b = float(dane_numeryczne.iloc[0, i+1])
            suma = pkt_a + pkt_b
            
            if suma >= 4.5:
                zdane.append(nazwa_ladna)
            else:
                do_zrobienia.append(nazwa_ladna)
        except:
            continue

    # Wyświetlanie w dwóch kolumnach pod tabelą
    col_zdane, col_do = st.columns(2)
    
    with col_zdane:
        st.success("**✅ Zdane działy:**")
        if zdane:
            for z in zdane:
                st.write(f"✔️ {z}")
        else:
            st.write("Brak zdanych działów.")

    with col_do:
        st.warning("**🚀 Do poprawy/zrobienia:**")
        if do_zrobienia:
            for d in do_zrobienia:
                st.write(f"❌ {d}")
        else:
            st.write("Gratulacje! Wszystko zdane!")
