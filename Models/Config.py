Config = {

    "start_date": "2024-01-01",
    "end_date": "2025-01-01",
    # Choose data time frame for analysis
    "export_path": "Excels",
  
    "assets": [
      {
        "name": "NASDAQ",
        "ticker": "etfbndxpl.pl",
        "source": "stooq", # Or "yfinance" if data is not from stooq
        "interval": "d" # "d" for daily, "w" for weekly, "m" for monthly
      },
      {
        "name": "S&P500",
        "ticker": "etfsp500.pl",
        "source": "stooq",
        "interval": "d"
      },
      {
        "name": "DAX",
        "ticker": "etfdax.pl",
        "source": "stooq",
        "interval": "d"
      },
      {
        "name": "WIG20",
        "ticker": "etfbw20lv.pl",
        "source": "stooq",
        "interval": "d"
      },
      {
        "name": "APPLE",
        "ticker": "AAPL",
        "source": "yfinance",
        "interval": "1d" # "1d" for daily, "1wk" for weekly, "1mo" for monthly
      }
    ]
  }
  
    