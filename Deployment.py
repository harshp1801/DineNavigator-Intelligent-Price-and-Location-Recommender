import os
import pandas as pd 
import numpy as np 
from markupsafe import escape
import flask
import pickle
from flask import Flask, render_template, request

from importnb import imports 
with imports("ipynb"):
    import output1

import dictionaries 
cuidict = dictionaries.cuisinedict
addict = dictionaries.Addressdict

app=Flask(__name__)
loaded_model = pickle.load(open('MLProject.pkl','rb'))
model2 = pickle.load(open('rfc_model.pkl','rb'))
@app.route('/')
def home():
    print('home')
    return render_template('index.html')
loc = ''
keyword = ''
@app.route('/predict',methods = ['POST'])
def result():
    if request.method == 'POST':
        print('predicting1')
        cuisine = request.form.get('cuisine')
        
        price_for_one = request.form.get('price_for_one')
        print('predicting3')
     
        Preferred_Location = request.form.get('Preferred_Location')
        print(Preferred_Location)
        lst1 = output1.main2(Preferred_Location,cuisine)
        location = lst1[0]
        cuis = lst1[1]
        a = 1
        b = 1
        for j in cuidict.keys():
            if(cuis==j):
                print(j)
                a = cuidict.get(j)*b
        for i in addict.keys():
            if(location==i):
                print(i)
                b = addict.get(i)*b
        print(location,cuis)
        lst = output1.main(loc = Preferred_Location, keyword = cuisine)
        print('********************************************************')
        print(lst)
        c = lst[0]
        output = loaded_model.predict([[a, b, c]])
        out = model2.predict([[a,price_for_one,c]])[0]
        print(out)
        locout = [i for i in addict if addict[i] == out]
        print(locout)
        return render_template('prediction.html',prediction=output[0],locationpred = locout[0], prediction1=round(lst[0],2),prediction2=lst[1],prediction3=lst[2],prediction4=lst[3],
                              prediction5=lst[-1])

if __name__ == '__main__':
    app.run(debug=True)