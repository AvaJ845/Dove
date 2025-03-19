# modules/projections.py
# Handles future projections and growth calculations

import pandas as pd
import plotly.express as px

def calculate_future_income(annual_income, years, growth_rate):
    """Calculate future income with dividend growth"""
    future_years = list(range(1, years + 1))
    future_annual_income = [annual_income * ((1 + growth_rate/100) ** year) for year in future_years]
    future_monthly_avg = [annual / 12 for annual in future_annual_income]
    
    projection_df = pd.DataFrame({
        'Year': future_years,
        'Annual Income': future_annual_income,
        'Monthly Average': future_monthly_avg
    })
    
    return projection_df

def create_projection_chart(projection_df, years, growth_rate):
    """Create a chart visualizing future income projections"""
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
        if year in projection_df['Year'].values:
            idx = projection_df[projection_df['Year'] == year].index[0]
            annual = projection_df.loc[idx, 'Annual Income']
            monthly = projection_df.loc[idx, 'Monthly Average']
            
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
    
    return fig

def calculate_drip_growth(total_investment, annual_income, years, drip_percentage, additional_investment, price_growth):
    """Calculate compound growth with DRIP"""
    years_list = list(range(0, years + 1))
    investment_value = [total_investment]
    annual_dividend = [annual_income]
    
    for year in range(1, years + 1):
        prev_investment = investment_value[-1]
        prev_dividend = annual_dividend[-1]
        
        # Amount reinvested from dividends