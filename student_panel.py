import streamlit as st
import re

def show_panel(wiersz_ucznia):
    # Górny pasek z powitaniem i wylogowaniem
    c_pow, c_sp, c_log = st.columns([6, 2, 2])
    c_pow.header(f"Witaj, {wiersz_ucznia.iloc[0, 1]}!")
    
    if c_log.button("Wyloguj", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # Sekcja podsumowania (Metryki)
    try:
        p_val = wiersz_ucznia.iloc[0, 15]
        o_val = wiersz_ucznia.iloc[0, 16]
        
        m1, m2, _ = st.columns([2, 2, 6])
        m1.metric("Twoje punkty", f"{p_val} / 60")
        m2.metric("Ocena końcowa", o_val)
    except:
        st.error("Błąd odczytu danych podsumowujących.")

    st.subheader("Szczegóły Twoich wyników:")
    
    # Renderowanie tabeli z wynikami cząstkowymi
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    try:
        # Wybieramy te same kolumny co u admina (bez ostatnich 4 technicznych)
        widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
        
        # Generowanie HTML
        html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
        # Czyszczenie nagłówków Unnamed
        html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
        
        st.markdown(html_table, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Nie udało się wyświetlić tabeli wyników: {e}")
    st.markdown('</div>', unsafe_allow_html=True)
