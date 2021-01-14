
data = {
                'age': 11
                ,'bu': 12
                ,'bgr': 11
                ,'sc': 11
                ,'bp': 11
                ,'hemo':11
                ,'htn':11
                ,'dm':11
                ,'cad':11
                ,'appet':1
                ,'ane':2
                ,'al':2
                ,'su':2
                ,'ba':1
}

meanOfNumericalData,modeOfCategoricalData,classifier = model.Model().RandomForestModel()
output = model.predict(data
                                ,meanOfNumericalData
                                ,modeOfCategoricalData
                                ,classifier).predict()
print(output)