import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
            .stApp { background-color: #f0f7ff; }
            .table-container {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.05);
                margin-top: 20px;
            }
            .tales-table { 
                width: 100%; border-collapse: collapse; 
                font-family: sans-serif; font-size: 13px; 
            }
            .tales-table thead th { 
                background-color: #e1e9f5 !important; 
                color: #2c3e50; border: 1px solid #c8d6e5 !important; 
                padding: 10px 5px; text-align: center; vertical-align: middle;
            }
            .tales-table td { border: 1px solid #eee; padding: 8px; text-align: center; }
            .tales-table tr:nth-child(even) { background-color: #fcfdfe; }
            .stButton>button { border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)