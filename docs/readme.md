# Financial Dashboard – Visualization Market Data OHLC

---

## INTRODUCTION

**Project developed in Python**

Dashboard template to streaming real-time FX EURUSD OHLC market data from **Interactive Brokers (IBAPI)** for customizable applications.

This is a **demo version** and certain files or logic were intentionally excluded due to confidentiality agreements.

The original project was developed to a private company of Algorithmic Trading.

---

## RESUME

Flexible and scalable Dashboard-based architecture capable of real time market data visualization

Both backend and frontend layers are intentionally modular, allowing the server to adapt to various market data providers, dashboard frameworks.

This enables the solution to scale according to customer development.

Suitable for different business or project requirements.

---

## FUNCIONALITY

- Overlay SMA Close windows [3, 5, 8]m.
- Subpanel: RSI, ATR.
- Multi Time Frame
- Multi Instrument (FX, Stocks, CMMDTY, etc.) (each window for every instrument)
- Local Deploy

---

## Technology Stack (Replaceable)

### Backend

- IBAPI
- TA
- Pandas / NumPy

## Frontend

- Bokeh

### Optional Integrations (Examples)

- Polygon.io
- Alpaca Markets
- Crypto WebSocket feeds
- Cloud Server
- Dash
- Ploty
- Streamlit
- Desktop Versions

> **NOTE:** Both backend and frontend can be replaced or extended depending on customer needs. Also programming languages.

---

## Possible Uses & Custom Modifications

- Custom Technical Indicators
- Portfolio Monitoring & Risk Tools
- Market Analytics
- News & Sentiment Feeds

---
