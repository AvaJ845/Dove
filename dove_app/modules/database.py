# modules/database.py
# Handles database operations for saving and loading portfolios

import sqlite3
import json
import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Create database directory if it doesn't exist
os.makedirs('data', exist_ok=True)
DB_PATH = 'data/dove_portfolios.db'

def initialize_database():
    """Initialize the database if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create portfolios table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        monthly_etfs TEXT,
        group1_stocks TEXT,
        group2_stocks TEXT,
        group3_stocks TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

def save_portfolio(name, description=""):
    """Save current portfolio to database"""
    # Get current portfolio data from session state
    monthly_etfs = json.dumps(st.session_state.monthly_etfs_data)
    group1_stocks = json.dumps(st.session_state.group1_data)
    group2_stocks = json.dumps(st.session_state.group2_data)
    group3_stocks = json.dumps(st.session_state.group3_data)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if portfolio with this name already exists
    cursor.execute("SELECT id FROM portfolios WHERE name = ?", (name,))
    existing = cursor.fetchone()
    
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if existing:
        # Update existing portfolio
        cursor.execute('''
        UPDATE portfolios 
        SET description = ?, updated_at = ?, 
            monthly_etfs = ?, group1_stocks = ?, 
            group2_stocks = ?, group3_stocks = ? 
        WHERE name = ?
        ''', (description, current_time, monthly_etfs, group1_stocks, 
              group2_stocks, group3_stocks, name))
        result = "updated"
    else:
        # Insert new portfolio
        cursor.execute('''
        INSERT INTO portfolios 
        (name, description, created_at, updated_at, 
         monthly_etfs, group1_stocks, group2_stocks, group3_stocks)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, current_time, current_time, 
              monthly_etfs, group1_stocks, group2_stocks, group3_stocks))
        result = "created"
    
    conn.commit()
    conn.close()
    return result

def load_portfolio(portfolio_id):
    """Load portfolio from database into session state"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT monthly_etfs, group1_stocks, group2_stocks, group3_stocks 
    FROM portfolios WHERE id = ?
    ''', (portfolio_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        monthly_etfs, group1_stocks, group2_stocks, group3_stocks = result
        
        # Update session state with loaded data
        st.session_state.monthly_etfs_data = json.loads(monthly_etfs)
        st.session_state.group1_data = json.loads(group1_stocks)
        st.session_state.group2_data = json.loads(group2_stocks)
        st.session_state.group3_data = json.loads(group3_stocks)
        
        return True
    
    return False

def delete_portfolio(portfolio_id):
    """Delete a portfolio from the database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM portfolios WHERE id = ?", (portfolio_id,))
    
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def get_all_portfolios():
    """Get list of all saved portfolios"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT id, name, description, created_at, updated_at 
    FROM portfolios ORDER BY updated_at DESC
    ''')
    
    portfolios = []
    for row in cursor.fetchall():
        portfolios.append({
            'id': row[0],
            'name': row[1],
            'description': row[2],
            'created_at': row[3],
            'updated_at': row[4]
        })
    
    conn.close()
    return portfolios

def export_portfolio_to_csv(portfolio_id, file_path):
    """Export portfolio data to CSV files"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT name, monthly_etfs, group1_stocks, group2_stocks, group3_stocks 
    FROM portfolios WHERE id = ?
    ''', (portfolio_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    
    name, monthly_etfs, group1_stocks, group2_stocks, group3_stocks = result
    
    # Create directory for portfolio export
    export_dir = os.path.join(file_path, f"dove_portfolio_{name.replace(' ', '_')}")
    os.makedirs(export_dir, exist_ok=True)
    
    # Export each component to a separate CSV
    monthly_df = pd.DataFrame(json.loads(monthly_etfs))
    group1_df = pd.DataFrame(json.loads(group1_stocks))
    group2_df = pd.DataFrame(json.loads(group2_stocks))
    group3_df = pd.DataFrame(json.loads(group3_stocks))
    
    monthly_df.to_csv(os.path.join(export_dir, "monthly_etfs.csv"), index=False)
    group1_df.to_csv(os.path.join(export_dir, "group1_stocks.csv"), index=False)
    group2_df.to_csv(os.path.join(export_dir, "group2_stocks.csv"), index=False)
    group3_df.to_csv(os.path.join(export_dir, "group3_stocks.csv"), index=False)
    
    return export_dir

def import_portfolio_from_csvs(name, description, monthly_csv, group1_csv, group2_csv, group3_csv):
    """Import portfolio data from CSV files"""
    try:
        # Read CSVs
        monthly_df = pd.read_csv(monthly_csv)
        group1_df = pd.read_csv(group1_csv)
        group2_df = pd.read_csv(group2_csv)
        group3_df = pd.read_csv(group3_csv)
        
        # Convert to the format needed for session state
        monthly_data = {col: monthly_df[col].tolist() for col in monthly_df.columns}
        group1_data = {col: group1_df[col].tolist() for col in group1_df.columns}
        group2_data = {col: group2_df[col].tolist() for col in group2_df.columns}
        group3_data = {col: group3_df[col].tolist() for col in group3_df.columns}
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Check if portfolio with this name already exists
        cursor.execute("SELECT id FROM portfolios WHERE name = ?", (name,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing portfolio
            cursor.execute('''
            UPDATE portfolios 
            SET description = ?, updated_at = ?, 
                monthly_etfs = ?, group1_stocks = ?, 
                group2_stocks = ?, group3_stocks = ? 
            WHERE name = ?
            ''', (description, current_time, json.dumps(monthly_data), json.dumps(group1_data), 
                  json.dumps(group2_data), json.dumps(group3_data), name))
            result = "updated"
        else:
            # Insert new portfolio
            cursor.execute('''
            INSERT INTO portfolios 
            (name, description, created_at, updated_at, 
             monthly_etfs, group1_stocks, group2_stocks, group3_stocks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, description, current_time, current_time, 
                  json.dumps(monthly_data), json.dumps(group1_data), 
                  json.dumps(group2_data), json.dumps(group3_data)))
            result = "created"
        
        conn.commit()
        conn.close()
        return True, result
        
    except Exception as e:
        return False, str(e)