import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
import os
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.utils import resample
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
import gzip
import numpy as np


# mtbls87_training_set = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\mtbls87.csv')
# cao_hilic_training_set = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\Cao_HILIC.csv')

"""
Bring in specified training set files and conglomerate them into training set
"""
orb_plasma_df = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/orb_plasma.csv')
fem_long_df = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/fem_long.csv')
mtbls36_training_set = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/MTBLS36.csv')
mtbls87_training_set = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/mtbls87.csv')
# list_of_df= [orb_plasma_df,fem_long_df]
# list_of_df = []
list_of_df = [mtbls87_training_set,mtbls36_training_set,fem_long_df,orb_plasma_df]
SMRT_file_path = 'WorkingModel/'
i = 1
for file in os.listdir(SMRT_file_path):
    if i < 5:
        print(file)
        try:
            df = pd.read_csv(SMRT_file_path + file)
            list_of_df.append(df)
            i +=1 
        except:
            print('you messed up')
    else:
        break
#
#list_of_df = [fem_long_training_set,life_new_training_set,MTBLS36_new_training_set,first_smrt_training_set]
training_set = pd.concat(list_of_df)
#training_set = training_set.iloc[:,:-1]
# training_set = training_set.drop(['Result'],axis=1)
"""
Fill in na of training set with zeros, drop unnamed index column, set X/Y and split
"""
training_set = training_set.fillna(0)
#training_set = fem_long_training_set

cols_to_be_removed = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/columnstoberemoved.csv')
columns = [col for col in cols_to_be_removed.columns]
X = training_set.iloc[:,:-1]
if 'Unnamed: 0' in X.columns:
        X = X.drop(['Unnamed: 0'],axis=1)
for col in columns:
    if col in X.columns:
        X = X.drop([col],axis=1)

Y = training_set.iloc[:,-1:].values.ravel()
#X = X.drop(['Aisomeric_smiles','Bisomeric_smiles','ASystem','BSystem','Afingerprint','Bfingerprint','Acactvs_fingerprint','Bcactvs_fingerprint'],axis=1)
X = X.fillna(0)
x_train, x_test, y_train, y_test = train_test_split(
		X, Y, test_size=0.25, random_state=42)

"""
Some playing around with hyperparameters
"""
# # Number of trees in random forest
# n_estimators = [200,400,600,800]
# # Number of features to consider at every split
# max_features = ['auto', 'sqrt']
# # Maximum number of levels in tree
# max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
# # Minimum number of samples required to split a node
# min_samples_split = [2, 5, 10]
# # Minimum number of samples required at each leaf node
# min_samples_leaf = [1, 2, 4]
# # Method of selecting samples for training each tree
# bootstrap = [True, False]
# # Create the random grid

# for n in n_estimators:
#     for depth in max_depth:
#         print('Running with {} estimators ad {} depth'.format(n,depth))
#         rf = RandomForestClassifier(n_estimators=n,max_depth = depth,max_features='sqrt')
#         rf.fit(x_train,y_train)
#         predictions = rf.predict(x_test)
#         print('accuracy for {} estimators and max_depth {} is {}'.format(n,depth,metrics.accuracy_score(y_test,predictions) * 100))



# predictions = rf_random_model.predict(x_test)
cols_to_be_removed = pd.read_csv(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/ModelCreationScripts/columnstoberemoved.csv')
columns = [col for col in cols_to_be_removed.columns]
n_ests = [500,600,700                                                   ]
max_deps = [30,40,50]
for n_est in n_ests:
    for dep in max_deps:
        print('on {} ests and {} depth'.format(n_est,dep))
        rf = RandomForestClassifier(n_estimators=n_est,max_depth=dep,max_features='sqrt')
# rf = RandomForestClassifier()
        rf.fit(x_train,y_train)
        predictions = rf.predict(x_test)
        prob_a = rf.predict_proba(x_test)
        skipped = []
        new_pred= []
        new_y_test = []
        index = 0
        for prob in prob_a:
            if prob[0] >.4 and prob[0] < .6:
                skipped.append(prob)
                index+=1
            else:
                new_pred.append(predictions[index])
                new_y_test.append(y_test[index])
                index+=1
        hp_acc = metrics.accuracy_score(new_y_test,new_pred) * 100        
        print(metrics.accuracy_score(new_y_test,new_pred) * 100)
        print(metrics.accuracy_score(y_test,predictions) * 100)
        feature_importance = rf.feature_importances_
        with open('log_hard_Predictions.txt','a') as file:
            file.write('Accuracy for {} estimators and {} Depth is {}\n'.format(n_est,dep,hp_acc))
"""
saving model file in pickled format
"""
# print(metrics.accuracy_score(y_test,predictions) * 100)
#importance_rf = rf_model.feature_importances_

# with open('RanForc18predretSMRTfeaturereduc.pickle', 'wb') as handle:
#     pickle.dump(rf, handle)
# #
# #mlp_model = MLPClassifier(max_iter=10000)
# #mlp_model.fit(x_train,y_train)
# #predictions = mlp_model.predict(x_test)
# #print(metrics.accuracy_score(y_test,predictions) * 100)

"""
loop to run a handful of classifiers and record their results
"""
# classifiers = [
#     KNeighborsClassifier(3),
#     DecisionTreeClassifier(),
#     RandomForestClassifier(),
#     AdaBoostClassifier(),
#     GradientBoostingClassifier(),
#     GaussianNB(),
#     LinearDiscriminantAnalysis(),
#     QuadraticDiscriminantAnalysis()]


# # Logging for Visual Comparison
# log_cols=["Classifier", "Accuracy", "Log Loss"]
# log = pd.DataFrame(columns=log_cols)

# for clf in classifiers:
#     clf.fit(x_train, y_train)
#     name = clf.__class__.__name__
    
#     print("="*30)
#     print(name)
    
#     print('****Results****')
#     train_predictions = clf.predict(x_test)
#     acc = accuracy_score(y_test, train_predictions)
#     print("Accuracy: {:.4%}".format(acc))
    
#     train_predictions = clf.predict_proba(x_test)
#     ll = log_loss(y_test, train_predictions)
#     print("Log Loss: {}".format(ll))
    
#     log_entry = pd.DataFrame([[name, acc*100, ll]], columns=log_cols)
#     log = log.append(log_entry)
    
# print("="*30 + '\n')
# cv_nums = [3,4,5,10]
# with open('log.txt','w') as file:
#     for cv_num in cv_nums:
#         print('Current CV is {}\n'.format(cv_num))
#         file.write('Current CV is {}\n'.format(cv_num))
#         for clf in classifiers:
#             print('current model is {}\n'.format(clf))
#             scores = cross_val_score(clf,X, Y,cv=cv_num)
#             name = clf.__class__.__name__
            
#             file.write(("="*30) + '\n')
#             file.write(name)
            
#             file.write('****Results****\n')
#             file.write("Accuracy: %0.3f (+/- %0.3f)\n" % (scores.mean() *100, (scores.std() * 2)*100))
    
# # print("="*30)
# #svm_model = SVC()
# #svm_model.fit(x_train,y_train)
# #predictions = svm_model.predict(x_test)
# #
# #print(metrics.accuracy_score(y_test,predictions) * 100)
# #importance = svm_model.feature_importances_
# #
# #with open('SVM.pickle', 'wb') as handle:
# #    pickle.dump(svm_model, handle)




