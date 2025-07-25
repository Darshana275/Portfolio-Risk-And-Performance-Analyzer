import os
import pandas as pd

def export_statistics_to_excel(stats_dicts,
                               export_path="Excels",
                               file_name="portfolio_statistics.xlsx"):
    os.makedirs(export_path, exist_ok=True)
    output_file = os.path.join(export_path, file_name)

    with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
        for interval, stats in stats_dicts.items():
            df = pd.DataFrame.from_dict(stats, orient="index").T
            df.index.name = "Statistic"
            df.to_excel(writer, sheet_name=f"{interval}_Statistics", startrow=0, startcol=0)

            workbook = writer.book
            worksheet = writer.sheets[f"{interval}_Statistics"]

            # Number formats
            format_two_decimals = workbook.add_format({'num_format': '0.00'})
            format_five_decimals = workbook.add_format({'num_format': '0.00000'})

            # Adjust column A width (Statistic names)
            max_stat_len = max(len(str(stat)) for stat in df.index)
            worksheet.set_column('A:A', max_stat_len + 2)

            # Format data and adjust column widths
            for col_num in range(1, df.shape[1] + 1):
                max_width = len(str(df.columns[col_num - 1]))

                for row_num in range(df.shape[0]):
                    value = df.iloc[row_num, col_num - 1]

                    try:
                        # Convert safely to float using .item() if possible
                        float_value = value.item() if hasattr(value, "item") else float(value)
                        cell_format = format_two_decimals if row_num == 0 else format_five_decimals
                        worksheet.write_number(row_num + 1, col_num, float_value, cell_format)

                        # Estimate column width based on formatted string
                        formatted_value = f"{float_value:.2f}" if row_num == 0 else f"{float_value:.5f}"
                        max_width = max(max_width, len(formatted_value))

                    except Exception:
                        str_value = str(value)
                        worksheet.write(row_num + 1, col_num, str_value)
                        max_width = max(max_width, len(str_value))

                worksheet.set_column(col_num, col_num, max_width + 2)

    print(f"\n[3]✅ Exported full analysis to Excel: {output_file}")
