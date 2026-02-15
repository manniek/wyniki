import streamlit as st
import pandas as pd
import os
import hashlib

st.set_page_config(page_title="System TALES", layout="centered")

# --- FUNKCJE POMOCNICZE ---

def check_password(input_password):
    """Zamienia wpisany tekst na hash i porównuje z oryginałem."""
    # Hash dla hasła: profesor123
    # Nawet jeśli uczeń to widzi, nie wie jakie to hasło.
    stored_hash = "f7134375b06d87948a27a85c347d4e339a16f6b30f4060879c94132840001099"
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    return input_hash == stored_hash

def wczytaj_dane(sciezka):
    """Wczytuje strukturę Twojego pliku Excel."""
    df_w = pd.read_excel(sciezka, sheet_name='Arkusz1', header=[0,1,2])
    df_h = pd.read_excel(sciezka, sheet_name='Arkusz2', header=None)
    df_h.columns = ["Lp", "Haslo"]
    return df_w, df_h

# --- INTERFEJS ---

st.sidebar.title("Nawigacja")
tryb = st.sidebar.radio("Wybierz panel:", ["Uczeń", "Nauczyciel"])

if tryb == "Nauczyciel":
    st.header("🔐 Panel Administratora")
    # type="password" sprawia, że kropki zasłaniają wpisywane hasło
    haslo_wpisane = st.text_input("Hasło dostępowe:", type="password")
    
    if check_password(haslo_wpisane):
        st.success("Dostęp autoryzowany.")
        plik = st.file_uploader("Wgraj aktualny arkusz Excel (oceny.xlsx)", type="xlsx")
        if plik:
            with open("baza.xlsx", "wb") as f:
                f.write(plik.getbuffer())
            st.success("Baza została zaktualizowana na serwerze!")
            st.balloons()
    elif haslo_wpisane != "":
        st.error("Błędne hasło admina.")

else:
    st.header("🎓 Twoje Wyniki")
    
    # Sprawdzamy czy plik baza.xlsx w ogóle istnieje na serwerze
    if os.path.exists("baza.xlsx"):
        df_w, df_h = wczytaj_dane("baza.xlsx")
        
        # Pobieramy listę nazwisk z drugiej kolumny (indeks 1)
        lista = df_w.iloc[:, 1].dropna().unique().tolist()
        
        wybrany = st.selectbox("Wybierz swoje nazwisko:", ["---"] + lista)
        kod_ucznia = st.text_input("Wpisz swoje hasło z Arkusza 2:", type="password")
        
        if st.button("Pokaż moje wyniki"):
            if wybrany == "---":
                st.warning("Wybierz najpierw nazwisko!")
            else:
                # Szukamy wiersza wybranego ucznia
                wiersz = df_w[df_w.iloc[:, 1] == wybrany]
                lp_ucznia = wiersz.iloc[0, 0]
                
                # Pobieramy hasło przypisane do tego Lp z Arkusz2
                prawdziwe_haslo_ucznia = str(df_h[df_h["Lp"] == lp_ucznia]["Haslo"].values[0])
                
                if kod_ucznia == prawdziwe_haslo_ucznia:
                    st.divider()
                    st.subheader(f"Witaj, {wybrany}!")
                    
                    # Pobieranie danych (kolumna 15 to suma, 16 to ocena)
                    suma_pkt = float(wiersz.iloc[0, 15])
                    ocena = str(wiersz.iloc[0, 16])
                    max_pkt = 60 # Tutaj wpisz ile było max do zdobycia
                    
                    # Prezentacja oceny
                    if "5" in ocena or "4.5" in ocena:
                        st.success(f"### Twoja ocena: {ocena} 🏆")
                        st.balloons()
                    elif "2" in ocena:
                        st.error(f"### Twoja ocena: {ocena} (wymagana poprawa)")
                    else:
                        st.info(f"### Twoja ocena: {ocena}")

                    # Wizualizacja punktów
                    procent = min(suma_pkt / max_pkt, 1.0)
                    st.write(f"Zdobyte punkty: **{suma_pkt}** z {max_pkt}")
                    st.progress(procent)
                    
                    # Komentarz automatyczny
                    if suma_pkt >= 50:
                        st.write("🌟 Fenomenalnie!")
                    elif suma_pkt >= 30:
                        st.write("👍 Dobry wynik, gratulacje.")
                    else:
                        st.write("📖 Mogło być lepiej, zapraszam na konsultacje.")
                else:
                    st.error("Hasło ucznia jest nieprawidłowe.")
    else:
        st.info("Baza ocen nie została jeszcze udostępniona.")
