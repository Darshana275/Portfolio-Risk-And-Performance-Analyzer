from Models.Config import Config
from Models.Download_Stooq import download_stooq
from Models.Download_Yahoo import download_yahoo
from Models.Portfolio_analysis import analyze_log_return_statistics
from Models.Export_excel import export_statistics_to_excel

import pandas as pd

def main():

    print("\n[1]✅ Downloading data...")
    asset_data = {}

    for asset in Config["assets"]:
        print(f"Downloading data for: {asset['name']}")

        if asset["source"] == "yfinance":
            df = download_yahoo(
                ticker=asset["ticker"],
                start_date=Config["start_date"],
                end_date=Config["end_date"],
                interval=asset["interval"]
            )
        elif asset["source"] == "stooq":
            df = download_stooq(
                ticker=asset["ticker"],
                start_date=Config["start_date"],
                end_date=Config["end_date"],
                interval=asset["interval"]
            )
        else:
            print(f"❌ Unknown data source for {asset['name']}")
            continue

        if not df.empty:
            asset_data[asset["name"]] = df
        else:
            print(f"❌ Data for {asset['name']} is empty and will be skipped.")

    # 2. Analyze statistics for all defined intervals
    stats_dicts = analyze_log_return_statistics(asset_data)

    # 3. Export to Excel with all intervals as separate sheets
    export_statistics_to_excel(stats_dicts)

# Run the function
main()