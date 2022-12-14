import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import joblib
import requests
from lime import lime_tabular
from matplotlib import pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
pickled_model=joblib.load('model.pkl')

data=pd.read_json(r'data.json')
predict_data=pd.read_json(r'predict_df.json')
predict_data=predict_data.set_index('index')

explainer = lime_tabular.LimeTabularExplainer(data.drop('TARGET',axis=1).values, mode="classification",
                                              class_names=[0,1],
                                              feature_names=data.columns)
def lime(client_id):
	
    explanation = explainer.explain_instance(predict_data.loc[client_id,:].values, pickled_model.predict_proba,
    	                                      num_features=len(predict_data.columns))

    return(explanation)





header=st.container()
client_score=st.container()
feature_importance_local=st.container()
feature_graph=st.container()
featur_importance_global=st.container()
client_info=st.container()
modeltraining=st.container()

def request(client_number):
    url = 'http://localhost:1239/api'
    r = requests.get(url,json={'client_num':client_number})
    return r.json()


with header:
	st.title('Welcome to my Data Science project')
	client_num=st.number_input('Client number')


with feature_importance_local:
     st.header('Local Explanation')	
     if st.button("Explain Results"):

        with st.spinner('Calculating...'):

	        components.html(lime(client_num).as_html(), height=800)
	#st.pyplot(lime(client_num).as_pyplot_figure())
	#plt.clf()
    #st.markdown(lime(client_num).as_html(), unsafe_allow_html=True)
with client_score:
	  fig=go.Figure(go.Indicator(mode="gauge+number",value=request(client_num),title={'text':'Score'}))
	  st.header('Prediction')
	  st.plotly_chart(fig,use_container_width=True)
	#st.write(request(client_num))
	  


with feature_graph:
	 st.header('Feature vs Target bar chart')
	 inp_col,out_col=st.columns(2)
with inp_col:
     st.header('Select Feature') 	 	
     inp=st.selectbox('Select Feature',data.columns)
with out_col:
     #hist_data=[list(data[data['TARGET']==0].head(100)[inp].values)]
     #fig=ff.create_distplot(hist_data,group_labels='0')
     st.header('Feature Graphs')
     #st.plotly_chart(fig,use_container_width=True)

     st.bar_chart(data,x='TARGET',y=inp) 








