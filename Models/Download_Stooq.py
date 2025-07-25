import pandas as pd

# Function to download historical data from Stooq
def download_stooq(ticker, start_date, end_date, interval="d"):
    print(f"Downloading data from Stooq: {ticker}")

    # Convert start and end dates to Stooq format (YYYYMMDD)
    d1 = pd.to_datetime(start_date).strftime("%Y%m%d")
    d2 = pd.to_datetime(end_date).strftime("%Y%m%d")

    # Build the download URL
    url = f"https://stooq.pl/q/d/l/?s={ticker}&d1={d1}&d2={d2}&i={interval}"

    try:
        # Read CSV data directly from the URL
        df = pd.read_csv(url)

        # Normalize column names
        df.columns = [col.lower() for col in df.columns]

        # Map common column names
        date_col = 'data' if 'data' in df.columns else 'date'
        close_col = 'zamkniecie' if 'zamkniecie' in df.columns else 'close'
        volume_col = 'wolumen' if 'wolumen' in df.columns else 'volume'

        # Check if required columns are present
        required_cols = [date_col, close_col, volume_col]
        for col in required_cols:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        # Select and rename relevant columns
        df = df[[date_col, close_col, volume_col]]
        df.columns = ['Date', 'Close', 'Volume']

        # Convert date column to datetime and sort the data chronologically
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date').reset_index(drop=True)

        return df

    except Exception as e:
        print(f"❌ Error while downloading data from Stooq for {ticker}: {e}")
        return pd.DataFrame()
