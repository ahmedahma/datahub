import os

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import matplotlib.pyplot as plt
import altair as alt

from shapash.explainer.smart_explainer import SmartExplainer
from mlxtend.plotting import plot_confusion_matrix
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, precision_score, roc_curve


def evaluation(Y_test, predictions):
    recall = recall_score(Y_test, predictions)
    precision = precision_score(Y_test, predictions)
    accuracy = accuracy_score(Y_test, predictions)

    print("Rappel: {}".format(recall))
    print("Precision: {}".format(precision))
    print("Accuracy: {}".format(accuracy))
    print("0 : match \n1: non match")
    plot_confusion_matrix(confusion_matrix(Y_test, predictions))

    return recall, precision, accuracy


pathname = os.path.dirname(os.path.abspath(__file__))

classifier = joblib.load(os.path.join(pathname, 'data/lgbm.pkl'))

train = pd.read_csv(os.path.join(pathname, 'data/train.csv'))
results = pd.read_csv(os.path.join(pathname, 'data/results.csv'))

carbon_emissions = pd.read_csv(os.path.join(pathname, 'data/emissions.csv'))

X_train = train[['given_name_score', 'surname_score', 'address_1_score', 'soc_sec_id_score']]
X_test = results[['given_name_score', 'surname_score', 'address_1_score', 'soc_sec_id_score']]
y_train, y_test = train['label'], results['label']
cm = plot_confusion_matrix(confusion_matrix(results['label'], results['predictions']))[0]

global_recall, global_precision, global_accuracy = evaluation(results['label'], results['predictions'])

features = {
    'given_name_score': 'given_name_score',
    'surname_score': 'surname_score',
    'address_1_score': 'address_1_score',
    'soc_sec_id_score': 'soc_sec_id_score'
}

cohorts = {
    'Global': results.copy(),
    'True_Positive': results[(results['label'] == 1) & (results['predictions'] == 1)].copy(),
    'True_Negative': results[(results['label'] == 0) & (results['predictions'] == 0)].copy(),
    'False_Positive': results[(results['label'] == 0) & (results['predictions'] == 1)].copy(),
    'False_Negative': results[(results['label'] == 1) & (results['predictions'] == 0)].copy()
}
fp = results[(results['label'] == 0) & (results['predictions'] == 1)].copy()
fn = results[(results['label'] == 1) & (results['predictions'] == 0)].copy()

x_columns = ['given_name_score', 'surname_score', 'address_1_score', 'soc_sec_id_score']
X_fp = fp[x_columns]
y_fp = fp['label']
X_fn = fn[['given_name_score', 'surname_score', 'address_1_score', 'soc_sec_id_score']]
y_fn = fn['label']


def interpret_cohort(dataset_x_test_cohort, model, dataset_y_pred):
    xpl = SmartExplainer(features_dict=features)
    xpl.compile(
        x=dataset_x_test_cohort,
        model=model,
        y_pred=dataset_y_pred
    )
    return xpl


st.title('Classifier model card')
st.write('Le classifieur présenté dans cette carte d\'identité de modèle est utilisé pour dédupliquer des individus ' +
         'dans un annuaire. Ce classifieur se base sur le calcul de 4 scores de proximité, chacun calculé ' +
         'différement, + sur 4 colonnes différentes : Nom, Prénom, Adresse et n° de sécurité sociale.')
st.write('Sur cette page, vous pourrez voir comment le classifieur performe sur différentes cohortes de données, ' +
         'notamment celles sur lesquelles il fait des erreurs de prédictions.' + '\n' +
         'La dernière partie de l\'outil est dédiée au diagnostic manuel de ces erreurs.')
st.subheader('General metrics')
st.write('Global confusion matrix', cm)

st.write('Global ROC')
roc_fig = plt.figure()
fp_rate, tp_rate, _ = roc_curve(results['label'], results['predictions'])

fig, ax = plt.subplots(num=1, clear=True)
ax.scatter(fp_rate, tp_rate)
plt.show()
st.pyplot(fig)


st.write('Quantité équivalente de carbone émis suite à l\'entraînement de l\'algorithme')
st.markdown('[Access to Carbon Board](http://localhost:8050)')

carbon_emissions_emissions = carbon_emissions.copy()
carbon_emissions_emissions['emissions'] = carbon_emissions['emissions']*1000000
carbon_emissions_emissions['range'] = list(range(1, len(carbon_emissions)+1))

line_chart = alt.Chart(carbon_emissions_emissions).mark_line(interpolate='basis').encode(
    alt.X('range', title='Nombre de ré entrainement du model'),
    alt.Y('emissions', title='CO2eq en kg (x10^6)')
).properties(
    title = 'Quantité équivalente de carbone émis suite à l\'entraînement de l\'algorithme',
    width=750,
    height=500
)
st.altair_chart(line_chart)

st.write('Quantité d\'énergie utilisée de carbone émis suite à l\'entraînement de l\'algorithme')

carbon_emissions_energy = carbon_emissions.copy()
carbon_emissions_energy['energie_consommee'] = carbon_emissions['energy_consumed']*1000000
carbon_emissions_energy['range'] = list(range(1, len(carbon_emissions)+1))

line_chart = alt.Chart(carbon_emissions_energy).mark_line(interpolate='basis').encode(
    alt.X('range', title='Nombre de ré entrainement du model'),
    alt.Y('energie_consommee', title='Energie utilisée en kWh (x10^6)')
).properties(
    title='Quantité d\'énergie utilisée de carbone émis suite à l\'entraînement de l\'algorithme',
    width=750,
    height=500
)
st.altair_chart(line_chart)

categories_count = ['Global', 'True_Positive', 'True_Negative', 'False_Positive', 'False_Negative']
chosen_count = st.sidebar.selectbox(
    'Which cohort to study ?',
    categories_count
)
df = cohorts[chosen_count]
cohort_explainer = interpret_cohort(df[x_columns], classifier, df['label'])
recall, precision, accuracy = evaluation(df['label'], df['predictions'])
FI = cohort_explainer.contributions

st.subheader("Cohorte sélectionnée : " + chosen_count)

feature_importance = pd.DataFrame({
    'Labels': ['a', 'given_name_score', 'address_1_score', 'surname_score'],
    'FI': [0.058668, 0.112885, 0.381223, 0.447224]
})

fig3 = px.box(feature_importance, x='FI', y='Labels', notched=True)
boxplot_chart = st.plotly_chart(fig3)

st.write('Feature importance description')

st.line_chart(cohort_explainer.contributions[1][:5])


GoodExplanation = st.radio('L\'interprétation proposée vous semble correcte ?', ('Oui', 'Non', 'NSPP'))
IntepretedFeatureImportance = st.radio("L'ordre d'importance des features vous semble-t-il correct ?", ('Oui', 'Non',
                                                                                                        'NSPP'))
CustomFeatureImportance = st.multiselect('Quel ordre d\'importance pour les features ? ', ['', ''])
IncohrentValue = st.text_input("Quelle est la valeur qui a pu troubler l'algorithme ?", "Oui")
DataCollectionIssue = st.radio("Y a t il des incohérences qui vous semblent liées à la collecte", ('Oui', 'Non', 'NSPP'))

if st.checkbox('Mode Exploration :'):
    st.write('Exploration de plusieurs valeurs de F1')
    st.write('Exploration de plusieurs méthodes d\'indexation')
    st.write('Exploration de plusieurs méthodes de calcul de distance')

# Explication locale
# Par record, évaluer :
if st.checkbox('Mode diagnostique :'):
    st.write('Revue des enregistrements erronés')
    st.write("Local Explanations")
    st.write("Exemples de record : ")
    st.write(df)
    LocalCustomFeatureImportance = st.multiselect('Quel ordre d\'importance pour les features ? ',
                                                  feature_importance['Labels'])
    LocalIncoherentValues = st.multiselect('Quel sont les valeurs incohérentes ? ', df.columns)



st.subheader('Performances spécialiste métier')
st.write('Collaboration Humain-AI : lignes à classifier')

st.write(cohorts['False_Negative'])