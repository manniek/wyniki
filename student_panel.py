import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # Tworzymy 3 główne sekcje: Powitanie (lewa), Progi (środek), Przycisk (prawa)
    # Proporcje [2, 6, 2] oznaczają, że środkowa część na progi jest najszersza
    c_pow, c_progi, c_btn = st.columns([2, 6, 2])

    with c_pow:
        st.subheader(f"👋 {wiersz_ucznia.iloc[0, 1]}")

    with c_progi:
        # Wewnątrz środkowej kolumny robimy 6 mniejszych na progi
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        
        # Stylizacja CSS dla małych boksów (zmniejszona czcionka i padding, żeby się zmieściło)
        style = 'style="color:white; padding:2px; text-align:center; border-radius:3px; font-size:12px; line-height:1.2;"'
        style_dark = 'style="color:black; padding:2px; text-align:center; border-radius:3px; font-size:12px; line-height:1.2;"'
        
        with p1:
            st.markdown(f'<div {style} style="background-color:#FF0000;"><b>2</b><br>0-40</div>', unsafe_allow_html=True)
        with p2:
            st.markdown(f'<div {style_dark} style="background-color:#92D050;"><b>3</b><br>40-52</div>', unsafe_allow_html=True)
        with p3:
            st.markdown(f'<div {style} style="background-color:#00B050;"><b>3.5</b><br>52-64</div>', unsafe_allow_html=True)
        with p4:
            st.markdown(f'<div {style} style="background-color:#00B0F0;"><b>4</b><br>64-76</div>', unsafe_allow_html=True)
        with p5:
            st.markdown(f'<div {style} style="background-color:#0070C0;"><b>4.5</b><br>76-88</div>', unsafe_allow_html=True)
        with p6:
            st.markdown(f'<div {style_dark} style="background-color:#FFC000;"><b>5</b><br>88-100</div>', unsafe_allow_html=True)

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
        except:
            continue

    # Pobieramy sumę całkowitą (zgodnie z testem jest na indeksie 16)
    # Pobieramy sumę bezpośrednio z indeksu 16 (tak jak podałeś)
    try:
        suma_total = float(dane[15])
    except:
        suma_total = 0.0

    # 5. WYŚWIETLANIE W DWÓCH POŁOWACH
    st.write("") 
    col_lewa, col_prawa = st.columns(2)

    # Pobieramy ocenę (indeks 16) i sumę (indeks 15)
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""
    suma_total = float(dane[15]) if dane[15] not in [None, "nan", ""] else 0.0

    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        
        # Logika oceny / punktów
        if ocena and ocena != "":
            st.success(f"🎓 **Twoja ocena to: {ocena}**")
        else:
            # Zamiast komunikatu o braku oceny, pokazujemy sumę punktów
            st.info(f"📊 **Zdobyłeś {suma_total:.1f} punktów**")

    with col_prawa:
        st.warning("**🚀 Do robienia: działy**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        
        # Sekcja brakujących punktów (tylko jeśli brak oceny)
        if not ocena:
            if suma_total < 40.5:
                brakujace = 40.5 - suma_total
                st.error(f"📉 **Brakuje Ci:** {brakujace:.1f} pkt do zaliczenia")
            else:
                st.success("")





