import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

sns.set_theme(style="whitegrid")

def plot_statistics(stats_dicts, asset_data, save_folder="graphs"):
    """
    Visualize risk and return metrics with Seaborn and Matplotlib and save plots.
    
    stats_dicts: dict -> Output from analyze_log_return_statistics()
    asset_data: dict -> Original asset price data for distribution and time-series plots
    save_folder: str -> Folder to save the graphs
    """

    # Create save folder if not exists
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Convert nested dictionary to DataFrame
    data = []
    for interval, assets in stats_dicts.items():
        for asset, metrics in assets.items():
            row = {"Interval": interval, "Asset": asset}
            row.update(metrics)
            data.append(row)
    df = pd.DataFrame(data)

    # Melt for plotting
    metrics_list = ["Mean Return", "Standard Deviation", "VaR 95%", "ES 95%", "CAGR", "Max Drawdown"]
    df_melt = df.melt(id_vars=["Interval", "Asset"], value_vars=metrics_list,
                      var_name="Metric", value_name="Value")

    # Clean types and drop NaN
    df_melt.dropna(subset=["Value"], inplace=True)
    df_melt["Interval"] = df_melt["Interval"].astype(str)
    df_melt["Asset"] = df_melt["Asset"].astype(str)
    df_melt["Value"] = pd.to_numeric(df_melt["Value"], errors="coerce")

    # ================================
    # 1. Barplots for Mean Return
    # ================================
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Interval", y="Value", hue="Asset",
                data=df_melt[df_melt["Metric"] == "Mean Return"], palette="Set2")
    plt.title("Mean Log Return across Intervals")
    plt.ylabel("Mean Return")
    plt.savefig(os.path.join(save_folder, "mean_return.png"))
    plt.close()

    # Barplots for Standard Deviation
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Interval", y="Value", hue="Asset",
                data=df_melt[df_melt["Metric"] == "Standard Deviation"], palette="coolwarm")
    plt.title("Standard Deviation across Intervals")
    plt.ylabel("Standard Deviation")
    plt.savefig(os.path.join(save_folder, "std_deviation.png"))
    plt.close()

    # ================================
    # 2. Lineplot for VaR & ES (95%)
    # ================================
    plt.figure(figsize=(12, 6))
    sns.lineplot(x="Interval", y="Value", hue="Asset", style="Metric",
                 data=df_melt[df_melt["Metric"].isin(["VaR 95%", "ES 95%"])],
                 markers=True, dashes=False, palette="tab10")
    plt.title("VaR & ES (95%) across Intervals")
    plt.ylabel("Risk Value")
    plt.savefig(os.path.join(save_folder, "var_es.png"))
    plt.close()

    # ================================
    # 3. Barplot for CAGR & Max Drawdown
    # ================================
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Interval", y="Value", hue="Metric",
                data=df_melt[df_melt["Metric"].isin(["CAGR", "Max Drawdown"])],
                palette="Paired")
    plt.title("CAGR and Max Drawdown across Intervals")
    plt.ylabel("Value")
    plt.savefig(os.path.join(save_folder, "cagr_drawdown.png"))
    plt.close()

    # ================================
    # 4. Correlation Heatmap
    # ================================
    plt.figure(figsize=(10, 6))
    df_numeric = df[metrics_list].apply(pd.to_numeric, errors="coerce")
    corr = df_numeric.corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation of Risk & Return Metrics")
    plt.savefig(os.path.join(save_folder, "correlation_heatmap.png"))
    plt.close()

    # ================================
    # 5. Distribution Plots for Log Returns
    # ================================
    for asset, df_asset in asset_data.items():
        df_asset = df_asset.copy()
        df_asset["Log_Return"] = df_asset["Close"].pct_change().apply(lambda x: np.log(1 + x))
        df_asset.dropna(inplace=True)

        plt.figure(figsize=(10, 5))
        sns.histplot(df_asset["Log_Return"], kde=True, color="blue", bins=50)
        plt.title(f"Distribution of Daily Log Returns - {asset}")
        plt.xlabel("Log Return")
        plt.ylabel("Frequency")
        plt.savefig(os.path.join(save_folder, f"{asset}_log_return_distribution.png"))
        plt.close()

    # ================================
    # 6. Time Series of Cumulative Returns
    # ================================
    plt.figure(figsize=(12, 6))
    for asset, df_asset in asset_data.items():
        df_asset = df_asset.copy()
        df_asset["Cumulative_Return"] = (df_asset["Close"] / df_asset["Close"].iloc[0]) - 1
        plt.plot(df_asset["Date"], df_asset["Cumulative_Return"], label=asset)
    plt.title("Cumulative Returns Over Time")
    plt.ylabel("Cumulative Return")
    plt.xlabel("Date")
    plt.legend()
    plt.savefig(os.path.join(save_folder, "cumulative_returns.png"))
    plt.close()

    return df, df_melt
