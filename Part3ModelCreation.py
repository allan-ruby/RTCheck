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


fem_long_training_set = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\fem_long.csv')
life_new_training_set = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\FEM_orbitrap_plasma.csv')
MTBLS36_new_training_set = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\MTBLS36.csv')
list_of_df = [fem_long_training_set,life_new_training_set,MTBLS36_new_training_set]
#SMRT_file_path = 'WorkingModel/'
#for file in os.listdir(SMRT_file_path):
#    print(file)
#    infile = open(SMRT_file_path + file,'rb')
#    complete_DF= pickle.load(infile)
#    infile.close()
#    list_of_df.append(complete_DF)

#
#list_of_df = [fem_long_training_set,life_new_training_set,MTBLS36_new_training_set,first_smrt_training_set]
training_set = pd.concat(list_of_df)
#training_set = training_set.iloc[:,:-1]
# training_set = training_set.drop(['Result'],axis=1)
training_set = training_set.fillna(0)
#training_set = fem_long_training_set
X = training_set.iloc[:,:-1]
Y = training_set.iloc[:,-1:].values.ravel()
#X = X.drop(['Aisomeric_smiles','Bisomeric_smiles','ASystem','BSystem','Afingerprint','Bfingerprint','Acactvs_fingerprint','Bcactvs_fingerprint'],axis=1)
#X = X.fillna(0)
x_train, x_test, y_train, y_test = train_test_split(
		X, Y, test_size=0.25, random_state=42)


rf_model = RandomForestClassifier()
scores = cross_val_score(rf_model,X,Y,cv=4)
print(scores)
rf_model.fit(x_train,y_train)
predictions = rf_model.predict(x_test)

print(metrics.accuracy_score(y_test,predictions) * 100)
#importance_rf = rf_model.feature_importances_

with open('TESTRFClassifier.pickle', 'wb') as handle:
    pickle.dump(rf_model, handle)
importance = rf_model.feature_importances_
#
#mlp_model = MLPClassifier(max_iter=10000)
#mlp_model.fit(x_train,y_train)
#predictions = mlp_model.predict(x_test)
#print(metrics.accuracy_score(y_test,predictions) * 100)

classifiers = [
    KNeighborsClassifier(3),
    DecisionTreeClassifier(),
    RandomForestClassifier(),
    AdaBoostClassifier(),
    GradientBoostingClassifier(),
    GaussianNB(),
    LinearDiscriminantAnalysis(),
    QuadraticDiscriminantAnalysis()]

# Logging for Visual Comparison
log_cols=["Classifier", "Accuracy", "Log Loss"]
log = pd.DataFrame(columns=log_cols)

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
    
print("="*30 + '\n')
cv_nums = [3,4,5,10]
with open('log.txt','w') as file:
    for cv_num in cv_nums:
        print('Current CV is {}\n'.format(cv_num))
        file.write('Current CV is {}\n'.format(cv_num))
        for clf in classifiers:
            print('current model is {}\n'.format(clf))
            scores = cross_val_score(clf,X, Y,cv=cv_num)
            name = clf.__class__.__name__
            
            file.write(("="*30) + '\n')
            file.write(name)
            
            file.write('****Results****\n')
            file.write("Accuracy: %0.3f (+/- %0.3f)\n" % (scores.mean() *100, (scores.std() * 2)*100))
    
print("="*30)
#svm_model = SVC()
#svm_model.fit(x_train,y_train)
#predictions = svm_model.predict(x_test)
#
#print(metrics.accuracy_score(y_test,predictions) * 100)
#importance = svm_model.feature_importances_
#
#with open('SVM.pickle', 'wb') as handle:
#    pickle.dump(svm_model, handle)




