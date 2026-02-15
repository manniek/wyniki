import streamlit as st
import re

def show_panel(wiersz_ucznia):
    # 1. GÓRNY PASEK: Witaj (lewo) i Wyloguj (prawo) w jednej linii
    c_pow, c_spacer, c_log = st.columns([6, 2, 2])
    
    with c_pow:
        st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    
    with c_log:
        if st.button("Wyloguj", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.write("---") # Subtelna linia oddzielająca

    # 2. TABELA Z WYNIKAMI
    st.markdown("#### Twoje wyniki szczegółowe:")
    
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    try:
        # Wybieramy dane (bez kolumn technicznych na końcu)
        widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
        
        # Generowanie HTML bez indeksu
        html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
        
        # Usuwanie technicznych nagłówków "Unnamed"
        html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
        
        st.markdown(html_table, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Błąd podczas ładowania tabeli: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Informacja stopki (opcjonalnie)
    st.caption("Jeśli widzisz błąd w swoich punktach, skontaktuj się bezpośrednio z prowadzącym.")
