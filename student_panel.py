import streamlit as st
import re
import pandas as pd

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
    st.markdown("#### Twoje wyniki szczegółowe:")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") 

    # 3. POPRAWIONA ANALIZA DZIAŁÓW
    suma_total = float(wiersz_ucznia.iloc[0, 15])
    
    zdane = []
    do_zrobienia = []

    # Definiujemy nazwy działów, które nas interesują
    # Możesz je tu wpisać ręcznie, żeby mieć 100% pewności
    lista_dzialow = ["log+zb", "ciągi", "f.wykładnicza", "trygonometria"] # dopisz resztę nazw z Excela

    # Iterujemy po kolumnach, szukając wyników dla tych działów
    for col_name in wiersz_ucznia.columns:
        # Sprawdzamy czy nazwa działu (poziom 1) jest na liście i czy to kolumna "wynikowa"
        # Często w MultiIndex kolumna sumaryczna ma nazwę zadania pustą lub taką samą jak dział
        if isinstance(col_name, tuple):
            dzial_nazwa = col_name[1] 
            zadanie_nazwa = col_name[2]
            
            # Logika: Jeśli kolumna nazywa się tak samo jak dział lub zawiera "Suma" / jest pusta
            if dzial_nazwa in lista_dzialow and ("Unnamed" in str(zadanie_nazwa) or zadanie_nazwa == ""):
                idx = wiersz_ucznia.columns.get_loc(col_name)
                wartosc = wiersz_ucznia.iloc[0, idx]
                
                try:
                    wynik = float(wartosc) if wartosc != "" else 0.0
                    if wynik >= 4.5:
                        if dzial_nazwa not in zdane: zdane.append(dzial_nazwa)
                    else:
                        if dzial_nazwa not in do_zrobienia: do_zrobienia.append(dzial_nazwa)
                except:
                    continue

    # 4. WYŚWIETLANIE
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
