import csv
import math

PASSENGER_ID = 0
P_CLASS = 1
NAME = 2
SEX = 3
AGE = 4
SIB_SP = 5
PARCH = 6
SURVIVED = 7


# Read CSV file
def read_csv(name):
    passenger_list = []
    with open(name, newline='') as csvFile:
        passenger_reader = csv.reader(csvFile, delimiter=',')
        for index, row in enumerate(passenger_reader):
            if index > 0:
                passenger_list.append(row)
    return passenger_list


# Change age attribute
def update_age_attribute(passenger_list):
    for passenger in passenger_list:
        passenger_age = int(passenger[AGE])
        if 0 <= passenger_age <= 20:
            passenger[AGE] = "young"
        elif 20 < passenger_age <= 40:
            passenger[AGE] = "middle"
        else:
            passenger[AGE] = "old"


# Entropy calculation
def get_entropy_dict(attribute, passengers):
    entropy_dictionary = {}
    for p in passengers:
        passenger_attribute = p[attribute]
        attribute_value = entropy_dictionary.get(passenger_attribute)
        if attribute_value is None:
            entropy_dictionary[passenger_attribute] = 1
        else:
            entropy_dictionary[passenger_attribute] = attribute_value + 1
    return entropy_dictionary


# Calculate Survived Entropy
def calculate_entropy(dict, passengers):
    survived_entropy = 0
    for value in dict.values():
        survived_entropy -= value / len(passengers) * math.log2(value/len(passengers))
    return survived_entropy


# Get Conditional Entropy Dictionary
def get_conditional_entropy_dict(attribute, attr_key, passengers):
    conditional_entropy_dict = {}
    for p in passengers:
        if p[attribute] == attr_key:
            decision = p[SURVIVED]
            attribute_value = conditional_entropy_dict.get(decision)
            if attribute_value is None:
                conditional_entropy_dict[decision] = 1
            else:
                conditional_entropy_dict[decision] = attribute_value + 1
    return conditional_entropy_dict


# Calculate Conditional Entropy
def calculate_conditional_entropy(conditional_entropy_dict, passengers):
    dict_sum = 0
    for v in conditional_entropy_dict.values():
        dict_sum += v
    entropy = 0
    for value in conditional_entropy_dict.values():
        entropy -= (value/dict_sum) * math.log2(value/dict_sum)
    conditional_entropy_result = dict_sum/len(passengers) * entropy
    return conditional_entropy_result


# Calculate Conditional Entropy
def conditional_entropy(attribute, passengers):
    attribute_dict = get_entropy_dict(attribute, passengers)
    entropy_cond = 0
    for attr in attribute_dict.keys():
        conditional_entropy_dict = get_conditional_entropy_dict(attribute, attr, passengers)
        entropy_cond += calculate_conditional_entropy(conditional_entropy_dict, passengers)
    return entropy_cond


# Calculate conditional entropy
def calculate_gain(entropy, conditional_entropy):
    return entropy - conditional_entropy


def calculate_intrinsic_info(conditional_entropy_dict, passengers):
    dict_sum = 0
    for v in conditional_entropy_dict.values():
        dict_sum += v
    return (-dict_sum/len(passengers)) * math.log2(dict_sum/len(passengers))


# Intrinsic Info
def intrinsic_info(attribute, passengers):
    attribute_dict = get_entropy_dict(attribute, passengers)
    intrinsic_info_result = 0
    for attr in attribute_dict.keys():
        conditional_entropy_dict = get_conditional_entropy_dict(attribute, attr, passengers)
        intrinsic_info_result += calculate_intrinsic_info(conditional_entropy_dict, passengers)
    return intrinsic_info_result


def gain_ratio(gain, intrinsic_info_value):
    return gain/intrinsic_info_value


# Main
def main():
    passenger_list = read_csv('titanic.csv')
    update_age_attribute(passenger_list)
    entropy_dict = get_entropy_dict(SURVIVED, passenger_list)
    entropy = calculate_entropy(entropy_dict, passenger_list)
    print("Entropy: " + str(entropy) + "\n")

    for i in range(1, SURVIVED):
        if i == P_CLASS:
            print("=============")
            print("P_CLASS")
            print("=============")
        elif i == NAME:
            continue
        elif i == SEX:
            print("=============")
            print("SEX")
            print("=============")
        elif i == AGE:
            print("=============")
            print("AGE")
            print("=============")
        elif i == SIB_SP:
            print("=============")
            print("SIB_SP")
            print("=============")
        elif i == PARCH:
            print("=============")
            print("PARCH")
            print("=============")

        conditional_entropy_result = conditional_entropy(i, passenger_list)
        print("Conditional entropy: " + str(conditional_entropy_result))
        gain_result = calculate_gain(entropy, conditional_entropy_result)
        print("Gain: " + str(gain_result))
        intrinsic_info_result = intrinsic_info(i, passenger_list)
        print("Intrinsic Info: " + str(intrinsic_info_result))
        gain_ratio_result = gain_ratio(gain_result, intrinsic_info_result)
        print("Gain Ratio: " + str(gain_ratio_result))
        print("")


if __name__ == "__main__":
    main()

