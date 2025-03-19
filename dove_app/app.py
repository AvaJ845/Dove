# app.py - Simplified working version

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from modules.data import initialize_data, load_dataframes
from modules.calculations import calculate_monthly_income, calculate_portfolio_metrics
from modules.visualizations import create_monthly_chart, create_allocation_pie, create_income_source_pie
from modules.projections import calculate_future_income, create_projection_chart, calculate_drip_growth
from modules.ui_components import (render_portfolio_editor, render_projection_controls, 
                                  render_drip_controls, display_metrics, 
                                  display_header, display_footer)
from modules.database import initialize_database

# Set page configuration
st.set_page_config(
    page_title="Dove - Dividend Income Calculator",
    page_icon="🕊️",
    layout="wide"
)

# Initialize data if needed
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    initialize_data()
    initialize_database()  # Initialize the SQLite database

# Display header
display_header()

# Introduction
st.markdown("""
This application helps you track and project dividend income from a portfolio of Dividend Kings, 
Aristocrats, and monthly dividend ETFs. Adjust share quantities to see how your monthly and yearly income changes.
""")

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Dashboard", "📝 Portfolio Editor", "📈 Income Projections", "💾 Portfolio Manager", "ℹ️ About"])

with tab1:
    st.header("Monthly Dividend Income Dashboard")
    
    # Load and calculate dataframes
    monthly_etfs_df, group1_df, group2_df, group3_df = load_dataframes()
    
    # Calculate income distribution
    months, monthly_income, monthly_etf_income, group1_quarterly, group2_quarterly, group3_quarterly = calculate_monthly_income(
        monthly_etfs_df, group1_df, group2_df, group3_df
    )
    
    # Calculate portfolio metrics
    total_investment, annual_income, average_monthly_income, portfolio_yield = calculate_portfolio_metrics(
        monthly_etfs_df, group1_df, group2_df, group3_df, monthly_etf_income, 
        group1_quarterly, group2_quarterly, group3_quarterly
    )
    
    # Display key metrics
    display_metrics(total_investment, annual_income, average_monthly_income, portfolio_yield)
    
    # Monthly income chart
    st.subheader("Monthly Income Distribution")
    fig = create_monthly_chart(months, monthly_income, average_monthly_income)
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset allocation charts
    st.subheader("Asset Allocation")
    
    monthly_etf_total = monthly_etfs_df['Investment'].sum()
    group1_total = group1_df['Investment'].sum()
    group2_total = group2_df['Investment'].sum()
    group3_total = group3_df['Investment'].sum()
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        fig = create_allocation_pie(
            monthly_etf_total, group1_total, group2_total, group3_total
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Income Sources")
        fig2 = create_income_source_pie(
            monthly_etf_income * 12,
            group1_quarterly * 4,
            group2_quarterly * 4, 
            group3_quarterly * 4
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("Portfolio Editor")
    st.markdown("""
    Adjust your share quantities below to see how it affects your dividend income.
    Each change you make will be reflected in the Dashboard and Projections.
    """)
    
    render_portfolio_editor()

with tab3:
    st.header("Income Projections")
    
    # Load and calculate dataframes
    monthly_etfs_df, group1_df, group2_df, group3_df = load_dataframes()
    
    # Calculate income distribution
    months, monthly_income, monthly_etf_income, group1_quarterly, group2_quarterly, group3_quarterly = calculate_monthly_income(
        monthly_etfs_df, group1_df, group2_df, group3_df
    )
    
    # Calculate portfolio metrics
    total_investment, annual_income, average_monthly_income, portfolio_yield = calculate_portfolio_metrics(
        monthly_etfs_df, group1_df, group2_df, group3_df, monthly_etf_income, 
        group1_quarterly, group2_quarterly, group3_quarterly
    )
    
    # Create monthly income breakdown table
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
    
    years, growth_rate = render_projection_controls()
    
    # Calculate and display projections
    projection_df = calculate_future_income(annual_income, years, growth_rate)
    fig = create_projection_chart(projection_df, years, growth_rate)
    st.plotly_chart(fig, use_container_width=True)
    
    # Format the projection dataframe for display
    formatted_projection_df = projection_df.copy()
    formatted_projection_df['Annual Income'] = formatted_projection_df['Annual Income'].apply(lambda x: f"${x:,.2f}")
    formatted_projection_df['Monthly Average'] = formatted_projection_df['Monthly Average'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(formatted_projection_df, use_container_width=True)
    
    # DRIP section with simplified chart
    st.subheader("Compound Growth with DRIP")
    
    drip_percentage, additional_investment, price_growth = render_drip_controls()
    
    try:
        # Calculate DRIP growth
        drip_df = calculate_drip_growth(
            total_investment, annual_income, years, 
            drip_percentage, additional_investment, price_growth
        )
        
        # Simplified chart creation
        if isinstance(drip_df, pd.DataFrame) and not drip_df.empty and len(drip_df) > 1:
            # Create figure directly with go.Figure for reliability
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=drip_df['Year'], 
                y=drip_df['Portfolio Value'],
                name='Portfolio Value',
                mode='lines+markers'
            ))
            
            fig.add_trace(go.Scatter(
                x=drip_df['Year'], 
                y=drip_df['Annual Dividend Income'],
                name='Annual Dividend Income',
                mode='lines+markers'
            ))
            
            fig.update_layout(
                title="Portfolio and Dividend Growth with DRIP",
                xaxis_title="Years from Now",
                yaxis_title="Amount ($)",
                legend_title="Type",
                yaxis_type="log"  # Logarithmic scale for better visualization
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Format and display the dataframe
            formatted_drip_df = drip_df.copy()
            for col in ['Portfolio Value', 'Annual Dividend Income', 'Monthly Income']:
                if col in formatted_drip_df.columns:
                    formatted_drip_df[col] = formatted_drip_df[col].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(formatted_drip_df, use_container_width=True)
            
            # Final metrics
            if years > 0 and len(drip_df) > years:
                final_year = years
                final_portfolio_value = drip_df['Portfolio Value'].iloc[-1]
                final_annual_income = drip_df['Annual Dividend Income'].iloc[-1]
                final_monthly_income = final_annual_income / 12
                final_yield = (final_annual_income / final_portfolio_value) * 100 if final_portfolio_value > 0 else 0
                
                st.subheader(f"Projected Status After {final_year} Years")
                display_metrics(final_portfolio_value, final_annual_income, final_monthly_income, final_yield)
        else:
            st.warning("Unable to generate DRIP chart - insufficient data.")
    except Exception as e:
        st.error(f"Error in DRIP calculations. Please try adjusting your settings.")
        st.write("Technical details:", str(e))

with tab4:
    st.header("Portfolio Manager")
    from modules.portfolio_manager import render_portfolio_manager
    render_portfolio_manager()

with tab5:
    st.header("About")
    from modules.about import render_about_page
    render_about_page()

# Add a footer
display_footer()