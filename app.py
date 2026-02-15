import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="wide")

# --- 1. FUNKCJE ---

def check_admin_password(input_password):
    # Hash dla hasła: profesor
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane(sciezka):
    try:
        # Wczytujemy Arkusz1 (wyniki) i Arkusz2 (hasła)
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
                # Szukamy nazwiska w drugiej kolumnie
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
                        st.error("Błędne hasło ucznia.")
                else:
                    st.error("Nie znaleziono nazwiska.")
        else:
            st.warning("Baza nie istnieje. Zaloguj się jako admin.")

# --- 4. PO ZALOGOWANIU ---

else:
    with st.sidebar:
        st.write(f"Zalogowano jako: **{st.session_state.rola}**")
        if st.button("Wyloguj"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # --- PANEL NAUCZYCIELA ---
    if st.session_state.rola == "admin":
        st.header("👨‍🏫 Panel Nauczyciela")
        tab1, tab2 = st.tabs(["📊 Podgląd Wyników", "📤 Zarządzanie Bazą"])
        
        with tab2:
            plik = st.file_uploader("Wgraj nową bazę .xlsx", type="xlsx")
            if plik:
                with open("baza.xlsx", "wb") as f:
                    f.write(plik.getbuffer())
                st.success("Plik zaktualizowany!")
                st.balloons()
        
        with tab1:
            if os.path.exists("baza.xlsx"):
                df_w, _ = wczytaj_dane("baza.xlsx")
                if df_w is not None:
                    # Wybieramy zakres kolumn: od Lp (0) do Ocena (16)
                    widok = df_w.iloc[:, 0:17].copy()
                    
                    st.metric("Liczba rekordów", len(df_w))
                    szukaj = st.text_input("Szukaj studenta (po nazwisku):")
                    if szukaj:
                        widok = widok[widok.iloc[:, 1].astype(str).str.contains(szukaj, case=False)]

                    # SZTYWNY NAGŁÓWEK (ZGODNY Z TWOIM SCREENEM)
                    st.markdown("""
                    <style>
                        .tales-table { width: 100%; border-collapse: collapse; font-family: sans-serif; font-size: 13px; text-align: center; }
                        .tales-table th { border: 1px solid #ddd; background-color: #f8f9fa; padding: 8px; font-weight: bold; }
                    </style>
                    <table class="tales-table">
                        <tr>
                            <th rowspan="3">Lp.</th>
                            <th rowspan="3">NAZWISKO I IMIĘ</th>
                            <th rowspan="3">Akt. (10)</th>
                            <th colspan="12">Działy</th>
                            <th rowspan="3">Pkt</th>
                            <th rowspan="3">Ocena</th>
                        </tr>
                        <tr>
                            <th colspan="2">Log+zb 15(5)</th>
                            <th colspan="2">ciągi 15(5)</th>
                            <th colspan="2">funkcje 15(5)</th>
                            <th colspan="2">poch. 15(5)</th>
                            <th colspan="2">mac+wyz 15(5)</th>
                            <th colspan="2">uk_r_l 15(5)</th>
                        </tr>
                        <tr>
                            <th>a</th><th>b, c</th><th>a</th><th>b, c</th><th>a</th><th>b, c</th>
                            <th>a</th><th>b, c</th><th>a</th><th>b, c</th><th>a</th><th>b, c</th>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)

                    # Wyświetlan
