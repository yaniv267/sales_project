import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# --- General Plot Settings
sns.set_style("whitegrid")
plt.rcParams['axes.unicode_minus'] = False

def plot_sales_over_time(df, CHARTS_DIR="output/charts"):
    """
    Plots the quarterly Net Sales trend using the
     "InvoiceDate" and "NetSales" columns.
    """
    #  Prepare data
    df['InvoiceQuarter'] = df['InvoiceDate'].dt.to_period('Q').astype(str)
    quarterly_sales = df.groupby('InvoiceQuarter')['NetSales'].sum().reset_index()

    plt.figure(figsize=(14, 6))
    ax = sns.lineplot(
        data=quarterly_sales,
        x='InvoiceQuarter',
        y='NetSales',
        marker='o',
        color='skyblue'
    )

    #  X-axis
    labels = quarterly_sales['InvoiceQuarter'].tolist()
    ax.set_xticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha='right')

    #  Titles and labels
    plt.title('Quarterly Net Sales Trend', fontsize=16)
    plt.xlabel('Quarter/Year')
    plt.ylabel('Net Sales')
    plt.tight_layout()

    #  Save chart
    start_quarter = quarterly_sales['InvoiceQuarter'].min()
    end_quarter = quarterly_sales['InvoiceQuarter'].max()
    output_file = os.path.join(CHARTS_DIR, f'Net_Sales_{start_quarter}_to_{end_quarter}.png')
    plt.savefig(output_file)
    plt.close()

    print("=" * 50 + "\n" +
          f"[PLOT] Generated: 1 Quarterly Net Sales Trend from {start_quarter} to {end_quarter}")
def plot_top_net_sales_products(df, CHARTS_DIR="output/charts"):
    """
    Plots Top 10 products by Net Sales..
    - using 'Description'' columns
    """
    # Filter positive NetSales and get top 10
    top_products_df = (
        df[df['NetSales'] > 0]
        .groupby('Description')['NetSales']
        .sum()
        .nlargest(10)
        .sort_values(ascending=True)
        .reset_index()
    )

    # Plot
    plt.figure(figsize=(10, 7))
    ax=sns.barplot(data=top_products_df,
                x='NetSales',
                y='Description',
                hue='Description',
                palette="viridis",
                legend = False)

    #  Add value labels at the end of each bar
    for container in ax.containers:
        ax.bar_label(container, fmt='{:,.0f}', padding=5)
    # Titles and Saving
    plt.title('Top 10 Products by Net Sales ', fontsize=16)
    plt.xlabel('Total Net Sales (in Millions)')
    plt.ylabel('Product Description')
    ax.set_xlim(right=top_products_df['NetSales'].max() * 1.15)
    plt.tight_layout()
    # Save chart
    os.makedirs(CHARTS_DIR, exist_ok=True)
    output_file = os.path.join(CHARTS_DIR, 'Top_10_Products_By_NetSales.png')
    plt.savefig(output_file)
    plt.close()
    print("[PLOT] Generated 2. Top 10 Products by Net Sales")

def plot_top_returned_products(df, CHARTS_DIR="output/charts"):
        """
         Plots Top 10 most frequently returned products.
         using 'Description' and 'IsReturn' columns
         """
        #  Group and sum the IsReturn flag
        # --- Prepare data ---
        # Prepare top 10 returns
        top_returns_df = (
            df.groupby('Description')['IsReturn']
            .sum()
            .nlargest(10)
            .sort_values(ascending=True)
            .reset_index(name='ReturnCount')
        )
        # --- Plot ---
        plt.figure(figsize=(10, 7))
        ax = sns.barplot(data=top_returns_df,
                         x='ReturnCount',
                         y='Description',
                         hue='Description',
                         palette="autumn",
                         legend=False)
        #  Add  value labels
        for container in ax.containers:
            ax.bar_label(container, fmt='{:,.0f}', padding=5)
        #  Titles and Saving
        plt.title('Top 10 Most Frequent Returns (by Product Description )', fontsize=16)
        plt.xlabel('Total Return Product Description')
        plt.ylabel('Product Description')
        plt.tight_layout()
        # Save chart
        output_file = os.path.join(CHARTS_DIR, 'Top_10_Returned_Products')
        plt.savefig(output_file)
        plt.close()
        print(f"[PLOT] Generated 3: Top 10 Returned Products")

        print(f"[PLOT] All charts are located at the path: {CHARTS_DIR}")
