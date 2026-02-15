import streamlit as st
import pandas as pd
import os
import hashlib
import styles
import admin_panel
import student_panel

st.set_page_config(page_title="System TALES", layout="wide")
styles.apply_styles()

# --- FUNKCJE POMOCNICZE ---
def check_admin_password(input_password):
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane():
    if not os.path.exists("baza.xlsx"): return None, None
    try:
        df_w = pd.read_excel("baza.xlsx", sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel("baza.xlsx", sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except: return None, None

# --- LOGIKA SESJI ---
if "zalogowany" not in st.session_state:
    st.session_state.update({"zalogowany": False, "rola": None, "dane": None})

# --- EKRAN LOGOWANIA ---
if not st.session_state.zalogowany:
    st.title("🛡️ System TALES")
    with st.form("form_logowania"):
        uzytkownik = st.text_input("Nazwisko lub Identyfikator:")
        haslo_wpisane = st.text_input("Hasło:", type="password")
        if st.form_submit_button("Zaloguj się", use_container_width=True):
            login_clean = uzytkownik.strip().lower()
            pass_clean = haslo_wpisane.strip()
            
            if login_clean == "admin" and check_admin_password(pass_clean):
                st.session_state.update({"zalogowany": True, "rola": "admin"})
                st.rerun()
            else:
                df_w, df_h = wczytaj_dane()
                if df_w is not None:
                    nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                    if login_clean in nazwiska:
                        idx = nazwiska.index(login_clean)
                        lp = df_w.iloc[idx, 0]
                        poprawne_haslo = str(df_h[df_h["Lp"] == lp]["Haslo"].values[0]).strip()
                        if pass_clean == poprawne_haslo:
                            st.session_state.update({"zalogowany": True, "rola": "uczen", "dane": df_w.iloc[[idx]]})
                            st.rerun()
                st.error("Błędne dane logowania.")

# --- PRZEKIEROWANIE DO PANELI ---
else:
    if st.session_state.rola == "admin":
        df_w, _ = wczytaj_dane()
        admin_panel.show_panel(df_w, wczytaj_dane)
    else:
        student_panel.show_panel(st.session_state.dane)