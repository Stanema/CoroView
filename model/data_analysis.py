from optparse import Values
import pandas as pd
import plotly as py
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import base64
from io import BytesIO
import plotly.graph_objs as go
import json
import random


class CData:
    def __init__(self,df):
        self.data = df
        
        super().__init__()
    
    def data_by_id(self):
        d = self.data.groupby(["id"]).sum().sort_index()   
        d.id = d.index
        return d
    
    def get_countries(self):
        return sorted(self.data["Country"].unique())
    
    def get_genders(self):
        return sorted(self.data["Gender"].unique())
    
    def get_ages(self):
        return sorted(self.data["Age"].unique())
    
    def get_ids(self):
        return sorted(self.data["id"].unique())

    
    def data_by_country(self,country):
        new_df = self.data[self.data["Country"]== country]
        self.data = new_df
        
        return self
    
    def data_by_age(self,age):
        new_df = self.data[self.data["Age"]== age]
        self.data = new_df
        
        return self
    
    def data_by_gender(self,gender):
        new_df = self.data[self.data["Gender"]== gender]
        self.data = new_df
        
        return self
    
    # Age_0-9,Age_10-19,Age_20-24,Age_25-59,Age_60+   
    def categorise_age(row):  
        if row['Age_0-9'] == 1:
            return '0-9'
        elif row['Age_10-19'] == 1:
            return '10-19'
        elif row['Age_20-24'] == 1:
            return '20-24'
        elif row['Age_25-59'] == 1:
            return '25-59'
        elif row['Age_60+'] == 1:
            return '60+'
        return 'Age_is_missing'    
    
    # Gender_Female,Gender_Male,Gender_Transgender
    def categorise_gender(row):  
        if row['Gender_Female'] == 1:
            return 'Female'
        elif row['Gender_Male'] == 1:
            return 'Male'
        elif row['Gender_Transgender'] == 1:
            return 'Transgender'
        return 'Gender_is_missing'
    
    # Severity_Mild,Severity_Moderate,Severity_None,Severity_Severe
    def categorise_severity(row):  
        if row['Severity_Mild'] == 1:
            return 'Mild'
        elif row['Severity_Moderate'] == 1:
            return 'Moderate'
        elif row['Severity_None'] == 1:
            return 'None'
        elif row['Severity_Severe'] == 1:
            return 'Severe'
        return 'Severity_is_missing'          

    # Contact_Dont-Know,Contact_No,Contact_Yes
    def categorise_contact(row):  
        if row['Contact_Dont-Know'] == 1:
            return 'Dont-Know'
        elif row['Contact_No'] == 1:
            return 'No'
        elif row['Contact_Yes'] == 1:
            return 'Yes'
        return 'Contact_is_missing'
    
    
    def sumarize_data(self):
        list_of_column_names = []
        list_of_occurences = []
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        #print(len(self.data.columns))
        for col in self.data.columns:
            list_of_column_names.append(col)
            print(col)
        #1-11
        
        plot_df = pd.DataFrame({
            "Symptoms": list_of_column_names,
            #"Occurence":list_of_occurences,
            "Occurence": [1, self.data['Fever'].sum(), self.data['Tiredness'].sum(), self.data['Dry-Cough'].sum(), self.data['Difficulty-in-Breathing'].sum(), self.data['Sore-Throat'].sum(), self.data['None_Sympton'].sum(), self.data['Pains'].sum(), self.data['Nasal-Congestion'].sum(), self.data['Runny-Nose'].sum(), self.data['Diarrhea'].sum(),self.data['None_Experiencing'].sum(),13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31, 32],
        })
        plot_df = plot_df.iloc[1:12, :]
        #plot_df = df['Score'].sum()
        return plot_df

    @staticmethod
    def load_file(filepath):
        #df = pd.read_csv(filepath,  nrows=1000)
        df = pd.read_csv(filepath)
        df = df.sample(n = 1000, random_state = 1)
        
        df.insert(loc=0, column='id', value=df.index + 1)
        df['Age'] = df.apply(lambda row: CData.categorise_age(row), axis=1)
        df['Gender'] = df.apply(lambda row: CData.categorise_gender(row), axis=1)
        df['Severity'] = df.apply(lambda row: CData.categorise_severity(row), axis=1)
        df['Contact'] = df.apply(lambda row: CData.categorise_contact(row), axis=1)

        
        #covid.ObservationDate = pd.to_datetime(covid.ObservationDate)  
        data_head = df.head()
        print(data_head)
        print(df.Age)
        
        return CData(df)
        #return data

class Patient:
    def __init__(self, id):
        patient =  id
        #self.name = patient[0]
        #self.country = patient[27]
        #self.age = patient[28]
        #self.gender = patient[29]
        #self.symptoms
        #self.contact = patient[31]
        super().__init__()
    
    @staticmethod
    def patient_select(id, data):
        df = data.data
        id = int(id)
        patient = df.loc[df['id'] == id]
        patient_info = []
        name = patient.iloc[0]['id']
        patient_info.append(name)
        country = patient.iloc[0]['Country']
        patient_info.append(country)
        age = patient.iloc[0]['Age']
        patient_info.append(age)
        gender = patient.iloc[0]['Gender']
        patient_info.append(gender)
        severity = patient.iloc[0]['Severity']
        patient_info.append(severity)
        
        return patient_info
    
    @staticmethod
    def symptoms_select(id, data):
        df = data.data
        id = int(id)
        patient = df.loc[df['id'] == id]
        symptoms = patient.iloc[0,1:12]
        list_of_column_names = []
        string_of_symptoms = ""

        for col in patient.columns:
            list_of_column_names.append(col)
        indx = 0
        for sym in symptoms:
            if sym == 1:
                string_of_symptoms = string_of_symptoms + symptoms.index[indx] + ", "
            indx = indx + 1

        return string_of_symptoms
     
    @staticmethod
    def medication_select(id, data):
        df = data.data
        id = int(id)
        patient = df.loc[df['id'] == id]
        symptoms = patient.iloc[0,1:12]
        #list_of_column_names = []
                                #Fever,Tiredness,Dry-Cough,Difficulty-in-Breathing,Sore-Throat,None_Sympton,Pains,Nasal-Congestion,Runny-Nose,Diarrhea,None_Experiencing
        list_of_medication = ["Ibalgin","Herbal-tea","Sinupret","Eucalyptus-inhalation","Strepsils","","Paralen","Xlear","Claritin","Smecta",""]
        print(list_of_medication)
        string_of_medication = ""
        
        indx = 0
        for sym in symptoms:
            if sym == 1:
                string_of_medication = string_of_medication + list_of_medication[indx] + ", "
            indx = indx + 1
        
        
        return string_of_medication
    
    @staticmethod
    def sumarize_data(id, data):
        list_of_column_names = []
        list_of_occurences = []
        df = data.data
        id = int(id)
        df = df.loc[df['id'] == id]
        for col in df.columns:
            list_of_column_names.append(col)
        #1-11
        
        plot_df = pd.DataFrame({
            "Symptoms": list_of_column_names,
            #"Occurence":list_of_occurences,
            "Occurence": [1, df['Fever'].sum(), df['Tiredness'].sum(), df['Dry-Cough'].sum(), df['Difficulty-in-Breathing'].sum(), df['Sore-Throat'].sum(), df['None_Sympton'].sum(), df['Pains'].sum(), df['Nasal-Congestion'].sum(), df['Runny-Nose'].sum(), df['Diarrhea'].sum(), df['None_Experiencing'].sum(),13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31, 32],
        })
        plot_df = plot_df.iloc[1:12, :]
        #plot_df = df['Score'].sum()
        return plot_df
        
        
        

class Pie:
    def __init__(self):
        super().__init__()
   
    def pie_data(self,coviddf):
        data=[
            #go.pie(args=coviddf.Fever, name="Fever"),
            #go.pie(args=coviddf.Symptoms, name="plot"),
            go.Bar(x=coviddf.Symptoms, y=coviddf.Occurence, name="plot"),
            #go.Scatter(x=coviddf.id, y=coviddf.Tiredness, name="Tiredness")
        ]
        return data
    def json_pie(self,coviddf):
        data = self.plot_data(coviddf)
        return json.dumps(data, cls=py.utils.PlotlyJSONEncoder)

    
    def show(self,df):
        fig = go.Figure(data=[go.Bar(x=df.Symptoms, y=df.Occurence, name="plot")])
        fig.show()
    
class Plot:
    def __init__(self):
        super().__init__()
    
    def plot_data(self,coviddf):
        data=[
            #go.pie(args=coviddf.Fever, name="Fever"),
            #go.pie(args=coviddf.Symptoms, name="plot"),
            go.Bar(x=coviddf.Symptoms, y=coviddf.Occurence, name="plot"),
            #go.Scatter(x=coviddf.id, y=coviddf.Tiredness, name="Tiredness")
        ]
        return data
    def json_plot(self,coviddf):
        data = self.plot_data(coviddf)
        return json.dumps(data, cls=py.utils.PlotlyJSONEncoder)

    
    def show(self,df):
        fig = go.Figure(data=[go.Bar(x=df.Symptoms, y=df.Occurence, name="plot")])
        fig.show()

#Fever,Tiredness,Dry-Cough,Difficulty-in-Breathing,Sore-Throat,None_Sympton,Pains,Nasal-Congestion,Runny-Nose,Diarrhea,None_Experiencing,Age_0-9,Age_10-19,Age_20-24,Age_25-59,Age_60+,Gender_Female,Gender_Male,Gender_Transgender,Severity_Mild,Severity_Moderate,Severity_None,Severity_Severe,Contact_Dont-Know,Contact_No,Contact_Yes,Country
class Table:
    def __init__(self):
        super().__init__()
        
    def table_data(self, df):
        data=[
            go.Table(
            header=dict(values=[df.data.columns[0], df.data.columns[28],df.data.columns[29],df.data.columns[27]],
                        fill_color='#1F77B4', 
                        font=dict(color='white'),
                        align='left'),
            cells=dict(values=[df.data.id, df.data.Age, df.data.Gender, df.data.Country],
                    fill_color='aliceblue',
                    align='left'))
        ]
        return data
    
    def json_table(self,df):
        data = self.table_data(df)
        return json.dumps(data, cls=py.utils.PlotlyJSONEncoder)
    
    def show(self, df):
            fig = go.Figure(data=[go.Table(
            header=dict(values=[df.data.columns[0], df.data.columns[28],df.data.columns[29],df.data.columns[27]],
                        fill_color='cornflowerblue',
                        align='left'),
            cells=dict(values=[df.data.id, df.data.Age, df.data.Gender, df.data.Country],
                    fill_color='aliceblue',
                    align='left'))
            ])
            fig.show()