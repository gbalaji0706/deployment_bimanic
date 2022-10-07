
from flask import Flask, render_template, request

from flask_mail import Mail, Message

from quiz_questions import quiz_details

import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler 
from tensorflow import keras
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)


mail = Mail()
mail.init_app(app) 
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'modelbimanic@gmail.com'
app.config['MAIL_PASSWORD'] = 'tgovkqlnimlowkjh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

print("SMTP mail setup success..")



print("Please wait, supporting files is loading..........")
df_mean=pd.read_excel("Dep_Mean_2015_without.xlsx")
df_mean=df_mean.drop(['Unnamed: 0'],axis=1)
print("Supporting files loaded successfully, creating temporary files to run program..........")

# Preprocessing 

f=['AS001', 'AS002', 'AS003', 'AS004', 'AS005', 'AS006', 'AS007', 'AS008', 'AS009', 'AS010', 'AS011', 'AS013', 'AS014', 'AS015', 'AS016', 'AS017', 'ED003', 'ED004', 'ED005', 'ED006', 'ED007', 'ED008', 'ED010', 'EG001', 'EG002', 'EG006', 'FT002', 'FT003', 'FT004', 'FT005', 'FT006', 'FT007', 'FT008', 'FT009', 'FT010', 'HM001', 'IH001', 'IH002', 'IH003', 'IH004', 'IS003', 'IS004', 'IS005', 'IS006', 'LE001', 'MT001', 'MT002', 'MT003', 'MT004', 'MT005', 'MT006', 'MT007', 'MT008', 'MT009', 'NA001', 'NH001', 'NI001', 'NM001', 'NN001', 'NR001', 'NS001', 'NU001', 'OE001', 'OE002', 'OE005', 'OE011', 'OE012', 'OE014', 'OE015', 'OE016', 'OE017', 'OE018', 'OE020', 'OE022', 'OE023', 'OE024', 'OE026', 'OE028', 'OE035', 'OE036', 'OE037', 'OE040', 'OE041', 'OE042', 'OE043', 'OE045', 'PD003', 'PI005', 'QF001', 'SA001', 'SA006', 'SA011', 'SA012', 'SA013', 'SA014', 'SA015', 'SA016', 'SA017', 'SA021', 'SA022', 'SA023', 'SA024', 'SA026', 'SA027', 'SA028', 'SA031', 'SA032', 'SA033', 'SA034', 'SA041', 'SA042', 'SA043', 'SA051', 'SA053', 'SA061', 'SA062', 'SA063', 'SA064', 'SA071', 'SA072', 'SA073', 'SA083', 'SA084', 'SA085', 'SA086', 'SA087', 'SA088', 'SA089', 'SA090', 'SA092', 'SA093', 'SA094', 'SA097', 'SA098', 'SA099', 'SA100', 'SA101', 'SA102', 'SA106', 'SA107', 'SA108', 'SA109', 'SA110', 'SA111', 'SA116', 'SA117', 'SA126', 'SA127', 'SA128', 'SA129', 'SA136', 'SA137', 'SA138', 'SA139', 'SA140', 'SA141', 'SA142', 'SA148', 'SA149', 'SA150', 'SA151', 'SA156', 'SA157', 'SA158', 'SA166', 'SA176', 'SA177', 'SA178', 'SA186', 'SA187', 'SA188', 'SA196', 'SA206', 'SA207', 'SA208', 'SA209', 'SA211', 'SA212', 'SA216', 'SA217', 'SA218', 'SA226', 'SA227', 'SA228', 'SA229', 'SA236', 'SA237', 'SA256', 'SA257', 'SA260', 'SA261', 'SA266', 'SA267', 'SA268', 'SA276', 'SA277', 'SA278', 'SA279', 'SE001', 'SE002', 'SE003', 'SE004', 'SE005', 'SE007', 'SE008', 'SE009', 'SE011', 'SE022', 'SE053', 'SE055', 'SE056', 'SE061', 'SE064', 'SE068', 'SE069', 'SE070', 'SE071', 'SE072', 'SE073', 'SE074', 'SE091', 'SE092', 'SE094', 'SE101', 'SE103', 'SE105', 'SE131', 'SE133', 'SE134', 'SE135', 'SE145', 'SE154', 'SE174', 'SE182', 'SE194', 'SE211', 'SE212', 'SE214', 'SE215', 'SE231', 'SE232', 'SE236', 'SE237', 'SE244', 'SE251', 'SE253', 'SE254', 'SE271', 'SE303', 'SE305', 'SE306', 'SE307', 'SE311', 'SE312', 'SE313', 'SE314', 'SE324', 'SE332', 'SE351', 'SE361', 'SE371', 'SE400', 'SE401', 'SE402', 'SE404', 'SE405', 'SE406', 'SE411', 'SE412', 'SE421', 'SE430', 'SE440', 'SE441', 'SE460', 'SE470', 'SE471', 'SE472', 'SE473', 'SE480', 'SE481', 'SE482', 'SE483', 'SE490', 'SE491', 'SE492', 'SE500', 'SE501', 'SE502', 'SE503', 'SE504', 'SE505', 'SE520', 'SE521', 'SE522', 'SE523', 'SE524', 'SE526', 'SE529', 'SE530', 'SE531', 'SE532', 'SE533', 'SE534', 'SE540', 'SE541', 'SE542', 'SE543', 'SE550', 'SE551', 'SE553', 'SE554', 'SE555', 'SE560', 'SE561', 'SE562', 'SE563', 'SE564', 'SE565', 'SE573', 'SE580', 'SE581', 'SE583', 'SE600', 'SE601', 'SE602', 'SE603', 'SE610', 'SE611', 'SE620', 'SE621', 'SE622', 'SE623', 'SE624', 'SE630', 'SE631', 'SE632', 'SE633', 'SE634', 'SE635', 'SE636', 'SE640', 'SE641', 'SE642', 'SE643', 'SE644', 'SE645', 'SE646', 'SE650', 'SE651', 'SE652', 'SE653', 'SE654', 'SE660', 'SE661', 'SE662', 'SE663', 'SE664', 'SE665', 'SE670', 'SE671', 'SE680', 'SE682', 'SE683', 'SE700', 'SE702', 'SE710', 'SE711', 'SE712', 'SE720', 'SE721', 'SE722', 'SE730', 'SE732', 'SE733', 'SE740', 'SE741', 'SE742', 'SE743', 'SE760', 'SE770', 'SE780', 'SE781', 'SE782', 'SE790', 'SE791', 'SE792', 'SE793', 'SE794', 'SE796', 'SE799', 'SE900', 'SE901', 'SE902', 'SE903', 'SE905', 'SE906', 'SE910', 'SE920', 'SE922', 'SE923', 'SE924', 'SE925', 'SE926', 'SE927', 'SE930', 'SE935', 'SF011', 'SF012', 'SF013', 'SF014', 'SF016', 'SF017', 'SF023', 'SF024', 'SF026', 'SF028', 'SF031', 'SF032', 'SF034', 'SF041', 'SF051', 'SF061', 'SF062', 'SF063', 'SF064', 'SF071', 'SF072', 'SF081', 'SF091', 'SF096', 'SF106', 'SF108', 'SF109', 'SF116', 'SF126', 'SF127', 'SF146', 'SF147', 'SF152', 'SF153', 'SF156', 'SF157', 'SF167', 'SF176', 'SF177', 'SF178', 'SF186', 'SF187', 'SF188', 'SF196', 'SF216', 'SF217', 'SF218', 'SF229', 'SF256', 'SF257', 'SF277', 'SF278', 'SF279', 'SI021', 'SI023', 'SI054', 'SI055', 'SI061', 'SI070', 'SI075', 'SI078', 'SP011', 'SP012', 'SP013', 'SP014', 'SP015', 'SP016', 'SP017', 'SP023', 'SP024', 'SP026', 'SP028', 'SP031', 'SP032', 'SP034', 'SP041', 'SP051', 'SP061', 'SP062', 'SP063', 'SP064', 'SP071', 'SP072', 'SP081', 'SP091', 'SP096', 'SP106', 'SP107', 'SP108', 'SP109', 'SP116', 'SP126', 'SP127', 'SP146', 'SP147', 'SP152', 'SP153', 'SP156', 'SP157', 'SP167', 'SP176', 'SP177', 'SP178', 'SP186', 'SP187', 'SP196', 'SP216', 'SP217', 'SP218', 'SP229', 'SP256', 'SP257', 'SP277', 'SP278', 'SP279', 'SQ001', 'SQ050', 'SQ055', 'SQ100', 'SQ150', 'SQ200', 'SQ250', 'SQ255', 'SQ300', 'SQ350', 'SQ500', 'SQ550', 'SQ600', 'SQ650', 'SQ660', 'SQ670', 'SQ700', 'SQ780', 'SQ800', 'SR006', 'SR011', 'SR012', 'SR015', 'SR016', 'SR017', 'SR021', 'SR023', 'SR024', 'SR026', 'SR027', 'SR031', 'SR032', 'SR033', 'SR034', 'SR041', 'SR042', 'SR051', 'SR053', 'SR062', 'SR064', 'SR071', 'SR072', 'SR073', 'SR083', 'SR084', 'SR085', 'SR086', 'SR087', 'SR088', 'SR089', 'SR090', 'SR092', 'SR094', 'SR097', 'SR098', 'SR099', 'SR100', 'SR101', 'SR102', 'SR106', 'SR107', 'SR108', 'SR109', 'SR110', 'SR111', 'SR116', 'SR126', 'SR128', 'SR129', 'SR136', 'SR137', 'SR138', 'SR139', 'SR140', 'SR141', 'SR142', 'SR148', 'SR149', 'SR150', 'SR151', 'SR156', 'SR157', 'SR176', 'SR177', 'SR186', 'SR187', 'SR188', 'SR196', 'SR206', 'SR207', 'SR208', 'SR209', 'SR211', 'SR212', 'SR216', 'SR218', 'SR226', 'SR227', 'SR228', 'SR229', 'SR236', 'SR237', 'SR256', 'SR257', 'SR276', 'SR277', 'SR278', 'SR279', 'TC001', 'TC002', 'TC003', 'TC004', 'TC005', 'TC006', 'TC007', 'TC012', 'TC013', 'VT001', 'VT002', 'VT003', 'VT004', 'VT005', 'VT006', 'VT007', 'VT008', 'VT009', 'VT010', 'VT011', 'VT012', 'VT014']

for label in f:

    df_mean[label]=np.where(df_mean['FIRST_CHOICE_CODE']==label,1,0)

for label in f:
    df_mean[label]=np.where(df_mean['SECOND_CHOICE_CODE']==label,1,0)
for label in f:

    df_mean[label]=np.where(df_mean['THIRD_CHOICE_CODE']==label,1,0)
for i in df_mean.index:
    c1=df_mean['FIRST_CHOICE_CODE'][i]
    c2=df_mean['SECOND_CHOICE_CODE'][i]
    c3=df_mean['THIRD_CHOICE_CODE'][i]
    if c1==0 or c2==0 or c3==0:
        
        continue
    df_mean[c1][i]=1
    df_mean[c2][i]=1
    df_mean[c3][i]=1


print(df_mean.shape)
# PreProcessing and cleaning Data Set
df_mean=df_mean.drop(['FIRST_CHOICE_CODE','SECOND_CHOICE_CODE','THIRD_CHOICE_CODE'],axis=1)
te=df_mean['CHOICE_NUM_ALLOCATED']
for i in df_mean.index:
  if te[i]>3:
    te[i]=4
y_data=df_mean['CHOICE_NUM_ALLOCATED']
x_data=df_mean.drop('CHOICE_NUM_ALLOCATED',axis=1)

x_train,x_test,y_train,y_test=train_test_split(x_data,y_data,test_size=0.002,random_state=42)
x_train=x_train.values
sc=StandardScaler().fit(x_train)
x_data_scaled=sc.transform(x_train)


# Pre Processing Done



model = keras.models.load_model("model_14_08_2015_removing_personal_details1.h5")

y_pred=model.predict(x_data_scaled)
y_pred = np.argmax(y_pred, axis=1)
y_train_l=list(y_train)
y_pred_l=list(y_pred)
count=0
for i in range(len(y_train_l)):
  if y_pred_l[i]+1==y_train_l[i]:
    count+=1
if count>15000:
    print("Model is Working fine")
## Formulating Dictionary ##
sam=pd.read_excel("Final_Majors2.xlsx")
samp={}
sam_i=list(sam.index)
for i in range(len(sam_i)):
    s_l=[]
    s_l.append(sam['PROGRAM_NAME'][i])
    s_l.append(sam['MAJOR_GROUP_NAME'][i])
    samp[sam['PROGRAM_CODE'][i]]=s_l

print("Hello World")


def batch_preprocessing(x):
  for label in f:
    
    x[label]=0
  return x
samp_l_test=list(samp.keys())

app = Flask(__name__)
major_q =" "
quiz_mode =" "
choice_q =" "


co_curricular=" "
extra_curricular=" "
aptitude_result=" "
q1_curricular=" "
q2_curricular=" "




@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index')
def index():
    return render_template('dummy.html')


@app.route('/index1')
def index1():
    return render_template('index1.html')

@app.route('/co_curricular')
def co_curricular():
    return render_template('co_curricular.html')











@app.route('/predict', methods=['POST'])
def predict():
    # Creating Sample DataFrame
    d={
   
   "SCIENCE":[0],
   "GEOGRAPHY":[0],
   "PHYSICS":[0],
   "ISLAMICEDUCATION":[0],
   "ARABICLANGUAGE":[0],
   "BIOLOGY":[0],
   "CHEMISTRY":[0],
   "ENGLISHLANGUAGE":[0],
   "MATH":[0]

}
# Getting User Input and performing preprocessing to generate Data Frame
    d=pd.DataFrame.from_dict(d)

 
 
    
    d['MATH']=float(request.form['math'])
  
    d['SOCIALSTUDIESCIVICS']=float(request.form['socialstudiescivics'])
    d['SCIENCE']=float(request.form['science'])

    d['GEOGRAPHY']=float(request.form['geography'])
    d['PHYSICS']=float(request.form['physics'])
    d['ISLAMICEDUCATION']=float(request.form['islamiceducation'])
    d['ARABICLANGUAGE']=float(request.form['arabiclanguage'])
    d['BIOLOGY']=float(request.form['biology'])
    d['CHEMISTRY']=float(request.form['chemistry'])
    d['ENGLISHLANGUAGE']=float(request.form['englishlanguage'])

    res=batch_preprocessing(d)
    ch1=str(request.form['c1'])
    ch2=str(request.form['c2'])
    ch3=str(request.form['c3'])
    
   
    res[ch1]=1
    res[ch2]=1
    res[ch3]=1
   
    
    # Predicting 
    res1=res.loc[0].values
    res1=res1.reshape(-1,661)
    res_data=sc.transform(res1)
    y_temp_pred=model.predict(res_data)
    y_temp = np.argmax(y_temp_pred, axis=1)
    p=y_temp[0]+1

   




    

    
    if p==1:
        c_c=ch1 
        if c_c in samp_l_test:
            sam_l=samp[c_c] 
            p_name=sam_l[0] 
            m_name=sam_l[1]
        else:
            p_name="Not Available"
            m_name="Not Available"

    elif p==2:
        c_c=ch2
        if c_c in samp_l_test:
            sam_l=samp[c_c] 
            p_name=sam_l[0] 
            m_name=sam_l[1]
        else:
            p_name="Not Available"
            m_name="Not Available"
    elif p==3:
        c_c=ch3
        if c_c in samp_l_test:
            sam_l=samp[c_c] 
            p_name=sam_l[0] 
            m_name=sam_l[1]
        else:
            p_name="Not Available"
            m_name="Not Available"
    elif p==4:
        c_c="Not Eligible"
        p_name="Not Available in Majors List"
        m_name="Not Available in Majors List"



    global major_q
    global quiz_mode
    global choice_q

  

    choice_q=c_c
    major_q=m_name
    quiz_mode=m_name


    print(choice_q) 
    print(major_q) 
    print(quiz_mode) 
    
    
   
  
    return render_template('after.html',pred=p,p_name=p_name,m_name=m_name,c_c=c_c)


questions=[]
answers=[]
m_questions=[]
m_answers=[]
flag=0

@app.route('/quiz',methods=['POST','GET'])
def quiz():
   
   '''
    if major_q=="Health":
        quiz_mode="Health"
        return render_template('quiz.html')
    quiz_mode="Normal"
    return render_template('default_quiz.html',major_q=major_q)


   '''
   global questions
   global answers
   global m_questions
   global m_answers

   quiz_list=["Natural and Physical Sciences","Information Technology","Engineering and Related Technologies","Architecture and building","Agriculture, environmental and related studies","Health","Education","Management and commerce","Society and Culture","Religion and philosophy","Creative Arts"]

   if major_q in quiz_list:

       questions,answers=quiz_details.quiz_q(major_q)
       m_questions,m_answers=quiz_details.quiz_q("Maths")

       return render_template('default_quiz.html',data=questions,m_data=m_questions,major_q=major_q)
   else:
       global flag
       flag=1
       m_questions,m_answers=quiz_details.quiz_q("Maths")

       return render_template('default_quiz_maths.html',data=questions,m_data=m_questions,major_q=major_q)

       







@app.route('/validate_quiz',methods=['POST','GET'])
def validate_quiz():

    '''
    global aptitude_result
    maths_key=['A', 'C', 'B', 'B', 'C', 'A', 'A', 'A', 'A', 'D']
    health_key=['D', 'C', 'A', 'B', 'D', 'B', 'B', 'A', 'C', 'C', 'B', 'C', 'B', 'D', 'B', 'D', 'A', 'C', 'B', 'D', 'A', 'C', 'B', 'C', 'A', 'D', 'B', 'C', 'A', 'C']
    if major_q=="Health":
        q1=str(request.form['question1'])
        q2=str(request.form['question2'])
        q3=str(request.form['question3'])
        q4=str(request.form['question4'])
        q5=str(request.form['question5'])
        q6=str(request.form['question6'])
        q7=str(request.form['question7'])
        q8=str(request.form['question8'])
        q9=str(request.form['question9'])
        q10=str(request.form['question10'])
        q11=str(request.form['question11'])
        q12=str(request.form['question12'])
        q13=str(request.form['question13'])
        q14=str(request.form['question14'])
        q15=str(request.form['question15'])
        q16=str(request.form['question16'])
        q17=str(request.form['question17'])
        q18=str(request.form['question18'])
        q19=str(request.form['question19'])
        q20=str(request.form['question20'])
        q21=str(request.form['question21'])
        q22=str(request.form['question22'])
        q23=str(request.form['question23'])
        q24=str(request.form['question24'])
        q25=str(request.form['question25'])
        q26=str(request.form['question26'])
        q27=str(request.form['question27'])
        q28=str(request.form['question28'])
        q29=str(request.form['question29'])
        q30=str(request.form['question30'])

        maths_ans=[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26, q27, q28, q29,q30]
        
        q101=str(request.form['question101'])
        q102=str(request.form['question102'])
        q103=str(request.form['question103'])
        q104=str(request.form['question104'])
        q105=str(request.form['question105'])
        q106=str(request.form['question106'])
        q107=str(request.form['question107'])
        q108=str(request.form['question108'])
        q109=str(request.form['question109'])
        q110=str(request.form['question110'])
        q111=str(request.form['question111'])
        q112=str(request.form['question112'])
        q113=str(request.form['question113'])
        q114=str(request.form['question114'])
        q115=str(request.form['question115'])
        q116=str(request.form['question116'])
        q117=str(request.form['question117'])
        q118=str(request.form['question118'])
        q119=str(request.form['question119'])
        q120=str(request.form['question120'])
        q121=str(request.form['question121'])
        q122=str(request.form['question122'])
        q123=str(request.form['question123'])       
        q124=str(request.form['question124'])
        q125=str(request.form['question125'])
        q126=str(request.form['question126'])
        q127=str(request.form['question127'])
        q128=str(request.form['question128'])
        q129=str(request.form['question129'])
        q130=str(request.form['question130'])
        health_ans=[q101, q102, q103, q104, q105, q106, q107, q108, q109, q110, q111, q112, q113, q114, q115, q116, q117, q118, q119, q120, q121, q122, q123, q124, q125, q126, q127, q128, q129, q130]

        quiz_count=0
        for i in range(len(maths_ans)):
            if maths_ans[i]==maths_key[i]:
                quiz_count+=1
            if health_ans[i]==health_key[i]:
                quiz_count+=1

        

        if quiz_count>=29:
            
            aptitude_result="The results of aptitude shows that you are eligible to perform in this speciality"
            return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)

        aptitude_result="The results of aptitude shows that you are not eligible to perform in this speciality"

        return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)

    else:
        q1=str(request.form['question1'])
        q2=str(request.form['question2'])
        q3=str(request.form['question3'])   
        q4=str(request.form['question4'])
        q5=str(request.form['question5'])
        q6=str(request.form['question6'])
        q7=str(request.form['question7'])
        q8=str(request.form['question8'])
        q9=str(request.form['question9'])
        q10=str(request.form['question10'])

        q11=str(request.form['question11'])
        q12=str(request.form['question12'])
        q13=str(request.form['question13'])
        q14=str(request.form['question14'])
        q15=str(request.form['question15'])
        q16=str(request.form['question16'])
        q17=str(request.form['question17'])
        q18=str(request.form['question18'])
        q19=str(request.form['question19'])
        q20=str(request.form['question20'])
        q21=str(request.form['question21'])
        q22=str(request.form['question22'])
        q23=str(request.form['question23'])
        q24=str(request.form['question24'])
        q25=str(request.form['question25'])
        q26=str(request.form['question26'])
        q27=str(request.form['question27'])
        q28=str(request.form['question28'])
        q29=str(request.form['question29'])
        q30=str(request.form['question30'])
       
        
        q11=str(request.form['questione1'])
        q12=str(request.form['questione2'])
        q13=str(request.form['questione3'])   
        q14=str(request.form['questione4'])
        q15=str(request.form['questione5'])
        q16=str(request.form['questione6'])
        q17=str(request.form['questione7'])
        q18=str(request.form['questione8'])
        q19=str(request.form['questione9'])
        q20=str(request.form['questione10'])


        maths_ans=[q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20]

        engineering_key=['B', 'B', 'D', 'B', 'B', 'C', 'A', 'B', 'A', 'D']

    
        
        quiz_count=0
        for i in range(10):
            if maths_ans[i]==maths_key[i]:

                quiz_count+=1


        for i in range(10,20):
            if maths_ans[i]==engineering_key[i-10]:
                quiz_count+=1



   
       

        if quiz_count>=10:
            aptitude_result="The results of aptitude shows that you are eligible to perform in this speciality"
            return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)

        aptitude_result="The results of aptitude shows that you are not eligible to perform in this speciality"

        return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)

    '''
    global aptitude_result

    result = 0
    total = 0
    if flag==0:
        for question in questions:
   

            if request.form[question.get('id')] == answers[result]:
                        
                            total += 1
            result += 1

    result=0
    for question in m_questions:

        if request.form[question.get('id')] == m_answers[result]:
                        
                        total += 1
        result += 1



    
    if total>=(total/2):
            
        aptitude_result="The results of aptitude shows that you are eligible to perform in this speciality"
        return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)

    aptitude_result="The results of aptitude shows that you are not eligible to perform in this speciality"

    return render_template('quiz_result.html',major_q=major_q,choice_q=choice_q,text=aptitude_result)






@app.route('/report',methods=['POST','GET'])

def report():


    global co_curricular
    global extra_curricular
    global q1_curricular
    global q2_curricular

    q1_curricular=str(request.form['question1_c'])
    co_curricular="You have not Participated in any co curricular activities"
    extra_curricular="You have not Participated in any extra curricular activities"

    if q1_curricular=='yes':
        co_curricular=str(request.form['cocurricular'])
    q2_curricular=str(request.form['question2_c'])

    if q2_curricular=='yes':
        extra_curricular=str(request.form['extracurricular'])

    if aptitude_result=="The results of aptitude shows that you are eligible to perform in this speciality":

        aptitude_text="you have performed well in aptitude please keep up the good work"
    else:
        aptitude_text="Aptitude tests are used for the purpose of prediction for future success both in educational and vocational careers  so you need to put more effort to improve your aptitude skills"

    if q1_curricular=='yes' and q2_curricular=='yes':
        curricular_text=" You have participated in both extra and co-curricular activities please keep up the good work"
    elif q1_curricular=='yes' and q2_curricular=='no':
        curricular_text="Participating in extracurricular activities benefits students personal and academic success  and provides opportunities for students to experience the importance of community involvement, so please do participate and improve on your extracurricular activities"

    else:
        curricular_text=" The purpose of co-curricular activities is to fuel student learning and to build important life skills. Skills built, such as social and leadership skills, can enrich a student's academic experience.So please do participate and improve on your co-curricular activity."









    return render_template('report.html',aptitude_result=aptitude_result,major_q=major_q,co_curricular=co_curricular,extra_curricular=extra_curricular,aptitude_text=aptitude_text,curricular_text=curricular_text)
   

        



@app.route("/send_mail",methods=['POST','GET'])
def send_mail():


   user=str(request.form['user'])
   msg = Message(
                'Performance report generated using BIMANIC model',
                sender ='gbalaji07061999',
                recipients = [user]
               )

  

  

   msg_text="          Artificial Intelligence-driven Gen-Alpha education guidance indicator to craft quality citizens In the Sultanate of Oman"+"\n"+"\n"+"Based on your marks and chosen preferred choice, the following programme is offered:"+major_q+"\n"+"Aptitude tests are used for the purpose of prediction for further success both in education and vocational careers."+"\n"+aptitude_result+"\n"+"You have participated in the following extracurricular activities:" + extra_curricular + "\n"+ "You have participated in the following co-curricular activities:"+co_curricular + "\n" +"Please keep up your good work" + "\n" + "\n"+ "             Thanks for using BIMANIC model. We wish you all the very best." +"\n"+"\n"+"\n"+"Note: This is just to help you to select the right specialization. And please note that MOHERI has limited seats and distributed as per the MOHERI regulations"
            




   msg.body = msg_text
   mail.send(msg)







   return render_template('mail_success.html')


@app.route('/predict1', methods=['POST'])
def predict1():
    
    d=pd.read_excel("BIMANIC.xlsx")
    print(d.shape)
    t={'male':1,'female':0}
    s={'low_income':0,'other':1,'social_security':2}
    name = request.form['name']
    civilid=request.form['civilid']
    d['AGE']=float(request.form['age'])
    d[request.form['gender']]=t[request.form['gender']]
    d[request.form['socialstatus']]=s[request.form['socialstatus']]
    d['MATH']=float(request.form['math'])
  
    d['SOCIALSTUDIESCIVICS']=float(request.form['socialstudiescivics'])
    d['SCIENCE']=float(request.form['science'])

    d['GEOGRAPHY']=float(request.form['geography'])
    d['PHYSICS']=float(request.form['physics'])
    d['ISLAMICEDUCATION']=float(request.form['islamiceducation'])
    d['ARABICLANGUAGE']=float(request.form['arabiclanguage'])
    d['BIOLOGY']=float(request.form['biology'])
    d['CHEMISTRY']=float(request.form['chemistry'])
    d['ENGLISHLANGUAGE']=float(request.form['englishlanguage'])
    
    del d['RANK_MARKS']


    
    sc=StandardScaler()
    d=d.values
    d=sc.fit_transform(d)
    data=np.argmax(model.predict(d), axis=1)[0]+1 

  
    
    
    
   
  
    return render_template('after.html',data=data,name=name,civilid=civilid)

if __name__ == "__main__":
    app.run(debug=True)