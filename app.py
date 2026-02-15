import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="centered")

# --- 1. FUNKCJE POMOCNICZE ---

def check_admin_password(input_password):
    # Hash dla: profesor123
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    # Zamieniamy to co wpiszesz na hash i porównujemy
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane(sciezka):
    try:
        df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except Exception as e:
        return None, None

# --- 2. ZARZĄDZANIE SESJĄ ---

if "zalogowany" not in st.session_state:
    st.session_state.zalogowany = False
    st.session_state.rola = None
    st.session_state.dane = None

# --- 3. EKRAN LOGOWANIA ---

if not st.session_state.zalogowany:
    st.title("🛡️ System TALES")
    st.subheader("Logowanie do systemu")
    
    # Brak "with st.form" sprawia, że Enter w polach tekstowych działa od razu
    uzytkownik = st.text_input("Nazwisko lub Identyfikator (np. admin):")
    haslo_wpisane = st.text_input("Hasło:", type="password")
    
    # Przycisk logowania
    kliknieto = st.button("Zaloguj się", use_container_width=True)

    # Logika sprawdzania (uruchamia się po kliknięciu LUB po Enterze)
    if kliknieto or (uzytkownik and haslo_wpisane):
        login_clean = uzytkownik.strip().lower()
        pass_clean = haslo_wpisane.strip()

        if login_clean == "admin":
            if check_admin_password(pass_clean):
                st.session_state.zalogowany = True
                st.session_state.rola = "admin"
                st.rerun()
            elif kliknieto: # Pokazuj błąd tylko jeśli faktycznie kliknął lub zatwierdził oba pola
                st.error("Błędne hasło administratora.")
        
        elif os.path.exists("baza.xlsx"):
            df_w, df_h = wczytaj_dane("baza.xlsx")
            if df_w is not None:
                # Normalizacja listy nazwisk z Excela
                nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                
                if login_clean in nazwiska:
                    idx = nazwiska.index(login_clean)
                    wiersz = df_w.iloc[[idx]]
                    lp = wiersz.iloc[0, 0]
                    
                    # Sprawdzanie hasła ucznia z Arkusza 2
                    poprawne_haslo = str(df_h[df_h["Lp"] == lp]["Haslo"].values[0]).strip()
                    if pass_clean == poprawne_haslo:
                        st.session_state.zalogowany = True
                        st.session_state.rola = "uczen"
                        st.session_state.dane = wiersz
                        st.rerun()
                    elif kliknieto:
                        st.error("Błędne hasło ucznia.")
                elif kliknieto:
                    st.error("Nie znaleziono takiego nazwiska.")
        elif kliknieto:
            st.warning("Baza danych nie jest wgrana. Zaloguj się jako admin.")

# --- 4. WIDOK PO ZALOGOWANIU ---

else:
    # Przycisk wyloguj zawsze dostępny w pasku bocznym
    if st.sidebar.button("Wyloguj"):
        st.session_state.zalogowany = False
        st.session_state.rola = None
        st.session_state.dane = None
        st.rerun()

    # PANEL NAUCZYCIELA
    if st.session_state.rola == "admin":
        st.header("👨‍🏫 Panel Nauczyciela")
        st.write("Wgraj plik Excel, aby zaktualizować bazę ocen dla uczniów.")
        
        plik = st.file_uploader("Wybierz plik .xlsx", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Plik został pomyślnie zapisany na serwerze!")
            st.balloons()

    # PANEL UCZNIA
    elif st.session_state.rola == "uczen":
        w = st.session_state.dane
        st.header(f"Witaj, {w.iloc[0, 1]}!")
        
        # Pobranie wyników (kolumny 15 i 16)
        try:
            punkty = float(w.iloc[0, 15])
            ocena = str(w.iloc[0, 16])
            max_pkt = 60 # Tutaj możesz wpisać swoją wartość max
            
            c1, c2 = st.columns(2)
            c1.metric("Twoje punkty", f"{punkty} / {max_pkt}")
            c2.metric("Ocena końcowa", ocena)
            
            st.progress(min(punkty/max_pkt, 1.0))
            
            if punkty >= 30:
                st.balloons()
        except:
            st.error("Wystąpił problem z odczytem Twoich punktów z pliku.")

