import streamlit as st
import re

def show_panel(wiersz_ucznia):
    # GÓRNY PASEK
    c_pow, c_spacer, c_btn = st.columns([6, 2, 2])
    with c_pow:
        st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.write("---")

    # TABELA WYNIKÓW
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") 

    # TWOJA LOGIKA: Pary kolumn od 4 do 15 (indeksy 3 do 14)
    nazwy_dzialow = ["Log+zb", "Ciągi", "F. wykładnicza", "Trygonometria", "Geometria", "Inne"]
    zdane = []
    do_zrobienia = []
    
    dzial_idx = 0
    # i to indeksy kolumn: 3, 5, 7, 9, 11, 13
    for i in range(3, 15, 2):
        if dzial_idx < len(nazwy_dzialow):
            try:
                val1 = wiersz_ucznia.iloc[0, i]
                val2 = wiersz_ucznia.iloc[0, i+1]
                
                # Konwersja na float, jeśli puste to 0
                f1 = float(val1) if (val1 != "" and val1 is not None) else 0.0
                f2 = float(val2) if (val2 != "" and val2 is not None) else 0.0
                
                suma_pary = f1 + f2
                nazwa = nazwy_dzialow[dzial_idx]
                
                if suma_pary >= 4.5:
                    zdane.append(nazwa)
                else:
                    do_zrobienia.append(nazwa)
            except:
                pass
            dzial_idx += 1

    # Suma całkowita z kolumny o indeksie 15
    suma_total = float(wiersz_ucznia.iloc[0, 15])

    # PODSUMOWANIE W DWÓCH KOLUMNACH
    col_lewa, col_prawa = st.columns(2)

    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if suma_total > 40:
            st.success(f"🏆 **Zdobyte punkty:** {suma_total}")

    with col_prawa:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if suma_total <= 40:
            brakujace = 40.5 - suma_total
            st.error(f"📉 **Punkty do zdobycia:** {brakujace:.1f}")
