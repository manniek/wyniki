import streamlit as st
import pandas as pd
import os
import hashlib
import glob
import styles
import admin_panel
import student_panel

st.set_page_config(page_title="RB oceny", layout="wide")
styles.apply_styles()

# --- FUNKCJE ---
def check_admin_password(input_password):
    stored_hash = "cffa965d9faa1d453f2d336294b029a7f84f485f75ce2a2c723065453b12b03b"
    return hashlib.sha256(input_password.strip().encode()).hexdigest() == stored_hash

def wczytaj_dane():
    pliki = glob.glob("*.xlsx")
    if not pliki:
        return None, None
    
    sciezka = pliki[0]
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

# --- LOGIKA ---
if not st.session_state.zalogowany:
    st.title("🛡️ RB oceny")
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
                    nazwiska = df_w.iloc[:, 1].astype(str).str.strip().str.lower().tolist()
                    if login_clean in nazwiska:
                        idx = nazwiska.index(login_clean)
                        lp = df_w.iloc[idx, 0]
                        pass_row = df_h[df_h["Lp"] == lp]
                        
                        if not pass_row.empty:
                            poprawne_haslo = str(pass_row.iloc[0, 1]).strip()
                            hash_wpisany = hashlib.sha256(pass_clean.encode()).hexdigest()
                            
                            # Porównujemy hash wpisany z hashem z Excela
                            # Porównujemy hash wpisany z hashem z Excela
                            if hash_wpisany == poprawne_haslo:
                                
                                # 1. SPŁASZCZANIE NAZW KOLUMN (Rozprawiamy się z MultiIndexem)
                                # Zmienia ('Działy', 'Liczby zesp.', 'a') na "Liczby zesp. a"
                                nowe_nazwy = []
                                for col in df_w.columns:
                                    # Pobieramy tylko te części, które nie są "Unnamed"
                                    czesci = [str(poziom) for poziom in col if "Unnamed" not in str(poziom)]
                                    # Usuwamy słowo "Działy" z nazwy, żeby nie śmieciło (opcjonalnie)
                                    if "Działy" in czesci: czesci.remove("Działy")
                                    nowe_nazwy.append(" ".join(czesci).strip())
                                
                                df_w.columns = nowe_nazwy

                                # 2. TŁUMACZENIE (Tworzymy listę zdanych działów dla ucznia)
                                wiersz_ucznia = df_w.iloc[idx]
                                zdane_przetlumaczone = []

                                for col_name in df_w.columns:
                                    # Sprawdzamy czy w danej kolumnie jest "zal" lub "1" (dostosuj do swojego Excela)
                                    if str(wiersz_ucznia[col_name]).lower() in ["zal", "1", "1.0", "x"]:
                                        
                                        # Szukamy czy nazwa kolumny pasuje do naszej mapy
                                        znaleziono = False
                                        for klucz, tlumaczenie in mapa_nazw.items():
                                            if klucz.lower() in col_name.lower():
                                                zdane_przetlumaczone.append(tlumaczenie)
                                                znaleziono = True
                                                break
                                        
                                        # Jeśli nie ma w mapie, dodaj surową nazwę (np. "dupa")
                                        if not znaleziono and col_name not in ["Lp.", "NAZWISKO I IMIĘ", "Pkt", "Ocena"]:
                                            zdane_przetlumaczone.append(col_name)

                                # 3. ZAPIS DO SESJI
                                st.session_state.update({
                                    "zalogowany": True, 
                                    "rola": "uczen", 
                                    "dane": df_w.iloc[[idx]],
                                    "zdane_list": list(set(zdane_przetlumaczone)) # set usuwa duplikaty a i b,c
                                })
                                
                                # Debugowanie - teraz zobaczysz czy działa!
                                st.success(f"Zalogowano! Twoje działy: {', '.join(zdane_przetlumaczone)}")
                                
                                # Odkomentuj rerun po sprawdzeniu czy napisy są poprawne
                                # st.rerun()
                                
                else:
                    st.error("Błędny login lub hasło.")

else:
    # Sekcja wyświetlania po zalogowaniu
    df_w, _ = wczytaj_dane()
    if st.session_state.rola == "admin":
        admin_panel.show_panel(df_w)
    else:
        student_panel.show_panel(st.session_state.dane)







