import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, plot_roc_curve

# Importing data file
data = pd.read_csv('clean_data/rf_model.csv')

# Extracting X and Y
X = data.drop(columns = ['CurrentApprovalAmount', 'Y_2', 'Y_4', 'Y_7'])
Y_2 = data['Y_2']

######################################## Max Depth ########################################

# i_depth = np.arange(1, 31)
# train_depth = []
# test_depth = []

# for i in i_depth:

#     # Splitting data into train and test
#     X_train, X_test, Y_train, Y_test = train_test_split(X, Y_2, test_size = 0.25, random_state = 100)

#     # Feature Scaling
#     sc = StandardScaler()
#     X_train = sc.fit_transform(X_train)
#     X_test = sc.transform(X_test)

#     # Training the model
#     rf_class_depth = RandomForestClassifier(max_depth = i, random_state = 42)
#     rf_class_depth.fit(X_train, Y_train)

#     # Predicitng test set
#     Y_pred = rf_class_depth.predict(X_test)

#     # Evaluating score of model
#     rf_train_accuracy = rf_class_depth.score(X_train, Y_train)
#     rf_test_accuracy = rf_class_depth.score(X_test, Y_test)

#     # Stroing the results
#     train_depth.append(rf_train_accuracy * 100)
#     test_depth.append(rf_test_accuracy * 100)

#     # printing results
#     print(rf_test_accuracy * 100)

# depth_plot = sns.lineplot(x = i_depth, y = train_depth, label = 'Traning Accuracy')
# depth_plot = sns.lineplot(x = i_depth, y = test_depth, label = 'Test Accuracy')
# depth_plot.set_xlabel('Maximum Depth of Decision Tree')
# depth_plot.set_ylabel('Accuracy [%]')
# depth_plot.set_title('Maximum Tree Depth vs Accuracy for 2 Classifications')
# plt.show()

# ######################################## Min Split ########################################

# i_split = np.arange(2, 31)
# train_split = []
# test_split = []

# for i in i_split:

#     # Splitting data into train and test
#     X_train, X_test, Y_train, Y_test = train_test_split(X, Y_2, test_size = 0.25, random_state = 100)

#     # Feature Scaling
#     sc = StandardScaler()
#     X_train = sc.fit_transform(X_train)
#     X_test = sc.transform(X_test)

#     # Training the model
#     rf_class_split = RandomForestClassifier(max_depth = 7, random_state = 42, min_samples_split = i)
#     rf_class_split.fit(X_train, Y_train)

#     # Predicitng test set
#     Y_pred = rf_class_split.predict(X_test)

#     # Evaluating score of model
#     rf_train_accuracy = rf_class_split.score(X_train, Y_train)
#     rf_test_accuracy = rf_class_split.score(X_test, Y_test)

#     # Stroing the results
#     train_split.append(rf_train_accuracy * 100)
#     test_split.append(rf_test_accuracy * 100)

#     # printing results
#     print(rf_test_accuracy * 100)

# split_plot = sns.lineplot(x = i_split, y = train_split, label = 'Traning Accuracy')
# split_plot = sns.lineplot(x = i_split, y = test_split, label = 'Test Accuracy')
# split_plot.set_xlabel('Minimum Number of Samples')
# split_plot.set_ylabel('Accuracy [%]')
# split_plot.set_title('Minimum Number of Samples for Split vs Accuracy for 2 Classifications')
# plt.show()

######################################## Final Model ########################################

# Splitting data into train and test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_2, test_size = 0.25, random_state = 100)

# Feature Scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Training the model
rf_class_best = RandomForestClassifier(max_depth = 7, random_state = 42, min_samples_split = 10)
rf_class_best.fit(X_train, Y_train)

# Predicitng test set
Y_pred = rf_class_best.predict(X_test)

# Evaluating score of model
rf_train_accuracy = rf_class_best.score(X_train, Y_train)
rf_test_accuracy = rf_class_best.score(X_test, Y_test)

# printing results
print(rf_train_accuracy * 100, rf_test_accuracy * 100)

######################################## ROC Curve ########################################

ax = plt.gca()
rfc_disp = plot_roc_curve(rf_class_best, X_test, Y_test, ax = ax, alpha = 0.8)
plt.title('ROC Curve for 2 Classifications')
plt.show()

######################################## Confusion Matrix ########################################

cm = confusion_matrix(Y_test, Y_pred)
cm_display = ConfusionMatrixDisplay(cm).plot(cmap = 'Greens')
plt.title('Confusion Matrix for 2 Classifications')
plt.show()

######################################## Feature Importance ########################################

# Creating zipped list of feature importance
tuples_list = list(zip(X.columns, rf_class_best.feature_importances_))

# Converting list to dataframe
feat_imp = pd.DataFrame(tuples_list, columns = ['Features', 'Importance'])

# Sorting the dataframe
feat_imp = feat_imp.sort_values(by = ['Importance'], ascending = False)

# Selecting top 15 rows
feat_imp_plot = feat_imp.iloc[:10]

# Plotting feature importance
# plt.figure(figsize=(8, 6))
feature_imp = sns.barplot(data = feat_imp_plot, x = 'Importance', y = 'Features', orient = 'h')
feature_imp.set_xlabel('Feature')
feature_imp.set_ylabel('Importance')
feature_imp.set_title('Feature Importance for 2 Classifications')
plt.tight_layout()
plt.show()
