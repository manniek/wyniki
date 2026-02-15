import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="centered")

# --- KONFIGURACJA I FUNKCJE ---

def check_admin_password(input_password):
    # Hash dla: profesor123
    stored_hash = "f7134375b06d87948a27a85c347d4e339a16f6b30f4060879c94132840001099"
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash

def wczytaj_dane(sciezka):
    df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
    df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
    df_h.columns = ["Lp", "Haslo"]
    return df_w, df_h

# --- INTERFEJS LOGOWANIA ---

st.title("🛡️ System Weryfikacji Wyników")
st.write("Wprowadź swoje dane, aby uzyskać dostęp.")

with st.container(border=True):
    login = st.text_input("Nazwisko lub Identyfikator:")
    haslo = st.text_input("Hasło:", type="password")
    zaloguj = st.button("Zaloguj się", use_container_width=True)

# --- LOGIKA PO KLIKNIĘCIU ---

if zaloguj:
    # 1. SPRAWDZAMY CZY TO ADMIN
    if login.lower() == "admin":
        if check_admin_password(haslo):
            st.session_state["role"] = "admin"
            st.success("Zalogowano jako Administrator.")
        else:
            st.error("Błędne hasło administratora.")
    
    # 2. SPRAWDZAMY CZY TO UCZEŃ
    else:
        if os.path.exists("baza.xlsx"):
            df_w, df_h = wczytaj_dane("baza.xlsx")
            # Szukamy czy nazwisko istnieje (ignorujemy wielkość liter przy szukaniu)
            lista_nazwisk = df_w.iloc[:, 1].astype(str).tolist()
            
            if login in lista_nazwisk:
                wiersz = df_w[df_w.iloc[:, 1] == login]
                lp_ucznia = wiersz.iloc[0, 0]
                prawdziwe_haslo = str(df_h[df_h["Lp"] == lp_ucznia]["Haslo"].values[0])
                
                if haslo == prawdziwe_haslo:
                    st.session_state["role"] = "user"
                    st.session_state["user_data"] = wiersz
                    st.success(f"Witaj {login}!")
                else:
                    st.error("Nieprawidłowe hasło ucznia.")
            else:
                st.error("Nie znaleziono takiego nazwiska w bazie.")
        else:
            st.warning("Baza danych nie jest dostępna. Skontaktuj się z wykładowcą.")

# --- WYŚWIETLANIE TREŚCI ZALEŻNIE OD ROLI ---

if "role" in st.session_state:
    st.divider()
    
    if st.session_state["role"] == "admin":
        st.subheader("📁 Panel Zarządzania")
        plik = st.file_uploader("Wgraj nowy plik ocen (.xlsx)", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Plik został pomyślnie zapisany!")
            st.balloons()
            
    elif st.session_state["role"] == "user":
        wiersz = st.session_state["user_data"]
        suma_pkt = float(wiersz.iloc[0, 15])
        ocena = str(wiersz.iloc[0, 16])
        max_pkt = 60

        # Wygląd wyników
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Twoja Ocena", ocena)
        with col2:
            st.metric("Punkty", f"{suma_pkt} / {max_pkt}")
        
        st.progress(min(suma_pkt/max_pkt, 1.0))
        
        if suma_pkt >= 50:
            st.confetti = True # Streamlit nie ma wbudowanego confetti poza balloons, ale to miły akcent w opisie
            st.balloons()
