from flask import Blueprint , render_template , request
import pandas as pd
import csv
from os.path import join, dirname, realpath
import os
from collections import OrderedDict
from operator import getitem
import math
import gensim
import nltk
from nltk import word_tokenize
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
views = Blueprint('views' , __name__)

@views.route('/')
@views.route('/login')
def home():
    return  render_template('login.html')

@views.route('/Dashboard')
def Dashboard():
    return  render_template('Dashboard.html')    

@views.route('/Embezzlement')
def Embezzlement():
    return  render_template('Embezzlement.html')   

@views.route('/EntityPreview_NEW')
def EntityPreview_NEW():
    return  render_template('EntityPreview_NEW.html')   

@views.route('/House_Theft')
def House_Theft():
    return  render_template('House_Theft.html')  

@views.route('/MainResult' , methods=['GET', 'POST'])
def MainResult():
    if request.method == 'POST':
        Report_title  = request.form.get('Report_title')
        Reporter_name  =request.form.get('Reporter_name')
        Incident_date  =  request.form.get('Incident_date')
        time  =  request.form.get('time')
        City  = request.form.get('City')
        Day  =  request.form.get('Day')
        Place  =  request.form.get('Place')
        District  = request.form.get('District')
        street  = request.form.get('street')
        loot  = request.form.get('loot')
        loot_description  = request.form.get('loot_description')
        is_camera  =  request.form.get('is_camera')
        loot_methodology  =  request.form.get('loot_methodology')
        estemated_loot_value  =  request.form.get('estemated_loot_value')
        Accused =  request.form.get('accused_name')
        weapon_existens  = request.form.get('weapon_existens')
        Accuseds_number  =  request.form.get('Accuseds_number')
        number_of_accused  = request.form.get('number_of_accused')
        Accused_description  = request.form.get('Accused_description')
        skin_colour  =  request.form.get('skin_colour')  
        Nationality  =  request.form.get('Nationality')   
        Age  =  request.form.get('Age')   
        accused_body  = request.form.get('accused_body')
        Report_content =  request.form.get('Report_content')
        known_vehicle =  request.form.get('known_vehicle')
 

        path1 = join(dirname(realpath(__file__)), 'static/Data', 'datatest.txt')
        text_file = open(path1, "r")
        lines = text_file.readlines()
        text_file.close()

        path = join(dirname(realpath(__file__)), 'static/Data', 'data_1111111.csv')
        #print(path) # /var/www/public_html/app/myfile.json
        data = pd.read_csv(path, nrows=500)
        data = data.to_dict('records')
        def tagged_document(list_of_list_of_words):
            for i, list_of_words in enumerate(list_of_list_of_words):
                yield gensim.models.doc2vec.TaggedDocument(list_of_words, [i])
        data_for_training = list(tagged_document(data[:999]))
        model = gensim.models.doc2vec.Doc2Vec(vector_size = 40, min_count = 2, epochs = 30)
        model.build_vocab(data_for_training)
        model.train(data_for_training, total_examples = model.corpus_count, epochs = model.epochs )
        #print(model.infer_vector("نا فاطمة المالك أرغب بالتبليغ عن حادثة سرقة منزل تمت السرقة في تاريخ 44402 الوقت 03:".split()))
        print(model.docvecs.most_similar([10]))
        token = Report_content.split()
        new_vector  = model.infer_vector(doc_words=token, alpha=0.025,min_alpha=0.001)




        path = join(dirname(realpath(__file__)), 'static/Data', 'data_1111111.csv')
        #print(path) # /var/www/public_html/app/myfile.json
        data = pd.read_csv(path, nrows=500)
        data = data.to_dict('records')
       # print(data[0])
        new = {
        'Report_title':  Report_title ,
        'Reporter_name': Reporter_name ,
        'Incident_date': Incident_date,
        'Day': Day,
        'time': time,
        'Place': Place,
        'City': City,
        'District': District,
        'street': street,
        'loot': loot,
        'loot_description': loot_description,
        'is_camera': is_camera,
        'loot_methodology': loot_methodology ,
        'estemated_loot_value': estemated_loot_value,
        'Accused': Accused,
        'weapon_existens': weapon_existens,
        'Accuseds_number': Accuseds_number,
        'Accused_description': Accused_description,
        'skin_colour': skin_colour,
        'Nationality':  Nationality ,
        'Age':Age,
        'known_vehicle': known_vehicle,
        'accused_body': accused_body,
        'Report_content':Report_content}

        y = 0

        res_d = {y : {}}

        for key in data:
            # print(key)
            row = key
            res = False
            count = 0
            similar_feileds = []
            for key in new:
                if new.get(key) == row.get(key):
                    res = True
                    count = count + 1
                    similar_feileds.append(key)

            similarity = count/ len(new)            
            if(similarity != 0):
                print('break')
                res_d[y] = {}
                res_d[y]['similarity'] = similarity
                res_d[y]['Report_content'] = row["Report_content"]
                #print(res_d[y])
                #print(y)
                y =  y + 1
                
            #print("first")
            #print(res_d)
        # print("second")
        # print(res_d)
        res = OrderedDict(sorted(res_d.items(),reverse=True, key = lambda x: getitem(x[1], 'similarity')))
        sim1 = res[0]['similarity']
        sim1 = round(sim1 , 4)
        report1 = res[0]['Report_content']
        sim2 = res[1]['similarity']
        sim2 = round(sim2 , 4)
        report2 = res[1]['Report_content']
        sim3 = res[2]['similarity']
        sim3 = round(sim3 , 4)
        report3 = res[2]['Report_content']
        sim4 = res[3]['similarity']
        sim4 = round(sim4 , 4)
        report4 = res[3]['Report_content']
        sim5 = res[4]['similarity']
        sim5 = round(sim5 , 4)
        report5 = res[4]['Report_content']

        return  render_template('MainResult.html' , brv = Report_content, val1_S = sim1 , val1_r = report1 ,val2_S = sim2 , val2_r = report2 , val3_S = sim3 ,val3_r = report3, val4_S = sim4 ,val4_r = report4,  val5_S = sim5 ,val5_r = report5 )    
    return  render_template('MainResult.html' )  

@views.route('/Preview_NEW_Embezzlement')
def Preview_NEW_Embezzlement():
    return  render_template('Preview_NEW_Embezzlement.html')  

@views.route('/Preview_NEW_House_Theft')
def Preview_NEW_House_Theft():
    return  render_template('Preview_NEW_House_Theft.html')  

@views.route('/ProceedingPreview_OLD')
def ProceedingPreview_OLD():
    return  render_template('Preview_NEW_House_Theft.html')  

@views.route('/ReportContent')
def ReportContent():
    return  render_template('ReportContent.html') 

@views.route('/AdvancedResults')
def AdvancedResults():
    return  render_template('AdvancedResults.html')   

    