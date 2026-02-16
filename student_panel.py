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

    st.write("") 

    # 3. SŁOWNIK MAPOWANIA (TŁUMACZ SKRÓTÓW)
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

    # 4. ANALIZA DZIAŁÓW (PARY KOLUMN)
    zdane = []
    do_zrobienia = []
    kolumny = wiersz_ucznia.columns
    
    for i in range(3, 15, 2):
        try:
            raw_name = str(kolumny[i][1]) # Pobieramy np. "funkcje 15(5)"
            
            if "Unnamed" in raw_name: continue
            
            # CZYSZCZENIE NAZWY: 
            # bierzemy tylko to, co jest przed pierwszą spacją
            # "funkcje 15(5)" zamieni się w "funkcje"
            clean_name = raw_name.split(" ")[0]
            
            # Małpowanie (mapowanie) na pełną nazwę
            # Jeśli "clean_name" jest w słowniku, bierzemy opis, jeśli nie - zostawiamy oryginał
            nazwa_pelna = mapa_nazw.get(clean_name, raw_name)

            val1 = wiersz_ucznia.iloc[0, i]
            val2 = wiersz_ucznia.iloc[0, i+1]
            
            f1 = float(val1) if (val1 != "" and val1 is not None) else 0.0
            f2 = float(val2) if (val2 != "" and val2 is not None) else 0.0
            suma_pary = f1 + f2
            
            if suma_pary >= 4.5:
                zdane.append(nazwa_pelna)
            else:
                do_zrobienia.append(nazwa_pelna)
        except:
            continue
    # Suma całkowita (indeks 15)
    suma_total = float(wiersz_ucznia.iloc[0, 15])

    # 5. WYŚWIETLANIE DWÓCH POŁÓW
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

