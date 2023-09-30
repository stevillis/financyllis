from datetime import date

import investpy as inv
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
import yfinance as yf

MENU_ITEMS = ["Home", "Panorama do Mercado", "Mapa Mensal", "Fundamentos"]


def home():
    col1, col2, col3 = st.columns([1, 2, 3])
    with col1:
        st.image("logo_financyllis_transparent_bg.png", width=100)
    with col2:
        st.title("Financyllys")

    st.header("An app for financial analysis")


def overview():
    pass


def monthly_map():
    pass


def fundamentals():
    pass


def main():
    st.sidebar.image("logo_financyllis_transparent_bg.png", width=100)
    st.sidebar.title("Financyllis")
    st.sidebar.markdown("---")

    menu_choice = st.sidebar.radio("Escolha a opção", MENU_ITEMS)

    if menu_choice == MENU_ITEMS[0]:  # Home
        home()
    if menu_choice == MENU_ITEMS[1]:  # Panorama do Mercado
        overview()
    if menu_choice == MENU_ITEMS[2]:  # Mapa Mensal
        monthly_map()
    if menu_choice == MENU_ITEMS[3]:  # Fundamentos
        fundamentals()


if __name__ == "__main__":
    main()
