# -*- coding: utf-8 -*-
"""gao1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pjrjX9s7We7wD_8s7vqfFYlP6-ybut1B
"""

import requests
import streamlit as st
import streamlit as st2
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

def extract_article_links(url):    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')  # Find all article elements
        article_data = []
        for article in articles:
          links = article.find_all('a', href=True)
          for link in links:
            article_data.append({
              'text': link.text.strip(),
              'href': link['href']
            })
        return article_data

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching URL: {e}")
        return []

def extract_article_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1', class_='banner__title')
        caption = soup.find('div', class_='banner__caption')
        published_time = soup.find('time', class_='published')
        content_div = soup.find('div', class_='content-col article__main-content')

        if content_div:
          content = content_div.get_text(separator=' ', strip=True)

          # 5. "Downloads", "Video summary" 삭제
          content = content.split("Downloads")[0] if "Downloads" in content else content
          content = content.split("Video summary")[0] if "Video summary" in content else content

          # 6. "Jump to downloads" 삭제
          content = content.replace("Jump to downloads", "")

          # 7. 특정 문자열 교체
          content = content.replace("Background to the report", "\n-' Background to the report : ")
          content = content.replace("Scope of the report", "\n-' Scope of the report : ")
          content = content.replace("Conclusions", "\n-' Conclusions : ")
        else:
          content = None

        return {
            'title': title.text.strip() if title else None,
            'caption': caption.text.strip() if caption else None,
            'published_time': published_time.text.strip() if published_time else None,
            'content': content
            }

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching URL: {e}")
        return None
    except AttributeError as e:
      st.write(f"Error parsing HTML: {e}")
      return None
###########################################################################
# Streamlit 앱 제목
st.title("Parser")
st.markdown("<h2 style='font-size: 20px;'>Powered by Goo Kim @ Digital Audit Research Team</h2>", unsafe_allow_html=True)

tab1, tab2= st.tabs(['Government Accountability Office' , 'National Audit Office'])

with tab1:
    # 콤보박스 옵션 목록    
    options = {
        'GAO Reports': 'https://www.gao.gov/rss/reports.xml',
        'GAO Reports-Brief': 'https://www.gao.gov/rss/reports-450.xml',
        'GAO Legal Products': 'https://www.gao.gov/rss/reportslegal.xml',
        'GAO Legal Products-Reports on Federal Agency Major Rules': 'https://www.gao.gov/rss/reports_majrule.xml',
        'GAO Press Releases': 'https://www.gao.gov/rss/press.xml'
    }
    
    # 콤보박스 생성
    selected_option = st.selectbox("Select Feed :", list(options.keys()))
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

                channels = soup.find_all('channel')                                
                for channel in channels:
                    lastBuildDate = channel.find('lastBuildDate').text.strip()
                    st.write("Last build date : ", lastBuildDate)
                    
                st.write("Feed URL : ", url)                       
                st.write("-" * 20)               
                           
                items = soup.find_all('item')            
                for item in items:
                    title = item.find('title').text.strip()
                    link = item.find('link').text.strip()
                    description = item.find('description').text.strip()
    
                    # Replace tabs with spaces in the description
                    description = description.replace('\t', ' ')
            
                    st.write(f"[원문링크] {link}")
                    st.write(f"- Title (English)")
                    st.write(f"{title}")
                    st.write(f"- 제목 (한국어)")
                    st.write(f"{translate_text(title)}")
                    st.write(f"- Description (English)")
                    st.write(f"{description}")
                    st.write(f"- 설명 (한국어)")
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
    # 콤보박스 옵션 목록    
    options2 = {
        'Selected filters : Reports': 'https://www.nao.org.uk/?post_type=report&s='       
    }
    
    # 콤보박스 생성
    selected_option2 = st2.selectbox("Select :", list(options2.keys()))
    url2 = options2[selected_option2] 

    if st2.button("Submit2"):    
        if url2:            
            st.write("Selected filter : ", selected_option2)
            st.write("URL : ", url2)                       
            st.write("-" * 20)
    
            if __name__ == "__main__":
                target_url = url2 # Replace with the actual URL
                translator = Translator()
            
                article_links = extract_article_links(target_url)
                for article in article_links:
                  # st.write(f"Article Text: {article['text']}")
                  st.write(f"[원문링크] {article['href']}")
            
                  article_content = extract_article_content(article['href'])
                  if article_content:
                      title_translation = translator.translate(article_content['title'], dest='ko')
                      content_translation = translator.translate(article_content['content'], dest='ko')
            
                      st.write(f"- Title(English)")
                      st.write(f"{article_content['title']}")
                      st.write(f"- 제목(한국어)")
                      st.write(f"{title_translation.text}")                      
                      st.write(f"- Caption : {article_content['caption']}")                      
                      st.write(f"- Published Time : {article_content['published_time']}")
                      st.write(f"- Content(English)")
                      st.write(f"{article_content['content']}")
                      st.write(f"- 내용(한국어)")
                      st.write(f"{content_translation.text}")
                      st.write("-" * 20)
        
        st.write("done")
