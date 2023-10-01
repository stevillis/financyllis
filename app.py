from datetime import date

import investpy as inv
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
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
    st.title("Panorama do mercado")
    st.markdown(date.today().strftime("%d/%m/%Y"))

    st.subheader("Mercados pelo Mundo")

    # Download tickers
    if "assets_df" not in st.session_state:
        tickers = {
            "Bovespa": "^BVSP",
            "S&P500": "^GSPC",
            "NASDAQ": "^IXIC",
            "DAX": "^GDAXI",
            "FTSE 100": "^FTSE",
            "Cruid Oil": "CL=F",
            "Gold": "GC=F",
            "BITCOIN": "BTC-USD",
            "ETHERUM": "ETH-USD",
        }

        assets_df = pd.DataFrame({"Asset": tickers.keys(), "Ticker": tickers.values()})

        assets_df["Last_Value"] = ""
        assets_df["Percentage"] = ""

        placeholder_progress_bar = st.empty()
        with placeholder_progress_bar:
            progress_bar = st.progress(value=0, text="Carregando dados...")

        progress_count = 0
        for index, ticker in enumerate(tickers.values()):
            quotes_df = yf.download(ticker, period="7d")["Adj Close"]
            variation = ((quotes_df.iloc[-1] / quotes_df.iloc[-2]) - 1) * 100

            assets_df["Last_Value"][index] = round(quotes_df.iloc[-1], 2)
            assets_df["Percentage"][index] = round(variation, 2)

            progress_count = round(progress_count + (1 / len(tickers.keys())), 2)
            if progress_count >= 0.99:
                progress_count = 1.0

            progress_bar.progress(progress_count)

        placeholder_progress_bar.empty()  # Removes progress bar after tickers' download is completed
        st.session_state["assets_df"] = assets_df

    assets_df = st.session_state.get("assets_df")

    # Mount tickers' metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        for index in range(3):
            st.metric(
                assets_df["Asset"][index],
                value=assets_df["Last_Value"][index],
                delta=f"{assets_df['Percentage'][index]}%",
            )

    with col2:
        for index in range(3, 6):
            st.metric(
                assets_df["Asset"][index],
                value=assets_df["Last_Value"][index],
                delta=f"{assets_df['Percentage'][index]}%",
            )

    with col3:
        for index in range(6, 9):
            st.metric(
                assets_df["Asset"][index],
                value=assets_df["Last_Value"][index],
                delta=f"{assets_df['Percentage'][index]}%",
            )

    # Índices
    st.markdown("---")
    st.subheader("Comportamento durante o dia")

    daily_indexes_list = ["IBOV", "S&P500", "NASDAQ"]
    daily_index = st.selectbox("Selecione o Índice", daily_indexes_list)

    if daily_index == "IBOV":
        daily_index_df = yf.download("^BVSP", period="1d", interval="5m")
    if daily_index == "S&P500":
        daily_index_df = yf.download("^GSPC", period="1d", interval="5m")
    if daily_index == "NASDAQ":
        daily_index_df = yf.download("^IXIC", period="1d", interval="5m")

    fig_daily_index = go.Figure(
        data=[
            go.Candlestick(
                x=daily_index_df.index,
                open=daily_index_df["Open"],
                high=daily_index_df["High"],
                low=daily_index_df["Low"],
                close=daily_index_df["Close"],
            )
        ]
    )

    fig_daily_index.update_layout(title=daily_index, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig_daily_index)

    # Ações
    st.markdown("---")
    st.subheader("Ações")

    financial_actions_list = ["PETR4.SA", "VALE3.SA", "EQTL3.SA", "CSNA3.SA"]
    financial_action = st.selectbox("Selecione a Ação", financial_actions_list)

    financial_action_df = yf.download(financial_action, period="1d", interval="5m")

    fig_financial_action = go.Figure(
        data=[
            go.Candlestick(
                x=financial_action_df.index,
                open=financial_action_df["Open"],
                high=financial_action_df["High"],
                low=financial_action_df["Low"],
                close=financial_action_df["Close"],
            )
        ]
    )

    fig_financial_action.update_layout(
        title=financial_action, xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig_financial_action)


def monthly_map():
    st.title("Análise de Retornos Mensais")

    with st.expander("Avaliação de Histórico", expanded=True):
        option = st.radio("Selecione", ["Índices", "Ações"])

    if option == "Índices":
        with st.form(key="form_indexes"):
            ticker = st.selectbox(
                "Índice", ["Bovespa", "Financials", "Basic Materials"]
            )
            analyse_button = st.form_submit_button("Analisar")
    else:
        with st.form(key="form_actions"):
            ticker = st.selectbox("Ações", ["PETR4", "EQTL3", "VALE3"])
            analyse_button = st.form_submit_button("Analisar")

    # Implementation stopped because of: https://github.com/alvarobartt/investpy/issues/600
    # if analyse_button:
    # initial_date = "01/12/1999"
    # final_date = "01/10/2023"

    # if option == "Índices":
    #     index_historical_data_df = inv.get_index_historical_data(
    #         ticker, country="brazil", from_date=initial_date, to_date=final_date, interval="Monthly"
    #     )["Close"].pct_change()

    #     st.write(index_historical_data_df)
    # else:
    #     stock_historical_data_df = inv.get_stock_historical_data(
    #         ticker, country="Brazil", from_date=initial_date, to_date=final_date, interval="Monthly"
    #     )["Close"].pct_change()

    #     st.write(stock_historical_data_df)


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
