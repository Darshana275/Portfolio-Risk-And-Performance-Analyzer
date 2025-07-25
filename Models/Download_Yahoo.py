import yfinance as yf
import pandas as pd

def download_yahoo(ticker, start_date, end_date, interval="1d"):
    print(f"Downloading from Yahoo Finance: {ticker}")

    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        df.reset_index(inplace=True)

        # Keep only standard column names
        df = df[['Date', 'Close', 'Volume']]  # Leave as-is for consistency
        df.dropna(inplace=True)
        df = df.sort_values('Date').reset_index(drop=True)

        return df

    except Exception as e:
        print(f"❌ Error downloading {ticker} from Yahoo: {e}")
        return pd.DataFrame()
