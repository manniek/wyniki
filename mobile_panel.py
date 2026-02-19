import streamlit as st
import pandas as pd

def show_mobile_panel(wiersz_ucznia):
    # 1. POBIERANIE DANYCH
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    
    pelne_dane = str(dane[1])
    imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
    
    suma_total = float(dane[15])
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""

    # 2. NAGŁÓWEK MOBILNY (Usunięto color:white - Streamlit sam dobierze kolor do tła)
    st.markdown(f'<h2 style="text-align:center;">👋 Witaj, {imie}!</h2>', unsafe_allow_html=True)
    
    # 3. DRABINKA OCEN
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
            st.markdown(f'<div style="{styles[stopien]} padding:12px; border-radius:10px; margin-bottom:8px; text-align:center; font-weight:bold;">Ocena {stopien}: {punkty} pkt</div>', unsafe_allow_html=True)

    st.divider()

    # 4. STATUS ZALICZENIA (Komponenty systemowe - najlepiej czytelne na telefonie)
    if ocena:
        st.success(f"### 🎓 Twoja ocena: {ocena}")
    else:
        # Używamy st.metric dla lepszej widoczności punktów
        st.metric("Twoje punkty", f"{suma_total:.1f} pkt")
        if suma_total < 40.5:
            st.error(f"📉 Brakuje Ci: {40.5 - suma_total:.1f} pkt")

    # 5. LISTA DO ZROBIENIA
    st.subheader("🚀 Do zrobienia:")
    # Tutaj warto pobrać realne dane z Twojego Excela, jeśli masz tam kolumny z zadaniami
    for dzial in ["Logika", "Ciągi"]: 
        st.info(f"📍 **{dzial}**")

    # 6. WYLOGUJ NA DOLE
    st.write("")
    if st.button("🔴 WYLOGUJ", use_container_width=True):
        st.session_state.clear()
        st.rerun()
