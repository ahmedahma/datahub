import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

diabetes = datasets.load_diabetes()
X = diabetes.data
y = diabetes.target

Y = np.array([y]).transpose()
d = np.concatenate((X, Y), axis=1)
cols = ['age', 'sex', 'bmi', 'bp', 's1', 's2', 's3', 's4', 's5', 's6', 'progression']
data = pd.DataFrame(d, columns=cols)

data.head()

mlflow.set_experiment('/Shared/tracking_demo')


def train_diabetes(data, model, tags={}, params={}):
    def eval_metrics(actual, pred):
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    # Spliting dataset 80% for training, 20% for testing
    train, test = train_test_split(data, test_size=0.2)

    # Removing the target from features
    train_x = train.drop(["progression"], axis=1)
    test_x = test.drop(["progression"], axis=1)

    # The model target
    train_y = train[["progression"]]
    test_y = test[["progression"]]

    with mlflow.start_run():
        model.fit(train_x, train_y)
        ypred = model.predict(test_x)
        (rmse, mae, r2) = eval_metrics(test_y, ypred)

        print("RMSE: %s" % rmse)
        print("MAE: %s" % mae)
        print("R2: %s" % r2)

        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(model, "model")

        mlflow.set_tags(tags)
        mlflow.log_params(params)


baseline_model = DummyRegressor()
train_diabetes(data, baseline_model, tags={'model_type': 'lr_baseline'})

linear_model = LinearRegression()
train_diabetes(data, linear_model, tags={'model_type': 'linear_regression'})

elastic_model = ElasticNet(alpha=0.010000, l1_ratio=1.000000)
train_diabetes(data, elastic_model, tags={'model_type': 'elastic_model'},
               params=dict(alpha=0.010000, l1_ratio=1.000000))

