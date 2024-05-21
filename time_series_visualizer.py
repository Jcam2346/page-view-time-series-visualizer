import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates=True)
pd.options.display.float_format='{:.0f}'.format

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
df_clean = df
df_clean['date'] = pd.to_datetime(df_clean['date'])

def draw_line_plot():
    # Draw line plot

    fig, ax1 = plt.subplots(figsize=(25, 8))
    ax1.plot(df_clean['date'], df_clean['value'])
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Page Views')
    plt.locator_params(axis='x', nbins=8)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    df_bar = df_bar.set_index('date')
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month_name()
    
    df_bar = pd.DataFrame(df_bar.groupby(by=['Years','Months'], sort= False)['value'].mean().round().astype(int))
    df_bar = df_bar.reset_index()

    fill_data = {
        "Years": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]
    }

    df_bar = pd.concat([pd.DataFrame(fill_data),df_bar])
    
    df_bar = df_bar.rename(columns={'value':'Average Page Views'})
    
    df_bar = df_bar.reset_index(drop = True)
    
    fig, ax1 = plt.subplots(layout = 'constrained', figsize=(15, 9))
    ax1.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    #Legend set to false within sns.barplot because otherwise the legend rectangles are counted towards the total number of bars and we fail the test
    sns.barplot(data = df_bar, x='Years', y='Average Page Views', ax= ax1, hue = df_bar['Months'], palette= 'inferno', legend=False)
        #handles, labels = ax1.get_legend_handles_labels()
    #unfortunately the legend labels have to go uncoloured because of this method
    ax1.legend(labels = list(df_bar['Months'].unique()))
        #sns.move_legend(ax1, bbox_to_anchor=(1,0.5), loc = 'center left', frameon=False)
    
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    #print(df_box.head(30))

    # Draw box plots (using Seaborn)
    sort_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
       
    fig, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(16, 9))
    sns.boxplot(data=df_box, x = df_box['year'], y = df_box['value'], ax=ax1[0], palette= 'tab10')
    ax1[0].set_title('Year-wise Box Plot (Trend)')
    ax1[0].set_xlabel('Year')
    ax1[0].set_ylabel('Page Views')
    sns.boxplot(data=df_box, x = df_box['month'], y = df_box['value'], order=sort_order, ax=ax1[1], hue = df_box['month'], palette= 'inferno')
    ax1[1].set_title('Month-wise Box Plot (Seasonality)')
    ax1[1].set_xlabel('Month')
    ax1[1].set_ylabel('Page Views')
    
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
