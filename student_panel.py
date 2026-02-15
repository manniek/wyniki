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
    st.markdown("#### Twoje wyniki szczegółowe:")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    # Przygotowanie danych do analizy
    # Zakładamy: kolumna 15 to suma punktów (indeks 15)
    suma_punktow = float(wiersz_ucznia.iloc[0, 15])
    
    # Wybieramy zadania (np. od kolumny indeks 3 do 14 - dostosuj jeśli masz inaczej)
    # Dla przykładu sprawdzamy zadania z poziomów nagłówka
    dane_zadan = wiersz_ucznia.iloc[0, 3:15] 
    
    # Generowanie tabeli HTML
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") # Odstęp

    # 3. LOGIKA PODZIAŁU POD TABELĄ
    col_lewa, col_prawa = st.columns(2)

    # Analiza zdanych działów (wynik >= 4.5)
    zdane = []
    do_zrobienia = []

    for i, (nazwa_kol, wynik) in enumerate(dane_zadan.items()):
        # Wyciągamy nazwę zadania z MultiIndex (zazwyczaj ostatni poziom)
        nazwa = nazwa_kol[-1] if isinstance(nazwa_kol, tuple) else nazwa_kol
        try:
            val = float(wynik) if wynik != "" else 0
            if val >= 4.5:
                zdane.append(nazwa)
            else:
                do_zrobienia.append(nazwa)
        except:
            continue

    # LEWA STRONA: Sukcesy
    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if suma_punktow > 40:
            st.success(f"🏆 **Zdobyte punkty:** {suma_punktow}")

    # PRAWA STRONA: Do poprawy
    with col_prawa:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if suma_punktow <= 40:
            brakujace = 40.5 - suma_punktow
            st.error(f"📉 **Punkty do zdobycia:** {brakujace:.1f}")
