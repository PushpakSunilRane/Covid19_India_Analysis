import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime

# Set page config
st.set_page_config(page_title="COVID-19 India Analysis", layout="wide")

# Load and clean data
@st.cache_data
def load_data():
    # Load COVID-19 cases data
    cases_df = pd.read_csv('dataset/covid_19_india.csv')
    
    # Convert date column to datetime
    cases_df['Date'] = pd.to_datetime(cases_df['Date'])
    
    # Clean state names
    cases_df['State/UnionTerritory'] = cases_df['State/UnionTerritory'].str.strip()
    
    # Handle missing values
    cases_df['Confirmed'] = cases_df['Confirmed'].fillna(0)
    cases_df['Deaths'] = cases_df['Deaths'].fillna(0)
    cases_df['Cured'] = cases_df['Cured'].fillna(0)
    
    # Convert numeric columns to integers
    numeric_columns = ['Confirmed', 'Deaths', 'Cured']
    for col in numeric_columns:
        cases_df[col] = pd.to_numeric(cases_df[col], errors='coerce').fillna(0).astype(int)
    
    # Remove duplicate entries
    cases_df = cases_df.drop_duplicates(subset=['Date', 'State/UnionTerritory'], keep='last')
    
    # Sort by date
    cases_df = cases_df.sort_values('Date')
    
    return cases_df

# Data preprocessing
def preprocess_data(cases_df, selected_state):
    if selected_state == 'All India':
        # Aggregate cases data by date for all India
        state_data = cases_df.groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Cured': 'sum'
        }).reset_index()
    else:
        # Filter data for selected state
        state_data = cases_df[cases_df['State/UnionTerritory'] == selected_state].copy()
        state_data = state_data.groupby('Date').agg({
            'Confirmed': 'sum',
            'Deaths': 'sum',
            'Cured': 'sum'
        }).reset_index()
    
    # Calculate daily new cases
    state_data['New Cases'] = state_data['Confirmed'].diff().fillna(0)
    state_data['New Deaths'] = state_data['Deaths'].diff().fillna(0)
    state_data['New Recoveries'] = state_data['Cured'].diff().fillna(0)
    
    # Remove any negative values (data correction artifacts)
    state_data['New Cases'] = state_data['New Cases'].clip(lower=0)
    state_data['New Deaths'] = state_data['New Deaths'].clip(lower=0)
    state_data['New Recoveries'] = state_data['New Recoveries'].clip(lower=0)
    
    # Calculate 7-day moving averages
    state_data['New Cases MA'] = state_data['New Cases'].rolling(window=7).mean()
    state_data['New Deaths MA'] = state_data['New Deaths'].rolling(window=7).mean()
    state_data['New Recoveries MA'] = state_data['New Recoveries'].rolling(window=7).mean()
    
    return state_data

# Create visualizations
def create_visualizations(state_data, selected_state):
    # Create subplots
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=('Daily New Cases', 'Daily Deaths',
                                      'Daily Recoveries', 'Total Cases Over Time'))
    
    # Daily new cases with moving average
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Cases'],
                  name='Daily Cases', line=dict(color='blue', width=1)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Cases MA'],
                  name='7-day Average', line=dict(color='red', width=2)),
        row=1, col=1
    )
    
    # Daily deaths with moving average
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Deaths'],
                  name='Daily Deaths', line=dict(color='red', width=1)),
        row=1, col=2
    )
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Deaths MA'],
                  name='7-day Average', line=dict(color='black', width=2)),
        row=1, col=2
    )
    
    # Daily recoveries with moving average
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Recoveries'],
                  name='Daily Recoveries', line=dict(color='green', width=1)),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['New Recoveries MA'],
                  name='7-day Average', line=dict(color='darkgreen', width=2)),
        row=2, col=1
    )
    
    # Total cases
    fig.add_trace(
        go.Scatter(x=state_data['Date'], y=state_data['Confirmed'],
                  name='Total Cases', line=dict(color='purple')),
        row=2, col=2
    )
    
    fig.update_layout(
        height=1000, 
        width=1500, 
        title_text=f"COVID-19 Trends in {selected_state}",
        showlegend=True,
        hovermode='x unified'
    )
    
    # Update y-axis labels
    fig.update_yaxes(title_text="Number of Cases", row=1, col=1)
    fig.update_yaxes(title_text="Number of Deaths", row=1, col=2)
    fig.update_yaxes(title_text="Number of Recoveries", row=2, col=1)
    fig.update_yaxes(title_text="Total Cases", row=2, col=2)
    
    return fig

# Main Streamlit app
def main():
    st.title("COVID-19 Trends Analysis 😷💉🏥")
    
    # Load and clean data
    cases_df = load_data()
    
    # Create sidebar for controls
    st.sidebar.title("Controls")
    
    # State selection
    state_options = ['All India'] + sorted(cases_df['State/UnionTerritory'].unique().tolist())
    selected_state = st.sidebar.selectbox(
        "Select State",
        state_options,
        index=0
    )
    
    # Preprocess data for selected state
    state_data = preprocess_data(cases_df, selected_state)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cases", f"{state_data['Confirmed'].max():,}")
    with col2:
        st.metric("Total Deaths", f"{state_data['Deaths'].max():,}")
    with col3:
        st.metric("Total Recoveries", f"{state_data['Cured'].max():,}")
    with col4:
        st.metric("Active Cases", f"{(state_data['Confirmed'].max() - state_data['Cured'].max() - state_data['Deaths'].max()):,}")
    
    # Create and display visualizations
    fig = create_visualizations(state_data, selected_state)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display data table
    st.subheader(f"Latest COVID-19 Data for {selected_state}")
    latest_data = state_data[state_data['Date'] == state_data['Date'].max()]
    st.dataframe(latest_data)

if __name__ == "__main__":
    main() 