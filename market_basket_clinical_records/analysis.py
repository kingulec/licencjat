"""
Market basket analysis script for
heart failure dataset
"""
import pandas
from matplotlib import pyplot as plt
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import tools
import operator


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
    Creates items (elements) frequency plot

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
    This function analyze dataset T and counts apriori rules.
    Then apriori rules are sorted and printed.
    It prints the most frequent items and the strongest apriori rules.

    @param T The dataset to analysis
    @param alpha Minimal support value (in %)
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
    confidence = apriori_rules['confidence']
    no_filter = 0
    for num in range(0, len(lift_col)):
        if int(lift_col[num]) == 1:
            continue
        elif int(lift_col[num]) < 1:
            continue
        elif int(lift_col[num]) > 1:
            no_filter += 1
            dictionary = {'lift': lift_col[num],
                          'support': support_col[num],
                          'confidence': confidence[num],
                          'antecedents': set(antecedents_col[num]),
                          'consequents': set(consequent_col[num])}
            filter_rules.append(dictionary)
    print(f"\nNumber of rules with lift greater than 1: {no_filter}")
    # print 10 rules with best lift
    sort_apriori_rules(filter_rules, 'lift')
    print("rules with best support")
    # print 10 rules with best support
    sort_apriori_rules(filter_rules, 'support')
    #  print 10 rules with best confidence
    sort_apriori_rules(filter_rules, 'confidence')


def sort_apriori_rules(rules_list, rule_name):
    """
    Sort apriori rules from largest to smallest
    and prints 10 strengths rules.

    @param rules_list List with apriori rules (list[dict])
    @param rule_name Name of rule to sort by
    """
    sorted_dict_list = sorted(rules_list, key=operator.itemgetter(rule_name), reverse=True)
    keys = sorted_dict_list[0].keys()
    values = []
    for dictionary in sorted_dict_list:
        values.append(list(dictionary.values()))

    sorted_rules_set = pandas.DataFrame(data=values, columns=keys)
    print(sorted_rules_set[['lift', 'antecedents', 'consequents']].head(10))


def main():
    """
    The main function
    """
    dataset = load_data()
    market_basket_analysis(dataset, 0.04)

    frequenty_plot(dataset)


if __name__ == '__main__':
    main()




