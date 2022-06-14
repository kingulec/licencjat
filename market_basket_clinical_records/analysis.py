import arules
import pandas
import numpy
from matplotlib import pyplot as plt
import plotly.express as px
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import arulesviz
import tools
from decimal import Decimal
#import plotly.express as px


def load_data(path='..\market_basket_clinical_records\modified_dataset.csv'):
    """
    Loads and prepare data to analysis

    @param path Path to csv file with dataset
    @return Parsed dataset
    """
    T = pandas.read_csv(path, delimiter=";",
                        encoding='utf-8')
    print(T.info())  # Checks if dataset contains null values.
    # This dataset doesn't consists null values.
    T = T.drop(columns=["czas"])  # We will not consider 'czas' columns to analysis
    T.head()
    print(type(T))
    return T


def frequenty_plot(dataset):
    """
    Creates items (elements) frequenty plot

    @param dataset Pandas dataframe
    """
    dict = tools.count_freq(dataset)
    dict = tools.sort_dict(dict)
    courses = list(dict.keys())
    values = list(dict.values())
    plt.rc('font', size=20)
    plt.figure(figsize=(10, 5))
    plt.bar(range(len(courses)), values, color='grey', width=0.7)
    plt.ylabel("Liczba wystąpień cechy")
    plt.xticks(range(len(courses)), courses, rotation=65)
    plt.show()


def market_basket_analysis(T, alpha):
    """

    @param T
    @param alpha Minimal support value (in %)

    @return
    """
    freq_items = apriori(T, min_support=alpha,
                         use_colnames=True)
    print("Frequent items:\n")
    # generate frequent item sets
    most_freq_items = freq_items.sort_values('support',
                                             ascending=False)
    print(most_freq_items.head())
    print("Number of rules: ", len(freq_items))
    # Count rules with min therehold 1
    apriori_rules = association_rules(freq_items, metric="lift", min_threshold=1)
    print(apriori_rules.head())
    # Filter rules with lift greater than 1
    filter_rules = []
    print(apriori_rules)
    lift_col = apriori_rules['lift']
    antecedents_col = apriori_rules['antecedents']
    consequent_col = apriori_rules['consequents']
    support_col = apriori_rules['support']
    no_filter = 0
    for num in range(0, len(lift_col)):
        if int(lift_col[num]) == 1:
            continue
        elif int(lift_col[num]) < 1:
            continue
        elif int(lift_col[num]) > 1:
            no_filter += 1
            print(f"lift({set(antecedents_col[num])}"
                  f"=>{set(consequent_col[num])})="
                  f"{Decimal(lift_col[num])}")
            dictionary = {'lift': lift_col[num],
                          'support': support_col[num],
                          'antecedents_col': antecedents_col[num],
                          'consequents_col': consequent_col[num]}
            filter_rules.append(dictionary)
    print(f"\nNumber of rules with lift greater than 1: {no_filter}")


def main():
    dataset = load_data()
    market_basket_analysis(dataset, 0.04)

    # frequenty_plot(dataset)


if __name__ == '__main__':
    main()




