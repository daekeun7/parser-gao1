# -*- coding: utf-8 -*-
"""gao1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pjrjX9s7We7wD_8s7vqfFYlP6-ybut1B
"""

import requests
import streamlit as st
from bs4 import BeautifulSoup
from googletrans import Translator

def translate_text(text, target_language='ko'):
    translator = Translator()
    # Split the text into chunks (adjust chunk size as needed)
    chunk_size = 4000  # Example chunk size
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []
    for chunk in chunks:
        translation = translator.translate(chunk, dest=target_language)
        translated_chunks.append(translation.text)
    return ''.join(translated_chunks)

# Streamlit 앱 제목
st.title("Parser")
st.markdown("<h2 style='font-size: 20px;'>Powered by Goo Kim @ Digital Audit Research Team</h2>", unsafe_allow_html=True)

tab1, tab2= st.tabs(['GAO' , 'NAO'])

with tab1:
    # 콤보박스 옵션 목록
    # options = ['https://www.gao.gov/rss/reports.xml', 'https://www.gao.gov/rss/reports-450.xml', 'https://www.gao.gov/rss/reports_majrule.xml']
    # options = ['GAO Reports', 'GAO Reports-Brief', 'GAO Legal Products', 'GAO Legal Products-Reports on Federal Agency Major Rules']
    options = {
        'GAO Reports': 'https://www.gao.gov/rss/reports.xml',
        'GAO Reports-Brief': 'https://www.gao.gov/rss/reports-450.xml',
        'GAO Legal Products': 'https://www.gao.gov/rss/reportslegal.xml',
        'GAO Legal Products-Reports on Federal Agency Major Rules': 'https://www.gao.gov/rss/reports_majrule.xml'
    }
    
    # 콤보박스 생성
    selected_option = st.selectbox("Select Feed:", list(options.keys()))
    url = options[selected_option]    
    
    if st.button("Submit"):    
        if url:            
            st.write("Selected feed : ", selected_option)
            # st.write("LastBuildDate : ", lastBuildDate)
            # st.write("Feed URL : ", url)                       
            # st.write("-" * 20)
            
            try:
                response = requests.get(url)
                response.raise_for_status()  # 오류 발생 시 예외 발생
            
                soup = BeautifulSoup(response.content, 'xml')            
                items = soup.find_all('item')

                for item in items:
                    lastBuildDate = item.find('lastBuildDate').text.strip()
                    st.write("LastBuildDate : ", lastBuildDate)
                st.write("Feed URL : ", url)                       
                st.write("-" * 20)
            
                for item in items:
                    title = item.find('title').text.strip()
                    link = item.find('link').text.strip()
                    description = item.find('description').text.strip()
    
                    # Replace tabs with spaces in the description
                    description = description.replace('\t', ' ')
            
                    st.write(f"[원문링크] {link}")
                    st.write(f"- Title (English) : {title}")
                    st.write(f"- 제목 (한국어) : {translate_text(title)}")                    
                    st.write(f"- Description (English) :")
                    st.write(f"{description}")
                    st.write(f"- 설명 (한국어) :")
                    st.write(f"{translate_text(description)}")
                    st.write("-" * 20)
            
            except requests.exceptions.RequestException as e:
                st.write(f"Error fetching the URL: {e}")
            except AttributeError as e:
                st.write(f"Error parsing the XML: {e}")
            except Exception as e:
                st.write(f"An unexpected error occurred: {e}")
    
        st.write("done")
with tab2:
    st.write("Under construction")

