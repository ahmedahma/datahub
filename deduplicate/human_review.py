import pandas as pd
from local_deps.shapash.shapash.explainer.smart_explainer import SmartExplainer


def explain(X_test: pd.DataFrame, y_test: pd.DataFrame, classifier: object, features: dict):
    """
    Parameters:
    -----------
        X_test (pd.DataFrame) : DataFrame used to test classifier
        y_test (pd.DataFrme) : DataFrame used to test classifier
        features (dict) : Features present in DataFrame
        classifier (object) : classifier used to make prediction

    Return:
    -----------
        xpl (object) : SmartExplainer
    """

    xpl = SmartExplainer(features_dict=features)  # optional parameter
    xpl.compile(
        x=X_test,
        model=classifier,
        y_pred=y_test
    )
    return xpl


def plot_explain(explainer, feature_contribution):
    explainer.plot.features_importance()
    explainer.plot.contribution_plot(col=feature_contribution)
