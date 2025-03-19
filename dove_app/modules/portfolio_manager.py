# modules/portfolio_manager.py
# UI components for managing portfolios (saving, loading, etc.)

import streamlit as st
import pandas as pd
from modules.database import (
    initialize_database, save_portfolio, load_portfolio, 
    delete_portfolio, get_all_portfolios, export_portfolio_to_csv, 
    import_portfolio_from_csvs
)
from modules.data import load_dataframes
from modules.calculations import calculate_portfolio_metrics, calculate_monthly_income
import os
import tempfile

def render_portfolio_manager():
    """Render the portfolio management section"""
    
    # Initialize database if needed
    initialize_database()
    
    st.subheader("Portfolio Management")
    
    tab1, tab2, tab3 = st.tabs(["💾 Save/Load", "📊 Portfolio List", "📤 Import/Export"])
    
    with tab1:
        render_save_load_tab()
    
    with tab2:
        render_portfolio_list_tab()
    
    with tab3:
        render_import_export_tab()

def render_save_load_tab():
    """Render the save/load portfolio tab"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Save Current Portfolio")
        
        portfolio_name = st.text_input("Portfolio Name", key="save_portfolio_name")
        portfolio_desc = st.text_area("Description (optional)", key="save_portfolio_desc", height=100)
        
        if st.button("Save Portfolio", use_container_width=True):
            if not portfolio_name:
                st.error("Please enter a portfolio name")
            else:
                result = save_portfolio(portfolio_name, portfolio_desc)
                if result == "created":
                    st.success(f"Portfolio '{portfolio_name}' saved successfully!")
                else:
                    st.success(f"Portfolio '{portfolio_name}' updated successfully!")
    
    with col2:
        st.markdown("### Load Saved Portfolio")
        
        portfolios = get_all_portfolios()
        if not portfolios:
            st.info("No portfolios saved yet. Create your first portfolio by customizing shares and saving it.")
        else:
            portfolio_options = {f"{p['name']} (Last updated: {p['updated_at']})": p['id'] for p in portfolios}
            selected_portfolio = st.selectbox(
                "Select a portfolio to load", 
                options=list(portfolio_options.keys()),
                key="load_portfolio_select"
            )
            
            if selected_portfolio:
                selected_id = portfolio_options[selected_portfolio]
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Load Portfolio", use_container_width=True):
                        if load_portfolio(selected_id):
                            st.success(f"Portfolio loaded successfully!")
                            st.session_state.portfolio_loaded = True
                
                with col2:
                    if st.button("Delete Portfolio", use_container_width=True):
                        if delete_portfolio(selected_id):
                            st.success(f"Portfolio deleted successfully!")
                            st.rerun()  # Refresh the page to update the portfolio list

def render_portfolio_list_tab():
    """Render the portfolio list tab"""
    
    portfolios = get_all_portfolios()
    
    if not portfolios:
        st.info("No portfolios saved yet. Create your first portfolio by customizing shares and saving it.")
    else:
        st.markdown("### Your Saved Portfolios")
        
        # Create a DataFrame for display
        portfolio_data = []
        for p in portfolios:
            portfolio_data.append({
                "ID": p['id'],
                "Name": p['name'],
                "Description": p['description'] or "-",
                "Created": p['created_at'],
                "Last Updated": p['updated_at']
            })
        
        portfolio_df = pd.DataFrame(portfolio_data)
        st.dataframe(portfolio_df, use_container_width=True)
        
        # Portfolio comparison section
        if len(portfolios) >= 2:
            st.markdown("### Compare Portfolios")
            
            # Allow selection of portfolios to compare
            col1, col2 = st.columns(2)
            
            with col1:
                portfolio_options1 = {f"{p['name']}": p['id'] for p in portfolios}
                selected_portfolio1 = st.selectbox(
                    "Select first portfolio", 
                    options=list(portfolio_options1.keys()),
                    key="compare_portfolio1"
                )
            
            with col2:
                portfolio_options2 = {f"{p['name']}": p['id'] for p in portfolios}
                selected_portfolio2 = st.selectbox(
                    "Select second portfolio", 
                    options=list(portfolio_options2.keys()),
                    key="compare_portfolio2"
                )
            
            if st.button("Compare Portfolios", use_container_width=True):
                # Temporarily save current state
                temp_monthly = st.session_state.monthly_etfs_data.copy()
                temp_group1 = st.session_state.group1_data.copy()
                temp_group2 = st.session_state.group2_data.copy()
                temp_group3 = st.session_state.group3_data.copy()
                
                # Load first portfolio
                load_portfolio(portfolio_options1[selected_portfolio1])
                monthly_etfs_df1, group1_df1, group2_df1, group3_df1 = load_dataframes()
                months, monthly_income1, monthly_etf_income1, group1_quarterly1, group2_quarterly1, group3_quarterly1 = calculate_monthly_income(
                    monthly_etfs_df1, group1_df1, group2_df1, group3_df1
                )
                total_investment1, annual_income1, avg_monthly_income1, portfolio_yield1 = calculate_portfolio_metrics(
                    monthly_etfs_df1, group1_df1, group2_df1, group3_df1, 
                    monthly_etf_income1, group1_quarterly1, group2_quarterly1, group3_quarterly1
                )
                
                # Load second portfolio
                load_portfolio(portfolio_options2[selected_portfolio2])
                monthly_etfs_df2, group1_df2, group2_df2, group3_df2 = load_dataframes()
                months, monthly_income2, monthly_etf_income2, group1_quarterly2, group2_quarterly2, group3_quarterly2 = calculate_monthly_income(
                    monthly_etfs_df2, group1_df2, group2_df2, group3_df2
                )
                total_investment2, annual_income2, avg_monthly_income2, portfolio_yield2 = calculate_portfolio_metrics(
                    monthly_etfs_df2, group1_df2, group2_df2, group3_df2, 
                    monthly_etf_income2, group1_quarterly2, group2_quarterly2, group3_quarterly2
                )
                
                # Restore original state
                st.session_state.monthly_etfs_data = temp_monthly
                st.session_state.group1_data = temp_group1
                st.session_state.group2_data = temp_group2
                st.session_state.group3_data = temp_group3
                
                # Display comparison
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### {selected_portfolio1}")
                    st.metric("Total Investment", f"${total_investment1:,.2f}")
                    st.metric("Annual Income", f"${annual_income1:,.2f}")
                    st.metric("Monthly Average", f"${avg_monthly_income1:,.2f}")
                    st.metric("Portfolio Yield", f"{portfolio_yield1:.2f}%")
                
                with col2:
                    st.markdown(f"### {selected_portfolio2}")
                    st.metric("Total Investment", f"${total_investment2:,.2f}")
                    st.metric("Annual Income", f"${annual_income2:,.2f}")
                    st.metric("Monthly Average", f"${avg_monthly_income2:,.2f}")
                    st.metric("Portfolio Yield", f"{portfolio_yield2:.2f}%")
                
                # Highlight differences
                st.markdown("### Portfolio Differences")
                
                diff_investment = total_investment2 - total_investment1
                diff_annual = annual_income2 - annual_income1
                diff_monthly = avg_monthly_income2 - avg_monthly_income1
                diff_yield = portfolio_yield2 - portfolio_yield1
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Investment Difference", 
                             f"${diff_investment:,.2f}", 
                             f"{diff_investment/total_investment1*100:.1f}%",
                             delta_color="normal")
                
                with col2:
                    st.metric("Annual Income Difference", 
                             f"${diff_annual:,.2f}", 
                             f"{diff_annual/annual_income1*100:.1f}%",
                             delta_color="normal")
                
                with col3:
                    st.metric("Monthly Income Difference", 
                             f"${diff_monthly:,.2f}", 
                             f"{diff_monthly/avg_monthly_income1*100:.1f}%",
                             delta_color="normal")
                
                with col4:
                    st.metric("Yield Difference", 
                             f"{diff_yield:.2f}%", 
                             f"{diff_yield:.2f}%",
                             delta_color="normal")

def render_import_export_tab():
    """Render the import/export portfolio tab"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Export Portfolio")
        
        portfolios = get_all_portfolios()
        if not portfolios:
            st.info("No portfolios saved yet to export.")
        else:
            portfolio_options = {f"{p['name']}": p['id'] for p in portfolios}
            selected_portfolio = st.selectbox(
                "Select a portfolio to export", 
                options=list(portfolio_options.keys()),
                key="export_portfolio_select"
            )
            
            if selected_portfolio:
                selected_id = portfolio_options[selected_portfolio]
                
                if st.button("Export to CSV", use_container_width=True):
                    with tempfile.TemporaryDirectory() as temp_dir:
                        export_path = export_portfolio_to_csv(selected_id, temp_dir)
                        
                        if export_path:
                            # Create a zip file for download
                            import zipfile
                            import shutil
                            
                            # Create a zip file in the temporary directory
                            zip_path = os.path.join(temp_dir, f"dove_portfolio_{selected_portfolio}.zip")
                            with zipfile.ZipFile(zip_path, 'w') as zipf:
                                for root, dirs, files in os.walk(export_path):
                                    for file in files:
                                        file_path = os.path.join(root, file)
                                        zipf.write(file_path, os.path.relpath(file_path, export_path))
                            
                            # Read the zip file
                            with open(zip_path, "rb") as file:
                                st.download_button(
                                    label="Download CSV Export",
                                    data=file,
                                    file_name=f"dove_portfolio_{selected_portfolio}.zip",
                                    mime="application/zip",
                                    key="portfolio_export_download"
                                )
                            
                            st.success(f"Portfolio '{selected_portfolio}' exported successfully!")
    
    with col2:
        st.markdown("### Import Portfolio")
        
        portfolio_name = st.text_input("New Portfolio Name", key="import_portfolio_name")
        portfolio_desc = st.text_area("Description (optional)", key="import_portfolio_desc", height=50)
        
        # Upload files
        st.markdown("Upload CSV files for each component:")
        
        monthly_csv = st.file_uploader("Monthly ETFs CSV", type=["csv"], key="upload_monthly")
        group1_csv = st.file_uploader("Jan/Apr/Jul/Oct Stocks CSV", type=["csv"], key="upload_group1")
        group2_csv = st.file_uploader("Feb/May/Aug/Nov Stocks CSV", type=["csv"], key="upload_group2")
        group3_csv = st.file_uploader("Mar/Jun/Sep/Dec Stocks CSV", type=["csv"], key="upload_group3")
        
        if st.button("Import Portfolio", use_container_width=True):
            if not portfolio_name:
                st.error("Please enter a portfolio name")
            elif not all([monthly_csv, group1_csv, group2_csv, group3_csv]):
                st.error("Please upload all required CSV files")
            else:
                # Create temporary files for the uploads
                with tempfile.TemporaryDirectory() as temp_dir:
                    monthly_path = os.path.join(temp_dir, "monthly.csv")
                    group1_path = os.path.join(temp_dir, "group1.csv")
                    group2_path = os.path.join(temp_dir, "group2.csv")
                    group3_path = os.path.join(temp_dir, "group3.csv")
                    
                    # Write uploaded data to temp files
                    with open(monthly_path, "wb") as f:
                        f.write(monthly_csv.getvalue())
                    with open(group1_path, "wb") as f:
                        f.write(group1_csv.getvalue())
                    with open(group2_path, "wb") as f:
                        f.write(group2_csv.getvalue())
                    with open(group3_path, "wb") as f:
                        f.write(group3_csv.getvalue())
                    
                    # Import from temp files
                    success, result = import_portfolio_from_csvs(
                        portfolio_name, portfolio_desc,
                        monthly_path, group1_path, group2_path, group3_path
                    )
                    
                    if success:
                        if result == "created":
                            st.success(f"Portfolio '{portfolio_name}' imported successfully!")
                        else:
                            st.success(f"Portfolio '{portfolio_name}' updated successfully!")
                    else:
                        st.error(f"Error importing portfolio: {result}")