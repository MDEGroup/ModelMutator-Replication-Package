import matplotlib.pyplot as plt
import numpy as np


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


if __name__ == "__main__":
    plot_d1_stats()