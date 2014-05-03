import numpy as np
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from sklearn import decomposition
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.grid_search import GridSearchCV

np.set_printoptions(threshold=np.nan, linewidth=np.nan)

TrainFile = 'TrainingData.csv'
TestFile = 'TestData.csv'

traindata = np.genfromtxt(TrainDile, delimiter=',', dtype=float)
testdata = np.genfromtxt(TestFile, delimiter=',', dtype=float)

TEAM_NAMES =  np.genfromtxt('input_data/combined_final_test.csv', delimiter=',', dtype="string")[:,0]
COMPETITOR_NAMES = np.genfromtxt('input_data/combined_final_test.csv', delimiter=',', dtype="string")[:,1]

X_TRAIN = traindata[:len(traindata), 2 : -1]
Y_TRAIN = traindata[:len(traindata),   -1]

X_TEST = testdata[:, 2 : -1]
Y_TEST = testdata[:, -1]

max_score = 0
num_components = 0
'''
Initialize sequence of estimators:
    Data pre-processing
    Feature selection
    Classifier
'''
estimators = []
estimators.append(('scaler', preprocessing.StandardScaler()))
estimators.append(('FeatureSelection', decomposition.SparsePCA()))
estimators.append(('clf', SGD = SGDClassifier(loss='log', penalty='elasticnet', n_iter=100)))
'''
Form a pipeline from the estimators
'''
model = Pipeline(estimators)
'''
Set hyper parameters for grid search
'''
parameters = {
    'FeatureSelection__n_components': (4, 8, 12, 16),
    'FeatureSelection__alpha': (0.1, 1, 10, 100),
    'clf__alpha': (0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001),
    'clef__l1_ratio': (0, 0.15, 0.5, 0.85, 1),
    'clf__n_iter': (10, 50, 80, 250)
}
'''
Set up a cross-validated grid search for the pipeline
'''
grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=1)
'''
TODO
    Run grid_search
    Test fit
    Evaluate AUC
    Analyze pipeline components
'''

