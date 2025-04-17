# COVID-19 India Analysis Dashboard

A comprehensive data analysis and visualization dashboard for COVID-19 trends in India, built using Python and Streamlit.

## Features

- **Interactive State Selection**: Choose between "All India" view or specific state analysis
- **Real-time Metrics Display**:
  - Total Confirmed Cases
  - Total Deaths
  - Total Recoveries
  - Active Cases
- **Interactive Visualizations**:
  - Daily New Cases with 7-day Moving Average
  - Daily Deaths with 7-day Moving Average
  - Daily Recoveries with 7-day Moving Average
  - Total Cases Over Time
- **Data Quality Features**:
  - Automatic handling of missing values
  - Removal of duplicate entries
  - Data cleaning and preprocessing
  - Moving averages for trend analysis

## Technologies Used

- **Python Libraries**:
  - `pandas`: Data manipulation and analysis
  - `numpy`: Numerical computations
  - `plotly`: Interactive visualizations
  - `streamlit`: Web application framework
  - `datetime`: Date handling

## Dataset

The project uses the following dataset:
- `covid_19_india.csv`: Contains daily COVID-19 cases, deaths, and recoveries for each state in India

## Setup Instructions

1. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   ```

2. **Activate Virtual Environment**:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run covid_analysis.py
   ```

## Project Structure

```
Covid19/
├── dataset/
│   └── covid_19_india.csv
├── covid_analysis.py
├── requirements.txt
└── README.md
```

## Data Processing Pipeline

1. **Data Loading**:
   - Load COVID-19 dataset
   - Convert dates to datetime format
   - Clean state names
   - Handle missing values

2. **Data Cleaning**:
   - Remove duplicate entries
   - Convert numeric columns to integers
   - Sort data by date

3. **Data Preprocessing**:
   - Calculate daily new cases, deaths, and recoveries
   - Compute 7-day moving averages
   - Handle negative values and data artifacts

4. **Visualization**:
   - Create interactive plots using Plotly
   - Display key metrics
   - Show data tables


## Features in Detail

### Data Cleaning
- Automatic handling of missing values
- Removal of duplicate entries
- Conversion of data types
- Sorting and organization of data

### Visualizations
- Interactive line charts
- 7-day moving averages for trend analysis
- Unified hover mode for easy data exploration
- Clear labeling and legends

### Metrics Display
- Real-time calculation of key metrics
- Formatted numbers for better readability
- Active cases calculation