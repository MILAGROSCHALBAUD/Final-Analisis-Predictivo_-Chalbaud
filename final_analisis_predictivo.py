# -*- coding: utf-8 -*-
"""Final_Analisis_Predictivo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WL2H4XVUnZGsrlNGL8XKKK7kuZtkZ6BC
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, RandomizedSearchCV, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn import preprocessing
from sklearn.metrics import r2_score
from sklearn.preprocessing import scale
from math import *

from google.colab import drive
drive.mount('/content/gdrive')

datos = pd.read_csv('/content/gdrive/MyDrive/FINAL PREDICITVO/final.csv',sep=',')

import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(15, 10))
sns.heatmap(datos.corr(), annot=True, center=True)

corr_matrix = datos.corr()
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
fig = plt.figure(figsize=[10,8])
sns.heatmap(corr_matrix,cmap='seismic',linewidth=1.5,linecolor='white',vmax = 1, vmin=-1,mask=mask, annot=True,fmt='0.2f')
plt.title('Correlation matrix', weight='bold',fontsize=20)

x_datos = datos.loc[:, datos.columns != 'y']

y_datos = datos.loc[:, datos.columns == 'y']

x_datos.head()

y_datos.head()

"""BALANCEO CLASES"""

!pip install --upgrade imbalanced-learn

from imblearn.over_sampling import SMOTE

sm = SMOTE(random_state=27)
x_datos, y_datos = sm.fit_resample(x_datos, y_datos)

y_datos.value_counts()

x_datos.info()

datos_cor = pd.concat([y_datos, x_datos], axis=1,)
datos_cor

datos_cor.info()

"""PARTICION DE LA BASE"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train,y_test = train_test_split(x_datos,y_datos,test_size = 0.3,random_state = 0 )

print("Training: {}".format(len(x_train)))
print("Testing: {}".format(len(x_test)))

"""RANDOM FOREST"""

from sklearn.ensemble import RandomForestClassifier
random_forest_model = RandomForestClassifier(max_depth=18, random_state= 42)

random_forest_model.fit(x_train, y_train)

random_forest_model.score(x_test, y_test)

random_forest_model.score(x_train, y_train)

!pip install scikit-learn

import sklearn
print(sklearn.__version__)

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Obtener las predicciones del modelo en el conjunto de prueba
y_pred_test = random_forest_model.predict(x_test)

# Crear la matriz de confusión
cm = confusion_matrix(y_test, y_pred_test)

# Crear figura y ejes
fig, ax = plt.subplots()

# Graficar la matriz de confusión
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)

# Configurar el formato del gráfico
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
ax.set_title('Confusion Matrix - Test Set')

# Mostrar el gráfico
plt.show()

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error
from sklearn import metrics
y_pred = random_forest_model.predict(x_test)

print("Accuracy Score: {}".format(accuracy_score(y_test,y_pred)))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, random_forest_model.predict_proba(x_test)[:,1])

"""XG BOOST"""

import xgboost as xgb
XGboost = xgb.XGBClassifier(max_depth = 22, n_estimators = 160, colsample_bytree = 0.3)
XGboost.fit(x_train,y_train)

XGboost.score(x_test,y_test)

XGboost.score(x_train,y_train)

xgb.plot_importance(XGboost)
plt.rcParams['figure.figsize'] = [5, 5]
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Obtener las predicciones del modelo en el conjunto de prueba
y_pred_test = XGboost.predict(x_test)

# Crear la matriz de confusión
cm = confusion_matrix(y_test, y_pred_test)

# Crear figura y ejes
fig, ax = plt.subplots()

# Graficar la matriz de confusión
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)

# Configurar el formato del gráfico
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
ax.set_title('Confusion Matrix - Test Set')

# Mostrar el gráfico
plt.show()

y_pred = XGboost.predict(x_test)

print("Accuracy Score: {}".format(accuracy_score(y_test,y_pred)))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

roc_auc_score(y_test, XGboost.predict_proba(x_test)[:,1])

"""NAIVE BAYES"""

from sklearn.naive_bayes import GaussianNB
modeloNB = GaussianNB()
modeloNB.fit(x_train, y_train)

modeloNB.score(x_test, y_test)

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Obtener las predicciones del modelo en el conjunto de prueba
y_pred_test = modeloNB.predict(x_test)

# Crear la matriz de confusión
cm = confusion_matrix(y_test, y_pred_test)

# Crear figura y ejes
fig, ax = plt.subplots()

# Graficar la matriz de confusión
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)

# Configurar el formato del gráfico
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
ax.set_title('Confusion Matrix - Test Set')

# Mostrar el gráfico
plt.show()

y_pred = modeloNB.predict(x_test)
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

from sklearn.metrics import roc_curve

y_pred_xb_proba = modeloNB.predict_proba(x_test)
fpr, tpr, thresholds = roc_curve(y_test, y_pred_xb_proba[:,1])
plt.figure(figsize=(6,4))
plt.plot(fpr,tpr,'-g',linewidth=1)
plt.plot([0,1], [0,1], 'k--' )
plt.title('ROC curve for NB Model')
plt.xlabel("False Positive Rate")
plt.ylabel('True Positive Rate')
plt.show()

"""REGRESION"""

from sklearn.linear_model import LogisticRegression
classifier_logreg = LogisticRegression(solver='liblinear', random_state=42)
classifier_logreg.fit(x_train, y_train)

y_pred = classifier_logreg.predict(x_test)
y_pred

roc_auc_score(y_test, classifier_logreg.decision_function(x_test))

print("Accuracy Score: {}".format(accuracy_score(y_test,y_pred)))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
print("RMSE: %f" % (rmse))

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Obtener las predicciones del modelo en el conjunto de prueba
y_pred_test = classifier_logreg.predict(x_test)

# Crear la matriz de confusión
cm = confusion_matrix(y_test, y_pred_test)

# Crear figura y ejes
fig, ax = plt.subplots()

# Graficar la matriz de confusión
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)

# Configurar el formato del gráfico
ax.set_xlabel('Predicted label')
ax.set_ylabel('True label')
ax.set_title('Confusion Matrix - Test Set')

# Mostrar el gráfico
plt.show()

"""ANALISIS DE RESULTADOS



Random Forest:

Precisión: 0.9625

Recall: 0.9277

Exactitud: 0.9449


XGBoost:


Precisión: 0.9620

Recall: 0.9295

Exactitud: 0.9455

Naive Bayes:

Precisión: 0.8810

Recall: 0.8670

Exactitud: 0.8729

Regresión:


Precisión: 0.9782

Recall: 0.8982

Exactitud: 0.9381


Estos resultados indican el rendimiento de cada modelo en términos de precisión, recall y exactitud. La precisión representa la proporción de resultados positivos correctamente clasificados, mientras que el recall indica la proporción de casos positivos que se identificaron correctamente. La exactitud es una medida general de la precisión global del modelo.

En función de estos resultados, se puede observar que los modelos Random Forest y XGBoost obtuvieron resultados similares y superiores en términos de precisión, recall y exactitud en comparación con los modelos Naive Bayes y Regresión. Esto sugiere que los modelos Random Forest y XGBoost pueden ser más adecuados para predecir la suscripción a depósitos a plazo fijo en este contexto.

"""