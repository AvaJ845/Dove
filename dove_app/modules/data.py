# modules/data.py
# Handles data initialization, storage, and retrieval

import pandas as pd
import streamlit as st

def initialize_data():
    """Initialize default portfolio data in session state"""
    
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

def calculate_monthly_etf_income(df):
    """Calculate monthly income from ETFs"""
    df['Monthly_Income'] = df['Price'] * df['Shares'] * df['Monthly_Yield'] / 100
    df['Investment'] = df['Price'] * df['Shares']
    return df

def calculate_quarterly_income(df):
    """Calculate quarterly income from stocks"""
    df['Quarterly_Income'] = df['Price'] * df['Shares'] * df['Annual_Yield'] / 400  # Annual yield / 4 quarters
    df['Monthly_Equivalent'] = df['Quarterly_Income'] / 3  # Spreading quarterly over 3 months
    df['Investment'] = df['Price'] * df['Shares']
    return df

def load_dataframes():
    """Load and calculate all dataframes"""
    # Convert session state data to DataFrames
    monthly_etfs_df = pd.DataFrame(st.session_state.monthly_etfs_data)
    monthly_etfs_df = calculate_monthly_etf_income(monthly_etfs_df)
    
    group1_df = pd.DataFrame(st.session_state.group1_data)
    group1_df = calculate_quarterly_income(group1_df)
    
    group2_df = pd.DataFrame(st.session_state.group2_data)
    group2_df = calculate_quarterly_income(group2_df)
    
    group3_df = pd.DataFrame(st.session_state.group3_data)
    group3_df = calculate_quarterly_income(group3_df)
    
    return monthly_etfs_df, group1_df, group2_df, group3_df

def update_shares(ticker_group, ticker, shares):
    """Update shares for a specific ticker in a group"""
    group_data = getattr(st.session_state, f"{ticker_group}_data")
    ticker_index = group_data['Ticker'].index(ticker)
    group_data['Shares'][ticker_index] = shares

def get_all_stocks():
    """Get a list of all stocks in the portfolio for reference"""
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
    
    return pd.DataFrame(all_stocks)