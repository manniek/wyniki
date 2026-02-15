import streamlit as st
import pandas as pd
import os
import hashlib
import re

st.set_page_config(page_title="System TALES", layout="wide")

# --- 1. FUNKCJE ---

def check_admin_password(input_password):
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane(sciezka):
    try:
        df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except:
        return None, None

# --- 2. SESJA ---

if "zalogowany" not in st.session_state:
    st.session_state.zalogowany = False
    st.session_state.rola = None
    st.session_state.dane = None

# --- 3. LOGOWANIE ---

if not st.session_state.zalogowany:
    st.title("🛡️ System TALES")
    with st.form("form_logowania"):
        uzytkownik = st.text_input("Nazwisko lub Identyfikator:")
        haslo_wpisane = st.text_input("Hasło:", type="password")
        przycisk = st.form_submit_button("Zaloguj się", use_container_width=True)

    if przycisk:
        login_clean = uzytkownik.strip().lower()
        pass_clean = haslo_wpisane.strip()
        if login_clean == "admin":
            if check_admin_password(pass_clean):
                st.session_state.zalogowany = True
                st.session_state.rola = "admin"
                st.rerun()
            else:
                st.error("Błędne hasło administratora.")
        elif os.path.exists("baza.xlsx"):
            df_w, df_h = wczytaj_dane("baza.xlsx")
            if df_w is not None:
                nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                if login_clean in nazwiska:
                    idx = nazwiska.index(login_clean)
                    wiersz = df_w.iloc[[idx]]
                    lp = wiersz.iloc[0, 0]
                    poprawne_haslo = str(df_h[df_h["Lp"] == lp]["Haslo"].values[0]).strip()
                    if pass_clean == poprawne_haslo:
                        st.session_state.zalogowany = True
                        st.session_state.rola = "uczen"
                        st.session_state.dane = wiersz
                        st.rerun()
                    else:
                        st.error("Błędne hasło.")
                else:
                    st.error("Nie znaleziono nazwiska.")

# --- 4. PO ZALOGOWANIU ---

else:
    with st.sidebar:
        st.write(f"Zalogowano jako: **{st.session_state.rola}**")
        if st.button("Wyloguj"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    if st.session_state.rola == "admin":
        st.header("👨‍🏫 Panel Nauczyciela")
        tab1, tab2 = st.tabs(["📊 Podgląd Wyników", "📤 Zarządzanie Bazą"])
        
        with tab2:
            plik = st.file_uploader("Wgraj nową bazę .xlsx", type="xlsx")
            if plik:
                with open("baza.xlsx", "wb") as f:
                    f.write(plik.getbuffer())
                st.success("Baza zaktualizowana!")
                st.balloons()
        
        with tab1:
            if os.path.exists("baza.xlsx"):
                df_w, _ = wczytaj_dane("baza.xlsx")
                if df_w is not None:
                    # 1. Tniemy kolumny i czyścimy NaN
                    widok = df_w.iloc[:, :-4].copy()
                    widok = widok.fillna("")
                    
                    st.metric("Liczba rekordów", len(df_w))
                    szukaj = st.text_input("Szukaj studenta:")
                    
                    if szukaj:
                        widok = widok[widok.iloc[:, 1].astype(str).str.contains(szukaj, case=False)]
                    
                    # 2. Generowanie HTML - KLUCZ: index=False usuwa tę pierwszą kolumnę z numerami
                    html_table = widok.to_html(classes='tales-table', border=0, na_rep="", index=False)
                    
                    # 3. Usuwamy techniczne napisy Unnamed
                    html_table =
