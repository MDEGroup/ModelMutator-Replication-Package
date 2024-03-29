import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MaxNLocator

def plot_d1_stats(figsize=(4, 4)):
    # Data
    domains = ['Families', 'MySQL', 'IEEE1471', 'Table']
    create =  [8, 2, 7, 3]
    edit = [0, 0, 0, 0]
    remove = [0, 0, 0, 0]

    x = np.arange(len(domains))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots(figsize=figsize)
    # Using different shades of blue for each category
    rects1 = ax.bar(x - width, create, width, label='Create', color='darkred')  # Light Orange
    rects2 = ax.bar(x, edit, width, label='Edit', color='sandybrown')  # Medium Orange
    rects3 = ax.bar(x + width, remove, width, label='Remove', color='chocolate')  # Dark Orange
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.set_title('')
    ax.set_xticks(x)
    ax.set_xticklabels(domains)
    ax.legend()

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))


    #fig.tight_layout()

    plt.show()
    plt.savefig('d1_stats.pdf')




def plot():
    # Data

    data = {
        'rules': ['create'] * 4 + ['edit'] * 4 + ['remove'] * 4,
        'Domains': ['ASPLE', 'PFSM', 'BPMN', 'SecurityPol',
                    'Families', 'MySQL', 'IEEE1471', 'Table',
                    'Families', 'MySQL', 'IEEE1471', 'Table'],
        'Count': [0, 1620, 1479, 1479,
                  3828, 2985, 1969, 1479,
                  3828, 2985, 1969, 1479]
    }

    # Creating a DataFrame
    df = pd.DataFrame(data)

    # Assign color groups based on domain
    color_map = {domain: 'blue' if domain in ['ASPLE', 'PFSM', 'BPMN', 'SecurityPol'] else 'green' for domain in
                 df['Domains']}

    # Plotting
    plt.figure(figsize=(12, 8))
    sns.barplot(x='rules', y='Count', hue='Domains', data=df, palette=color_map, dodge=True)

    # Customizing the plot
    plt.legend(title="Domains", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.title('Bar Plot Grouped by Rules with Individual Domain Bars')
    plt.xlabel('Rules')
    plt.ylabel('Count')
    plt.tight_layout()

    # Display the plot
    plt.show()

if __name__ == "__main__":
    plot_d1_stats()