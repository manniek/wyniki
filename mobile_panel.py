import streamlit as st
import pandas as pd

def show_mobile_panel(wiersz_ucznia):
    # 1. POBIERANIE DANYCH
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    
    # Imię (Twoja nowa logika)
    pelne_dane = str(dane[1])
    imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
    
    # Ocena i suma
    suma_total = float(dane[15])
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""

    # 2. NAGŁÓWEK MOBILNY
    st.markdown(f'<h2 style="text-align:center; color:white;">👋 Witaj, {imie}!</h2>', unsafe_allow_html=True)
    
    # 3. DRABINKA OCEN (Pionowa, szerokie kafle)
    with st.expander("📊 Sprawdź progi punktowe"):
        styles = {
            "2": "background-color:#FF0000; color:white;",
            "3": "background-color:#92D050; color:black;",
            "3.5": "background-color:#00B050; color:white;",
            "4": "background-color:#00B0F0; color:white;",
            "4.5": "background-color:#0070C0; color:white;",
            "5": "background-color:#FFC000; color:black;"
        }
        progi = [("2", "0-40"), ("3", "40-52"), ("3.5", "52-64"), ("4", "64-76"), ("4.5", "76-88"), ("5", "88-100")]
        for stopien, punkty in progi:
            st.markdown(f'<div style="{styles[stopien]} padding:10px; border-radius:10px; margin-bottom:5px; text-align:center;"><b>Ocena {stopien}</b>: {punkty} pkt</div>', unsafe_allow_html=True)

    st.divider()

    # 4. STATUS ZALICZENIA (Wielka karta)
    if ocena:
        st.success(f"### 🎓 Twoja ocena: {ocena}")
    else:
        st.info(f"### 📊 Punkty: {suma_total:.1f}")
        if suma_total < 40.5:
            st.error(f"📉 Brakuje Ci: {40.5 - suma_total:.1f} pkt")

    # 5. LISTA DO ZROBIENIA (Duże checkboxy/karty)
    st.subheader("🚀 Do zrobienia:")
    # Tutaj wstaw swoją pętlę generującą listę 'do_zrobienia'
    for dzial in ["Logika", "Ciągi"]: # Przykład, użyj swojej listy
        st.warning(f"📍 {dzial}")

    # 6. WYLOGUJ NA DOLE (Wielki przycisk)
    st.write("")
    if st.button("🔴 WYLOGUJ", use_container_width=True):
        st.session_state.clear()
        st.rerun()