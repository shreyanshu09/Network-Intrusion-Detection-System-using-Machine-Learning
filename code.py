# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13uAX6bX187B8JFtnkjtYtbz6_S9shhvm

# ***Network Intrusion Detection System Using Machine Learning***

---



---

# Import Relevant Modules
"""

! pip install pygam

# Commented out IPython magic to ensure Python compatibility.
!pip install ipython-autotime

# %load_ext autotime

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_confusion_matrix
import pandas as pd
import numpy as np
import seaborn as sns
import sklearn
import imblearn

import warnings
warnings.filterwarnings('ignore')

# Libraries

print("pandas : {0}".format(pd.__version__))
print("numpy : {0}".format(np.__version__))
print("matplotlib : {0}".format(matplotlib.__version__))
print("seaborn : {0}".format(sns.__version__))
print("sklearn : {0}".format(sklearn.__version__))
print("imblearn : {0}".format(imblearn.__version__))

"""# Loading Training And Testing Data"""

from google.colab import files

uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

# Dataset field names

field_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","attack", "last_flag"]

# Loading Train Dataset
train_data = pd.read_table("Train.txt", sep=",", names=field_names)
# Removes an unwanted extra field
train_data = train_data.iloc[:,:-1] 

# Loading Test Dataset
test_data = pd.read_table("Test.txt", sep=",", names=field_names)
# Removes an unwanted extra field
test_data = test_data.iloc[:,:-1]

data = pd.read_table("Train.txt", sep=",", names=field_names)

corr = data.corr()

mask = np.zeros_like(corr)
mask[np.triu_indices_from(mask)] = True

fig = plt.figure(figsize = (10, 5))

ax = sns.heatmap(corr, 
                 mask = mask, 
                 vmax = 0.3, 
                 square = True,  
                 cmap = "viridis")

ax.set_title("Heatmap using seaborn");

"""# Preview of Training And Testing Data"""

# Preview of Training Data
train_data.head(4)

# Set Dimensions For Training Data
print('Train set dimension: {} rows, {} columns'.format(train_data.shape[0], train_data.shape[1]))

# Preview of Testing Data
test_data.head(4)

# Set Dimensions For Training Data
print('Test set dimension: {} rows, {} columns'.format(test_data.shape[0], test_data.shape[1]))

"""# Data Preprocessing

Mapping Different Attacks into 4 Major Attack Classes:

1.   Denial of Service (DoS)
2.   Probing Attack (Probe)
3.   User to Root Attack (U2R)
4.   Remote to Local Attack (R2L)
"""

map = {'ipsweep': 'Probe','satan': 'Probe','nmap': 'Probe','portsweep': 'Probe','saint': 'Probe','mscan': 'Probe',
        'teardrop': 'DoS','pod': 'DoS','land': 'DoS','back': 'DoS','neptune': 'DoS','smurf': 'DoS','mailbomb': 'DoS',
        'udpstorm': 'DoS','apache2': 'DoS','processtable': 'DoS',
        'perl': 'U2R','loadmodule': 'U2R','rootkit': 'U2R','buffer_overflow': 'U2R','xterm': 'U2R','ps': 'U2R',
        'sqlattack': 'U2R','httptunnel': 'U2R',
        'ftp_write': 'R2L','phf': 'R2L','guess_passwd': 'R2L','warezmaster': 'R2L','warezclient': 'R2L','imap': 'R2L',
        'spy': 'R2L','multihop': 'R2L','named': 'R2L','snmpguess': 'R2L','worm': 'R2L','snmpgetattack': 'R2L',
        'xsnoop': 'R2L','xlock': 'R2L','sendmail': 'R2L',
        'normal': 'Normal'
        }

# Apply attack class mappings to the dataset
train_data['attack_class'] = train_data['attack'].apply(lambda v: map[v])
test_data['attack_class'] = test_data['attack'].apply(lambda v: map[v])

# Drop attack field from both train and test data
train_data.drop(['attack'], axis=1, inplace=True)
test_data.drop(['attack'], axis=1, inplace=True)

# Preview of top 4 Train Data 
train_data.head(4)

# Descriptive statistics
da = train_data.describe()
da

train_data['num_outbound_cmds'].value_counts()

test_data['num_outbound_cmds'].value_counts()

train_data.drop(['num_outbound_cmds'], axis=1, inplace=True)

test_data.drop(['num_outbound_cmds'], axis=1, inplace=True)

# Attack Class Distribution
atk_train = train_data[['attack_class']].apply(lambda x: x.value_counts())
atk_test = test_data[['attack_class']].apply(lambda x: x.value_counts())
atk_train['frequency_train_percent'] = round((100 * atk_train / atk_train.sum()),2)
atk_test['frequency_test_percent'] = round((100 * atk_test / atk_test.sum()),2)

atk_dist = pd.concat([atk_train,atk_test], axis=1) 
atk_dist

# Attack class bar plot
plot = atk_dist[['frequency_train_percent', 'frequency_test_percent']].plot(kind="bar");
plot.set_title("Attack Class Distribution", fontsize=30);
plot.grid(color='lightblue', alpha=1.0);

train_data.head()

# Scaling numerical Attributes

from sklearn.preprocessing import StandardScaler
std_scaler = StandardScaler()

# extract numerical attributes from data and scale it to have zero mean and unit variance  
clmns = train_data.select_dtypes(include=['float64','int64']).columns
scaler_train = std_scaler.fit_transform(train_data.select_dtypes(include=['float64','int64']))
scaler_test = std_scaler.fit_transform(test_data.select_dtypes(include=['float64','int64']))

# turn the result back to a dataframe
scaler_train_frame = pd.DataFrame(scaler_train, columns = clmns)
scaler_test_frame = pd.DataFrame(scaler_test, columns = clmns)

# Encoding of Categorical Attributes

from sklearn.preprocessing import LabelEncoder
l_encoder = LabelEncoder()

# extracting the categorical attributes from both training and testing  datasets 
categorical_train = train_data.select_dtypes(include=['object']).copy()
categorical_test = test_data.select_dtypes(include=['object']).copy()

# encoding the categorical attributes
train_categorical = categorical_train.apply(l_encoder.fit_transform)
test_categorical = categorical_test.apply(l_encoder.fit_transform)

# separating target column from encoded data 
encode_train = train_categorical.drop(['attack_class'], axis=1)
encode_test = test_categorical.drop(['attack_class'], axis=1)

categorical_Ytrain = train_categorical[['attack_class']].copy()
categorical_Ytest = test_categorical[['attack_class']].copy()

# Data Sampling

from imblearn.over_sampling import RandomOverSampler 
from collections import Counter

# defining columns and extracting encoded train dataset for sampling 
scaler_train_frame = train_data.select_dtypes(include=['float64','int64'])
ref_class_column = pd.concat([scaler_train_frame, encode_train], axis=1).columns
ref_class = np.concatenate((scaler_train, encode_train.values), axis=1)
X = ref_class

# reshaping target column to 1D array shape  
c, r = categorical_Ytest.values.shape
y_test = categorical_Ytest.values.reshape(c,)

c, r = categorical_Ytrain.values.shape
y = categorical_Ytrain.values.reshape(c,)

# applying the random over-sampling
sampling = RandomOverSampler(random_state=42)
X_res, y_res = sampling.fit_sample(X, y)
print('Original dataset shape {}'.format(Counter(y)))
print('Resampled dataset shape {}'.format(Counter(y_res)))

"""# Feature Selection Using RandomForest Classifier Model"""

from sklearn.ensemble import RandomForestClassifier
random_forest = RandomForestClassifier();

# fitting random forest classifier on the training set
random_forest.fit(X_res, y_res);
# extracting important features
scoring = np.round(random_forest.feature_importances_,3)
important = pd.DataFrame({'feature':ref_class_column,'importance':scoring})
important = important.sort_values('importance',ascending=False).set_index('feature')
# plotting important features in bar graph
plt.rcParams['figure.figsize'] = (15, 5)
important.plot.bar();

from sklearn.feature_selection import RFE
import itertools
random_forest = RandomForestClassifier()

# creating the RFE model and selecting 10 attributes
random_feature = RFE(random_forest, n_features_to_select=10)
random_forest = random_feature.fit(X_res, y_res)

# summarizing the selection of the attributes
feature_mapping = [(j, w) for j, w in itertools.zip_longest(random_feature.get_support(), ref_class_column)]
features = [w for j, w in feature_mapping if j==True]

features

"""# Dataset Partition"""

# defining columns to a new dataframe
new_column = list(ref_class_column)
new_column.append('attack_class')

# adding a dimension to target
new_y_res = y_res[:, np.newaxis]

# creating a dataframe from sampled data
res_array = np.concatenate((X_res, new_y_res), axis=1)
res_data_frame = pd.DataFrame(res_array, columns = new_column) 

# creating test dataframe
test_ref = pd.concat([scaler_test_frame, test_categorical], axis=1)
test_ref['attack_class'] = test_ref['attack_class'].astype(np.float64)
test_ref['protocol_type'] = test_ref['protocol_type'].astype(np.float64)
test_ref['flag'] = test_ref['flag'].astype(np.float64)
test_ref['service'] = test_ref['service'].astype(np.float64)

res_data_frame.shape

test_ref.shape

from collections import defaultdict
class_dict = defaultdict(list)

# creating two-target classes: normal class and an attack class
atk_list = [('DoS', 0.0), ('Probe', 2.0), ('R2L', 3.0), ('U2R', 4.0)]
nrml_class = [('Normal', 1.0)]

def create_class_dict():
    '''This function subdivides train and test dataset into two-class attack labels''' 
    for i, l in nrml_class: 
        for j, w in atk_list: 
            res_train_set = res_data_frame.loc[(res_data_frame['attack_class'] == l) | (res_data_frame['attack_class'] == w)]
            class_dict[i +'_' + j].append(res_train_set)
            # test labels
            ref_test_set = test_ref.loc[(test_ref['attack_class'] == l) | (test_ref['attack_class'] == w)]
            class_dict[i +'_' + j].append(ref_test_set)
        
create_class_dict()

pre_train = class_dict['Normal_DoS'][0]
pre_test = class_dict['Normal_DoS'][0]
group_class = 'Normal_DoS'

# Finalizing data preprocessing for training

from sklearn.preprocessing import OneHotEncoder
one_hot_encoder = OneHotEncoder()

X_res_data_frame = pre_train 
new_test = pre_test

X_res_data_frame_new = X_res_data_frame[features]
X_res_data_frame_num = X_res_data_frame_new.drop(['service'], axis=1)
X_res_data_frame_cat = X_res_data_frame_new[['service']].copy()

X_test_features = new_test[features]
X_test_data_frame_num = X_test_features.drop(['service'], axis=1)
X_test_cat = X_test_features[['service']].copy()

# Fitting training data
one_hot_encoder.fit(X_res_data_frame_cat)

# Transforming training data
X_train_one_hotencoder = one_hot_encoder.transform(X_res_data_frame_cat).toarray()
       
# Transforming testing data
X_test_one_hotencoder = one_hot_encoder.transform(X_test_cat).toarray()

X_train_dataframe = np.concatenate((X_res_data_frame_num.values, X_train_one_hotencoder), axis=1)
X_test_dataframe = np.concatenate((X_test_data_frame_num.values, X_test_one_hotencoder), axis=1) 

y_train_dataframe = X_res_data_frame[['attack_class']].copy()
c, r = y_train_dataframe.values.shape
Y_train_dataframe = y_train_dataframe.values.reshape(c,)

y_test_dataframe = new_test[['attack_class']].copy()
c, r = y_test_dataframe.values.shape
Y_test_dataframe = y_test_dataframe.values.reshape(c,)

"""# Training Using pyGAM And Different Classifier Models"""

from pygam import LogisticGAM
import time
# Logistic GAM
Logistic_gam = LogisticGAM()
Logistic_gam.fit(X_train_dataframe, Y_train_dataframe);

fig, axs = plt.subplots(1, 7)
titles = ['duration', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'hot']

for i, w in enumerate(axs):
    u = Logistic_gam.generate_X_grid(term=i)
    pdep, confi = Logistic_gam.partial_dependence(term=i, width=.95)

    w.plot(u[:, i], pdep)
    w.plot(u[:, i], confi, c='grey', ls='--')
    w.set_title(titles[i]);

from sklearn.svm import SVC 
from sklearn.naive_bayes import BernoulliNB 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier

# Train KNeighbors Classifier Model

KNeighbors_Classifier = KNeighborsClassifier(n_jobs=-1)
KNeighbors_Classifier.fit(X_train_dataframe, Y_train_dataframe);

# Train Gaussian Naive Baye Model

Naive_Baye_Classifier = BernoulliNB()
Naive_Baye_Classifier.fit(X_train_dataframe, Y_train_dataframe)

# Train Support Vector Machine Model

Support_vector_Classifier = SVC(random_state=0)
Support_vector_Classifier.fit(X_train_dataframe, Y_train_dataframe)

# Train RandomForestClassifier Model

Random_Forest_Classifier = RandomForestClassifier(criterion='entropy', n_jobs=-1, random_state=0)
Random_Forest_Classifier.fit(X_train_dataframe, Y_train_dataframe);

# Train Combined Models 1

model1 = [('Random Forest Classifier', Random_Forest_Classifier), ('KNN Classifier', KNeighbors_Classifier)]
model_1 = VotingClassifier(estimators = model1,voting = 'soft', n_jobs=-1)
model_1.fit(X_train_dataframe, Y_train_dataframe);

# Train Combined Models 2

model2 = [('Random Forest Classifier', Random_Forest_Classifier), ('Gaussian Naive Baye Classifier', Naive_Baye_Classifier)]
model_2 = VotingClassifier(estimators = model2,voting = 'soft', n_jobs=-1)
model_2.fit(X_train_dataframe, Y_train_dataframe);

"""# AUC-ROC Curve"""

# ROC curve for Random Forest Classifier and KNN Classifier


from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

probability1 = [0 for _ in range(len(Y_test_dataframe))]

probability2 = model_1.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

# ROC curve for Random Forest Classifier and Naive Baye Classifier


from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

probability1 = [0 for _ in range(len(Y_test_dataframe))]

probability2 = model_2.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

# ROC curve for Random Forest Classifier

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

probability1 = [0 for _ in range(len(Y_test_dataframe))]

probability2 = Random_Forest_Classifier.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

# ROC curve for SVM Classifier

from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot
from sklearn.calibration import CalibratedClassifierCV

probability1 = [0 for _ in range(len(Y_test_dataframe))]

model_svc = SVC(random_state=0)
model = CalibratedClassifierCV(model_svc)
model.fit(X_train_dataframe, Y_train_dataframe)

probability2 = model.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

# ROC curve for Naive Baye Classifier



from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

probability1 = [0 for _ in range(len(Y_test_dataframe))]

probability2 = Naive_Baye_Classifier.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

# ROC curve for KNN Classifier


from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot

probability1 = [0 for _ in range(len(Y_test_dataframe))]

probability2 = KNeighbors_Classifier.predict_proba(X_test_dataframe)
probability2 = probability2[:, 1]

auc1 = roc_auc_score(Y_test_dataframe, probability1)
auc2 = roc_auc_score(Y_test_dataframe, probability2)

print('No Skill: ROC AUC=%.3f' % (auc1))
print('Logistic: ROC AUC=%.3f' % (auc2))

f_probability_1, t_probability_1, _ = roc_curve(Y_test_dataframe, probability1)
f_probability_2, t_probability_2, _ = roc_curve(Y_test_dataframe, probability2)

pyplot.plot(f_probability_1, t_probability_1, linestyle='--', label='No Skill')
pyplot.plot(f_probability_2, t_probability_2, marker='.', label='Logistic')

pyplot.xlabel('False Positive Rate')
pyplot.ylabel('True Positive Rate')

pyplot.legend()
pyplot.show()

"""# Evaluating and Testing Models"""

from sklearn import metrics
from mlxtend.plotting import plot_confusion_matrix

classifier = []

classifier.append(('Random  Forest  Classifier  ', Random_Forest_Classifier))
classifier.append(('RFC and K-Neighbor Classifier', model_1))
classifier.append(("RFC & Naive Baye Classifier", model_2))
classifier.append(('K-Nearest Neighbor Classifier', KNeighbors_Classifier))
classifier.append(('Support V-Machine Classifier', Support_vector_Classifier))
classifier.append(('Logistic Generalized Additive', Logistic_gam))
classifier.append(("Naive  Baye's  Classifier   ", Naive_Baye_Classifier))


for i, v in classifier:

    Accuracy = metrics.accuracy_score(Y_train_dataframe, v.predict(X_train_dataframe))
    Confusion_matrix = metrics.confusion_matrix(Y_train_dataframe, v.predict(X_train_dataframe))
    classification = metrics.classification_report(Y_train_dataframe, v.predict(X_train_dataframe))
    
    print()
    print('============================== {} {} Model Evaluation =============================='.format(group_class, i))
    print()
    print ("Model Accuracy:" "\n", Accuracy)
    print()
    print("Confusion matrix:\n" "\n", Confusion_matrix)
    print()
    fig, ax = plot_confusion_matrix(conf_mat=Confusion_matrix, figsize=(4, 4))
    plt.show()
    print()
    print("Classification report:" "\n", classification) 
    print()

print()
print('=================================== Model Test Results ===================================')
print('|                                           |                                             |')
print('|            MODELS                         |               ACCURACY                      |')
print('|          ----------                       |              ------------                   |')

for i, v in classifier:
    Accuracy = metrics.accuracy_score(Y_test_dataframe, v.predict(X_test_dataframe))
       
    print('|                                           |                                             |')
    print('|    {} Model                '.format(i), Accuracy,'                                      ')    
    print('|                                           |                                             |')
   
print('==========================================================================================')

result = pd.DataFrame({'MODEL':['Random Forest Classifier Model','RFC and KNN Combined Model','RFC and Naive Bayes Combined Model','K-Nearest Neighbor Classifier Model','Support V-Machine Classifier Model','Logistic Generalized Additive Model','Naive Bayes Classifier Model'],
                   'Accuracy':[0.9999480272634127,0.9999257532334467,0.9984036945191037,0.9977577476500898,0.9891376980532498,0.9844750011137015,0.9737686173767133],
                   'Training Time':['12.5 s','19.3 s','12.5 s','3.35 s','2min 55s','36min 9s','183 ms']})

result

excel_writer = pd.ExcelWriter('result.xlsx')
result.to_excel(excel_writer)
excel_writer.save()

from google.colab import files
files.download('result.xlsx')