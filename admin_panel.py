import streamlit as st
import pandas as pd
import os
import re

def show_panel(df_w, wczytaj_dane_func):
    st.header("👨‍🏫 Panel Nauczyciela")
    tab1, tab2 = st.tabs(["📊 Podgląd Wyników", "📤 Zarządzanie Bazą"])
    
    with tab2:
        plik = st.file_uploader("Wgraj nową bazę .xlsx", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Baza zaktualizowana!")
            st.rerun()
    
    with tab1:
        if df_w is not None:
            c_meta, c_spacer, c_btn = st.columns([3, 5, 2])
            c_meta.metric("Liczba rekordów", len(df_w))
            
            if c_btn.button("Wyloguj się", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
            
            szukaj = st.text_input("Szukaj studenta:")
            widok = df_w.iloc[:, :-4].copy().fillna("")
            
            if szukaj:
                widok = widok[widok.iloc[:, 1].astype(str).str.contains(szukaj, case=False)]
            
            html_table = widok.to_html(index=False, classes='tales-table', border=0)
            html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
            st.markdown(f'<div class="table-container">{html_table}</div>', unsafe_allow_html=True)
        else:
            st.info("Baza danych jest pusta.")