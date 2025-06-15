import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

def load_data():
    """Load data from CSV files using pandas"""
    print("\nLoading data...")
    
    # Load daily activity data
    df = pd.read_csv('daily_activity_for_powerbi.csv')
    
    # Convert date column to datetime
    df['ActivityDate'] = pd.to_datetime(df['ActivityDate'])
    
    # Add weekday and week number columns
    df['Weekday'] = df['ActivityDate'].dt.day_name()
    df['WeekNumber'] = df['ActivityDate'].dt.week
    
    return df

def analyze_data(df):
    """Perform detailed analysis using pandas"""
    # Create output directory
    output_dir = 'pandas_analysis'
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Basic Statistics
    print("\n=== Basic Statistics ===")
    stats = {
        'Total Participants': df['Id'].nunique(),
        'Total Records': len(df),
        'Study Duration': f"{df['ActivityDate'].min().strftime('%Y-%m-%d')} to {df['ActivityDate'].max().strftime('%Y-%m-%d')}",
        'Average Steps': df['TotalSteps'].mean(),
        'Average Sedentary': df['SedentaryMinutes'].mean(),
        'Average Lightly Active': df['LightlyActiveMinutes'].mean(),
        'Average Fairly Active': df['FairlyActiveMinutes'].mean(),
        'Average Very Active': df['VeryActiveMinutes'].mean()
    }
    
    # Save statistics to CSV
    stats_df = pd.DataFrame(list(stats.items()), columns=['Metric', 'Value'])
    stats_df.to_csv(os.path.join(output_dir, 'basic_stats.csv'), index=False)
    
    # 2. Daily Trends Analysis
    print("\n=== Daily Trends Analysis ===")
    
    # Daily step distribution
    plt.figure(figsize=(12, 6))
    sns.histplot(df['TotalSteps'], bins=30, kde=True)
    plt.title('Daily Steps Distribution')
    plt.xlabel('Steps')
    plt.ylabel('Frequency')
    plt.savefig(os.path.join(output_dir, 'steps_distribution.png'))
    plt.close()
    
    # Steps by weekday
    plt.figure(figsize=(12, 6))
    weekday_steps = df.groupby('Weekday')['TotalSteps'].mean().sort_values()
    weekday_steps.plot(kind='bar')
    plt.title('Average Steps by Weekday')
    plt.xlabel('Weekday')
    plt.ylabel('Average Steps')
    plt.savefig(os.path.join(output_dir, 'weekday_steps.png'))
    plt.close()
    
    # 3. Correlation Analysis
    print("\n=== Correlation Analysis ===")
    
    # Calculate correlations
    numeric_cols = ['TotalSteps', 'SedentaryMinutes', 'LightlyActiveMinutes', 
                   'FairlyActiveMinutes', 'VeryActiveMinutes', 'Calories']
    corr_matrix = df[numeric_cols].corr()
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Correlation Matrix')
    plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
    plt.close()
    
    # 4. Time Series Analysis
    print("\n=== Time Series Analysis ===")
    
    # Daily activity trends
    plt.figure(figsize=(15, 6))
    df.set_index('ActivityDate')[['TotalSteps', 'Calories']].plot()
    plt.title('Daily Activity Trends')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.savefig(os.path.join(output_dir, 'activity_trends.png'))
    plt.close()
    
    # 5. Activity Type Distribution
    print("\n=== Activity Type Distribution ===")
    
    # Create stacked bar chart
    plt.figure(figsize=(15, 6))
    activity_types = ['SedentaryMinutes', 'LightlyActiveMinutes', 'FairlyActiveMinutes', 'VeryActiveMinutes']
    df.groupby('ActivityDate')[activity_types].sum().plot(kind='bar', stacked=True)
    plt.title('Daily Activity Distribution')
    plt.xlabel('Date')
    plt.ylabel('Minutes')
    plt.savefig(os.path.join(output_dir, 'activity_distribution.png'))
    plt.close()
    
    # 6. Save detailed analysis
    analysis_results = {
        'daily_stats': df.describe().to_dict(),
        'weekday_stats': df.groupby('Weekday').agg({
            'TotalSteps': ['mean', 'std'],
            'SedentaryMinutes': ['mean', 'std'],
            'LightlyActiveMinutes': ['mean', 'std'],
            'FairlyActiveMinutes': ['mean', 'std'],
            'VeryActiveMinutes': ['mean', 'std']
        }).to_dict(),
        'correlations': corr_matrix.to_dict()
    }
    
    # Save analysis results
    with open(os.path.join(output_dir, 'analysis_results.json'), 'w') as f:
        json.dump(analysis_results, f, indent=4)
    
    print(f"\nAnalysis results saved to {output_dir} directory")
    
    return stats

def main():
    try:
        # Load data
        df = load_data()
        
        # Perform analysis
        stats = analyze_data(df)
        
        # Print summary
        print("\n=== Analysis Summary ===")
        for metric, value in stats.items():
            print(f"{metric}: {value}")
            
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
