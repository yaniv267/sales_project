from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data_to_csv
from etl.kpi import generate_kpi_summary, format_kpi_value
from etl.plot import plot_sales_over_time,plot_top_net_sales_products,plot_top_returned_products

def main ():

    # Step 1: Extract
    df = extract_data()
    if df is None:
        return


    # Step 2: Transform
    df_transformed = transform_data(df)

    # Step 3: Load
    load_data_to_csv(df_transformed, "cleaned_data.csv")

    # Step 4: Generate KPI
    generate_kpi_summary(df_transformed,format_kpi_value)

    # Step 5: Plots
    plot_sales_over_time(df_transformed)
    plot_top_net_sales_products(df_transformed)
    plot_top_returned_products(df_transformed)

    # Personal message
    print("===" * 50)
    print("Shiran Alon. Thank you for your guidance and support!")
    pass

if __name__ == "__main__":
    main()