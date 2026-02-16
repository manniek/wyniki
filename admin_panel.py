import streamlit as st
import re

def show_panel(df_w):
    st.header("👨‍🏫 Panel Nauczyciela")
    
    if df_w is not None:
        # GÓRNY PASEK
        c_meta, c_spacer, c_btn = st.columns([3, 5, 2])
        c_meta.metric("Liczba rekordów", len(df_w))
        
        if c_btn.button("Wyloguj się", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # WYSZUKIWARKA
        szukaj = st.text_input("Szukaj studenta (Nazwisko):")
        
        # Przygotowanie widoku (ucinamy techniczne kolumny na końcu)
        widok = df_w.iloc[:, :-4].copy().fillna("")
        
        if szukaj:
            # Zakładamy, że nazwisko jest w kolumnie o indeksie 1
            widok = widok[widok.iloc[:, 1].astype(str).str.contains(szukaj, case=False)]
        
        # TABELA HTML
        st.markdown('<div class="table-container">', unsafe_allow_html=True)
        html_table = widok.to_html(index=False, classes='tales-table', border=0)
        html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
        st.markdown(html_table, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.error("Nie znaleziono żadnego pliku .xlsx na GitHubie!")
