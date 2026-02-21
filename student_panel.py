import streamlit as st
import pandas as pd
import re

def show_panel(wiersz_ucznia):
    # 1. POBIERANIE DANYCH (Twoja logika z wersji mobilnej)
    wiersz_clean = wiersz_ucznia.fillna(0)
    dane = wiersz_clean.iloc[0].values
    kol_info = wiersz_clean.columns

    # Wyciąganie imienia z kolumny 1
    pelne_dane = str(dane[1])
    imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
    
    # Wyciąganie punktów (kolumna 15) i oceny (kolumna 16)
    suma_total = float(dane[15])
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""

    # 2. NAGŁÓWEK (Układ komputerowy, kolory z mobilnego)
    c_pow, c_progi, c_btn = st.columns([3, 5, 2])
    
    with c_pow:
        st.markdown(f"""
            <div style="background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333;">
                <h3 style="color: #FFFFFF; margin: 0;">👋 Witaj, {imie}!</h3>
            </div>
        """, unsafe_allow_html=True)

    with c_progi:
        # Drabinka ocen z Twoimi kolorami (styl wymuszony kontrast)
        p = st.columns(6)
        progi_style = [
            ("#FF0000", "white", "2", "(0-40]"),
            ("#92D050", "black", "3", "(40-52]"),
            ("#00B050", "white", "3.5", "(52-64]"),
            ("#00B0F0", "white", "4", "(64-76]"),
            ("#0070C0", "white", "4.5", "(76-88]"),
            ("#FFC000", "black", "5", "(88-100]")
        ]
        for i, (bg, fg, oc, pr) in enumerate(progi_style):
            p[i].markdown(f'<div style="background-color:{bg}; color:{fg}; padding:5px; border-radius:5px; text-align:center; font-size:10px; font-weight:bold;">{oc}<br>{pr}</div>', unsafe_allow_html=True)

    with c_btn:
        if st.button("🔴 WYLOGUJ", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.divider()

    # 3. TABELA WYNIKÓW (Oryginalna, bez spłaszczania)
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    widok_tabela = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_tabela.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("")

    # 4. LOGIKA OSIĄGNIĘĆ (Na podstawie Twoich plików)
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

    # Analiza par działy (od kolumny 3 do 14)
    for i in range(3, 14, 2):
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
        except: continue

    # 5. WYŚWIETLANIE STATUSU (Z Twojego mobile_panel)
    col_l, col_p = st.columns(2)

    with col_l:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if ocena:
            st.success(f"### 🎓 Twoja ocena: {ocena}")
        else:
            st.metric("Twoje punkty", f"{suma_total:.1f} pkt")

    with col_p:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if not ocena:
            if suma_total < 40.5:
                brak = 40.5 - suma_total
                st.error(f"📉 Brakuje Ci: {brak:.1f} pkt do zaliczenia")
            else:
                st.success("Masz punkty na zaliczenie!")
