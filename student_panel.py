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
    
    st.write("### Diagnostyka danych:")
    
    # 1. Sprawdzamy co dokładnie widzi Python
    dane_wiersza = wiersz_ucznia.iloc[0]
    
    # 2. Wypisujemy każdą kolumnę z jej indeksem
    for i in range(len(dane_wiersza)):
        st.write(f"Indeks **{i}** | Wartość: `{dane_wiersza[i]}`")

    # 3. Twoja pętla (uproszczona do testu)
    zdane = []
    do_zrobienia = []
    nazwy_dzialow = ["Log+zb", "Ciągi", "F. wykładnicza", "Trygonometria", "Geometria", "Inne"]
    
    # Tymczasowo wypisujemy proces sumowania
    st.write("### Proces sprawdzania działów:")
    dzial_idx = 0
    for i in range(3, 15, 2):
        val1 = dane_wiersza[i]
        val2 = dane_wiersza[i+1]
        suma = (float(val1) if val1 and str(val1).replace('.','').isdigit() else 0) + \
               (float(val2) if val2 and str(val2).replace('.','').isdigit() else 0)
        
        st.write(f"Para {i}-{i+1} ({nazwy_dzialow[dzial_idx]}): {val1} + {val2} = {suma}")
        
        if suma >= 4.5:
            zdane.append(nazwy_dzialow[dzial_idx])
        else:
            do_zrobienia.append(nazwy_dzialow[dzial_idx])
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


