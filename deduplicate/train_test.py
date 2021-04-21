from sklearn.model_selection import train_test_split


def train_test(data):
    train, test = train_test_split(data, test_size=0.25)
    X_train = train.drop('label', axis=1, inplace=False)
    X_test = test.drop('label', axis=1, inplace=False)
    y_train = train[['label']]
    y_test = test[['label']]

    dic = {'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}

    return dic
