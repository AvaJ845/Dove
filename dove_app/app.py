#app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Dividend Income Calculator",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
<style>
    .main {
        padding: 1rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0 0;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4c86b0;
        color: white;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stSlider > div > div > div {
        color: #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)


# Title and introduction
st.title("📈 Dividend Income Calculator")
st.markdown("""
This application helps you track and project dividend income from a portfolio of Dividend Kings, 
Aristocrats, and monthly dividend ETFs. Adjust share quantities to see how your monthly and yearly income changes.
""")

# Initialize session state for remembering input values
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Monthly ETFs data
    st.session_state.monthly_etfs_data = {
        'Ticker': ['JEPI', 'JEPQ', 'DIVO', 'SDIV', 'CLM'],
        'Name': [
            'JPMorgan Equity Premium Income ETF',
            'JPMorgan Nasdaq Equity Premium Income ETF',
            'Amplify CWP Enhanced Dividend Income ETF',
            'Global X SuperDividend ETF',
            'Cornerstone Strategic Value Fund'
        ],
        'Price': [55, 48, 38, 22, 7],
        'Annual_Yield': [6.0, 5.4, 4.2, 8.4, 24.0],
        'Monthly_Yield': [0.5, 0.45, 0.35, 0.7, 2.0],
        'Shares': [500, 450, 400, 600, 1200]
    }
    
    # Group 1 quarterly stocks data (Jan/Apr/Jul/Oct)
    st.session_state.group1_data = {
        'Ticker': ['PG', 'KO', 'JNJ', 'PEP'],
        'Name': ['Procter & Gamble', 'Coca-Cola', 'Johnson & Johnson', 'PepsiCo'],
        'Price': [165, 60, 150, 170],
        'Annual_Yield': [2.4, 2.8, 3.0, 2.9],
        'Shares': [120, 200, 150, 110]
    }
    
    # Group 2 quarterly stocks data (Feb/May/Aug/Nov)
    st.session_state.group2_data = {
        'Ticker': ['MMM', 'ABT', 'XOM', 'LOW'],
        'Name': ['3M', 'Abbott Laboratories', 'Exxon Mobil', 'Lowe\'s'],
        'Price': [90, 110, 110, 220],
        'Annual_Yield': [5.6, 2.0, 3.5, 2.0],
        'Shares': [180, 150, 200, 100]
    }
    
    # Group 3 quarterly stocks data (Mar/Jun/Sep/Dec)
    st.session_state.group3_data = {
        'Ticker': ['KMB', 'T', 'CVX', 'MCD'],
        'Name': ['Kimberly-Clark', 'AT&T', 'Chevron', 'McDonald\'s'],
        'Price': [130, 17, 145, 270],
        'Annual_Yield': [3.5, 6.5, 4.2, 2.3],
        'Shares': [180, 2000, 160, 120]
    }

# Function to calculate monthly income from ETFs
def calculate_monthly_etf_income(df):
    df['Monthly_Income'] = df['Price'] * df['Shares'] * df['Monthly_Yield'] / 100
    df['Investment'] = df['Price'] * df['Shares']
    return df

# Function to calculate quarterly income from stocks
def calculate_quarterly_income(df):
    df['Quarterly_Income'] = df['Price'] * df['Shares'] * df['Annual_Yield'] / 400  # Annual yield / 4 quarters
    df['Monthly_Equivalent'] = df['Quarterly_Income'] / 3  # Spreading quarterly over 3 months
    df['Investment'] = df['Price'] * df['Shares']
    return df

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📝 Portfolio Editor", "📈 Income Projections", "ℹ️ About"])

with tab1:
    st.header("Monthly Dividend Income Dashboard")
    
    # Convert session state data to DataFrames
    monthly_etfs_df = pd.DataFrame(st.session_state.monthly_etfs_data)
    monthly_etfs_df = calculate_monthly_etf_income(monthly_etfs_df)
    
    group1_df = pd.DataFrame(st.session_state.group1_data)
    group1_df = calculate_quarterly_income(group1_df)
    
    group2_df = pd.DataFrame(st.session_state.group2_data)
    group2_df = calculate_quarterly_income(group2_df)
    
    group3_df = pd.DataFrame(st.session_state.group3_data)
    group3_df = calculate_quarterly_income(group3_df)
    
    # Calculate monthly income distribution
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']
    
    # Monthly ETF income is constant
    monthly_etf_income = monthly_etfs_df['Monthly_Income'].sum()
    
    # Quarterly income varies by month
    group1_quarterly = group1_df['Quarterly_Income'].sum()
    group2_quarterly = group2_df['Quarterly_Income'].sum()
    group3_quarterly = group3_df['Quarterly_Income'].sum()
    
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
    
    # Calculate portfolio summary
    total_investment = (
        monthly_etfs_df['Investment'].sum() + 
        group1_df['Investment'].sum() + 
        group2_df['Investment'].sum() + 
        group3_df['Investment'].sum()
    )
    
    annual_income = (
        monthly_etf_income * 12 + 
        group1_quarterly * 4 + 
        group2_quarterly * 4 + 
        group3_quarterly * 4
    )
    
    average_monthly_income = annual_income / 12
    portfolio_yield = annual_income / total_investment * 100
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Investment", f"${total_investment:,.2f}")
    
    with col2:
        st.metric("Annual Income", f"${annual_income:,.2f}")
    
    with col3:
        st.metric("Monthly Avg Income", f"${average_monthly_income:,.2f}")
    
    with col4:
        st.metric("Portfolio Yield", f"{portfolio_yield:.2f}%")
    
    # Monthly income chart
    st.subheader("Monthly Income Distribution")
    
    # Create Plotly figure
    fig = px.bar(
        x=months,
        y=monthly_income,
        labels={'x': 'Month', 'y': 'Income ($)'},
        color_discrete_sequence=['#1E3A8A'],
        title="Projected Monthly Dividend Income"
    )
    
    # Add a line for the average
    fig.add_hline(
        y=average_monthly_income, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"Average: ${average_monthly_income:.2f}",
        annotation_position="bottom right"
    )
    
    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Income ($)",
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    # Display amounts on top of bars
    fig.update_traces(
        text=[f"${x:,.2f}" for x in monthly_income],
        textposition='outside'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset allocation pie chart
    st.subheader("Asset Allocation")
    
    monthly_etf_total = monthly_etfs_df['Investment'].sum()
    group1_total = group1_df['Investment'].sum()
    group2_total = group2_df['Investment'].sum()
    group3_total = group3_df['Investment'].sum()
    
    labels = [
        'Monthly ETFs', 
        'Jan/Apr/Jul/Oct Stocks', 
        'Feb/May/Aug/Nov Stocks', 
        'Mar/Jun/Sep/Dec Stocks'
    ]
    
    values = [monthly_etf_total, group1_total, group2_total, group3_total]
    
    fig = px.pie(
        values=values,
        names=labels,
        title="Portfolio Allocation",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Income Sources")
        
        # Pie chart for income sources
        income_labels = [
            'Monthly ETFs', 
            'Jan/Apr/Jul/Oct Stocks', 
            'Feb/May/Aug/Nov Stocks', 
            'Mar/Jun/Sep/Dec Stocks'
        ]
        
        income_values = [
            monthly_etf_income * 12,
            group1_quarterly * 4,
            group2_quarterly * 4,
            group3_quarterly * 4
        ]
        
        fig2 = px.pie(
            values=income_values,
            names=income_labels,
            title="Income Distribution by Source",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig2.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hoverinfo='label+percent+value',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Portfolio Editor")
    st.markdown("""
    Adjust your share quantities below to see how it affects your dividend income.
    Each change you make will be reflected in the Dashboard and Projections.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Dividend ETFs")
        
        monthly_etfs_df = pd.DataFrame(st.session_state.monthly_etfs_data)
        
        for i, row in monthly_etfs_df.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            price = row['Price']
            
            st.session_state.monthly_etfs_data['Shares'][i] = st.number_input(
                f"{ticker} - ${price} ({row['Annual_Yield']}% yield) - Shares:",
                min_value=0,
                value=int(shares),
                step=10,
                key=f"monthly_{ticker}"
            )
        
        st.subheader("Jan/Apr/Jul/Oct Quarterly Stocks")
        
        group1_df = pd.DataFrame(st.session_state.group1_data)
        
        for i, row in group1_df.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            price = row['Price']
            
            st.session_state.group1_data['Shares'][i] = st.number_input(
                f"{ticker} - ${price} ({row['Annual_Yield']}% yield) - Shares:",
                min_value=0,
                value=int(shares),
                step=10,
                key=f"group1_{ticker}"
            )

    with col2:
        st.subheader("Feb/May/Aug/Nov Quarterly Stocks")
        
        group2_df = pd.DataFrame(st.session_state.group2_data)
        
        for i, row in group2_df.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            price = row['Price']
            
            st.session_state.group2_data['Shares'][i] = st.number_input(
                f"{ticker} - ${price} ({row['Annual_Yield']}% yield) - Shares:",
                min_value=0,
                value=int(shares),
                step=10,
                key=f"group2_{ticker}"
            )
        
        st.subheader("Mar/Jun/Sep/Dec Quarterly Stocks")
        
        group3_df = pd.DataFrame(st.session_state.group3_data)
        
        for i, row in group3_df.iterrows():
            ticker = row['Ticker']
            shares = row['Shares']
            price = row['Price']
            
            st.session_state.group3_data['Shares'][i] = st.number_input(
                f"{ticker} - ${price} ({row['Annual_Yield']}% yield) - Shares:",
                min_value=0,
                value=int(shares),
                step=10,
                key=f"group3_{ticker}"
            )

with tab3:
    st.header("Income Projections")
    
    # Convert session state data to DataFrames
    monthly_etfs_df = pd.DataFrame(st.session_state.monthly_etfs_data)
    monthly_etfs_df = calculate_monthly_etf_income(monthly_etfs_df)
    
    group1_df = pd.DataFrame(st.session_state.group1_data)
    group1_df = calculate_quarterly_income(group1_df)
    
    group2_df = pd.DataFrame(st.session_state.group2_data)
    group2_df = calculate_quarterly_income(group2_df)
    
    group3_df = pd.DataFrame(st.session_state.group3_data)
    group3_df = calculate_quarterly_income(group3_df)
    
    # Current monthly income
    monthly_etf_income = monthly_etfs_df['Monthly_Income'].sum()
    group1_quarterly = group1_df['Quarterly_Income'].sum()
    group2_quarterly = group2_df['Quarterly_Income'].sum()
    group3_quarterly = group3_df['Quarterly_Income'].sum()
    
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
    
    # Calculate annual income
    annual_income = sum(monthly_income)
    
    # Create a dataframe for displaying monthly income
    income_df = pd.DataFrame({
        'Month': months,
        'Monthly ETFs': [monthly_etf_income] * 12,
        'Group 1 (Jan/Apr/Jul/Oct)': [group1_quarterly if i % 3 == 0 else 0 for i in range(12)],
        'Group 2 (Feb/May/Aug/Nov)': [group2_quarterly if i % 3 == 1 else 0 for i in range(12)],
        'Group 3 (Mar/Jun/Sep/Dec)': [group3_quarterly if i % 3 == 2 else 0 for i in range(12)],
        'Total': monthly_income
    })
    
    # Format the dataframe for display
    formatted_income_df = income_df.copy()
    for col in formatted_income_df.columns:
        if col != 'Month':
            formatted_income_df[col] = formatted_income_df[col].apply(lambda x: f"${x:,.2f}")
    
    # Display the monthly income table
    st.subheader("Monthly Income Breakdown")
    st.dataframe(formatted_income_df, use_container_width=True)
    
    # Income growth projection
    st.subheader("Future Income Projections")
    
    col1, col2 = st.columns(2)
    
    with col1:
        years = st.slider("Projection Years", 1, 30, 10)
    
    with col2:
        growth_rate = st.slider("Annual Dividend Growth Rate (%)", 0.0, 15.0, 5.0, 0.1)
    
    # Calculate future income
    future_years = list(range(1, years + 1))
    future_annual_income = [annual_income * ((1 + growth_rate/100) ** year) for year in future_years]
    future_monthly_avg = [annual / 12 for annual in future_annual_income]
    
    projection_df = pd.DataFrame({
        'Year': future_years,
        'Annual Income': future_annual_income,
        'Monthly Average': future_monthly_avg
    })
    
    fig = px.line(
        projection_df,
        x='Year',
        y=['Annual Income', 'Monthly Average'],
        labels={'value': 'Income ($)', 'variable': 'Type'},
        title=f"Dividend Income Projection (assuming {growth_rate}% annual growth)",
        color_discrete_sequence=['#1E3A8A', '#4C86B0']
    )
    
    fig.update_layout(
        xaxis_title="Years from Now",
        yaxis_title="Income ($)",
        legend_title="Income Type",
        plot_bgcolor='rgba(0,0,0,0)',
        height=500
    )
    
    # Add markers and annotations for specific years
    marker_years = [1, 5, 10, 15, 20, 25, 30]
    marker_years = [year for year in marker_years if year <= years]
    
    for year in marker_years:
        if year in future_years:
            idx = future_years.index(year)
            annual = future_annual_income[idx]
            monthly = future_monthly_avg[idx]
            
            fig.add_annotation(
                x=year,
                y=annual,
                text=f"${annual:,.0f}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40
            )
            
            if year % 10 == 0:  # Only annotate some monthly points to avoid clutter
                fig.add_annotation(
                    x=year,
                    y=monthly,
                    text=f"${monthly:,.0f}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=30
                )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Format the projection dataframe for display
    formatted_projection_df = projection_df.copy()
    formatted_projection_df['Annual Income'] = formatted_projection_df['Annual Income'].apply(lambda x: f"${x:,.2f}")
    formatted_projection_df['Monthly Average'] = formatted_projection_df['Monthly Average'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(formatted_projection_df, use_container_width=True)
    
    # Compound growth calculator
    st.subheader("Compound Growth with DRIP")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        drip_percentage = st.slider("Percentage of Dividends Reinvested", 0, 100, 50)
    
    with col2:
        additional_investment = st.number_input(
            "Additional Annual Investment ($)",
            min_value=0,
            value=0,
            step=1000
        )
    
    with col3:
        price_growth = st.slider("Annual Stock Price Appreciation (%)", 0.0, 15.0, 3.0, 0.1)
    
    # Calculate compound growth with DRIP
    total_investment = (
        monthly_etfs_df['Investment'].sum() + 
        group1_df['Investment'].sum() + 
        group2_df['Investment'].sum() + 
        group3_df['Investment'].sum()
    )
    
    years_list = list(range(0, years + 1))
    investment_value = [total_investment]
    annual_dividend = [annual_income]
    
    for year in range(1, years + 1):
        prev_investment = investment_value[-1]
        prev_dividend = annual_dividend[-1]
        
        # Amount reinvested from dividends
        reinvested = prev_dividend * (drip_percentage / 100)
        
        # New investment value (previous + appreciation + reinvestment + additional contributions)
        new_investment = (
            prev_investment * (1 + price_growth/100) + 
            reinvested + 
            additional_investment
        )
        
        investment_value.append(new_investment)
        
        # New dividend income (based on new investment and yield)
        new_dividend = new_investment * (annual_income / total_investment)
        annual_dividend.append(new_dividend)
    
    drip_df = pd.DataFrame({
        'Year': years_list,
        'Portfolio Value': investment_value,
        'Annual Dividend Income': annual_dividend,
        'Monthly Income': [d/12 for d in annual_dividend]
    })
    
    fig = px.line(
        drip_df,
        x='Year',
        y=['Portfolio Value', 'Annual Dividend Income'],
        labels={'value': 'Amount ($)', 'variable': 'Type'},
        title="Portfolio and Dividend Growth with DRIP",
        color_discrete_sequence=['#1E6642', '#4CAF50']
    )
    
    fig.update_layout(
        xaxis_title="Years from Now",
        yaxis_title="Amount ($)",
        legend_title="Type",
        plot_bgcolor='rgba(0,0,0,0)',
        height=600,
        yaxis_type="log"  # Logarithmic scale for better visualization
    )
    
    # Add annotations for specific years
    for year in [0, 5, 10, 15, 20, 25, 30]:
        if year in years_list and year <= years:
            idx = years_list.index(year)
            value = investment_value[idx]
            dividend = annual_dividend[idx]
            
            # Only annotate some points to avoid clutter
            if year % 10 == 0 or year == 0:
                fig.add_annotation(
                    x=year,
                    y=value,
                    text=f"${value:,.0f}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=-40
                )
                
                fig.add_annotation(
                    x=year,
                    y=dividend,
                    text=f"${dividend:,.0f}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=30
                )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Format the DRIP dataframe for display
    formatted_drip_df = drip_df.copy()
    
    for col in ['Portfolio Value', 'Annual Dividend Income', 'Monthly Income']:
        formatted_drip_df[col] = formatted_drip_df[col].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(formatted_drip_df, use_container_width=True)
    
    # Final summary based on projections
    final_year = years
    final_portfolio_value = investment_value[-1]
    final_annual_income = annual_dividend[-1]
    final_monthly_income = final_annual_income / 12
    final_yield = (final_annual_income / final_portfolio_value) * 100
    
    st.subheader(f"Projected Status After {final_year} Years")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Portfolio Value", f"${final_portfolio_value:,.2f}")
    
    with col2:
        st.metric("Annual Income", f"${final_annual_income:,.2f}")
    
    with col3:
        st.metric("Monthly Income", f"${final_monthly_income:,.2f}")
    
    with col4:
        st.metric("Portfolio Yield", f"{final_yield:.2f}%")

with tab4:
    st.header("About This Application")
    
    st.markdown("""
    ### Dividend Income Calculator
    
    This application helps investors build and visualize a dividend portfolio strategy focused on generating consistent 
    monthly income using a mix of monthly dividend ETFs and quarterly dividend-paying stocks.
    
    #### Features:
    
    - **Portfolio Dashboard**: View your current investment allocation and projected monthly income
    - **Portfolio Editor**: Adjust share quantities to customize your dividend strategy
    - **Income Projections**: See how your dividend income could grow over time with reinvestment
    
    #### Tips for Using This Application:
    
    1. **Monthly Base Income**: The monthly ETFs provide a consistent foundation of income every month
    2. **Quarterly Boosts**: The quarterly dividend stocks are arranged in three groups to provide additional income in different months
    3. **Dividend Growth**: Many of the included stocks are Dividend Aristocrats/Kings with decades of dividend increases
    4. **Reinvestment Power**: Use the DRIP projections to see how reinvesting a portion of your dividends can accelerate income growth
    5. **Target Income**: Adjust share quantities until you reach your desired monthly income level
    
    #### Disclaimer:
    
    This application is for educational purposes only and does not constitute investment advice. Stock prices, 
    dividend yields, and other data are approximations and may not reflect current market conditions. Always conduct 
    your own research and consider consulting a financial advisor before making investment decisions.
    """)
    
    st.subheader("Dividend Stocks in This Portfolio")
    
    # Combine all stocks for the reference table
    all_stocks = []
    
    # Add monthly ETFs
    monthly_etfs_df = pd.DataFrame(st.session_state.monthly_etfs_data)
    for i, row in monthly_etfs_df.iterrows():
        all_stocks.append({
            'Ticker': row['Ticker'],
            'Name': row['Name'],
            'Type': 'Monthly ETF',
            'Annual Yield': f"{row['Annual_Yield']}%",
            'Payment Schedule': 'Monthly'
        })
    
    # Add Group 1 stocks
    group1_df = pd.DataFrame(st.session_state.group1_data)
    for i, row in group1_df.iterrows():
        all_stocks.append({
            'Ticker': row['Ticker'],
            'Name': row['Name'],
            'Type': 'Dividend Aristocrat/King',
            'Annual Yield': f"{row['Annual_Yield']}%",
            'Payment Schedule': 'Jan, Apr, Jul, Oct'
        })
    
    # Add Group 2 stocks
    group2_df = pd.DataFrame(st.session_state.group2_data)
    for i, row in group2_df.iterrows():
        all_stocks.append({
            'Ticker': row['Ticker'],
            'Name': row['Name'],
            'Type': 'Dividend Aristocrat/King',
            'Annual Yield': f"{row['Annual_Yield']}%",
            'Payment Schedule': 'Feb, May, Aug, Nov'
        })
    
    # Add Group 3 stocks
    group3_df = pd.DataFrame(st.session_state.group3_data)
    for i, row in group3_df.iterrows():
        all_stocks.append({
            'Ticker': row['Ticker'],
            'Name': row['Name'],
            'Type': 'Dividend Aristocrat/King',
            'Annual Yield': f"{row['Annual_Yield']}%",
            'Payment Schedule': 'Mar, Jun, Sep, Dec'
        })
    
    # Display the reference table
    all_stocks_df = pd.DataFrame(all_stocks)
    st.dataframe(all_stocks_df, use_container_width=True)
    
    st.markdown("""
    ### Considerations for Building a Dividend Portfolio:
    
    1. **Diversification**: This portfolio includes stocks across various sectors to reduce risk
    2. **Yield vs Growth**: Higher yields may offer more current income, but lower-yield stocks often have better dividend growth rates
    3. **Tax Efficiency**: Consider holding different types of dividend stocks in appropriate account types (taxable vs. tax-advantaged)
    4. **Total Return**: Remember that dividend yield is only one component of total return; price appreciation matters too
    5. **Sustainability**: Focus on companies with sustainable payout ratios and strong business fundamentals
    """)

# Add a footer
st.markdown("""
---
### Dividend Income Calculator | Created with Streamlit