import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # Nagłówek w Twoim stylu: [Powitanie, Drabinka, Przycisk]
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])

    with c_pow:
        pelne_dane = str(wiersz_ucznia.iloc[0, 1])
        czesci = pelne_dane.split()
        # Wyciągamy imię (druga część po nazwisku)
        imie = czesci[1] if len(czesci) > 1 else pelne_dane
        st.subheader(f"👋 {imie}!")

    with c_progi:
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        # Twoje style kolorystyczne
        s_w = 'display:block; color:white; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        s_b = 'display:block; color:black; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'

        p1.markdown(f'<div style="{s_w} background-color:#FF0000;">ocena 2:<br>(0-40]</div>', unsafe_allow_html=True)
        p2.markdown(f'<div style="{s_b} background-color:#92D050;">ocena 3:<br>(40-52]</div>', unsafe_allow_html=True)
        p3.markdown(f'<div style="{s_w} background-color:#00B050;">ocena 3.5:<br>(52-64]</div>', unsafe_allow_html=True)
        p4.markdown(f'<div style="{s_w} background-color:#00B0F0;">ocena 4:<br>(64-76]</div>', unsafe_allow_html=True)
        p5.markdown(f'<div style="{s_w} background-color:#0070C0;">ocena 4.5:<br>(76-88]</div>', unsafe_allow_html=True)
        p6.markdown(f'<div style="{s_b} background-color:#FFC000;">ocena 5:<br>(88-100]</div>', unsafe_allow_html=True)

    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # TWOJA ORYGINALNA TABELA WYNIKÓW
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    # Kopia wiersza do wyświetlenia (bez ostatnich 4 kolumn)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    
    # Twoja konwersja do HTML
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    
    # Twój regex do usuwania Unnamed z nagłówków
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
