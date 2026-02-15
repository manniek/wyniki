import streamlit as st
import re
import pandas as pd

def show_panel(wiersz_ucznia):
    # 1. GÓRNY PASEK
    c_pow, c_spacer, c_btn = st.columns([6, 2, 2])
    with c_pow:
        st.subheader(f"👋 Witaj, {wiersz_ucznia.iloc[0, 1]}")
    with c_btn:
        if st.button("Wyloguj", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.write("---")

    # 2. TABELA WYNIKÓW
    st.markdown("#### Twoje wyniki szczegółowe:")
    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    
    # Wybieramy dane do wyświetlenia (bez kolumn technicznych)
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") 

    # 3. ANALIZA DZIAŁÓW (Logika MultiIndex)
    # Pobieramy sumę całkowitą (kolumna 15)
    suma_total = float(wiersz_ucznia.iloc[0, 15])
    
    # Słownik na działy: { 'Nazwa Działu': suma_punktów_w_dziale }
    wyniki_dzialow = {}
    
    # Interujemy po kolumnach od 3 do 14 (tam gdzie są punkty za zadania)
    for col_idx in range(3, 15):
        nazwa_kol = wiersz_ucznia.columns[col_idx]
        # Pobieramy nazwę działu (zakładam poziom 1 w MultiIndex: np. "Ciągi")
        dzial = nazwa_kol[1] if isinstance(nazwa_kol, tuple) else "Inne"
        
        wartosc = wiersz_ucznia.iloc[0, col_idx]
        try:
            punktacja = float(wartosc) if wartosc != "" else 0.0
        except:
            punktacja = 0.0
            
        wyniki_dzialow[dzial] = wyniki_dzialow.get(dzial, 0.0) + punktacja

    zdane = [d for d, punkty in wyniki_dzialow.items() if punkty >= 4.5]
    do_zrobienia = [d for d, punkty in wyniki_dzialow.items() if punkty < 4.5]

    # 4. WYŚWIETLANIE DWÓCH POŁÓW
    col_lewa, col_prawa = st.columns(2)

    with col_lewa:
        st.info("**✅ Zdane działy:**\n\n" + (", ".join(zdane) if zdane else "Brak"))
        if suma_total > 40:
            st.success(f"🏆 **Zdobyte punkty:** {suma_total}")

    with col_prawa:
        st.warning("**🚀 Do zrobienia:**\n\n" + (", ".join(do_zrobienia) if do_zrobienia else "Wszystko zaliczone!"))
        if suma_total <= 40:
            brakujace = 40.5 - suma_total
            st.error(f"📉 **Punkty do zdobycia:** {brakujace:.1f}")
