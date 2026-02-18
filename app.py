import streamlit as st
import pandas as pd
import hashlib
import glob
import styles
import admin_panel
import student_panel

st.set_page_config(page_title="System TALES", layout="wide")
styles.apply_styles()

def check_admin_password(input_password):
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane():
    pliki = glob.glob("*.xlsx")
    if not pliki: return None, None
    try:
        df_w = pd.read_excel(pliki[0], sheet_name='Arkusz1', header=[0,1,2])
        df_h = pd.read_excel(pliki[0], sheet_name='Arkusz2', header=None)
        df_h.columns = ["Lp", "Haslo"]
        return df_w, df_h
    except: return None, None

if "zalogowany" not in st.session_state:
    st.session_state.update({"zalogowany": False, "rola": None, "dane": None})

if not st.session_state.zalogowany:
    st.title("🛡️ System TALES")
    with st.form("log_form"):
        uzytkownik = st.text_input("Nazwisko / Identyfikator:")
        haslo_wpisane = st.text_input("Hasło:", type="password")
        if st.form_submit_button("Zaloguj się", use_container_width=True):
            login_clean = uzytkownik.strip().lower()
            df_w, df_h = wczytaj_dane()
            if login_clean == "admin" and check_admin_password(haslo_wpisane):
                st.session_state.update({"zalogowany": True, "rola": "admin"})
                st.rerun()
            elif df_w is not None:
                nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                if login_clean in nazwiska:
                    idx = nazwiska.index(login_clean)
                    lp = df_w.iloc[idx, 0]
                    pass_row = df_h[df_h["Lp"] == lp]
                    if not pass_row.empty and str(pass_row.iloc[0, 1]).strip() == haslo_wpisane.strip():
                        st.session_state.update({"zalogowany": True, "rola": "uczen", "dane": df_w.iloc[[idx]]})
                        st.rerun()
            st.error("Błędny login lub hasło.")
# --- WYŚWIETLANIE ---
else:
    df_w, _ = wczytaj_dane()
    if st.session_state.rola == "admin":
        admin_panel.show_panel(df_w)
    else:
        # ROZDZIELACZ MOBILNY
        from streamlit_javascript import st_javascript
        width = st_javascript("window.innerWidth")

        if width is not None:
            if width < 700:
                # Jeśli ekran jest mały, ładujemy panel mobilny
                import mobile_panel
                mobile_panel.show_mobile_panel(st.session_state.dane)
            else:
                # Jeśli ekran jest duży, standardowy panel
                student_panel.show_panel(st.session_state.dane)
        else:
            # Placeholder, dopóki JS nie zmierzy ekranu
            st.info("Inicjalizacja widoku...")
