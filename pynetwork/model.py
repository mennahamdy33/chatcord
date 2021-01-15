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

class predict():
    def __init__(self, data,meanOfNumericalData,modeOfCategoricalData,classifier):  
        self.ord_enc = OrdinalEncoder()
        self.indexOfStartCatgoricalData = 6
        self.meanOfNumericalData = meanOfNumericalData
        self.modeOfCategoricalData = modeOfCategoricalData
        self.classifier = classifier
        self.data =  pd.DataFrame([data])
        print(self.data)
        self.NumericalData = self.data.iloc[:,:self.indexOfStartCatgoricalData]
        self.CategoricalData = self.data.iloc[:,self.indexOfStartCatgoricalData:]
        
    def predict(self):
        # convert dic into dataframe
        # replace '' with Null and check checkbox
        numericalData = self.NumericalData.replace(r'', np.NaN)

        numericalData = numericalData.fillna(self.meanOfNumericalData)
        
        categoricalData =self.CategoricalData.fillna(self.modeOfCategoricalData)
        
        inputData = numericalData.join(categoricalData)

        output = self.classifier.predict(inputData)

        if (output == 1): 
            return('You Have To see your Doctor ASAP')
        else:
            return('Nothing To worry about')

class Model():
    def __init__(self):
        self.indexOfStartCatgoricalData = 6
        self.ord_enc = OrdinalEncoder()
        

    def RandomForestModel(self):
            originalData = pd.read_excel(r"/home/menna/network/Model/kidney.xlsx")
            Data = originalData.copy()
            numericalData = Data.iloc[:,:self.indexOfStartCatgoricalData]
            categoricalData= Data.iloc[:,self.indexOfStartCatgoricalData:]

            # Mode and Mean Values
            meanOfNumericalData = numericalData.mean()
            modeOfCategoricalData = categoricalData.mode().iloc[0]
            # replace Nan Values and decode catogrical data 
            Data.iloc[:,:self.indexOfStartCatgoricalData] = numericalData.fillna(meanOfNumericalData )      
            Data.iloc[:,self.indexOfStartCatgoricalData:] = categoricalData.fillna(modeOfCategoricalData)
            Data.iloc[:,self.indexOfStartCatgoricalData:]= self.ord_enc.fit_transform(Data.iloc[:,self.indexOfStartCatgoricalData:])

            # apply Model
            X = Data.drop('class', axis=1)
            y = Data['class']
            classifier=RandomForestClassifier().fit(X,y) 
            return(meanOfNumericalData,modeOfCategoricalData,classifier)

