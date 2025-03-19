# modules/ui_components.py
# UI components and rendering functions

import streamlit as st
import pandas as pd
from modules.data import load_dataframes

def load_css():
    """Load custom CSS styles"""
    st.markdown("""
    <style>
        .main {
            padding: 1rem 1rem;
            margin-bottom: 60px; /* Space for footer */
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
        .header-container {
            text-align: center;
            padding: 1rem 0;
            margin-bottom: 2rem;
            background-color: #f8f9fa;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .footer-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: #f8f9fa;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #e9ecef;
            z-index: 999;
        }
        .dove-icon {
            font-size: 2.5rem;
            color: #6c757d;
            margin-bottom: 0.5rem;
        }
        .app-title {
            font-size: 2.2rem;
            font-weight: bold;
            margin: 0;
            color: #1E3A8A;
        }
        .app-subtitle {
            font-style: italic;
            margin: 0.3rem 0;
            color: #495057;
        }
        .company-name {
            font-weight: 500;
            color: #495057;
        }
    </style>
    """, unsafe_allow_html=True)

def display_metrics(value1, value2, value3, value4, labels=None):
    """Display key metrics in a row of columns"""
    if labels is None:
        labels = ["Total Investment", "Annual Income", "Monthly Avg Income", "Portfolio Yield"]
    
    formats = ["${:,.2f}", "${:,.2f}", "${:,.2f}", "{:.2f}%"]
    values = [value1, value2, value3, value4]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(labels[0], formats[0].format(values[0]))
    
    with col2:
        st.metric(labels[1], formats[1].format(values[1]))
    
    with col3:
        st.metric(labels[2], formats[2].format(values[2]))
    
    with col4:
        st.metric(labels[3], formats[3].format(values[3]))

def render_portfolio_editor():
    """Render the portfolio editor section"""
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

def render_projection_controls():
    """Render controls for projection settings"""
    col1, col2 = st.columns(2)
    
    with col1:
        years = st.slider("Projection Years", 1, 30, 10)
    
    with col2:
        growth_rate = st.slider("Annual Dividend Growth Rate (%)", 0.0, 15.0, 5.0, 0.1)
    
    return years, growth_rate

def render_drip_controls():
    """Render controls for DRIP (Dividend Reinvestment Plan) settings"""
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
    
    return drip_percentage, additional_investment, price_growth

def display_header():
    """Display the application header with styling"""
    st.markdown("""
        <div class="header-container">
            <div class="dove-icon">🕊️</div>
            <h1 class="app-title">Dove v1</h1>
            <p class="app-subtitle">Dividend Income Calculator</p>
            <p class="company-name">AvaResearch LLC</p>
        </div>
    """, unsafe_allow_html=True)

def display_footer():
    """Display the application footer"""
    st.markdown("""
        <div class="footer-container">
            <p style="margin-bottom: 0;">© 2025 AvaResearch LLC. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)