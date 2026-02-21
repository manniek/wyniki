import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # Nag艂贸wek w jednej linii: [Powitanie, Drabinka, Przycisk]
    c_pow, c_progi, c_btn = st.columns([2.5, 5.5, 2])

    with c_pow:
        # Pobieramy pe艂ny tekst, dzielimy go na wyrazy i bierzemy drugi element (imi臋)
        pelne_dane = str(wiersz_ucznia.iloc[0, 1])
        imie = pelne_dane.split()[1] if len(pelne_dane.split()) > 1 else pelne_dane
        st.subheader(f"馃憢 {imie}!")

    with c_progi:
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        
        # Definicje styl贸w dla ka偶dego koloru z osobna, by unikn膮膰 zlewania si臋 z t艂em
        # s_w = napisy bia艂e, s_b = napisy czarne
        s_w = 'display:block; color:white; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        s_b = 'display:block; color:black; padding:3px 0; text-align:center; border-radius:4px; font-size:11px; font-weight:bold; line-height:1.2;'
        
        p1.markdown(f'<div style="{s_w} background-color:#FF0000;">ocena 2:<br>(0-40]</div>', unsafe_allow_html=True)
        p2.markdown(f'<div style="{s_b} background-color:#92D050;">ocena 3:<br>(40-52]</div>', unsafe_allow_html=True)
        p3.markdown(f'<div style="{s_w} background-color:#00B050;">ocena 3.5:<br>(52-64]</div>', unsafe_allow_html=True)
        p4.markdown(f'<div style="{s_w} background-color:#00B0F0;">ocena 4:<br>(64-76]</div>', unsafe_allow_html=True)
        p5.markdown(f'<div style="{s_w} background-color:#0070C0;">ocena 4.5:<br>(76-88]</div>', unsafe_allow_html=True)
        p6.markdown(f'<div style="{s_b} background-color:#FFC000;">ocena 5:<br>(88-100]</div>', unsafe_allow_html=True)

    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.write("---")

    # 2. TABELA WYNIK脫W (Wy艣wietlamy orygina艂 bez zmian)
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
        "Log+zb": "logika i zbiory", "ci膮gi": "ci膮gi", "funkcje": "funkcje",
        "poch.": "pochodna", "mac+wyz": "macierze i wyznaczniki",
        "uk_r_l": "uk艂ady r贸wna艅 liniowych", "Liczby zesp": "liczby zespolone",
        "ca艂ka nieozn.": "ca艂ka nieoznaczona", "ca艂ka oznacz.": "ca艂ka oznaczona",
        "geometria an.": "geometria analityczna", "f(x,y)": "funkcje dw贸ch zmiennych",
        "r贸wn. r贸偶.": "r贸wnania r贸偶niczkowe"
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

    # Pobieramy sum臋 ca艂kowit膮 (zgodnie z testem jest na indeksie 16)
    # Pobieramy sum臋 bezpo艣rednio z indeksu 16 (tak jak poda艂e艣)
    try:
        suma_total = float(dane[15])
    except:
        suma_total = 0.0

    # 5. WY艢WIETLANIE W DW脫CH PO艁OWACH
    st.write("") 
    col_lewa, col_prawa = st.columns(2)

    # Pobieramy ocen臋 (indeks 16) i sum臋 (indeks 15)
    ocena = str(dane[16]).strip() if dane[16] not in [0, "0", None, "nan"] else ""
    suma_total = float(dane[15]) if dane[15] not in [None, "nan", ""] else 0.0

    with col_lewa:
        st.info("**鉁?Zdane dzia艂y:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        
        # Logika oceny / punkt贸w
        if ocena and ocena != "":
            st.success(f"馃帗 **Twoja ocena to: {ocena}**")
        else:
            # Zamiast komunikatu o braku oceny, pokazujemy sum臋 punkt贸w
            st.info(f"馃搳 **Zdoby艂e艣 {suma_total:.1f} punkt贸w**")

    with col_prawa:
        st.warning("**馃殌 Do robienia: dzia艂y**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        
        # Sekcja brakuj膮cych punkt贸w (tylko je艣li brak oceny)
        if not ocena:
            if suma_total < 40.5:
                brakujace = 40.5 - suma_total
                st.error(f"馃搲 **Brakuje Ci:** {brakujace:.1f} pkt do zaliczenia")
            else:
                st.success("")











