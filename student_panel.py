import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # 1. GÓRNY PASEK (Przywrócony układ z przyciskiem po prawej)
    c_pow, c_spacer, c_btn = st.columns([6, 2, 2])
    with c_pow:
        st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 2. TABELA WYNIKÓW (Wyświetlamy oryginał bez zmian)
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 3. PRZYGOTOWANIE LOGIKI (Mapowanie i czyszczenie NaN)
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    kol_info = wiersz_clean.columns
    
    mapa_nazw = {
        "Log+zb": "logika i zbiory", "ciągi": "ciągi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "układy równań liniowych", "Liczby zesp": "liczby zespolone",
        "całka nieozn.": "całka nieoznaczona", "całka oznacz.": "całka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dwóch zmiennych",
        "równ. róż.": "równania różniczkowe"
    }

    zdane = []
    do_zrobienia = []

    # Analiza par od indeksu 4 (Log+zb) do 15
    for i in range(4, 16, 2):
        try:
            raw_name = str(kol_info[i][1])
            if "Unnamed" in raw_name: continue
            
            clean_key = raw_name.split(" ")[0]
            nazwa_finalna = mapa_nazw.get(clean_key, raw_name)

            suma_pary = float(dane[i]) + float(dane[i+1])
            
            if suma_pary >= 4.5:
                zdane.append(nazwa_finalna)
            else:
                do_zrobienia.append(nazwa_finalna)
        except:
            continue

    # Pobieramy sumę całkowitą (zgodnie z testem jest na indeksie 16)
    try:
        suma_total = float(dane[16])
    except:
        suma_total = 0.0

    # 4. POWRÓT DO MOTYWACYJNEGO PODSUMOWANIA (Dwie kolumny)
    st.write("") 
    col_lewa, col_prawa = st.columns(2)

    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if suma_total >= 40.5:
            st.success(f"🏆 **Zdobyte punkty:** {suma_total} (ZALICZONE!)")

    with col_prawa:
        st.warning("**🚀 Do zrobienia: działy**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if suma_total < 40.5:
            brakujace = 40.5 - suma_total
            st.error(f"📉 **Brakuje Ci:** {brakujace:.1f} pkt do 40.5 pkt")
