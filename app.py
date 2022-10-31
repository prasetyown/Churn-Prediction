import pickle
import pandas as pd
import streamlit as st
 
# loading the trained model
pickle_in = open('model.pkl', 'rb') 
classifier = pickle.load(pickle_in)
 
@st.cache()
  
# defining the function which will make the prediction using the data which the user inputs 
def prediction(CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard,
       IsActiveMember, EstimatedSalary, Geography_France,
       Geography_Germany, Geography_Spain, Gender_Female, Gender_Male):

    if Geography_France == "France":
        Geography_France = 1
    else:
        Geography_France = 0

    if Geography_Germany == "Germany":
        Geography_Germany = 1
    else:
        Geography_Germany = 0  

    if Geography_Spain == "Spain":
        Geography_Spain = 1
    else:
        Geography_Spain = 0

    if Gender_Female == "Female":
        Gender_Female = 1
    else:
        Gender_Female = 0

    if Gender_Male == "Male":
        Gender_Male = 1
    else:
        Gender_Male = 0
 
    # Making predictions 
    prediction = classifier.predict( 
        [[CreditScore, Age, Tenure, Balance, NumOfProducts, HasCrCard,
       IsActiveMember, EstimatedSalary, Geography_France,
       Geography_Germany, Geography_Spain, Gender_Female, Gender_Male]])
     
    if prediction == 0:
        pred = 'Customer will stay subscribing'
    else:
        pred = 'Customer will unsubscribe'
    return pred
      
  
# this is the main function in which we define our webpage  
def main():       
    # front end elements of the web page 
    html_temp = """ 
    <div style ="background-color:yellow;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Streamlit Churn Prediction ML App</h1>
    <h3 style ="color:black;text-align:center;">Algorithm:Support Vector Machine</h1> 
    </div> 
    """
      
    # display the front end aspect
    st.markdown(html_temp, unsafe_allow_html = True) 
      
    # following lines create boxes in which user can enter data required to make prediction 
    CreditScore = st.number_input("Customer credit score")
    Age = st.number_input("Customer age") 
    Tenure = st.selectbox('Tenure Status',(1,0))
    Balance = st.number_input("Customer balance")
    NumOfProducts = st.selectbox('Number of products',(1,2,3,4))
    HasCrCard = st.selectbox('Have credit card?',(1,0))
    IsActiveMember = st.selectbox('Currently active as a member?',(1,0)) 
    EstimatedSalary = st.number_input("Customer salary") 
    Geography_ = st.selectbox("Customer's nationality?",('France','Germany','Spain'))
    Gender_ = st.selectbox('Gender',('Female','Male'))

    my_dict = {
    "CreditScore": CreditScore,
    "Age": Age,
    "Tenure": Tenure,
    "Balance": Balance,
    "NumOfProducts": NumOfProducts,
    "HasCrCard": HasCrCard,
    "IsActiveMember": IsActiveMember,
    "EstimatedSalary": EstimatedSalary,
    "Geography": Geography_,
    "Gender": Gender_
            }
       
    df = pd.DataFrame.from_dict([my_dict])

    columns=['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard',
       'IsActiveMember', 'EstimatedSalary', 'Geography_France',
       'Geography_Germany', 'Geography_Spain', 'Gender_Female', 'Gender_Male']
       
    df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
      
    # when 'Predict' is clicked, make the prediction and store it 
    if st.button("Predict"): 
        result = classifier.predict(df)
        st.success(result)
     
if __name__=='__main__': 
    main()
