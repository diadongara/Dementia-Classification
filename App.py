import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sklearn 

model_name = "RF_Model"
file_name = open(model_name, 'rb')
scaler_model_file = "standard_scaler"
final_model = pickle.load(file_name)
scaler_model_name = open(scaler_model_file,'rb')
scaler_model = pickle.load(scaler_model_name)

@st.cache_resource
def load_sklearn_models(model_path):

    with open(model_path, 'rb') as model_file:
        final_model = pickle.load(model_file)

    return final_model
    
#title of the web page
st.title("Dementia Prediction WebApp")

IMAGE_ADDRESS = "https://media.npr.org/assets/img/2024/05/22/gettyimages-1805884626_custom-12456c773bb5d72837b1b3534ff4e90e4f68a983.jpg?s=1100&c=85&f=jpeg"
# set the image
st.image(IMAGE_ADDRESS)

st.subheader("Please enter the details:")

#input for Gender
gender=st.selectbox("Choose a gender",("Male","Female"),)
if gender=="Male":
    g=0

else:
    g=1

#input for MR delay time
mr_delay=st.slider("What is the MR delay time", 0, 2639,1)

#input for age
age=st.slider("What is the age", 0, 120,1)

#input for years of education
educ=st.slider("What is the number of years of education", 0, 50,1)

#input for Socio Economic Status
ses=st.slider("What is the value for Socio Economic Status", 0, 5,1)

#input for MMSE
mmse=st.slider("What is the value for Mini Mental State Examination", 0, 40,1)

#input for Clinical Dementia Rating
cdr=st.slider("What is the value for Clinical Dementia Rating (CDR)", 0.0, 2.0,0.5)

#input for Estimated total intracranial volume
etiv=st.slider("What is the value for Estimated total intracranial volume", 500, 2500,1)

#input for Normalize Whole Brain Volume
nwbv=st.slider("What is the value for Normalize Whole Brain Volume", 0.0, 1.0,0.001)

#input for Atlas Scaling Factor
asf=st.slider("What is the value for Atlas Scaling Factor", 0.0, 2.0,0.01)

def predict(dictionary):
  categorical_value = [list(dictionary.values())[0]]
  numeric_values=list(dictionary.values())[1:]
  numeric_values_scaled = scaler_model.transform(np.array([numeric_values]))
  print(categorical_value)
  print(numeric_values_scaled)
  final_list = categorical_value + list(numeric_values_scaled[0])
  print(final_list)
  prediction=final_model.predict([final_list])
  print(prediction)
  if prediction==[0]:
      return 'demented'
    #print('demented')
  else:
      return 'non-demented'

if st.button('Predict Dementia'):
    input_data = {'M/F_M':g,'MR Delay':mr_delay,'Age':age,'EDUC':educ,'SES':ses,'MMSE':mmse,'CDR':cdr,'eTIV':etiv,'nWBV':nwbv,'ASF':asf}
    predictions=predict(input_data)
    st.spinner(text="In progress...")
    st.subheader("User Condition: {}".format(predictions))


