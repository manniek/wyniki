import streamlit as st
import pandas as pd
import os

# Konfiguracja strony
st.set_page_config(page_title="System TALES", layout="centered")

# Funkcja wczytująca
def wczytaj_dane(sciezka):
    # Wczytujemy Arkusz1 (wyniki) z nagłówkiem wielopoziomowym
    df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
    # Wczytujemy Arkusz2 (hasła)
    df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
    df_h.columns = ["Lp", "Haslo"]
    return df_w, df_h

# Menu boczne
st.sidebar.title("Nawigacja")
tryb = st.sidebar.radio("Wybierz panel:", ["Uczeń", "Nauczyciel"])

if tryb == "Nauczyciel":
    st.header("🔐 Panel Nauczyciela")
    haslo_admina = st.text_input("Hasło dostępowe:", type="password")
    
    if haslo_admina == "profesor123":
        st.success("Zalogowano!")
        plik = st.file_uploader("Wgraj plik oceny.xlsx", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Plik wgrany pomyślnie! Odśwież stronę.")
            st.balloons()
    elif haslo_admina != "":
        st.error("Błędne hasło admina")

else:
    st.header("🎓 Wyniki Studentów")
    if os.path.exists("baza.xlsx"):
        df_w, df_h = wczytaj_dane("baza.xlsx")
        lista = df_w.iloc[:, 1].dropna().unique().tolist()
        
        wybrany = st.selectbox("Wybierz swoje nazwisko:", ["---"] + lista)
        kod = st.text_input("Wpisz swoje hasło:", type="password")
        
        if st.button("Sprawdź"):
            wiersz = df_w[df_w.iloc[:, 1] == wybrany]
            lp_ucznia = wiersz.iloc[0, 0]
            prawdziwe_haslo = str(df_h[df_h["Lp"] == lp_ucznia]["Haslo"].values[0])
            
            if kod == prawdziwe_haslo:
                st.success(f"Witaj {wybrany}!")
                st.metric("Twoja Ocena", f"{wiersz.iloc[0, 16]}")
                st.write(f"Suma punktów: {wiersz.iloc[0, 15]}")
            else:
                st.error("Hasło nieprawidłowe.")
    else:
        st.info("Baza ocen jest pusta. Nauczyciel musi wgrać plik w panelu obok.")