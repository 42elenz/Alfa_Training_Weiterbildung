import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import StratifiedShuffleSplit

from sklearn.impute import KNNImputer
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

import time
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

def main():
    np.random.seed(42)

    """ Herunterladen der Daten, Vorbereitung der Umgebung und erste Einsichten in die Daten """
    source_train = os.path.join("/home" + os.sep, "esralenz", "Jupyter", "datasets", "titanic", "train.csv")
    source_test = os.path.join("/home" + os.sep, "esralenz", "Jupyter", "datasets", "titanic", "test.csv")
    train_raw = pd.read_csv(source_train)     # pandasdf der Trainingsdaten erstellen
    test_raw = pd.read_csv(source_test)     # pandasdf der Testdatendaten erstellen, wichtig: Hier keine Survived Spalte

    """ Erste Einsicht in den train_raw und test_raw, was für Daten sind hier, fehlen Werte, etc. (siehe Bericht) """
    #print("Train Tail:\n", train_raw.tail(), "Shape:", train_raw.shape)
    #print("Train Describe:\n", train_raw.describe())
   # print("Train Info:\n", train_raw.info())
    #print("Test Tail:\n", test_raw.tail(), "Shape:", test_raw.shape)
  #  print("Test Describe:\n", test_raw.describe())
  #  print("Test Info:\n", test_raw.info())

    """ Kopien der Ursprungsdaten """
    df = train_raw.copy()       
    df_test = test_raw.copy()
    print("DF TEST", df_test["PassengerId"])

    """ Im folgenden wird nur mit dem train_raw weitergearbeitet """
    df = drop_dataset(df)    # Funktion aufrufen, die unserer Meinung nach Redundanzen erhalten

    corr_matrix_all_data = df.corr()       # Korrelationsmatrix erstellen, sodass man sieht ob welche Korrelationen gibt
    print(corr_matrix_all_data["Survived"].sort_values(ascending=False))   

    """ Dadurch, dass die test_raw Daten KEINE Survived-Spalte erhalten, muss die train_raw / df Daten noch einmal gesplittet werden"""
    strat = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in strat.split(df, df["Survived"]):     # nach Survived stratifizieren
        train_set = df.iloc[train_index]
        test_set = df.iloc[test_index]

    """ Trennung der Survived, sodass wir xTrain, yTRain, xTest und yTest haben """
    xTrain_unprepared = train_set.drop("Survived", axis=1)
    yTrain = train_set["Survived"]
    xTest_unprepared = test_set.drop("Survived", axis=1)
    yTest = test_set["Survived"]

    """ Vorbereitung auf die Pipeline: Trennung in numerische und kategorische Daten """
    xTrain_num = xTrain_unprepared.drop(["Embarked", "Sex"], axis=1)

    col_names = "SibSp", "Parch", "Fare"
    # sibsp_ix, parch_ix, fare_ix = [xTrain_num.columns.get_loc(c) for c in col_names]     # NOCH LÖSCHEN
    list_index = [xTrain_num.columns.get_loc(c) for c in col_names]     # Liste aus Index für die Ergänzung von Spalten

    numeric_pipeline = Pipeline([               # Pipeline: in jeder Step wird ein fit_transform durchgeführt
        ('imputer', KNNImputer()),    # Imputer für leere Alter
        ('column_add', CombinedAttributesAdder(list_index)),       # Funktion mit den Indexen der benötigte Daten muss eingefügt werden.
        ('std_scaler', MinMaxScaler()),      # Standardisierung der Daten
    ])

    num_attribs = list(xTrain_num)
    ord_attribs = ["Sex"]
    one_attribs = ["Embarked"]

    full_pipeline = ColumnTransformer([
            ("num", numeric_pipeline, num_attribs),      # aufrufen der numeric_pipeline für die numerische Daten
            ("ord", OrdinalEncoder(), ord_attribs),    # Trennung in entweder 0 oder 1 für männlich oder weiblich
            ("cat", OneHotEncoder(sparse=False), one_attribs),      # Lage der Stadt wird durch ein 3er Vektor dargestellt
        ])

    xTrain = full_pipeline.fit_transform(xTrain_unprepared)             # np.array, fertig transformierte Daten
    xTest = full_pipeline.transform(xTest_unprepared)       # für die predict und scores später

    # ds = pd.DataFrame(xTrain, columns = ["Pclass", "Age", "SibSp", "Parch", "Fare", "Tot_Fam_Members", "Price_PP", "Sex", "City1", "City2", "City3"])
    # # Zwischenergebnis: Nach dem Transformieren kann man einen kurzen Blick in den Daten werfen

    """ Maschine Learning - Vorangehensweise: Zu jedem Klassifikationsmethode wurde erst einmal eine score erstellt mit den Default-Werte erstellt.
    Dafür würde die Klasse 'Model' erstellt, sodass man einzeilige Befehle hat (siehe unten). Anschließend wurde für Algorithmen mit vielen Parametern
    manuell etwas angepasst. Falls bessere Ergebnisse kamen, wurde ein GridSearchCV erstellt. """
    vergleich_ml = []
    model = Model(xTrain, yTrain, xTest, yTest)    # Aufrufen der Klasse mit dem Datensätze x/yTrain und xy/Test

    bayes_model = GaussianNB()      # Algorithmus wird erst initialisiert, anschließend die Funktion wird durchgeführt, analoge Vorgehensweise
    model.choose_model(bayes_model, "bayes_default", vergleich_ml)

    log_model = LogisticRegression()      
    model.choose_model(log_model, "logreg_default", vergleich_ml)
    
    knn_model = KNeighborsClassifier()       # default-Wert n_neighbors= 5
    model.choose_model(knn_model, "knn_default", vergleich_ml)

    KNN_model = KNeighborsClassifier(n_neighbors=10)      # schauen, ob es mit mehr Nachbarn besser wird; auch möglich: weight auf distance ändern
    model.choose_model(KNN_model, "knn_10_n", vergleich_ml)

    svc_model = SVC(random_state=42)
    model.choose_model(svc_model, "svc_default", vergleich_ml)

    SVC_model = SVC(C=10, decision_function_shape='ovr', probability = True, random_state=42)       # manuelles ausprobieren mit andere Parametern
    model.choose_model(SVC_model, "svc_c10", vergleich_ml)

    # # Ausprobieren mit parameter-grid, da es manuell besser wurde
    parameters_svc ={
        'decision_function_shape' : ('ovo','ovr'), # one vs all oder one vs rest 
        'C': (0.1, 1.0, 10) ,     # The strength of the regularization is inversely proportional to C: Breite der Straße
        'kernel' : ('linear', 'rbf'),      # wie der kernel von den datenmatrix pre-coputed wird
        'gamma' : ("scale", "auto"),
        }
    model.choose_grid(svc_model, parameters_svc, "svc_grid", vergleich_ml)

    tree_model = DecisionTreeClassifier(random_state=42)
    model.choose_model(tree_model, "tree_default", vergleich_ml)

    TREE_model = DecisionTreeClassifier(criterion='entropy', min_samples_leaf=4, max_features=8, random_state=42)   # manuelles ausprobieren mit andere Parametern
    model.choose_model(TREE_model, "tree_adapted", vergleich_ml)

    parameters_tree = {
                'criterion' : ('gini', 'entropy'),     # Kriteria, um das Splitting des Trees zu messen; Gini = impurity, Entropy = Zunahme an Information
                'max_depth': ('None', 5, 8, 11 ) ,      # Tiefe des Baumes
                'max_features' : (3, 6, 8, 11),        # Wie viele Features (Spalten) in die Entscheidung genommen werden sollen
                'min_samples_leaf' : (2, 3, 4, 5, 6, 7, 10, 12)     # Wie viele Daten in ein leaf node sein müssen
                }
    model.choose_grid(tree_model, parameters_tree, "tree_grid", vergleich_ml)


   # mpl_model = MLPClassifier(random_state=42)
    #model.choose_model(mpl_model, "mpl_default", vergleich_ml)

    #MLP_model = MLPClassifier(hidden_layer_sizes=(30), max_iter=1000, random_state=42)
    #model.choose_model(MLP_model, "mpl_adapted", vergleich_ml)

    #parameters_mlp ={
             # 'activation' : ('identity', 'logistic', 'tanh', 'relu'),
             # 'hidden_layer_sizes': [(150), (100), (80), (50), (30), (20)],   # Wie viele Hidden Layers soll es geben, Erklärung siehe Bericht
              #'solver' : ('lbfgs', 'sgd'),
               #'learning_rate' : ('constant', 'invscaling', 'adaptive'),
               # 'learning_rate_init' : (0.001, 0.01, 0.1, 1),    # Kontrolliert die Step-Size für das Updaten der Gewichte
              #'max_iter' : (100, 200, 400)     #  Wie viele Iterationen soll es machen, wenn es vorher abbrechen soll HIER NOCH EINMAL MIT 100?
               #  }
    #model.choose_grid(mpl_model, parameters_mlp, "mlp_grid", vergleich_ml)

    """ Voting: Es wird die mittlere predicted Wahrscheinlichkeit von den Klassifiers genutzt, um die Labels der Klassen zu predicten """
    voting_clf = VotingClassifier(
        estimators=[('DecisionTree', TREE_model), ('SVC', SVC_model), ('KNN', knn_model)],
        voting='soft')      # soft (prozentuale Anteil wird berechnet und anschließend zugeordnet)

    for clf in (TREE_model, SVC_model, knn_model, voting_clf):
        clf.fit(xTrain, yTrain)     # fitten jeweils der oben bessere Modelle
        yPred = clf.predict(xTest)     # Predicten mit der xTest-Menge
        print(clf.__class__.__name__, accuracy_score(yTest, yPred))    # printen des Scores zu jedem Algorithmus

    """ beste Algorithmus: DecisionTreeClassifier mit eigenen angegeben Parameter. Kann man dies genauer machen mit den RandomForest? """
    FOREST_model = RandomForestClassifier(criterion='entropy', min_samples_leaf=4, random_state=42)    # mit den oberen Werten
    model.choose_model(FOREST_model, "forest_adapted", vergleich_ml)

    forest_model = RandomForestClassifier(random_state=42)
    parameter_forest = {'bootstrap': [False], 'n_estimators': np.linspace(10, 150, num=8).astype(int), 
                        'max_features': [3, 5, 7]},    
    model.choose_grid(forest_model, parameter_forest, "forest_grid", vergleich_ml)    # GridSearchCV für den RandomForest: Wird es besser mit mehrere Features?

    """ Präsentieren der Scores """
    # pd.DataFrame(vergleich_ml, columns = ["Model", "Train-Score", "Test-Score", "Laufzeit"]).to_csv('Vergleich_Klassifikationen.csv')
    import xgboost as xgb

    class_compare = pd.DataFrame(vergleich_ml, columns = ["Model", "Train-Score", "Test-Score", "Laufzeit"])
    print(class_compare)

    """ Letztes: Modell für das df_test machen; auf Kaggle können die Ergebnisse hochgeladen werden """
    df_ID = df_test["PassengerId"]
    df_test = drop_dataset(df_test)     # löschen unnützende Spalten

    Test = full_pipeline.transform(df_test)     # transformieren der Daten
    Test = xgb.DMatrix(Test)

    xg_p_param = {"max_depth": 4,
                  "eta": 0.2,
                  "objective": "multi:softmax",
                  "num_class": 3
                  }
    epochs = 10

    final_model = TREE_model
    final_model.fit(xTrain, yTrain)
    final_predictions = final_model.predict(Test)
    print(final_predictions.T)
    df_ID["Survived"] = final_predictions
    print(df_ID)

    """ Predicted Werte mit dem df_test (hard copy von test.csv) in einer Dateien hinzufügen, die die unlabeled Daten aus test.csv erhalten. """
    df_result = pd.DataFrame(final_predictions)
    df_test["Survived"] = df_result
    df_test.to_csv("result.csv")


def drop_dataset(data):
    # # Drop some columns and rows due to unnecessary or unclear information
    data = data.dropna(subset=["Embarked"])   # deletes the rows with zero
    data = data.drop("Cabin", axis=1)      # to little values (204 of 891)
    data = data.drop("Ticket", axis=1)      # not clear what it says
    data = data.drop("Name", axis=1)    # redundance
    data = data.drop("PassengerId", axis=1)    # redundance
    return data

class CombinedAttributesAdder(BaseEstimator, TransformerMixin):
    # # Hinzufügen von neue Spalten: Anzahl der Gesamte Familienmitglieder und des Preises pro Person

    def __init__(self, liste): 
        self.liste = liste

    def fit(self, data, y=None):
        return self  # nothing else to do  
        
    def transform(self, data):
        Tot_Fam_Members = data[:, self.liste[0]] + data[:, self.liste[1]] + 1    # calculating the total number of relatives in one family
        Price_PP = data[:, self.liste[2]] / Tot_Fam_Members
        return np.c_[data, Tot_Fam_Members, Price_PP]


class Model():
    # # Klassen, die einerseits für ein Algorithmus den fit und score erstellen, andererseits der GridSearchCV automatisieren und direkt

    def __init__(self, xTrain, yTrain, xTest, yTest):
        self.xTrain =xTrain
        self.yTrain = yTrain
        self.xTest = xTest
        self.yTest =yTest

    def choose_model(self, model, name, liste):
        # # Laufzeit wird gemessen, Model wird gefittet und score angelegt.
        start = time.time()
        model.fit(self.xTrain, self.yTrain)
        train_score = model.score(self.xTrain, self.yTrain)
        test_score = model.score(self.xTest, self.yTest)
        laufzeit = '{:5.3f}s'.format(time.time()-start)
        liste.append([name, train_score, test_score, laufzeit])

    def choose_grid(self, estimator, parameter, name, liste):
        # # Hier werden zwei Schritte erstellt: Erst einmal das GridSearchCV erstellt und gefittet, anschließend das best_estimator_ herausgeholt
        # # Anschließend den Score mit dem besten Estimator durchgeführt.

        model = GridSearchCV(estimator, parameter, scoring='neg_mean_squared_error', n_jobs=-1, cv=5)
        model.fit(self.xTrain, self.yTrain)

        svc_best_est = model.best_estimator_
        train_score = svc_best_est.score(self.xTrain, self.yTrain)
        test_score = svc_best_est.score(self.xTest, self.yTest)

        liste.append([name, train_score, test_score, -1])   # in der Vergleichstabelle hinzugefügt


if __name__ == "__main__":
    main()