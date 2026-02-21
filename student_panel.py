import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. PRZYGOTOWANIE DANYCH I MAPY
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    # Spłaszczanie nazw kolumn tylko dla widoku panelu
    df_temp = wiersz_ucznia.copy()
    nowe_nazwy = []
    for col in df_temp.columns:
        czesci = [str(p) for p in col if "Unnamed" not in str(p)]
        if "Działy" in czesci: czesci.remove("Działy")
        nowe_nazwy.append(" ".join(czesci).strip())
    df_temp.columns = nowe_nazwy
    
    # 2. NAGŁÓWEK
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])
    with c_pow:
        pelne_dane = str(df_temp.iloc[0, 1])
        imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
        st.subheader(f"👋 {imie}!")

    with c_btn:
        if st.button("Wyloguj"):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 3. ANALIZA ZDANYCH DZIAŁÓW (Twoja logika par kolumn)
    dane = df_temp.fillna(0).iloc[0].values
    kolumny = df_temp.columns
    zdane = []
    do_zrobienia = []

    for i in range(3, 14, 2):
        try:
            raw_name = kolumny[i].split()[0]
            nazwa = mapa_nazw.get(raw_name, kolumny[i])
            suma = float(dane[i]) + float(dane[i+1])
            if suma >= 4.5: zdane.append(nazwa)
            else: do_zrobienia.append(nazwa)
        except: continue

    # 4. WYŚWIETLANIE
    col_l, col_p = st.columns(2)
    with col_l:
        st.info("**✅ Zdane:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
    with col_p:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko!"))

    # 5. TABELA
    st.write("### Twoje wyniki szczegółowe:")
    st.dataframe(df_temp.iloc[:, :-4])
