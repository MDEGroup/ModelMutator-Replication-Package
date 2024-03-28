import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

def plot_d1_stats():
    # Data
    metamodels = ['Families', 'IEEE', 'MySQL', 'Table', 'XML']
    classes =       [2, 14, 8, 3,5]
    attributes =    [2, 2, 7, 1,6]
    relationships = [8, 31, 7, 2,2]

    x = np.arange(len(metamodels))  # the label locations
    width = 0.2  # the width of the bars

    fig, ax = plt.subplots()
    # Using different shades of blue for each category
    rects1 = ax.bar(x - width, classes, width, label='Classes', color='peachpuff')  # Light Orange
    rects2 = ax.bar(x, attributes, width, label='Attributes', color='sandybrown')  # Medium Orange
    rects3 = ax.bar(x + width, relationships, width, label='Relationships', color='chocolate')  # Dark Orange
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Counts')
    ax.set_title('')
    ax.set_xticks(x)
    ax.set_xticklabels(metamodels)
    ax.legend()

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    fig.tight_layout()

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
    plot()