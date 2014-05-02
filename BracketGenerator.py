import numpy as np
from sklearn.linear_model import SGDClassifier, LogisticRegression

import SeasonMatcher
import KaggleMatcher
import Constants

np.set_printoptions(threshold=np.nan, linewidth=np.nan)

traindata = np.genfromtxt('input_data/combined_final_train.csv', delimiter=',', dtype=float)
testdata = np.genfromtxt('input_data/combined_final_test.csv', delimiter=',', dtype=float)

TEAM_NAMES =  np.genfromtxt('input_data/combined_final_test.csv', delimiter=',', dtype="string")[:,0]
COMPETITOR_NAMES = np.genfromtxt('input_data/combined_final_test.csv', delimiter=',', dtype="string")[:,1]

X_TRAIN = traindata[:len(traindata), 2 : -1]
Y_TRAIN = traindata[:len(traindata),   -1]

X_TEST = testdata[:, 2 : -1]
Y_TEST = testdata[:, -1]

max_score = 0
num_components = 0

def fit(alg, X, Y):
    Ycheck = alg.predict(X)
    Yproba = alg.predict_proba(X)
    total_sum = 0.0
    total_sum_incorrect_probability = 0.0
    for i in xrange(len(Y)):
        if Y[i] == Ycheck[i]:
            total_sum += 1
        else:
            if Y[i] == 1:
                total_sum_incorrect_probability += Yproba[i][0]
            else:
                total_sum_incorrect_probability += Yproba[i][1]
    
    for index, item in enumerate(Y):
        if Ycheck[index] < 0.5:
            Ycheck[index] = 0
        else:
            Ycheck[index] = 1

    team_seed = ""
    competitor_seed = ""
    #print TEAM_NAMES
    
    '''
    if Y is Y_TEST:
        year = Constants.rootdirs[Constants.year]
        for index, item in enumerate(Y):
            found_1 = False
            team_name = TEAM_NAMES[index]
            team_name_kaggle_num = KaggleMatcher.final_teams_indices[team_name[:-5]]
            for conference in SeasonMatcher.conferences_by_year[year]:
                if team_name_kaggle_num in SeasonMatcher.conferences_by_year[year][conference]:
                    team_seed = SeasonMatcher.conferences_by_year[year][conference][team_name_kaggle_num]
                    found_1 = True
                
            found_2 = False
            competitor = COMPETITOR_NAMES[index]
            competitor_kaggle_num = KaggleMatcher.final_teams_indices[competitor[:-5]]
            for conference in SeasonMatcher.conferences_by_year[year]:
                if competitor_kaggle_num in SeasonMatcher.conferences_by_year[year][conference]:
                    competitor_seed = SeasonMatcher.conferences_by_year[year][conference][competitor_kaggle_num]
                    found_2 = True

            if found_1 and found_2:
                seed_diff = team_seed - competitor_seed
            
                if(Yproba[index][0] >= 0.5):
                    prob_to_print = Yproba[index][0]
                else:
                    prob_to_print = Yproba[index][1]

            if prob_to_print < 0.6:
                if seed_diff >= 1 and Ycheck[index] == 1:
                    Ycheck[index] = 0
                    
                seed_diff = competitor_seed - team_seed
                if seed_diff >= 1 and Ycheck[index] == 0:
                    Ycheck[index] = 1
                
                if seed_diff >= 15 and Ycheck[index] == 1:
                    Ycheck[index] = 0
                    
                seed_diff = competitor_seed - team_seed
                if seed_diff >= 15 and Ycheck[index] == 0:
                    Ycheck[index] = 1
    '''
    '''
    if found_1 and found_2:
        seed_diff = team_seed - competitor_seed
        
        if(Yproba[index][0] >= 0.5):
            prob_to_print = Yproba[index][0]
        else:
            prob_to_print = Yproba[index][1]
        
        if prob_to_print < 0.52:
            if seed_diff >= 5 and Ycheck[index] == 1:
                Ycheck[index] = 0
                
            seed_diff = competitor_seed - team_seed
            if seed_diff >= 5 and Ycheck[index] == 0:
                Ycheck[index] = 1
        
        if seed_diff >= 15 and Ycheck[index] == 1:
            Ycheck[index] = 0
            
        seed_diff = competitor_seed - team_seed
        if seed_diff >= 15 and Ycheck[index] == 0:
            Ycheck[index] = 1
    '''

    all_data = []
    for index, item in enumerate(Y):
        if Ycheck[index] < 0.5:
            Ycheck[index] = 0
        else:
            Ycheck[index] = 1
        if Y is not Y_TRAIN:
            
            if(Yproba[index][0] >= 0.5):
                prob_to_print = Yproba[index][0]
            else:
                prob_to_print = Yproba[index][1]
            
            correct_or_incorrect = "CORRECT"
            
            if(Y[index] != Ycheck[index]):
                correct_or_incorrect = "INCORRECT"

            team_name = TEAM_NAMES[index]
            competitor = COMPETITOR_NAMES[index]
            
            data_result = [team_name, competitor, item, Ycheck[index], prob_to_print, correct_or_incorrect]

            all_data.append(data_result)

    all_data.sort(key=lambda x:float(x[4]), reverse=True)
    for row in all_data:
        print row[0] + "\t" + row[1] + "\t" + str(row[2]) + "\t" + str(row[3]) + "\t" + str(row[4]) + "\t" + row[5]# + "\t" + str(team_seed) + "\t" + str(competitor_seed)

    total_sum = sum([Y[j]==Ycheck[j] for j in xrange(len(Y))])
    score = float(total_sum)/len(Ycheck)

    return [score, total_sum, total_sum_incorrect_probability]

def run_alg(alg):
    clf = alg.fit(X_TRAIN, Y_TRAIN)
    
    result = fit(clf, X_TRAIN, Y_TRAIN) 
    print "TRAIN: " + str(result[0]) + "\t" + str(result[1]) + "\t" + str(result[2])
    
    result = fit(alg, X_TEST, Y_TEST) 
    print "TEST: " + str(result[0]) + "\t" + str(result[1]) + "\t" + str(result[2])

LG = LogisticRegression()
result = run_alg(LG)

'''
SGD = SGDClassifier(loss='log', penalty='elasticnet', alpha=0.1, n_iter=100)
result = run_alg(SGD)
'''