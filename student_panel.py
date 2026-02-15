import streamlit as st
import re

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
    
    widok_ucznia = wiersz_ucznia.iloc[:, :-4].copy().fillna("")
    html_table = widok_ucznia.to_html(index=False, classes='tales-table', border=0)
    html_table = re.sub(r'Unnamed: [\w_]+_level_\d+', '', html_table)
    st.markdown(html_table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.write("") 

    # 3. TWOJA LOGIKA: Pętla po parach kolumn
    # Zakładamy nazwy działów w kolejności par:
    nazwy_dzialow = ["Log+zb", "Ciągi", "F. wykładnicza", "Trygonometria", "Geometria", "Inne"]
    
    zdane = []
    do_zrobienia = []
    
    # Idziemy pętlą co 2 kolumny (od 3 do 15 w Pythonie, co odpowiada Twoim 4-15)
    # W Pythonie iloc[0, 3] to 4. kolumna w Excelu
    dzial_idx = 0
    for i in range(3, 15, 2):
        if dzial_idx < len(nazwy_dzialow):
            try:
                val1 = wiersz_ucznia.iloc[0, i]
                val2 = wiersz_ucznia.iloc[0, i+1]
                
                suma_pary = (float(val1) if val1 != "" else 0) + (float(val2) if val2 != "" else 0)
                
                nazwa = nazwy_dzialow[dzial_idx]
                if suma_pary >= 4.5:
                    zdane.append(nazwa)
                else:
                    do_zrobienia.append(nazwa)
            except:
                pass
            dzial_idx += 1

    # Pobieramy sumę całkowitą z kolumny 15 (indeks 15)
    suma_total = float(wiersz_ucznia.iloc[0, 15])

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
