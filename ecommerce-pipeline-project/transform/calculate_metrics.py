import pandas as pd
import os
from rich.console import Console

# Initialize console for rich text output
console = Console()

def calculate_average_order_value(orders_df: pd.DataFrame, payments_df: pd.DataFrame) -> float:
    """
    Calculate the average amount spent per order.
    
    Formula: Average Order Value = Total Revenue / Number of Orders
    
    Args:
        orders_df (pd.DataFrame): DataFrame containing order information
        payments_df (pd.DataFrame): DataFrame containing payment information
        
    Returns:
        float: Average order value
    """
    # Calculate total revenue from all payments
    total_revenue = payments_df['payment_value'].sum()
    
    # Count unique orders to avoid duplicates
    number_of_orders = orders_df['order_id'].nunique()
    
    # Calculate the average value per order
    average_order_value = total_revenue / number_of_orders
    
    return average_order_value

def analyze_reviews_by_state(customers_df: pd.DataFrame, reviews_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze review scores by customer state.
    
    Args:
        customers_df (pd.DataFrame): DataFrame containing customer information
        reviews_df (pd.DataFrame): DataFrame containing review information
        
    Returns:
        pd.DataFrame: Review score distribution by state
    """
    # Merge customer and review data using customer_id as key
    merged_df = pd.merge(customers_df, reviews_df, on='customer_id')
    
    # Create a pivot table of review scores by state
    review_distribution = merged_df.groupby(['customer_state', 'review_score']).size().unstack(fill_value=0)
    
    # Calculate total number of reviews for each state
    review_distribution['total_reviews'] = review_distribution.sum(axis=1)
    
    # Calculate weighted average review score for each state
    review_distribution['average_score'] = (
        review_distribution[1] * 1 + 
        review_distribution[2] * 2 + 
        review_distribution[3] * 3 + 
        review_distribution[4] * 4 + 
        review_distribution[5] * 5
    ) / review_distribution['total_reviews']
    
    return review_distribution

def analyze_shipping_by_month(items_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze shipping data by month.
    
    Args:
        items_df (pd.DataFrame): DataFrame containing order items information
        
    Returns:
        pd.DataFrame: Shipping analysis by month
    """
    # Convert shipping limit date to datetime format
    items_df['shipping_limit_date'] = pd.to_datetime(items_df['shipping_limit_date'])
    
    # Extract month and year components
    items_df['month'] = items_df['shipping_limit_date'].dt.month
    items_df['year'] = items_df['shipping_limit_date'].dt.year
    
    # Create a combined month-year column for better analysis
    items_df['month_year'] = items_df['shipping_limit_date'].dt.strftime('%Y-%m')
    
    # Calculate monthly statistics
    monthly_stats = items_df.groupby('month_year').agg({
        'order_id': 'count',          # Count number of orders
        'price': 'sum',               # Sum of all prices
        'freight_value': 'sum'        # Sum of all freight values
    }).rename(columns={
        'order_id': 'number_of_orders',
        'price': 'total_sales',
        'freight_value': 'total_freight'
    })
    
    # Calculate average order value for each month
    monthly_stats['average_order_value'] = monthly_stats['total_sales'] / monthly_stats['number_of_orders']
    
    return monthly_stats

def main():
    try:
        # Get the absolute path to the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(project_root, 'data')
        
        # Load all required datasets
        orders_df = pd.read_csv(os.path.join(data_dir, 'olist_orders_dataset.csv'))
        payments_df = pd.read_csv(os.path.join(data_dir, 'olist_order_payments_dataset.csv'))
        customers_df = pd.read_csv(os.path.join(data_dir, 'olist_customers_dataset.csv'))
        reviews_df = pd.read_csv(os.path.join(data_dir, 'olist_order_reviews_dataset.csv'))
        items_df = pd.read_csv(os.path.join(data_dir, 'olist_order_items_dataset.csv'))
        
        # Calculate and display average order value
        avg_order_value = calculate_average_order_value(orders_df, payments_df)
        console.print("\n[bold blue]Order Analysis Results:[/bold blue]")
        console.print(f"[green]Average Order Value:[/green] ${avg_order_value:.2f}")
        
        # Display additional order statistics
        console.print("\n[bold blue]Additional Statistics:[/bold blue]")
        console.print(f"[green]Total Revenue:[/green] ${payments_df['payment_value'].sum():.2f}")
        console.print(f"[green]Total Number of Orders:[/green] {orders_df['order_id'].nunique():,}")
        
        # Analyze and display payment method distribution
        payment_methods = payments_df['payment_type'].value_counts()
        console.print("\n[bold blue]Payment Method Distribution:[/bold blue]")
        for method, count in payment_methods.items():
            console.print(f"[cyan]{method}:[/cyan] {count:,} orders")
        
        # Analyze and display review distribution by state
        console.print("\n[bold blue]Review Analysis by State:[/bold blue]")
        review_distribution = analyze_reviews_by_state(customers_df, reviews_df)
        console.print(review_distribution)
        
        # Analyze and display shipping statistics by month
        console.print("\n[bold blue]Monthly Shipping Analysis:[/bold blue]")
        monthly_stats = analyze_shipping_by_month(items_df)
        console.print(monthly_stats)
        
    except Exception as e:
        # Handle and display any errors that occur during execution
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        raise

if __name__ == "__main__":
    main() 