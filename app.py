import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="wide") # Zmienione na wide dla lepszej tabeli

# --- 1. FUNKCJE ---

def check_admin_password(input_password):
    # Hash dla Twojego hasła (pamiętaj o właściwym hashu w Mathematica!)
    # Obecnie ustawiony na: profesor
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane(sciezka):
    try:
        # Wczytujemy z zachowaniem nagłówków (3 poziomy)
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
                # Kolumna 1 to nazwiska
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
    # Sidebar z przyciskiem wyloguj
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
            st.subheader("Aktualizacja pliku Excel")
            plik = st.file_uploader("Wgraj nową bazę .xlsx", type="xlsx")
            if plik:
                with open("baza.xlsx", "wb") as f:
                    f.write(plik.getbuffer())
                st.success("Plik baza.xlsx został zaktualizowany!")
                st.balloons()
        
with tab1:
            if os.path.exists("baza.xlsx"):
                df_w, _ = wczytaj_dane("baza.xlsx")
                if df_w is not None:
                    # 1. Wycinamy zakres (od kolumny nr 1 do 12 włącznie)
                    widok = df_w.iloc[:, 1:13].copy()
                    
                    # 2. NAPRAWA NAGŁÓWKÓW (to usunie liczby 0, 1, 2...)
                    nowe_nazwy = []
                    for col in widok.columns:
                        # Sklejamy poziomy nagłówka (np. "Logika - Zadanie 1")
                        # Pomijamy puste pola "Unnamed"
                        czesci = [str(p) for p in col if "Unnamed" not in str(p)]
                        nowe_nazwy.append(" - ".join(czesci) if czesci else "Dane")
                    
                    widok.columns = nowe_nazwy # Przypisujemy ładne nazwy do kolumn

                    st.metric("Liczba rekordów", len(df_w))
                    szukaj = st.text_input("Szukaj studenta (nazwisko):")
                    
                    if szukaj:
                        # Szukamy w pierwszej kolumnie widoku (bo Lp zostało odcięte)
                        widok = widok[widok.iloc[:, 0].astype(str).str.contains(szukaj, case=False)]
                    
                    # 3. WYŚWIETLANIE (hide_index=True usuwa liczby z lewej strony)
                    st.dataframe(widok, use_container_width=True, hide_index=True)
                else:
                    st.error("Problem z wyświetleniem pliku.")
            else:
                st.info("Baza jest pusta. Wgraj plik w zakładce obok.")

    # --- PANEL UCZNIA ---
    elif st.session_state.rola == "uczen":
        w = st.session_state.dane
        st.header(f"Witaj, {w.iloc[0, 1]}!")
        
        # Wyciąganie wyników
        try:
            punkty = float(w.iloc[0, 15])
            ocena = str(w.iloc[0, 16])
            
            c1, c2 = st.columns(2)
            c1.metric("Twoje punkty", f"{punkty} / 60")
            c2.metric("Ocena końcowa", ocena)
            st.progress(min(punkty/60, 1.0))
        except:
            st.error("Błąd podczas odczytu Twoich punktów.")


