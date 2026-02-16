import streamlit as st
import re

def show_panel(wiersz_ucznia):
    st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    
    # 1. POBIERAMY DANE (SUROWE)
    dane = wiersz_ucznia.iloc[0].values
    kol_info = wiersz_ucznia.columns
    
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych"
    }

    zdane = []
    do_zrobienia = []

    st.write("### 🔍 TEST LICZENIA (Co widzi system):")

    # Sprawdzamy pary od indeksu 2 do 14 (rozszerzyłem zakres, żeby nic nie umknęło)
    for i in range(2, 16, 2):
        try:
            val1 = dane[i]
            val2 = dane[i+1]
            raw_name = str(kol_info[i][1])
            
            # Próba konwersji na liczby
            def clean_val(v):
                try: return float(v) if v not in ["", None] else 0.0
                except: return 0.0

            n1, n2 = clean_val(val1), clean_val(val2)
            suma = n1 + n2
            
            clean_key = raw_name.split(" ")[0]
            nazwa_pelna = mapa_nazw.get(clean_key, raw_name)

            # WYŚWIETLAMY DEBUG (Tylko dla Ciebie do sprawdzenia)
            st.write(f"Indeksy {i} i {i+1} ({raw_name}): `{val1}` + `{val2}` = **{suma}**")

            if "Unnamed" not in raw_name and i < 15:
                if suma >= 4.5:
                    zdane.append(nazwa_pelna)
                else:
                    do_zrobienia.append(nazwa_pelna)
        except:
            continue

    st.write("---")

    # 2. WYNIKI DLA UCZNIA
    col1, col2 = st.columns(2)
    with col1:
        st.info("**✅ Zdane:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
    with col2:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Zaliczone!"))

    if st.button("Wyloguj"):
        st.session_state.clear()
        st.rerun()
