import pandas as pd
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def convert_month_to_int(month):
    match month:
        case 'Jan':
            month_int = 0
        case 'Feb':
            month_int = 1
        case 'Mar':
            month_int = 2
        case 'Apr':
            month_int = 3
        case 'May':
            month_int = 4
        case 'Jun':
            month_int = 5
        case 'Jul':
            month_int = 6
        case 'Aug':
            month_int = 7
        case 'Set':
            month_int = 8
        case 'Oct':
            month_int = 9
        case 'Nov':
            month_int = 10
        case 'Dec':
            month_int = 11
        case _:
            month_int = 0
    return month_int


def convert_visitor_type_to_int(vtype):
    match vtype:
        case 'Returning_Visitor':
            visitor_int = 1
        case 'New_Visitor':
            visitor_int = 0
        case _:
            visitor_int = 0
    return visitor_int


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)
    num_rows = len(df)
    evidence = []
    labels = []
    for i in range(num_rows):
        current = []
        current.append(int(df.iloc[i]['Administrative']))
        current.append(float(df.iloc[i]['Administrative_Duration']))
        current.append(int(df.iloc[i]['Informational']))
        current.append(float(df.iloc[i]['Informational_Duration']))
        current.append(int(df.iloc[i]['ProductRelated']))
        current.append(float(df.iloc[i]['ProductRelated_Duration']))
        current.append(float(df.iloc[i]['BounceRates']))
        current.append(float(df.iloc[i]['ExitRates']))
        current.append(float(df.iloc[i]['PageValues']))
        current.append(float(df.iloc[i]['SpecialDay']))
        current.append(convert_month_to_int(df.iloc[i]['Month']))
        current.append(int(df.iloc[i]['OperatingSystems']))
        current.append(int(df.iloc[i]['Browser']))
        current.append(int(df.iloc[i]['Region']))
        current.append(int(df.iloc[i]['TrafficType']))
        current.append(convert_visitor_type_to_int(df.iloc[i]['VisitorType']))
        current.append(int(df.iloc[i]['Weekend']))
        evidence.append(current)
        labels.append(int(df.iloc[i]['Weekend']))
    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create KNeighborsClassifier instance
    knn = KNeighborsClassifier(n_neighbors=1)
    # Train the classifier
    return knn.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    num_rows = len(labels)
    total_positive = 0
    num_positive = 0
    total_negative = 0
    num_negative = 0
    for i in range(num_rows):
        cur = labels[i]
        if cur == 0:
            total_negative = total_negative + 1
            if cur == predictions[i]:
                num_negative = num_negative + 1
        elif cur == 1:
            total_positive = total_positive + 1
            if cur == predictions[i]:
                num_positive = num_positive + 1
    sensitivity = num_positive / total_positive
    specificity = num_negative / total_negative
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
