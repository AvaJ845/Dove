# modules/visualizations.py
# Functions for creating data visualizations

import plotly.express as px
import plotly.graph_objects as go

def create_monthly_chart(months, monthly_income, average_monthly_income):
    """Create monthly income distribution chart"""
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
    
    return fig

def create_allocation_pie(monthly_etf_total, group1_total, group2_total, group3_total):
    """Create asset allocation pie chart"""
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
    
    return fig

def create_income_source_pie(monthly_etf_annual, group1_annual, group2_annual, group3_annual):
    """Create income sources pie chart"""
    income_labels = [
        'Monthly ETFs', 
        'Jan/Apr/Jul/Oct Stocks', 
        'Feb/May/Aug/Nov Stocks', 
        'Mar/Jun/Sep/Dec Stocks'
    ]
    
    income_values = [
        monthly_etf_annual,
        group1_annual,
        group2_annual,
        group3_annual
    ]
    
    fig = px.pie(
        values=income_values,
        names=income_labels,
        title="Income Distribution by Source",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hoverinfo='label+percent+value',
        marker=dict(line=dict(color='#FFFFFF', width=2))
    )
    
    return fig

def format_currency_dataframe(df, currency_columns):
    """Format currency columns in a dataframe"""
    formatted_df = df.copy()
    
    for col in currency_columns:
        if col in formatted_df.columns:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"${x:,.2f}")
    
    return formatted_df