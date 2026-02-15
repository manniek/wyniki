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
    df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
    df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
    df_h.columns = ["Lp", "Haslo"]
    return df_w, df_h

# --- INICJALIZACJA SESJI (Schowek) ---
if "zalogowany" not in st.session_state:
    st.session_state["zalogowany"] = False
    st.session_state["rola"] = None
    st.session_state["dane"] = None

# --- EKRAN LOGOWANIA ---
if not st.session_state["zalogowany"]:
    st.title("🛡️ System TALES - Logowanie")
    with st.form("formularz_logowania"):
        uzytkownik = st.text_input("Nazwisko lub Identyfikator:")
        haslo_wpisane = st.text_input("Hasło:", type="password")
        przycisk = st.form_submit_button("Zaloguj się", use_container_width=True)

        if przycisk:
            # Sprawdzanie Admina
            if uzytkownik.lower() == "admin" and check_admin_password(haslo_wpisane):
                st.session_state["zalogowany"] = True
                st.session_state["rola"] = "admin"
                st.rerun()
            
            # Sprawdzanie Ucznia
            elif os.path.exists("baza.xlsx"):
                df_w, df_h = wczytaj_dane("baza.xlsx")
                # Szukamy nazwiska (ignorujemy wielkość liter i spacje na końcach)
                df_w_copy = df_w.copy()
                df_w_copy.iloc[:, 1] = df_w_copy.iloc[:, 1].astype(str).str.strip()
                
                if uzytkownik.strip() in df_w_copy.iloc[:, 1].values:
                    wiersz = df_w_copy[df_w_copy.iloc[:, 1] == uzytkownik.strip()]
                    lp = wiersz.iloc[0, 0]
                    poprawne_haslo_ucznia = str(df_h[df_h["Lp"] == lp]["Haslo"].values[0]).strip()
                    
                    if haslo_wpisane.strip() == poprawne_haslo_ucznia:
                        st.session_state["zalogowany"] = True
                        st.session_state["rola"] = "uczen"
                        st.session_state["dane"] = wiersz
                        st.rerun()
                    else:
                        st.error("Błędne hasło ucznia.")
                else:
                    st.error("Nie znaleziono takiego użytkownika.")
            else:
                st.error("Błąd: Baza danych nie istnieje lub błędne dane.")

# --- EKRAN PO ZALOGOWANIU ---
else:
    if st.sidebar.button("Wyloguj"):
        st.session_state["zalogowany"] = False
        st.rerun()

    if st.session_state["rola"] == "admin":
        st.header("👨‍🏫 Panel Nauczyciela")
        plik = st.file_uploader("Wgraj plik Excel", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Baza zaktualizowana!")
            st.balloons()

    elif st.session_state["rola"] == "uczen":
        wiersz = st.session_state["dane"]
        st.header(f"Witaj, {wiersz.iloc[0, 1]}!")
        
        # Wyświetlanie wyników
        punkty = float(wiersz.iloc[0, 15])
        ocena = str(wiersz.iloc[0, 16])
        max_pkt = 60
        
        c1, c2 = st.columns(2)
        c1.metric("Twoje punkty", f"{punkty} / {max_pkt}")
        c2.metric("Ocena końcowa", ocena)
        
        st.progress(min(punkty/max_pkt, 1.0))
        if punkty >= 30: st.balloons()
