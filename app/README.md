# Python Financial Analysis
An interactive financial analytics dashboard built with Python and Streamlit. It fetches real stock market data, computes risk and return metrics, generates analyst-style insights, and visualizes everything in a clean, themeable interface inspired by professional trading terminals.

Overview
This dashboard helps analyze and compare stocks through a single interactive interface. Users can select any combination of tracked stocks, view performance and risk metrics, read auto-generated market commentary, and explore price action through candlestick and trend charts. The interface supports both dark and light themes.

Features

Live & historical data fetched via the yFinance API
Multi-stock comparison with an interactive selector
Key metrics — total return, annualized volatility, and Sharpe ratio
KPI cards highlighting the best performer and most volatile asset
Market intelligence panel — analyst-style insights generated automatically from the data
Interactive candlestick chart for detailed price action
Price trend & relative performance charts
30-day trend projection using a statistical regression model
Analyst summary table with sortable columns
Dark / Light theme toggle applied across the entire interface


Tech Stack
LayerToolsDashboard / UIStreamlitData AnalysisPandas, NumPyVisualizationPlotlyMarket DatayFinance

Project Structure
financial-dashboard/
├── app/
│   └── dashboard.py          # Main Streamlit dashboard
├── scripts/
│   ├── get_data.py           # Fetches and saves stock data
│   ├── analyze.py            # Standalone analytics
│   └── charts.py             # Standalone visualizations
├── data/
│   └── close_prices.csv      # Saved historical price data
├── .streamlit/
│   └── config.toml           # Theme configuration
├── requirements.txt          # Project dependencies
└── README.md

Getting Started
1. Clone the repository
bashgit clone https://github.com/Avi-1104/financial-dashboard.git
cd financial-dashboard
2. Create and activate a virtual environment
bashpython -m venv venv
# Windows
.\venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate
3. Install dependencies
bashpip install -r requirements.txt
4. Fetch the latest market data
bashpython scripts/get_data.py
5. Launch the dashboard
bashstreamlit run app/dashboard.py
The dashboard will open automatically in your browser.

Key Metrics Explained

Total Return — the percentage change in price over the analyzed period.
Volatility — annualized standard deviation of daily returns; a measure of risk.
Sharpe Ratio — return earned per unit of risk taken; higher values indicate more efficient performance.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Open%20App-success?style=for-the-badge)](https://python-financial-analysis-efbytlwecddi8lldbk4rrw.streamlit.app/)

**[▶ Open the live dashboard](https://python-financial-analysis-efbytlwecddi8lldbk4rrw.streamlit.app/)** — no installation needed.

Disclaimer
This project is for educational and analytical purposes only. The trend projection is a simple statistical estimate and does not constitute financial advice. Markets are influenced by many factors that no simple model can predict.
