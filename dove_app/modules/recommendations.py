# modules/recommendations.py
# Provides recommended portfolio strategies to reach income goals

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from modules.data import load_dataframes

def render_recommendations():
    """Render the recommendations page with strategies to reach income goals"""
    st.header("Dividend Strategy Recommendations")
    
    st.markdown("""
    This tab provides personalized recommendations to help you reach your monthly dividend income goals.
    Adjust your target monthly income and risk preference to see different strategies.
    """)
    
    # Get user inputs
    col1, col2 = st.columns(2)
    
    with col1:
        target_monthly_income = st.number_input(
            "Target Monthly Dividend Income ($)",
            min_value=100,
            max_value=10000,
            value=2000,
            step=100
        )
    
    with col2:
        risk_preference = st.select_slider(
            "Risk Preference",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate"
        )
    
    # Load data
    monthly_etfs_df, group1_df, group2_df, group3_df = load_dataframes()
    
    # Create combined dataframes for analysis
    # For monthly payers - need to convert annual yield to monthly
    monthly_payers = pd.DataFrame({
        'Ticker': monthly_etfs_df['Ticker'],
        'Name': monthly_etfs_df['Name'],
        'Price': monthly_etfs_df['Price'],
        'Annual_Yield': monthly_etfs_df['Annual_Yield'],
        'Monthly_Yield': monthly_etfs_df['Monthly_Yield'],
        'Payment_Frequency': ['Monthly'] * len(monthly_etfs_df),
        'Category': ['Monthly ETF/BDC'] * len(monthly_etfs_df)
    })
    
    # For quarterly payers - need to calculate effective monthly yield
    quarterly_payers1 = pd.DataFrame({
        'Ticker': group1_df['Ticker'],
        'Name': group1_df['Name'],
        'Price': group1_df['Price'],
        'Annual_Yield': group1_df['Annual_Yield'],
        'Monthly_Yield': group1_df['Annual_Yield'] / 12,  # Convert annual to monthly
        'Payment_Frequency': ['Quarterly (Jan/Apr/Jul/Oct)'] * len(group1_df),
        'Category': ['Dividend Stock'] * len(group1_df)
    })
    
    quarterly_payers2 = pd.DataFrame({
        'Ticker': group2_df['Ticker'],
        'Name': group2_df['Name'],
        'Price': group2_df['Price'],
        'Annual_Yield': group2_df['Annual_Yield'],
        'Monthly_Yield': group2_df['Annual_Yield'] / 12,  # Convert annual to monthly
        'Payment_Frequency': ['Quarterly (Feb/May/Aug/Nov)'] * len(group2_df),
        'Category': ['Dividend Stock'] * len(group2_df)
    })
    
    quarterly_payers3 = pd.DataFrame({
        'Ticker': group3_df['Ticker'],
        'Name': group3_df['Name'],
        'Price': group3_df['Price'],
        'Annual_Yield': group3_df['Annual_Yield'],
        'Monthly_Yield': group3_df['Annual_Yield'] / 12,  # Convert annual to monthly
        'Payment_Frequency': ['Quarterly (Mar/Jun/Sep/Dec)'] * len(group3_df),
        'Category': ['Dividend Stock'] * len(group3_df)
    })
    
    # Combine all dataframes
    all_stocks = pd.concat([monthly_payers, quarterly_payers1, quarterly_payers2, quarterly_payers3])
    
    # Calculate required shares and investment for each stock
    all_stocks['Required_Shares'] = np.ceil(target_monthly_income / (all_stocks['Price'] * all_stocks['Monthly_Yield'] / 100))
    all_stocks['Required_Investment'] = all_stocks['Required_Shares'] * all_stocks['Price']
    
    # Calculate efficiency (monthly income per $1000 invested)
    all_stocks['Income_per_1000'] = 1000 * all_stocks['Monthly_Yield'] / 100
    
    # Sort by investment required
    all_stocks = all_stocks.sort_values('Required_Investment')
    
    # Define risk categories based on yield
    def assign_risk_category(yield_value):
        if yield_value < 3.0:
            return "Low Risk"
        elif yield_value < 6.0:
            return "Moderate Risk"
        elif yield_value < 10.0:
            return "High Risk"
        else:
            return "Very High Risk"
    
    all_stocks['Risk_Category'] = all_stocks['Annual_Yield'].apply(assign_risk_category)
    
    # Filter based on risk preference
    if risk_preference == "Conservative":
        filtered_stocks = all_stocks[all_stocks['Risk_Category'].isin(["Low Risk", "Moderate Risk"])]
    elif risk_preference == "Moderate":
        filtered_stocks = all_stocks[all_stocks['Risk_Category'].isin(["Low Risk", "Moderate Risk", "High Risk"])]
    else:  # Aggressive
        filtered_stocks = all_stocks
    
    # If no stocks match the criteria, use all stocks
    if len(filtered_stocks) == 0:
        filtered_stocks = all_stocks
    
    # Create recommendations
    st.subheader("Recommended Strategies")
    
    # 1. Single Stock Strategy (lowest investment)
    single_stock = filtered_stocks.iloc[0]
    
    st.markdown("### Strategy 1: Single Stock Approach (Lowest Investment)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **{single_stock['Ticker']} - {single_stock['Name']}**
        - Price: ${single_stock['Price']:.2f} per share
        - Yield: {single_stock['Annual_Yield']:.2f}% annual ({single_stock['Monthly_Yield']:.2f}% monthly)
        - Payment frequency: {single_stock['Payment_Frequency']}
        - Risk level: {single_stock['Risk_Category']}
        """)
    
    with col2:
        st.markdown(f"""
        **To reach ${target_monthly_income:.2f} monthly income:**
        - Required shares: {int(single_stock['Required_Shares']):,}
        - Total investment: ${single_stock['Required_Investment']:,.2f}
        - Monthly income per $1,000 invested: ${single_stock['Income_per_1000']:.2f}
        """)
    
    st.warning(f"Note: This strategy concentrates all your investment in a single security ({single_stock['Ticker']}), which lacks diversification.")
    
    # 2. Balanced Monthly Income Strategy
    st.markdown("### Strategy 2: Balanced Monthly Income Portfolio")
    
    # Get top monthly payers (up to 3)
    monthly_only = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Monthly'].head(3)
    
    if len(monthly_only) > 0:
        # Calculate how to distribute the investment
        total_shares = []
        total_investment = []
        monthly_incomes = []
        
        # Distribute evenly among monthly payers
        target_per_stock = target_monthly_income / len(monthly_only)
        
        for idx, stock in monthly_only.iterrows():
            shares_needed = np.ceil(target_per_stock / (stock['Price'] * stock['Monthly_Yield'] / 100))
            investment = shares_needed * stock['Price']
            monthly_income = shares_needed * stock['Price'] * stock['Monthly_Yield'] / 100
            
            total_shares.append(int(shares_needed))
            total_investment.append(investment)
            monthly_incomes.append(monthly_income)
        
        # Create a dataframe for display
        monthly_strategy = pd.DataFrame({
            'Ticker': monthly_only['Ticker'].values,
            'Name': monthly_only['Name'].values,
            'Price': monthly_only['Price'].values,
            'Annual_Yield': monthly_only['Annual_Yield'].values,
            'Shares': total_shares,
            'Investment': total_investment,
            'Monthly_Income': monthly_incomes
        })
        
        st.write("This strategy focuses on monthly dividend payers for consistent income throughout the year.")
        
        # Display the strategy table
        display_df = monthly_strategy.copy()
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Annual_Yield'] = display_df['Annual_Yield'].apply(lambda x: f"{x:.2f}%")
        display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.2f}")
        display_df['Monthly_Income'] = display_df['Monthly_Income'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        total_monthly_income = sum(monthly_incomes)
        total_investment_amount = sum(total_investment)
        
        st.metric("Total Monthly Income", f"${total_monthly_income:.2f}")
        st.metric("Total Investment Required", f"${total_investment_amount:,.2f}")
    else:
        st.info("Not enough monthly dividend payers match your risk criteria.")
    
    # 3. Diversified Quarterly Strategy
    st.markdown("### Strategy 3: Diversified Quarterly Portfolio")
    
    # Get top stocks from each payment group (1 per group)
    group1 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Jan/Apr/Jul/Oct)'].sort_values('Required_Investment').head(1)
    group2 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Feb/May/Aug/Nov)'].sort_values('Required_Investment').head(1)
    group3 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Mar/Jun/Sep/Dec)'].sort_values('Required_Investment').head(1)
    
    quarterly_picks = pd.concat([group1, group2, group3])
    
    if len(quarterly_picks) > 0:
        # Distribute target among quarters
        target_per_month = target_monthly_income
        quarterly_target = target_per_month * 3  # Each stock needs to provide 3 months worth of income per quarter
        
        total_shares = []
        total_investment = []
        quarterly_incomes = []
        
        for idx, stock in quarterly_picks.iterrows():
            # Each stock needs to generate income for its quarter (3 months)
            shares_needed = np.ceil(quarterly_target / (stock['Price'] * stock['Annual_Yield'] / 400))  # Annual yield / 4 quarters
            investment = shares_needed * stock['Price']
            quarterly_income = shares_needed * stock['Price'] * stock['Annual_Yield'] / 400
            
            total_shares.append(int(shares_needed))
            total_investment.append(investment)
            quarterly_incomes.append(quarterly_income)
        
        # Create a dataframe for display
        quarterly_strategy = pd.DataFrame({
            'Ticker': quarterly_picks['Ticker'].values,
            'Name': quarterly_picks['Name'].values,
            'Price': quarterly_picks['Price'].values,
            'Annual_Yield': quarterly_picks['Annual_Yield'].values,
            'Payment_Schedule': quarterly_picks['Payment_Frequency'].values,
            'Shares': total_shares,
            'Investment': total_investment,
            'Quarterly_Income': quarterly_incomes
        })
        
        st.write("This strategy distributes investments across stocks that pay in different quarters to provide steady monthly income.")
        
        # Display the strategy table
        display_df = quarterly_strategy.copy()
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Annual_Yield'] = display_df['Annual_Yield'].apply(lambda x: f"{x:.2f}%")
        display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.2f}")
        display_df['Quarterly_Income'] = display_df['Quarterly_Income'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        monthly_equivalent = sum(quarterly_incomes) / 3
        total_investment_amount = sum(total_investment)
        
        st.metric("Approximate Monthly Income", f"${monthly_equivalent:.2f}")
        st.metric("Total Investment Required", f"${total_investment_amount:,.2f}")
    else:
        st.info("Not enough quarterly dividend payers match your risk criteria.")
    
    # 4. Blended Approach
    st.markdown("### Strategy 4: Blended Approach (Monthly + Quarterly)")
    
    # Try to build a portfolio with both monthly and quarterly payers
    # 60% monthly, 40% quarterly (distributed evenly)
    
    monthly_target = target_monthly_income * 0.6
    quarterly_target = target_monthly_income * 0.4
    
    # Get top monthly payer
    top_monthly = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Monthly'].sort_values('Required_Investment').head(1)
    
    # Get top quarterly payer from each group
    top_quarterly1 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Jan/Apr/Jul/Oct)'].sort_values('Required_Investment').head(1)
    top_quarterly2 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Feb/May/Aug/Nov)'].sort_values('Required_Investment').head(1)
    top_quarterly3 = filtered_stocks[filtered_stocks['Payment_Frequency'] == 'Quarterly (Mar/Jun/Sep/Dec)'].sort_values('Required_Investment').head(1)
    
    all_picks = []
    
    # Calculate monthly component
    if len(top_monthly) > 0:
        stock = top_monthly.iloc[0]
        shares_needed = np.ceil(monthly_target / (stock['Price'] * stock['Monthly_Yield'] / 100))
        investment = shares_needed * stock['Price']
        monthly_income = shares_needed * stock['Price'] * stock['Monthly_Yield'] / 100
        
        all_picks.append({
            'Ticker': stock['Ticker'],
            'Name': stock['Name'],
            'Price': stock['Price'],
            'Annual_Yield': stock['Annual_Yield'],
            'Payment_Schedule': stock['Payment_Frequency'],
            'Shares': int(shares_needed),
            'Investment': investment,
            'Monthly_Income': monthly_income,
            'Type': 'Monthly'
        })
    
    # Calculate quarterly components
    quarterly_picks = pd.concat([top_quarterly1, top_quarterly2, top_quarterly3])
    
    if len(quarterly_picks) > 0:
        quarter_target = quarterly_target * 3  # Each stock needs to provide 3 months worth
        
        for idx, stock in quarterly_picks.iterrows():
            shares_needed = np.ceil(quarter_target / (stock['Price'] * stock['Annual_Yield'] / 400))
            investment = shares_needed * stock['Price']
            quarterly_income = shares_needed * stock['Price'] * stock['Annual_Yield'] / 400
            
            all_picks.append({
                'Ticker': stock['Ticker'],
                'Name': stock['Name'],
                'Price': stock['Price'],
                'Annual_Yield': stock['Annual_Yield'],
                'Payment_Schedule': stock['Payment_Frequency'],
                'Shares': int(shares_needed),
                'Investment': investment,
                'Monthly_Income': quarterly_income / 3,  # Convert to monthly equivalent
                'Type': 'Quarterly'
            })
    
    if len(all_picks) > 0:
        blended_df = pd.DataFrame(all_picks)
        
        st.write("This strategy combines monthly and quarterly dividend payers for both consistency and higher yields.")
        
        # Display the strategy table
        display_df = blended_df.copy()
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Annual_Yield'] = display_df['Annual_Yield'].apply(lambda x: f"{x:.2f}%")
        display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.2f}")
        display_df['Monthly_Income'] = display_df['Monthly_Income'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        total_monthly_income = blended_df['Monthly_Income'].sum()
        total_investment_amount = blended_df['Investment'].sum()
        
        st.metric("Total Monthly Income", f"${total_monthly_income:.2f}")
        st.metric("Total Investment Required", f"${total_investment_amount:,.2f}")
    else:
        st.info("Not enough stocks match your risk criteria for a blended approach.")
    
    # 5. Most Efficient Strategy (best income per dollar invested)
    st.markdown("### Strategy 5: Most Efficient Income Generators")
    
    # Get top 5 most efficient stocks (highest income per $1000)
    efficient_stocks = filtered_stocks.sort_values('Income_per_1000', ascending=False).head(5)
    
    if len(efficient_stocks) > 0:
        # Calculate equal investment in each stock
        investment_per_stock = 10000  # $10,000 in each stock for this example
        
        stocks_data = []
        
        for idx, stock in efficient_stocks.iterrows():
            shares = np.floor(investment_per_stock / stock['Price'])
            actual_investment = shares * stock['Price']
            
            if stock['Payment_Frequency'] == 'Monthly':
                monthly_income = shares * stock['Price'] * stock['Monthly_Yield'] / 100
            else:
                # For quarterly payers, convert to monthly equivalent
                quarterly_income = shares * stock['Price'] * stock['Annual_Yield'] / 400
                monthly_income = quarterly_income / 3
            
            stocks_data.append({
                'Ticker': stock['Ticker'],
                'Name': stock['Name'],
                'Price': stock['Price'],
                'Annual_Yield': stock['Annual_Yield'],
                'Payment_Schedule': stock['Payment_Frequency'],
                'Shares': int(shares),
                'Investment': actual_investment,
                'Monthly_Income': monthly_income,
                'Income_per_1000': stock['Income_per_1000']
            })
        
        efficient_df = pd.DataFrame(stocks_data)
        
        st.write("This strategy focuses on stocks that generate the most income per dollar invested, regardless of payment schedule.")
        
        # Display the strategy table
        display_df = efficient_df.copy()
        display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.2f}")
        display_df['Annual_Yield'] = display_df['Annual_Yield'].apply(lambda x: f"{x:.2f}%")
        display_df['Investment'] = display_df['Investment'].apply(lambda x: f"${x:,.2f}")
        display_df['Monthly_Income'] = display_df['Monthly_Income'].apply(lambda x: f"${x:.2f}")
        display_df['Income_per_1000'] = display_df['Income_per_1000'].apply(lambda x: f"${x:.2f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        total_monthly_income = efficient_df['Monthly_Income'].sum()
        total_investment_amount = efficient_df['Investment'].sum()
        
        st.metric("Total Monthly Income", f"${total_monthly_income:.2f}")
        st.metric("Total Investment Required", f"${total_investment_amount:,.2f}")
        
        # Income needed to reach target
        remaining_income = target_monthly_income - total_monthly_income
        
        if remaining_income > 0:
            additional_investment = remaining_income * 1000 / efficient_df['Income_per_1000'].mean()
            st.info(f"To reach your target of ${target_monthly_income:.2f} monthly income, you would need approximately ${additional_investment:,.2f} in additional investment using this strategy.")
    else:
        st.info("Not enough stocks match your risk criteria for the efficiency strategy.")
    
    # Comparison chart
    st.subheader("Strategy Comparison")
    
    comparison_data = []
    
    # Add single stock strategy
    comparison_data.append({
        'Strategy': 'Single Stock',
        'Total Investment': single_stock['Required_Investment'],
        'Monthly Income': target_monthly_income,
        'Annual Return': target_monthly_income * 12 / single_stock['Required_Investment'] * 100
    })
    
    # Add monthly strategy if available
    if 'monthly_strategy' in locals():
        comparison_data.append({
            'Strategy': 'Monthly Portfolio',
            'Total Investment': sum(total_investment),
            'Monthly Income': sum(monthly_incomes),
            'Annual Return': sum(monthly_incomes) * 12 / sum(total_investment) * 100
        })
    
    # Add quarterly strategy if available
    if 'quarterly_strategy' in locals():
        comparison_data.append({
            'Strategy': 'Quarterly Portfolio',
            'Total Investment': sum(total_investment),
            'Monthly Income': sum(quarterly_incomes) / 3,
            'Annual Return': sum(quarterly_incomes) * 4 / sum(total_investment) * 100
        })
    
    # Add blended strategy if available
    if 'blended_df' in locals():
        comparison_data.append({
            'Strategy': 'Blended Approach',
            'Total Investment': blended_df['Investment'].sum(),
            'Monthly Income': blended_df['Monthly_Income'].sum(),
            'Annual Return': blended_df['Monthly_Income'].sum() * 12 / blended_df['Investment'].sum() * 100
        })
    
    # Add efficient strategy if available
    if 'efficient_df' in locals():
        comparison_data.append({
            'Strategy': 'Efficient Income',
            'Total Investment': efficient_df['Investment'].sum(),
            'Monthly Income': efficient_df['Monthly_Income'].sum(),
            'Annual Return': efficient_df['Monthly_Income'].sum() * 12 / efficient_df['Investment'].sum() * 100
        })
    
    if comparison_data:
        comparison_df = pd.DataFrame(comparison_data)
        
        # Create charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                comparison_df,
                x='Strategy',
                y='Total Investment',
                title='Required Investment by Strategy',
                color='Strategy',
                text_auto='.2s'
            )
            fig.update_layout(yaxis_title="Investment ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                comparison_df,
                x='Strategy',
                y='Annual Return',
                title='Annual Return by Strategy',
                color='Strategy',
                text_auto='.2f'
            )
            fig.update_layout(yaxis_title="Annual Return (%)")
            fig.update_traces(texttemplate='%{y:.2f}%')
            st.plotly_chart(fig, use_container_width=True)
    
    # Disclaimer
    st.markdown("""
    ---
    **Disclaimer:** These recommendations are for informational purposes only and do not constitute investment advice. 
    Past performance is not indicative of future results. Higher yields often come with higher risks. 
    Always do your own research and consider consulting with a financial advisor before making investment decisions.
    """)