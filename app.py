import streamlit as st
import pandas as pd
import hashlib
import glob
import styles
import admin_panel
import student_panel

st.set_page_config(page_title="RB oceny", layout="wide")
styles.apply_styles()

def wczytaj_dane():
    pliki = glob.glob("*.xlsx")
    if not pliki: return None, None
    try:
        df_w = pd.read_excel(pliki[0], sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(pliki[0], sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except: return None, None

if "zalogowany" not in st.session_state:
    st.session_state.zalogowany = False

df_w, df_h = wczytaj_dane()

if not st.session_state.zalogowany:
    st.title("🛡️ Logowanie")
    login = st.text_input("Numer indeksu / Login")
    haslo = st.text_input("Hasło", type="password")
    
    if st.button("Zaloguj", use_container_width=True):
        user_row = df_h[df_h.iloc[:, 0].astype(str) == login]
        if not user_row.empty:
            poprawne_haslo = str(user_row.iloc[0, 1]).strip()
            hash_wpisany = hashlib.sha256(haslo.encode()).hexdigest()
            if hash_wpisany == poprawne_haslo:
                idx = df_w[df_w.iloc[:, 0].astype(str) == login].index
                if not idx.empty:
                    st.session_state.zalogowany = True
                    st.session_state.dane = df_w.iloc[[idx[0]]]
                    st.rerun()
            else: st.error("Błędne hasło.")
        else: st.error("Nie znaleziono użytkownika.")
else:
    student_panel.show_panel(st.session_state.dane)
