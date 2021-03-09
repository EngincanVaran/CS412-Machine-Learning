# -*- coding: utf-8 -*-
"""Engincan Varan HW 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gzYIxQXWXD4Fm-o0XcpKLQOeq40v8fWS
"""

import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import numpy as np

"""# [25 pts] A Toy Example: Decision Boundary and Conditional Independence Assumption

### Gaussian Distributed Data fits better to Gaussian Naive Bayesian rather than Logistic Regression, unfortunately that is not the case most of the time.
Now, imagine we have two artificial dataset. Both are drawn from Gaussian distribution. One of the dataset is with standard deviation 1 and the other is 5. Each cluster is conditionally independent from each other.

make_blobs function samples data points from gaussian distribution.
"""

from sklearn.datasets import make_blobs
data1, label1 = make_blobs(n_samples=500, centers=2, n_features=2, cluster_std=1, random_state=11) # code comes here
data2, label2 = make_blobs(n_samples=500, centers=2, n_features=2, cluster_std=5, random_state=11) # code comes here

"""Let's split the datasets into train and test."""

(train_x_data1, test_x_data1, train_y_data1, test_y_data1) = train_test_split( data1, label1, train_size=0.8, random_state=11)      # code comes here
(train_x_data2, test_x_data2, train_y_data2, test_y_data2) = train_test_split( data2, label2, train_size=0.8, random_state=11)      # code comes here

"""Plot the first dataset with standard deviation 1."""

plt.scatter(data1[:,0], data1[:,1])
plt.title('Scatter plot data with standard deviation=1')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

"""Plot the first dataset with standard deviation 5."""

plt.scatter(data2[:,0], data2[:,1])
plt.title('Scatter plot data with standard deviation=5')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

"""Train a Gaussian Naive Bayesian and Logistic Regression with the 1st dataset."""

GNB = GaussianNB()   # code comes here
GNB.fit(train_x_data1, train_y_data1)   # code comes here

CLF = LogisticRegression(random_state=0)    # code comes here
CLF.fit(train_x_data1, train_y_data1)         # code comes here

"""### Perfect Decision Boundary"""

# Predict
print("Classification Report for Naive Bayesian:")
print(classification_report(GNB.predict(test_x_data1), test_y_data1))            # code comes here

# Extra
print("Confusion Matrix for Naive Bayesian")
print(confusion_matrix((GNB.predict(test_x_data1)), test_y_data1))

# Predict
print("Classification Report for Logistic Regression:")
print(classification_report(CLF.predict(test_x_data1,),test_y_data1))             # code comes here

# Extra
print("Confusion Matrix for Logistic Regression")
print(confusion_matrix((CLF.predict(test_x_data1)), test_y_data1))

"""### Both algorithm perfectly separate two data clusters for 1st dataset with standard deviation 1. The data points are linearly separable."""

GNB = GaussianNB()   # code comes here
GNB.fit(train_x_data2, train_y_data2)   # code comes here

CLF = LogisticRegression(random_state=5)    # code comes here
CLF.fit(train_x_data2, train_y_data2)       # code comes here

# Predict
print("Classification Report for Naive Bayesian:")
print(classification_report(GNB.predict(test_x_data2), test_y_data2))   # code comes here

# Extra
print("Confusion Matrix for Naive Bayesian")
print(confusion_matrix((GNB.predict(test_x_data2)), test_y_data2))

# Predict
print("Classification Report for Logistic Regression:")
print(classification_report(CLF.predict(test_x_data2,),test_y_data2))    # code comes here

# Extra
print("Confusion Matrix for Logistic Regression")
print(confusion_matrix((CLF.predict(test_x_data2)), test_y_data2))

"""### Use the scatter plot and draw the perfect decision boundary on two scatter plot. Discuss what is linear separability, decision boundary, which datapoints are harder to separate. Discuss the accuries and the why which model performs better.
 

### Please also read: [Equivalence of GNB and LR](https://appliedmachinelearning.blog/2019/09/30/equivalence-of-gaussian-naive-bayes-and-logistic-regression-an-explanation/)

# [75pts] Logistic Regression and Naive Bayesian Comparison

### The dataset
We will use Kaggle dataset. This dataset contains around 200k news headlines from the year 2012 to 2018 obtained from HuffPost.

You can [download.](https://www.kaggle.com/rmisra/news-category-dataset)
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from google.colab import drive
drive.mount('/content/drive')
#C:\Users\Penguin\Google Drive (Sabanci)\2019-2020 302\CS412\HW 3

df=pd.read_json("/content/drive/My Drive/2019-2020 302/CS412/HW 3/News_Category_Dataset_v2.json",lines=True)        # code comes here
print("JSON Done!")

"""## Select 4 categories: Politics, Wellness, Entertainment, Travel

use only 50K of data row
"""

df = df.sample(50000)

new_df = df[(df['category']== 'POLITICS') | (df['category']== 'WELLNESS') | (df['category']== 'ENTERTAINMENT') | (df['category']== 'TRAVEL')]

new_df['category'].value_counts()

"""Convert category names to digit labelling"""

y = (new_df['category'].to_numpy() == "WELLNESS")*1 + (new_df['category'].to_numpy() == "ENTERTAINMENT")*2 + (new_df['category'].to_numpy() == "TRAVEL")*3

"""Merge headlines with short descriptions"""

X = new_df['short_description'] + ' '+ new_df['headline']

"""### Create Tf-Idf model"""

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer(lowercase=True, stop_words="english")  # code comes here
x_train_counts = count_vect.fit_transform(X)                        # code comes here

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()                              # code comes here
x_train_tf = tfidf_transformer.fit_transform(x_train_counts)        # code comes here

"""Split train and test data"""

from sklearn.model_selection import train_test_split
(train_data, test_data, train_label, test_label) = train_test_split( x_train_tf, y, train_size=0.8)      # code comes here

"""### Gaussian Naive Bayesian"""

GNB = GaussianNB()  # code comes here
GNB.fit(train_data.toarray(),train_label)     # code comes here

# Predict
print("Classification Report for Naive Bayesian:")
print(classification_report(GNB.predict(test_data.toarray()),test_label))             # code comes here

# Extra
print("Confusion Matrix for Naive Bayesian")
print(confusion_matrix((GNB.predict(test_data.toarray())), test_label))

"""### 6) Logistic Regression"""

clf = LogisticRegression(random_state=0,max_iter=1000)    # code comes here
clf.fit(train_data.toarray(),train_label)   # code comes here

# Predict
print("Classification Report for Logistic Regression:")
print(classification_report(clf.predict(test_data.toarray()),test_label))              # code comes here

# Extra
print("Confusion Matrix for Logistic Regression")
print(confusion_matrix((clf.predict(test_data.toarray())), test_label))

"""### Observe Logistic Regression is much slower but more accurate. Discuss.

# REPORT

We tested a real-life dataset taken from HuffPost on 4 different topics of news such as politics, wellness, entertainment, travel. We use 2 different classifiers and compare them based on their performances. Since we are using real life data and not an artificial data created by Gaussian distribution, Logistic Regression’s accuracy was way over the Gaussian Naïve Bayesian approach. This is what we expected because real life data are not conditionally independent, so Naïve Bayesian approach is not very helpful in our case.
	We obtained the best results with the Linear Regression, which gives the accuracy of 89% on test data. Naïve Bayesian approach had 71% accuracy on test data. However, these results were based on accuracy of the classifiers. When we compare the time complexities of the classifiers, Logistic Regression took such a long time that we get an “iteration limit reached” error. We can solve this by letting it do more iterations if we want. We had a pretty big dataset yet; Naïve Bayesian approach was instant. In the end, Logistic Regression is undoubtedly giving the best results with a difference of nearly 20%. However, it took a really long time to do that.
"""