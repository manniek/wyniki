import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # 1. GÓRNY PASEK
    st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    
    # 2. PRZYGOTOWANIE DANYCH - kluczowe fillna(0)
    # Zamieniamy wszystkie puste pola (NaN) na 0.0, żeby dodawanie działało
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    kol_info = wiersz_clean.columns
    
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    zdane = []
    do_zrobienia = []

    # 3. PĘTLA STARTUJE OD 4 (bo tam masz Log+zb)
    # Jedziemy parzyście: (4,5), (6,7), (8,9), (10,11), (12,13), (14,15)
    for i in range(4, 16, 2):
        try:
            # Nazwa działu z poziomu 1 nagłówka
            raw_name = str(kol_info[i][1])
            if "Unnamed" in raw_name: continue
            
            # Małpowanie
            clean_key = raw_name.split(" ")[0]
            nazwa_finalna = mapa_nazw.get(clean_key, raw_name)

            # Sumowanie (teraz bezpieczne, bo NaN to 0)
            suma = float(dane[i]) + float(dane[i+1])
            
            if suma >= 4.5:
                zdane.append(nazwa_finalna)
            else:
                do_zrobienia.append(nazwa_finalna)
        except:
            continue

    # 4. SUMA TOTAL (z Twojego testu wynika, że jest na samym końcu, indeks 15 lub dalej)
    # Skoro uk_r_l kończy się na 15, suma total jest pewnie na 16
    try:
        suma_total = float(dane[16])
    except:
        suma_total = 0.0

    # 5. WYŚWIETLANIE
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
    with c2:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))

    if suma_total > 0:
        if suma_total >= 40.5:
            st.success(f"🏆 Gratulacje! Masz już {suma_total} pkt.")
        else:
            st.error(f"📉 Brakuje Ci {(40.5 - suma_total):.1f} pkt do zaliczenia (masz {suma_total}).")

    if st.button("Wyloguj"):
        st.session_state.clear()
        st.rerun()
