# modules/about.py
# About page content and information

import streamlit as st
import pandas as pd
from modules.data import get_all_stocks

def render_about_page():
    """Render the About page content"""
    st.header("About Dove")
    
    st.markdown("""
    ### Dove: Dividend Income Calculator
    
    Dove is a product of AvaResearch LLC designed to help investors build and visualize a dividend portfolio strategy focused on generating consistent 
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
    
    # Get and display the reference table of all stocks
    all_stocks_df = get_all_stocks()
    st.dataframe(all_stocks_df, use_container_width=True)
    
    st.markdown("""
    ### Considerations for Building a Dividend Portfolio:
    
    1. **Diversification**: This portfolio includes stocks across various sectors to reduce risk
    2. **Yield vs Growth**: Higher yields may offer more current income, but lower-yield stocks often have better dividend growth rates
    3. **Tax Efficiency**: Consider holding different types of dividend stocks in appropriate account types (taxable vs. tax-advantaged)
    4. **Total Return**: Remember that dividend yield is only one component of total return; price appreciation matters too
    5. **Sustainability**: Focus on companies with sustainable payout ratios and strong business fundamentals
    
    ### Understanding Dividend Kings and Aristocrats
    
    **Dividend Aristocrats** are S&P 500 companies that have increased their dividend payouts for at least 25 consecutive years.
    
    **Dividend Kings** are companies that have increased their dividend payments for at least 50 consecutive years.
    
    These companies demonstrate:
    - Financial stability
    - Consistent growth
    - Management's commitment to returning value to shareholders
    - Resilience through multiple economic cycles
    
    ### Why Monthly Income Planning Matters
    
    Planning for consistent monthly income from dividends offers several advantages:
    
    1. Better alignment with monthly expenses
    2. Reduced income volatility
    3. More frequent compounding opportunities
    4. Greater flexibility in retirement planning
    5. Psychological benefits of consistent income
    
    Using a combination of monthly ETFs with quarterly dividend stocks strategically arranged by payment month 
    creates a more balanced cash flow throughout the year.
    """)