from flask import Flask
from flask import render_template
from model.data_analysis import CData, Patient, Plot, Table, Pie
from flask import request
import pandas as pd

app = Flask(__name__, static_url_path="/static")

#df = pd.read_csv('data/Data.csv')

#data = CData.load_file('data/Data.csv')

# sloubce v csv: Fever,Tiredness,Dry-Cough,Difficulty-in-Breathing,Sore-Throat,None_Sympton,Pains,Nasal-Congestion,Runny-Nose,Diarrhea,None_Experiencing,Age_0-9,Age_10-19,Age_20-24,Age_25-59,Age_60+,Gender_Female,Gender_Male,Gender_Transgender,Severity_Mild,Severity_Moderate,Severity_None,Severity_Severe,Contact_Dont-Know,Contact_No,Contact_Yes,Country 
#comment = Ctrl + K + C / uncommnet = Ctrl + K + U 
# úvodní obrazovka -> 
@app.route("/")
def index():
    
    return render_template('login.html')

# zobrazí grafy příznaků pro všechny pacienty -> přepínání piechartu/ barchartu ->filtrace podle země, věku, závažnosti  ->tabulka s jednolivými pacienty -> nemusí obsahovat příznaky, jen id, pohlaví, věk, zemi,  ->kliknutí na hodnotu v tabulce by mělo přesměrovat na /patient
@app.route("/main")  
def overall():
    country =request.args.get('country')
    age = request.args.get('age')
    gender = request.args.get('gender')
    sel_id = request.args.get('id')
    covid = CData.load_file('data/Data.csv')
    
    gr = Plot()
    table = Table()  
           
    if not country is None:
        covid_by = covid.data_by_country(country)
        data_filt = CData.sumarize_data(covid_by)
        data = gr.json_plot(data_filt)
        table_data = table.json_table(covid_by)
    elif not age is None:
        covid_by = covid.data_by_age(age)
        data_filt = CData.sumarize_data(covid_by)
        data = gr.json_plot(data_filt)
        table_data = table.json_table(covid_by) 
    elif not gender is None:
        covid_by = covid.data_by_gender(gender)
        data_filt = CData.sumarize_data(covid_by)
        data = gr.json_plot(data_filt)
        table_data = table.json_table(covid_by)
    else:
        data_filt = CData.sumarize_data(covid)
        data = gr.json_plot(data_filt)
        table_data = table.json_table(covid)
  
    
    #table.show(covid)
    #gr.show(data_filt)
    countries = covid.get_countries()
    ages = covid.get_ages()
    genders = covid.get_genders()
    ids = covid.get_ids()
    return render_template('index.html',plot = data,country = country,countries = countries, table=table_data, ages = ages, genders = genders, ids = ids)

# ukáže detail pacienta -> jednotlivé příznaky, zemi a kontakty pro jeden řádek -> příznaky v barchartu?
@app.route("/patient")  
def patient():
    patient_id =request.args.get('id')
    covid = CData.load_file('data/Data.csv')
    gr = Plot()
    patient = Patient(patient_id)
    patient_info = patient.patient_select(patient_id, covid)
    medication = patient.medication_select(patient_id, covid)
    symptoms = patient.symptoms_select(patient_id, covid)
    data_filt = patient.sumarize_data(patient_id, covid)
    data = gr.json_plot(data_filt)
    print(data_filt)
    return render_template('patient.html',plot = data, id = patient_id, symptoms = symptoms,medication = medication, country = patient_info[1], age = patient_info[2], gender = patient_info[3], severity = patient_info[4])

@app.route("/title")  
def title():
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)