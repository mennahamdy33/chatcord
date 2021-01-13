from PyQt5 import QtWidgets,QtCore,QtGui,QtMultimedia
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import Questions  as ui
import math
import sys,os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier 
import csv
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

class ApplicationWindow(QDialog):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = ui.Ui_QuestionForm()
        self.ui.setupUi(self)
        self.ui.Result.clicked.connect(self.dataFromUser)        
        self.ord_enc = OrdinalEncoder()
        self.indexOfStartCatgoricalData = 6
        self.meanOfNumericalData = None
        self.modeOfCategoricalData = None
        self.classifier = None
        self.model()
     

    
    def dataFromUser(self):
        self.NumericalData = {'age': self.ui.AgeText.text()
                            ,'bu': self.ui.BloodUreaText.text()
                            ,'bgr': self.ui.GlucoseText.text()
                            ,'sc': self.ui.SerumText.text()
                            ,'bp': self.ui.BloodPressureText.text()
                            ,'hemo': self.ui.HemoglobinText.text()
                            }

        self.CategoricalData ={'htn':self.IsCheckBoxChecked(self.ui.Hypertension)
                                ,'dm':self.IsCheckBoxChecked(self.ui.Diabetes)
                                ,'cad':self.IsCheckBoxChecked(self.ui.Coronary)
                                ,'appet':self.ui.comboBox_3.currentIndex()-1
                                ,'ane':self.IsCheckBoxChecked(self.ui.Anemia)
                                ,'al':self.ui.AlbuminComboBox.currentIndex()-1
                                ,'su':self.ui.SugarComboBox.currentIndex()-1
                                ,'ba':self.IsCheckBoxChecked(self.ui.Bacteria)
                                }
                                # hemo/
        return self.predict()
       

        
    def IsCheckBoxChecked(self,checkBox):
        if (checkBox.isChecked()):
            return(1)
        else:
            return(0)
    
    def predict(self):
        # convert dic into dataframe
        # replace '' with Null and check checkbox
        numericalData = pd.DataFrame([self.NumericalData]).replace(r'', np.NaN)

        numericalData = numericalData.fillna(self.meanOfNumericalData)
        
        categoricalData =pd.DataFrame([self.CategoricalData]).fillna(self.modeOfCategoricalData.drop('class'))
        
        inputData = numericalData.join(categoricalData)

        output = self.classifier.predict(inputData)

        if (output == 0): 
            self.ui.ResultText.setText('You Have To see your Doctor ASAP')
        else:
            self.ui.ResultText.setText('Nothing To worry about')


    def model(self):
            originalData = pd.read_excel(r"D:\SBME 4\Network\Task\network\Model\kidney.xlsx",engine='openpyxl')
            Data = originalData.copy()
            numericalData = Data.iloc[:,:self.indexOfStartCatgoricalData]
            categoricalData= Data.iloc[:,self.indexOfStartCatgoricalData:]
            # Mode and Mean Values
            self.meanOfNumericalData = numericalData.mean()
            self.modeOfCategoricalData = categoricalData.mode().iloc[0]
            # replace Nan Values and decode catogrical data 
            Data.iloc[:,:self.indexOfStartCatgoricalData] = numericalData.fillna(self.meanOfNumericalData )      
            Data.iloc[:,self.indexOfStartCatgoricalData:] = categoricalData.fillna(self.modeOfCategoricalData)
            Data.iloc[:,self.indexOfStartCatgoricalData:]= self.ord_enc.fit_transform(Data.iloc[:,self.indexOfStartCatgoricalData:])
            # apply Model
            X = Data.drop('class', axis=1)
            y = Data['class']
            self.classifier=RandomForestClassifier().fit(X,y) 

   
def main():
    app=QApplication(sys.argv)
    mainwindow=ApplicationWindow()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.show()
    app.exec_()


if __name__ == "__main__":
   
    main()