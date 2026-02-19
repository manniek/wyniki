import streamlit as st

def apply_styles():
    st.markdown("""
    <style>
    /* 1. STYLE OGÓLNE (KOMPUTER) */
    .stApp {
        background-color: #f8f9fa;
    }

    /* 2. STYLO WANIE DLA TELEFONU (AUTOMATYCZNE) */
    @media (max-width: 768px) {
        /* Wymuszamy bardzo ciemny tekst, żeby był widoczny na jasnym tle */
        .stApp, .stMarkdown, p, span, label, h1, h2, h3 {
            color: #111111 !important;
        }
        
        /* Naprawiamy tabele, żeby nie uciekały za ekran */
        .stDataFrame, div[data-testid="stTable"] {
            width: 100% !important;
            overflow-x: auto;
        }

        /* Dodajemy tło pod sekcje, żeby odciąć je od reszty */
        div[data-testid="stVerticalBlock"] > div {
            background-color: #ffffff !important;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            border: 1px solid #dddddd;
        }
    }
    /* --- POPRAWKI MOBILNE --- */
    @media (max-width: 768px) {
        /* Biały tekst na przyciskach (Zaloguj/Wyloguj) */
        button p, button span {
            color: #ffffff !important;
        }

        /* Wymuszenie czarnego tekstu dla formułek i opisów */
        .stMarkdown, p, span, label {
            color: #111111 !important;
        }

        /* Specyficzna poprawka dla komunikatów typu st.info / st.warning */
        div[data-testid="stNotificationContent"] p {
            color: #111111 !important;
        }
    }
    /* Celujemy prosto w kontenery powiadomień (st.info, st.warning itp.) */
    div[data-testid="stNotification"] {
        background-color: #f0f2f6 !important; /* Jasnoszare tło dla ramki */
        border: 1px solid #d1d5db !important;
    }

    /* Wymuszamy czarny kolor dla tekstu wewnątrz KAŻDEGO rodzaju powiadomienia */
    div[data-testid="stNotification"] p, 
    div[data-testid="stNotification"] div,
    .stAlert p {
        color: #000000 !important;
        font-weight: 600 !important; /* Pogrubienie, żeby było lepiej widać */
    }
    </style>
    """, unsafe_allow_html=True)


