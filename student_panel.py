import streamlit as st
import re

def show_panel(wiersz_ucznia):
    # 1. GÓRNY PASEK
    c_pow, c_spacer, c_btn = st.columns([6, 2, 2])
    with c_pow:
        st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.write("---")

    # 2. TABELA WYNIKÓW
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. SŁOWNIK MAPOWANIA
    mapa_nazw = {
        "Log+zb": "logika i zbiory",
        "ciągi": "ciągi",
        "funkcje": "funkcje",
        "poch.": "pochodna",
        "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych",
        "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona",
        "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna",
        "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # 4. ANALIZA DZIAŁÓW - LOGIKA PĘTLI
    zdane = []
    do_zrobienia = []
    
    # Wyciągamy dane wiersza jako prostą listę, żeby uniknąć problemów z MultiIndexem
    dane_wiersza = wiersz_ucznia.iloc[0].values
    kolumny = wiersz_ucznia.columns

    # i to indeksy 3, 5, 7, 9, 11, 13
    for i in range(3, 15, 2):
        try:
            # Pobieramy nazwę z nagłówka (poziom 1)
            raw_name = str(kolumny[i][1])
            if "Unnamed" in raw_name:
                continue

            # Małpowanie: tniemy po spacji i szukamy w słowniku
            clean_key = raw_name.split(" ")[0]
            nazwa_finalna = mapa_nazw.get(clean_key, raw_name)

            # Pobieramy wartości punktowe
            val1 = dane_wiersza[i]
            val2 = dane_wiersza[i+1]

            # Konwersja na float - bezpieczna
            def to_f(x):
                try:
                    return float(x) if (x != "" and x is not None) else 0.0
                except:
                    return 0.0

            suma_pary = to_f(val1) + to_f(val2)

            # WARUNEK ZDANIA
            if suma_pary >= 4.5:
                zdane.append(nazwa_finalna)
            else:
                do_zrobienia.append(nazwa_finalna)
                
        except Exception as e:
            continue

    # Pobieramy sumę całkowitą z kolumny 15
    try:
        suma_total = float(dane_wiersza[15])
    except:
        suma_total = 0.0

    # 5. WYŚWIETLANIE W DWÓCH POŁOWACH
    st.write("") 
    col_lewa, col_prawa = st.columns(2)

    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if suma_total > 40:
            st.success(f"🏆 **Zdobyte punkty:** {suma_total}")

    with col_prawa:
        st.warning("**🚀 Do robienia: działy**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if suma_total <= 40:
            brakujace = 40.5 - suma_total
            st.error(f"📉 **Punkty do zdobycia:** {brakujace:.1f}")
