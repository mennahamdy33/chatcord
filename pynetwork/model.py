<<<<<<< HEAD
from PyQt5 import QtWidgets,QtCore,QtGui,QtMultimedia
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import Questions  as ui
import math
import pyqtgraph as pg
import sys,os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
import csv
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
# Class for create the Random Forset Model
class Model():
    def __init__(self):
        #  the Data contain two kind of data Categorical and Numerical data so we organize the file so the numerical data in the first
        #  6 columns and the rest of the columns contain catogrical data  
        self.indexOfStartCatgoricalData = 6
        # to convert categorical data which contain string and numbers into encoded form we used Ordinal Encoder
        self.ord_enc = OrdinalEncoder()
        

    def RandomForestModel(self):
            # The Data which we used for train our data  
            originalData = pd.read_excel(r"E:\Projects\networkFinal\network\pynetwork\kidney.xlsx")
            Data = originalData.copy()
            numericalData = Data.iloc[:,:self.indexOfStartCatgoricalData]
            categoricalData= Data.iloc[:,self.indexOfStartCatgoricalData:]

            # Get the mean of each column of the numerical data
            meanOfNumericalData = numericalData.mean()
            # Get mode value of each column in categoricl data
            modeOfCategoricalData = categoricalData.mode().iloc[0]
            # replace Nan Values in numerical data with mean .
            Data.iloc[:,:self.indexOfStartCatgoricalData] = numericalData.fillna(meanOfNumericalData )    
            #replace Nan Values in categorical data into mode .  
            Data.iloc[:,self.indexOfStartCatgoricalData:] = categoricalData.fillna(modeOfCategoricalData)
            # encode categorical data
            Data.iloc[:,self.indexOfStartCatgoricalData:]= self.ord_enc.fit_transform(Data.iloc[:,self.indexOfStartCatgoricalData:])
            # apply Model
            X = Data.drop('class', axis=1)
            y = Data['class']
            classifier=RandomForestClassifier().fit(X,y) 
            return(meanOfNumericalData,modeOfCategoricalData,classifier)

# class for prediction 
class predict():
    def __init__(self, data,meanOfNumericalData,modeOfCategoricalData,classifier):  
        self.ord_enc = OrdinalEncoder()
        self.indexOfStartCatgoricalData = 6
        self.meanOfNumericalData = meanOfNumericalData
        self.modeOfCategoricalData = modeOfCategoricalData
        self.classifier = classifier
        # convert data into Data Frame 
        self.data =  pd.DataFrame([data])        
        self.NumericalData = self.data.iloc[:,:self.indexOfStartCatgoricalData]
        self.CategoricalData = self.data.iloc[:,self.indexOfStartCatgoricalData:]
        
    def predict(self):
        # values from GUI don't return null if the user doesn't enter the values but return ''
        # so we user replace function to replcae each '' with Null.
        numericalData = self.NumericalData.replace(r'', np.NaN)

        numericalData = numericalData.fillna(self.meanOfNumericalData)
        print(numericalData)
        categoricalData = self.CategoricalData.fillna(self.modeOfCategoricalData)
        print(categoricalData)
        # to be able to used classifier, The data must be converted into one variable so join function used for that.
        inputData = numericalData.join(categoricalData)

        output = self.classifier.predict(inputData)
        # if the output zero so this patient have Coronary Kidney Disease
        if (output == 0): 
            return('you most probably have coronary kidney disease, So you have to see your Doctor ASAP')
        else:
            return('Nothing To worry about')
=======
from PyQt5 import QtWidgets,QtCore,QtGui,QtMultimedia
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import Questions  as ui
import math
import pyqtgraph as pg
import sys,os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
import csv
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
# Class for create the Random Forset Model
class Model():
    def __init__(self):
        #  the Data contain two kind of data Categorical and Numerical data so we organize the file so the numerical data in the first
        #  6 columns and the rest of the columns contain catogrical data  
        self.indexOfStartCatgoricalData = 6
        # to convert categorical data which contain string and numbers into encoded form we used Ordinal Encoder
        self.ord_enc = OrdinalEncoder()
        

    def RandomForestModel(self):
            # The Data which we used for train our data  
            originalData = pd.read_excel(r"kidney.xlsx")
            Data = originalData.copy()
            numericalData = Data.iloc[:,:self.indexOfStartCatgoricalData]
            categoricalData= Data.iloc[:,self.indexOfStartCatgoricalData:]

            # Get the mean of each column of the numerical data
            meanOfNumericalData = numericalData.mean()
            # Get mode value of each column in categoricl data
            modeOfCategoricalData = categoricalData.mode().iloc[0]
            # replace Nan Values in numerical data with mean .
            Data.iloc[:,:self.indexOfStartCatgoricalData] = numericalData.fillna(meanOfNumericalData )    
            #replace Nan Values in categorical data into mode .  
            Data.iloc[:,self.indexOfStartCatgoricalData:] = categoricalData.fillna(modeOfCategoricalData)
            # encode categorical data
            Data.iloc[:,self.indexOfStartCatgoricalData:]= self.ord_enc.fit_transform(Data.iloc[:,self.indexOfStartCatgoricalData:])

            # apply Model
            X = Data.drop('class', axis=1)
            y = Data['class']
            classifier=RandomForestClassifier().fit(X,y) 
            return(meanOfNumericalData,modeOfCategoricalData,classifier)

# class for prediction 
class predict():
    def __init__(self, data,meanOfNumericalData,modeOfCategoricalData,classifier):  
        self.ord_enc = OrdinalEncoder()
        self.indexOfStartCatgoricalData = 6
        self.meanOfNumericalData = meanOfNumericalData
        self.modeOfCategoricalData = modeOfCategoricalData
        self.classifier = classifier
        # convert data into Data Frame 
        self.data =  pd.DataFrame([data])        
        self.NumericalData = self.data.iloc[:,:self.indexOfStartCatgoricalData]
        self.CategoricalData = self.data.iloc[:,self.indexOfStartCatgoricalData:]
        
    def predict(self):
        # values from GUI don't return null if the user doesn't enter the values but return ''
        # so we user replace function to replcae each '' with Null.
        numericalData = self.NumericalData.replace(r'', np.NaN)

        numericalData = numericalData.fillna(self.meanOfNumericalData)
        
        categoricalData = self.CategoricalData.fillna(self.modeOfCategoricalData)
        # to be able to used classifier, The data must be converted into one variable so join function used for that.
        inputData = numericalData.join(categoricalData)

        output = self.classifier.predict(inputData)
        # if the output zero so this patient have Coronary Kidney Disease
        if (output == 0): 
            return('you most probably have coronary kidney disease, So you have to see your Doctor ASAP')
        else:
            return('Nothing To worry about')
>>>>>>> efac186f7195fd4a4db0e82ed0248bc0ffef8c14
