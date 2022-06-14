"""
This script contains useful tools for market basket analysis project
"""


def sort_dict(dictionary):
    """
    Sorts values in dictionary from the lowest to the highest

    @param dictionary Dictionary

    @return Sorted dictionary
    """
    sorted_values = sorted(dictionary.values())  # Sort the values
    sorted_dict = {}
    for val in sorted_values:
        for key in dictionary.keys():
            if dictionary[key] == val:
                sorted_dict[key] = dictionary[key]
                break
    return sorted_dict


def count_freq(dataset):
    """
    Counts the frequency of appearance items (elements)

    @param dataset Two dementional list in form [[List of items names],[1 or 0 values]]

    @return Dictionary with keys
    """
    dictionary = {}
    col_names = dataset.columns
    for i in range(0, 12):
        freq = 0
        print(col_names[i])
        for n in dataset[col_names[i]]:
            if n == 1:
                freq += 1
        dictionary[col_names[i]] = freq
    return dictionary


