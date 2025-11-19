import pandas as pd

pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', None)

def transform_data(df: pd.DataFrame):
#     """
#     Cleans and transforms the sales dataset.
#     Steps include:
#     - Checking for missing values
#     - Checking for duplicate rows
#     - Handling negative values
#     - Creating new calculated columns
#     - Returning a cleaned DataFrame
#     """

    if df is None:
     print("DataFrame is None. Cannot proceed.")
     return None

    df_transformed = df.copy()

    # print ("==========check duplicates=========")
    dup_count = df_transformed.duplicated().sum()
    if dup_count > 0:
        df_transformed.drop_duplicates(inplace=True)
        # print(f"{dup_count} Duplicate rows removed.")

    # print ("======= Missing values chek ==========")
    # missing_values =df_transformed.isnull().sum().sort_values(ascending=False)
    # missing_values=missing_values[missing_values > 0]
    # print(missing_values)

    # print ("======= Fill Missing Value For ShippingCost ==========")
    median_shipping = df_transformed['ShippingCost'].median()
    df_transformed['ShippingCost'] = df_transformed['ShippingCost'].fillna(median_shipping)
    # print(f"Filled ShippingCost missing values with median value: {median_shipping}")
    df_transformed['CustomerID'] = df_transformed['CustomerID'].fillna(-1).astype(int)
    # print(df_transformed['CustomerID'].dtype)
    # print("Filled CustomerID missing values with -1")

    df_transformed['WarehouseLocation']=df_transformed['WarehouseLocation'].fillna('Unknown')
    # print("Filled WarehouseLocation missing values with 'unknown'")

    # print ("======= Check data ==========")
    # print(df_transformed.describe())
    # print("Checking negative UnitPrice rules...")
    # total_observations_price  = len(df_transformed)
    # print(f"The dataset consists of {total_observations_price} rows")
    # # Filter rows with negative unit price
    # Negative_Price = df_transformed[df_transformed['UnitPrice'] < 0]
    # Check unit price by returnStatus
    #  print(Negative_Price["ReturnStatus"].value_counts())
    # # Filter unit price positive or returned
    df_transformed = df_transformed[
    (df_transformed["UnitPrice"] >= 0) |
    (df_transformed["ReturnStatus"].str.lower() == "returned")
    ]
   #  removed_unit_price = total_observations_price - len(df_transformed)
   #  print(f"Removed {removed_unit_price} invalid negative UnitPrice rows.")

   #  print("Checking negative Quantity rules...")
   #  total_observations_quantity = len(df_transformed)
   #  print(f"The dataset consists of {total_observations_quantity} rows")
   # #  # Filter rows with negative quantity
   #  negative_qty = df_transformed[df_transformed["Quantity"] < 0]
   # # Check quantity by returnStatus
   #  print(negative_qty["ReturnStatus"].value_counts())
   # # Filter quantity positive or returned
    df_transformed = df_transformed[
    (df_transformed["Quantity"] >= 0) |
    (df_transformed["ReturnStatus"].str.lower() == "returned")
    ]
   #  removed_quantity = total_observations_quantity - len(df_transformed)
   #  print(f"Removed {removed_quantity} invalid negative quantity rows.")

    #  # convert InvoiceDate to type datetime from object and check min and max value
    df_transformed['InvoiceDate'] = pd.to_datetime(df_transformed['InvoiceDate'], errors='coerce')
    # print(df_transformed['InvoiceDate'].dtype)
    # print(f"InvoiceDate ranges from {df_transformed['InvoiceDate'].min().strftime('%Y-%m-%d')} "
    # f"to {df_transformed['InvoiceDate'].max().strftime('%Y-%m-%d')}")

    #  print ("=======Create calculated columns==========")
    df_transformed['TotalPrice'] = df_transformed['Quantity'] * df_transformed['UnitPrice']
    df_transformed['IsReturn'] = (df_transformed['ReturnStatus'].str.lower() == "returned").astype(int)
    df_transformed['NetSales'] = ((df_transformed['TotalPrice'] * (1 - df_transformed['Discount']))
                                  + df_transformed['ShippingCost'])
    df_transformed['IsCreditNote'] = ((df_transformed['UnitPrice'] < 0) &
                                      (df_transformed['ReturnStatus'].str.lower() == "returned")).astype(int)
    df_transformed['Year'] = df_transformed['InvoiceDate'].dt.year

    # print(df_transformed.info())
    # print(df_transformed.sort_values(by=['Is_Credit_Note'],ascending=False).head(10))

    # Get the new dimensions
    new_rows, new_cols = df_transformed.shape
   # Print the requested English statement with the new dimensions

    print("=" * 50 + "\n" +
      "Data transformation and cleaning completed successfully.\n" +
      f"Resulting dataset contains {new_rows} rows and {new_cols} columns."
     )

    return df_transformed











