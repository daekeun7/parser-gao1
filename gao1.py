# -*- coding: utf-8 -*-
"""gao1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pjrjX9s7We7wD_8s7vqfFYlP6-ybut1B
"""

# !pip install googletrans==4.0.0-rc1
# !pip install beautifulsoup4

# # prompt: xml 페이지를 가져와서 파싱.
# # '<image>'안에 '<title>' 가져와서 프린트 해줘
# # '< lastBuildDate>'를 가져와서 프린트 해줘
# # '<item>' 별 '<title>', '<link>', '<description>'을 가져와서 프린트 해줘
# # '<title>'과 '<description>'은 영문으로 프린트 후 다음줄에 한글로 번역해서 프린트 해줘

# import requests
# from bs4 import BeautifulSoup
# from googletrans import Translator

# translator = Translator()

# def parse_xml_and_translate(url):
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for bad status codes

#         soup = BeautifulSoup(response.content, 'xml')

#         # Extract image title
#         image_title = soup.find('image').find('title').text
#         print("Image Title (Original):", image_title)

#         # Extract lastBuildDate
#         last_build_date = soup.find('lastBuildDate').text
#         print("\nLast Build Date:", last_build_date)


#         # Extract and translate item details
#         items = soup.find_all('item')
#         for item in items:
#             title = item.find('title').text
#             link = item.find('link').text
#             description = item.find('description').text

#             print("\nItem Title (Original):", title)
#             translated_title = translator.translate(title, dest='ko')
#             print("Item Title (Korean):", translated_title.text)

#             print("Item Link:", link)

#             print("\nItem Description (Original):", description)
#             translated_description = translator.translate(description, dest='ko')
#             print("Item Description (Korean):", translated_description.text)


#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred during the request: {e}")
#     except AttributeError as e:
#         print(f"An error occurred during parsing: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# # Example usage:
# xml_url = "https://www.gao.gov/rss/reports.xml" # paste your xml url
# parse_xml_and_translate(xml_url)

# prompt: xml 페이지를 가져와서 파싱. '<item>' 별 '<title>', '<link>', '<description>'을 가져와서 프린트 해줘
#  '<title>'과 '<description>'은 영문으로 프린트 후 다음줄에 한글로 번역해서 프린트 해줘

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

def translate_text(text, target_language='ko'):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

import streamlit as st

# Streamlit 앱 제목
st.title("GAO Parser")

# 텍스트 입력 필드 생성
url = st.text_input("Enter URL:", "")

if url:
    # 입력된 텍스트를 화면에 출력
    st.write("You entered:", url)
    
    # url = input("XML 페이지 URL을 입력하세요: ")  # 사용자로부터 URL 입력 받기
    print("-" * 20)

    
try:
    response = requests.get(url)
    response.raise_for_status()  # 오류 발생 시 예외 발생

    soup = BeautifulSoup(response.content, 'xml')

    items = soup.find_all('item')

    for item in items:
        title = item.find('title').text.strip()
        link = item.find('link').text.strip()
        description = item.find('description').text.strip()

        print(f"Title (English): {title}")
        print(f"Title (Korean): {translate_text(title)}")
        print(f"Link: {link}")
        print(f"Description (English): {description}")
        print(f"Description (Korean): {translate_text(description)}")
        print("-" * 20)

except requests.exceptions.RequestException as e:
    print(f"Error fetching the URL: {e}")
except AttributeError as e:
    print(f"Error parsing the XML: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
