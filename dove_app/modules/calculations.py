# modules/calculations.py
# Handles core calculation logic for dividend income and portfolio metrics

def calculate_monthly_income(monthly_etfs_df, group1_df, group2_df, group3_df):
    """Calculate monthly income distribution across the year"""
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Monthly ETF income is constant
    monthly_etf_income = monthly_etfs_df['Monthly_Income'].sum()
    
    # Quarterly income varies by month
    group1_quarterly = group1_df['Quarterly_Income'].sum()  # Jan, Apr, Jul, Oct
    group2_quarterly = group2_df['Quarterly_Income'].sum()  # Feb, May, Aug, Nov
    group3_quarterly = group3_df['Quarterly_Income'].sum()  # Mar, Jun, Sep, Dec
    
    # Calculate monthly distribution
    monthly_income = []
    for month in range(12):
        month_income = monthly_etf_income
        if month % 3 == 0:  # Jan, Apr, Jul, Oct
            month_income += group1_quarterly
        elif month % 3 == 1:  # Feb, May, Aug, Nov
            month_income += group2_quarterly
        else:  # Mar, Jun, Sep, Dec
            month_income += group3_quarterly
        monthly_income.append(month_income)
    
    return months, monthly_income, monthly_etf_income, group1_quarterly, group2_quarterly, group3_quarterly

def calculate_portfolio_metrics(monthly_etfs_df, group1_df, group2_df, group3_df, 
                               monthly_etf_income, group1_quarterly, group2_quarterly, group3_quarterly):
    """Calculate key portfolio metrics"""
    # Calculate total investment
    total_investment = (
        monthly_etfs_df['Investment'].sum() + 
        group1_df['Investment'].sum() + 
        group2_df['Investment'].sum() + 
        group3_df['Investment'].sum()
    )
    
    # Calculate annual income
    annual_income = (
        monthly_etf_income * 12 + 
        group1_quarterly * 4 + 
        group2_quarterly * 4 + 
        group3_quarterly * 4
    )
    
    # Calculate average monthly income
    average_monthly_income = annual_income / 12
    
    # Calculate portfolio yield
    portfolio_yield = annual_income / total_investment * 100
    
    return total_investment, annual_income, average_monthly_income, portfolio_yield

def calculate_income_breakdown(monthly_etf_income, group1_quarterly, group2_quarterly, group3_quarterly):
    """Calculate income breakdown by month and source"""
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_etfs = [monthly_etf_income] * 12
    
    group1_income = []
    group2_income = []
    group3_income = []
    total_income = []
    
    for month in range(12):
        # Group 1: Jan, Apr, Jul, Oct (months 0, 3, 6, 9)
        g1_income = group1_quarterly if month % 3 == 0 else 0
        group1_income.append(g1_income)
        
        # Group 2: Feb, May, Aug, Nov (months 1, 4, 7, 10)
        g2_income = group2_quarterly if month % 3 == 1 else 0
        group2_income.append(g2_income)
        
        # Group 3: Mar, Jun, Sep, Dec (months 2, 5, 8, 11)
        g3_income = group3_quarterly if month % 3 == 2 else 0
        group3_income.append(g3_income)
        
        # Total for the month
        total = monthly_etf_income + g1_income + g2_income + g3_income
        total_income.append(total)
    
    return {
        'Month': months,
        'Monthly ETFs': monthly_etfs,
        'Group 1 (Jan/Apr/Jul/Oct)': group1_income,
        'Group 2 (Feb/May/Aug/Nov)': group2_income,
        'Group 3 (Mar/Jun/Sep/Dec)': group3_income,
        'Total': total_income
    }