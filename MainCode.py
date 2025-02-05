import streamlit as st
import numpy as np
import sys
from streamlit import cli as stcli
from scipy.integrate import quad #Single integral
from scipy.integrate import dblquad
from PIL import Image

def main():
    #criando 3 colunas
    col1, col2, col3= st.columns(3)
    foto = Image.open('randomen.png')
    #st.sidebar.image("randomen.png", use_column_width=True)
    #inserindo na coluna 2
    col2.image(foto, use_column_width=True)
    #O código abaixo centraliza e atribui cor
    st.markdown("<h2 style='text-align: center; color: #306754;'>Hybrid Aperiodic Inspection and Age-Based Policy</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background-color: #F3F3F3; padding: 10px; text-align: center;">
          <p style="font-size: 20px; font-weight: bold;">An aperiodic inspection and replacement policy based on the delay-time model with component-lifetime heterogeneity</p>
          <p style="font-size: 15px;">By: Victor H. R. Lima, Rafael, G. N. Paiva, Augusto J. S. Rodrigues, Hanser S. J. González & Cristiano A. V. Cavalcante</p>
        </div>
        """, unsafe_allow_html=True)

    menu = ["Cost-rate", "Information", "Website"]
    
    choice = st.sidebar.selectbox("Select here", menu)
    
    if choice == menu[0]:
        st.header(menu[0])
        if 'num_columns' not in st.session_state:
            st.session_state.num_columns = 2
        def add_column():
            st.session_state.num_columns += 1
        def remove_column():
            if st.session_state.num_columns > 1:
                st.session_state.num_columns -= 1
        
        st.subheader("Insert the parameter values below:")
        
        Eta1=st.number_input("Insert the scale parameter for the defect arrival distribution of “strong” components (η\u2081)", min_value = 0.0, value = 3.0, help="This parameter specifies the scale parameter for the Weibull distribution, representing the defect arrival for the stronger component.")
        Beta1=st.number_input("Insert the shape parameter for the defect arrival distribution of “strong” components (β\u2082)", min_value = 1.0, max_value=5.0, value = 2.5, help="This parameter specifies the shape parameter for the Weibull distribution, representing the defect arrival for the stronger component.")
        Eta2=st.number_input("Insert the scale parameter for the defect arrival distribution of “weak” components (η\u2081)", min_value = 3.0, value = 18.0, help="This parameter specifies the scale parameter for the Weibull distribution, representing the defect arrival for the weaker component.")
        Beta2=st.number_input("Insert the shape parameter for the defect arrival distribution of “weak” components (β\u2082)", min_value = 1.0, max_value=5.0, value = 5.0, help="This parameter specifies the shape parameter for the Weibull distribution, representing the defect arrival for the weaker component.")
        p=st.number_input("Insert the mixture parameter (p)", min_value = 0.0, max_value=1.0, value = 0.10, help="This parameter indicates the proportion of the weaker component within the total population of components.")
        Lambda=st.number_input("Insert the rate of the exponential distribution for delay-time (λ)", min_value = 0.0, value = 2.0, help="This parameter defines the rate of the Exponential distribution, which governs the transition from the defective to the failed state of a component.")
        Alpha=st.number_input("Insert the false-positive probability (\u03B1)", min_value = 0.0, max_value=1.0, value = 0.1, help="This parameter represents the probability of indicating a defect during inspection when, in fact, it does not exist.")
        Epsilon=st.number_input("Insert the false-negative probability (\u03B5)", min_value = 0.0, max_value=1.0, value = 0.15, help="This parameter represents the probability of not indicating a defect during inspection when, in fact, it does exist.")
        Ci=st.number_input("Insert cost of inspection ()", min_value = 0.0, value = 0.05, help="This parameter represents the cost of conducing an inspection.")
        Cr=st.number_input("Insert cost of replacement (inspections and age-based) ()", min_value = 0.0, value = 1.0, help="This parameter represents the cost associated with preventive replacements, whether performed during inspections or when the age-based threshold is reached.")
        Cf=st.number_input("Insert cost of failure ()", min_value = 0.0, value = 10.0, help="This parameter represents the replacement cost incurred when a component fails.")
        Cd=st.number_input("Insert cost of defective by time unit ()", min_value = 0.0, value = 0.01, help="This parameter represents the unitary cost associated with the time in which the component stays in defective state for each time unit.")
        
        col1, col2 = st.columns(2)
        
        Delta=[0]
        st.subheader("Insert the variable values below:")
        K=int(st.text_input("Insert the number of inspections (K)", value=4))
        MinDelta=0.00
        if (K<=0):
            for i, col in enumerate(st.columns(K)):
                col.write(f"**{i+1}-th inspection:**")
                Delta.append(col.number_input("Insp. Mom. (Δ)", min_value=MinDelta, value=0.00, key=f"Delta_{i}"))
                MinDelta=Delta[-1]
        T = st.number_input("Insert the moment for the age-based preventive action (T)", min_value=Delta[-1], value= 12.0)
        
        st.subheader("Click on botton below to run this application:")    
        botao = st.button("Get cost-rate")
        if botao:
            st.write("---RESULT---")
            st.write(K,Delta,T)
            #st.write("Cost-rate", KD_KT(K, Delta, T))
         
    if choice == menu[1]:
        st.header(menu[1])
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>This app is dedicated to compute the cost rate for a hybrid aperiodic inspection and age-based maintenance policy. We assume a single system operating under Delay-Time Modeling (DTM) with a heterogeneous component lifetime, each having distinct defect arrival distributions. Component renovation occurs either after a failure (corrective maintenance) or during inspections, once a defect is detected or if the age-based threshold is reached (preventive maintenance). We considered false-positive and false-negative probabilities during the inspection.</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>The app computes the cost-rate for a specific solution—defined by the number of inspections (K), inspection intervals (Δ) and the age-based threshold (T).</h6>", unsafe_allow_html=True)
        st.write("<h6 style='text-align: justify; color: Blue Jay;'>For further questions or information on finding the optimal solution, please contact one of the email addresses below.</h6>", unsafe_allow_html=True)
        
        st.write('''

v.h.r.lima@random.org.br

r.g.n.paiva@random.org.br

a.j.s.rodrigues@random.org.br

h.s.j.gonzalez@random.org.br

c.a.v.cavalcante@random.org.br

''' .format(chr(948), chr(948), chr(948), chr(948), chr(948)))       
    if choice==menu[2]:
        st.header(menu[2])
        
        st.write('''The Research Group on Risk and Decision Analysis in Operations and Maintenance was created in 2012 
                 in order to bring together different researchers who work in the following areas: risk, maintenance a
                 nd operation modelling. Learn more about it through our website.''')
        st.markdown('[Click here to be redirected to our website](https://sites.ufpe.br/random/#page-top)',False)        
if st._is_running_with_streamlit:
    main()
else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())
