
import pandas as pd
from pathlib import Path


# Define Paths
BASE_DIR = PATH(__file__).resolve().parent.parent
OUTPUT_BASE_PATH = BASE_DIR / "output"  # לא יוצר תיקייה
INPUT_FILE = OUTPUT_BASE_PATH / "cleaned_data.csv"
SUMMARY_FILE = OUTPUT_BASE_PATH / "summary.csv"
# KPI value formatting
def format_kpi_value(row):
    """
    Formats the raw numerical KPI value ,
    based on the KPI Name in the current row.
       """
    value = row['Value']
    name = row['KPI Name']

    # Formatting rates
    if 'Rate' in name:
        # Use :.2% for professional presentation )
        return f"{value:.2%}"

    # Formatting Total Net Sales value
    elif 'Sales' in name:

        return f"{value:,.0f}"
    elif 'Average' in name or 'Per Customer' in name:
        return f"{value:.2f}"
    # Formatting other integers
    else:
        # Use round() for safe
        return f"{round(value):,}"

def generate_kpi_summary(df, format_func):
        """
        Calculates all defined KPIs from the transformed DataFrame and saves them
        to the specified summary CSV file path.
        """
        #  KPI CALCULATIONS

        Kpi_total_net_sales = df['NetSales'].sum().astype(int)
        Kpi_total_orders = df['InvoiceNo'].nunique()
        Kpi_return_rate = (df['IsReturn'].mean())
        Kpi_credit_note_rate = (df['IsCreditNote'].mean())
        Kpi_unique_customers = df['CustomerID'].nunique()
        Kpi_orders_per_customer = Kpi_total_orders / Kpi_unique_customers
        Kpi_total_quantity_sold = df['Quantity'].sum()
        Kpi_average_order_value = Kpi_total_net_sales / Kpi_total_orders
        Kpi_average_net_item_price = Kpi_total_net_sales / Kpi_total_quantity_sold
        Kpi_total_return_value = df[df['IsReturn'] == 1]['NetSales'].sum().astype(int)


        #  Create and Save summary.csv
        Kpi_df = pd.DataFrame({
            "KPI Name": [
                "Total Net Sales",
                "Unique Orders",
                "Return Rate (%)",
                "Credit Note Rate (%)",
                "Unique Customers",
                "Total Quantity Sold",
                "Average Order Value",
                "Average Net Item Price",
                "Orders Per Customer",
                "Total Return Value",
            ],
            "Value": [
                Kpi_total_net_sales,
                Kpi_total_orders,
                Kpi_return_rate,
                Kpi_credit_note_rate,
                Kpi_unique_customers,
                Kpi_total_quantity_sold,
                Kpi_average_order_value,
                Kpi_average_net_item_price,
                Kpi_orders_per_customer,
                Kpi_total_return_value
            ]
        })
        Kpi_df['Value'] = Kpi_df.apply(format_kpi_value, axis=1)
        Kpi_df.to_csv(SUMMARY_FILE, index=False)
        print("=" * 50 + "\n" +
         f"KPI summary saved in path {SUMMARY_FILE}")
