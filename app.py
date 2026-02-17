import streamlit as st
import pandas as pd
import os
import hashlib
import glob
import styles
import admin_panel
import student_panel

st.set_page_config(page_title="System TALES", layout="wide")
styles.apply_styles()

# --- FUNKCJE ---
def check_admin_password(input_password):
    # Hasło admina: 123admin
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane():
    # Szukamy dowolnego pliku xlsx
    pliki = glob.glob("*.xlsx")
    if not pliki:
        return None, None
    
    sciezka = pliki[0] # Bierzemy pierwszy lepszy plik excel
    try:
        df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except:
        return None, None

# --- SESJA ---
if "zalogowany" not in st.session_state:
    st.session_state.update({"zalogowany": False, "rola": None, "dane": None})

# --- LOGOWANIE ---
if not st.session_state.zalogowany:
    st.title("🛡️ System TALES")
    with st.form("log_form"):
        uzytkownik = st.text_input("Nazwisko / Identyfikator:")
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
                    # Nazwiska w kolumnie o indeksie 1
                    nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                    if login_clean in nazwiska:
                        idx = nazwiska.index(login_clean)
                        lp = df_w.iloc[idx, 0]
                        # Szukamy hasła w Arkusz2 po Lp
                        pass_row = df_h[df_h["Lp"] == lp]
                        if not pass_row.empty:
                            poprawne_haslo = str(pass_row.iloc[0, 1]).strip()
                            if pass_clean == poprawne_haslo:
                                st.session_state.update({
                                    "zalogowany": True, 
                                    "rola": "uczen", 
                                    "dane": df_w.iloc[[idx]]
                                })
                                st.rerun()
                st.error("Błędny login lub hasło.")

# --- WYŚWIETLANIE ---
else:
    df_w, _ = wczytaj_dane()
    if st.session_state.rola == "admin":
        admin_panel.show_panel(df_w)
    else:
        # student_panel.show_panel(st.session_state.dane)
        if st.session_state.zalogowany:
    if st.session_state.rola == "admin":
        import admin_panel
        admin_panel.show_panel()
    else:
        # TUTAJ BYŁO: student_panel.show_panel(st.session_state.dane)
        # ZAMIAST TEGO DAJEMY ROZDZIELACZ:
        
        from streamlit_javascript import st_javascript
        width = st_javascript("window.innerWidth")

        if width is not None:
            if width < 700:
                import mobile_panel
                mobile_panel.show_mobile_panel(st.session_state.dane)
            else:
                import student_panel
                student_panel.show_panel(st.session_state.dane)
        else:
            st.info("Inicjalizacja widoku premium...")

