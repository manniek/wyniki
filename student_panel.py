import streamlit as st

def show_panel(wiersz_ucznia):
    c_pow, c_sp, c_log = st.columns([6, 2, 2])
    c_pow.header(f"Witaj, {wiersz_ucznia.iloc[0, 1]}!")
    
    if c_log.button("Wyloguj", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.markdown('<div class="table-container">', unsafe_allow_html=True)
    try:
        p_val = wiersz_ucznia.iloc[0, 15]
        o_val = wiersz_ucznia.iloc[0, 16]
        st.metric("Twoje punkty", f"{p_val} / 60")
        st.metric("Ocena", o_val)
    except:
        st.error("Błąd odczytu danych.")
    st.markdown('</div>', unsafe_allow_html=True)