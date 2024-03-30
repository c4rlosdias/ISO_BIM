
import pandas as pd
import streamlit as st
from PIL import Image
import urllib.request
import plotly.express as px


# =========================================================================================================================
# page config
# =========================================================================================================================

im = Image.open('./img/Logo_ABNT.jpg')
st.set_page_config(
    page_title="ISO BIM",
    page_icon=im,
    layout="wide",
    initial_sidebar_state="expanded",
)

def monta_df():
    df = pd.read_excel('iso.xlsx', sheet_name='normas', dtype=str)

    return df

def monta_df_2():
    page = urllib.request.urlopen("https://www.iso.org/committee/49180/x/catalogue/p/1/u/0/w/0/d/0")
    text = page.read().decode("utf8")

    refnorma_start = 'href="/standard/'
    refnorma_end = 'title>'
    refname_start = 'entry-name'
    refname_end = 'span'
    refdescription_start = 'entry-description'
    refdescription_end = 'div'
    refstage_start = '</a>'
 
    l_name = []
    l_title = []
    l_stage = []
    l_ics = []
    l_html = []

    startfrom = 1
    while startfrom > 0:
        # procura proxima norma
        where = text.find(refnorma_start,startfrom)
        if where > -1:
            print(".found in pos: "+str(where))
        else:
            break
        input('sss')
        # procura nome da proxima norma para busca via html
        startfrom = where
        where = text.find(refnorma_end,startfrom)
        norm_html = text[startfrom:where]
        l_html.append(norm_html)
        print(norm_html)

        # procura o nome da norma
        startfrom = where + 1
        where = text.find(refname_start,startfrom)
        startfrom = where + len(refname_start) + 2
        where = text.find(refname_end,startfrom)
        name = text[startfrom:where-2]
        l_name.append(name)
        print(name)

        # procura a descricao da norma
        startfrom = where+1
        where = text.find(refdescription_start,startfrom)
        startfrom = where + len(refdescription_start) + 2
        where = text.find(refdescription_end,startfrom)
        description = text[startfrom:where-2]
        l_name.append(description)   
        startfrom = where

        # procura a estagio da norma
        startfrom = where+1
        where = text.find(refstage_start,startfrom)
        startfrom = where - 5
        where = text.find(refstage_start,startfrom)
        stage = text[startfrom:where-1]
        l_name.append(stage)   

        # procura o ics da norma
        startfrom = where+1
        where = text.find(refstage_start,startfrom)
        startfrom = where - 10
        where = text.find(refstage_start,startfrom)
        ics = text[startfrom:where-1]
        l_name.append(ics)  
        startfrom = where+1
    
    normas = {
        'Nome' : l_name,
        'Decrição' : l_title,
        'Estágio' : l_stage,
        'ICS' : l_ics,
        'link' : l_html
    }
    
    df = pd.DataFrame(normas)
    return df

# =========================================================================================================================
# System vars
# =========================================================================================================================



# =========================================================================================================================
# main
# =========================================================================================================================

with st.container():
    
    st.image(im, width=100)
    st.header('Normas da ISO/TC 59/SC 13 - Organization and digitization of information about buildings and civil engineering works, including building information modelling (BIM)')
    st.write('')    
    stage = st.radio('Estágio da norma:', ['Todas', 'Propostas', 'Estágio preparatório','No comitê', 'Em consulta', 'Em fase de aprovação','Publicada', 'Em revisão'], horizontal=True)
    dfi = monta_df()
    st.write('') 

    if stage == 'Todas':
        op = ['10.00', '10.20', '10.60', '10.92', '10.93', '10.98', '10.99',
              '20.00', '20.20', '20.60', '20.92', '20.93', '20.98', '20.99',
              '30.00', '30.20', '30.60', '30.92', '30.93', '30.98', '30.99',
              '40.00', '40.20', '40.60', '40.92', '40.93', '40.98', '40.99',
              '50.00', '50.20', '50.60', '50.92', '50.93', '50.98', '50.99',
              '60.00', '60.20', '60.60', '60.92', '60.93', '60.98', '60.99',
              '90.00', '90.20', '90.60', '90.92', '90.93', '90.98', '90.99']
    elif stage == 'Propostas':
        op = ['10.00', '10.20', '10.60', '10.92', '10.93', '10.98', '10.99']
    
    elif stage == 'Estágio preparatório':
        op = ['20.00', '20.20', '20.60', '20.92', '20.93', '20.98', '20.99']
    
    elif stage == 'No comitê':
        op = ['30.00', '30.20', '30.60', '30.92', '30.93', '30.98', '30.99']
    
    elif stage == 'Em consulta':
        op = ['40.00', '40.20', '40.60', '40.92', '40.93', '40.98', '40.99']
    
    elif stage == 'Em fase de aprovação':
        op = ['50.00', '50.20', '50.60', '50.92', '50.93', '50.98', '50.99']
    
    elif stage == 'Publicada':
        op = ['60.00', '60.20', '60.60', '60.92', '60.93', '60.98', '60.99']

    elif stage == 'Em revisão':
        op = ['90.00', '90.20', '90.60', '90.92', '90.93', '90.98', '90.99']

    df = dfi[dfi['ESTÁGIO'].isin(op)]
    st.dataframe(data=df, use_container_width=True, hide_index=True, ) 
    st.divider()
    st.write('Normas por estágio')
    fig = px.pie(df, names='ESTÁGIO', )
    st.plotly_chart(fig, use_container_width=True)





    

