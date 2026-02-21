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
        # Nagłówek 3-poziomowy dla wyników, brak dla haseł
        df_w = pd.read_excel(pliki[0], sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(pliki[0], sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except: return None, None

if "zalogowany" not in st.session_state:
    st.session_state.update({"zalogowany": False, "rola": None, "dane": None})

df_w, df_h = wczytaj_dane()

if not st.session_state.zalogowany:
    st.title("🛡️ Logowanie")
    uzytkownik = st.text_input("Login (Lp / Nazwisko):")
    haslo_wpisane = st.text_input("Hasło:", type="password")
    
    if st.button("Zaloguj się", use_container_width=True):
        login_s = uzytkownik.strip().lower()
        
        # LOGIKA DLA ADMINA
        if login_s == "admin" and hashlib.sha256(haslo_wpisane.encode()).hexdigest() == "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b":
            st.session_state.update({"zalogowany": True, "rola": "admin"})
            st.rerun()
            
        # LOGIKA DLA STUDENTA (Na podstawie Twojej sprawnej metody)
        elif df_h is not None:
            # Szukamy loginu w 1. kolumnie Arkusza haseł
            user_row = df_h[df_h.iloc[:, 0].astype(str).str.strip() == uzytkownik.strip()]
            if not user_row.empty:
                poprawne_h = str(user_row.iloc[0, 1]).strip()
                if hashlib.sha256(haslo_wpisane.encode()).hexdigest() == poprawne_h:
                    # Znajdujemy ten sam login w Arkuszu wyników
                    idx = df_w[df_w.iloc[:, 0].astype(str).str.strip() == uzytkownik.strip()].index
                    if not idx.empty:
                        st.session_state.update({"zalogowany": True, "rola": "uczen", "dane": df_w.iloc[[idx[0]]]})
                        st.rerun()
            st.error("Błędne dane logowania.")
else:
    if st.session_state.rola == "admin":
        admin_panel.show_panel(df_w)
    else:
        student_panel.show_panel(st.session_state.dane)
