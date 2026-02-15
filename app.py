import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="centered")

# --- FUNKCJE ---
def check_admin_password(input_password):
    # Hash dla: profesor123
    stored_hash = "f7134375b06d87948a27a85c347d4e339a16f6b30f4060879c94132840001099"
    return hashlib.sha256(input_password.encode()).hexdigest() == stored_hash

def wczytaj_dane(sciezka):
    try:
        df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except Exception as e:
        st.error(f"Błąd odczytu pliku: {e}")
        return None, None

# --- SESJA ---
if "zalogowany" not in st.session_state:
    st.session_state.zalogowany = False
    st.session_state.rola = None
    st.session_state.dane = None

# --- LOGIKA EKRANÓW ---

if not st.session_state.zalogowany:
    st.title("🛡️ System TALES - Logowanie")
    
    with st.form("login_form"):
        uzytkownik = st.text_input("Nazwisko lub Identyfikator:")
        haslo_wpisane = st.text_input("Hasło:", type="password")
        przycisk_wyslij = st.form_submit_button("Zaloguj się", use_container_width=True)

        if przycisk_wyslij:
            login_clean = uzytkownik.strip().lower()
            pass_clean = haslo_wpisane.strip()

            # 1. ADMIN
            if login_clean == "admin":
                if check_admin_password(pass_clean):
                    st.session_state.zalogowany = True
                    st.session_state.rola = "admin"
                    st.rerun()
                else:
                    st.error("Błędne hasło administratora.")
            
            # 2. UCZEŃ
            elif os.path.exists("baza.xlsx"):
                df_w, df_h = wczytaj_dane("baza.xlsx")
                if df_w is not None:
                    # Szukamy nazwiska
                    nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                    if login_clean in nazwiska:
                        idx = nazwiska.index(login_clean)
                        wiersz = df_w.iloc[[idx]]
                        lp = wiersz.iloc[0, 0]
                        
                        # Sprawdzamy hasło ucznia
                        poprawne_haslo = str(df_h[df_h["Lp"] == lp]["Haslo"].values[0]).strip()
                        if pass_clean == poprawne_haslo:
                            st.session_state.zalogowany = True
                            st.session_state.rola = "uczen"
                            st.session_state.dane = wiersz
                            st.rerun()
                        else:
                            st.error("Błędne hasło ucznia.")
                    else:
                        st.error("Nie znaleziono takiego nazwiska.")
            else:
                st.error("Brak bazy danych. Zaloguj się jako Admin i wgraj Excela.")

else:
    # --- PANEL PO ZALOGOWANIU ---
    if st.sidebar.button("Wyloguj"):
        st.session_state.zalogowany = False
        st.rerun()

    if st.session_state.rola == "admin":
        st.header("👨‍🏫 Panel Nauczyciela")
        plik = st.file_uploader("Wgraj plik Excel", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Plik baza.xlsx został zapisany!")
            st.balloons()

    elif st.session_state.rola == "uczen":
        w = st.session_state.dane
        st.header(f"Witaj, {w.iloc[0, 1]}!")
        
        # Wyciągamy punkty (kolumna 15) i ocenę (kolumna 16)
        punkty = float(w.iloc[0, 15])
        ocena = str(w.iloc[0, 16])
        
        col1, col2 = st.columns(2)
        col1.metric("Twoje punkty", f"{punkty} / 60")
        col2.metric("Ocena", ocena)
        st.progress(min(punkty/60, 1.0))
