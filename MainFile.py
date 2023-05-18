import numpy as np 
import pandas as pd 
import streamlit as st 
import re 
import openai
import os 

from pprint import pprint 


def clear_submit():
    st.session_state["submit"] = False



st.set_page_config(page_title="Address-GPT", page_icon="📖", layout="wide")
st.header("📖AddressGPT")

# sidebar()

# text_input = st.text_input(
#         "Enter the raw address here 👇",
#         label_visibility=st.session_state.visibility,
#         disabled=st.session_state.disabled,
#         placeholder=st.session_state.placeholder,

Address_given = st.text_input('Enter the address here...', 'e.g., A7-103 elita promenade J.P. nagar 7th phase A7-103 elita promenade J.P. nagar 7th phase bangalore 560078')
# st.write('The given raw address is', Address_given)


API_key = st.text_input('Enter your API Key here...')
# Set up the OpenAI API client
openai.api_key = API_key  #os.environ["OPENAI_API_KEY"]

# Define the prompt for the chatbot
# Address_given = "RING MARATHAHALLI NEAR KLM FASHION MALL 96 OUTTER  /VARTHUR ROAD OUTTER"# 
#prompt = "Given the following address, please add commas in the appropriate places: Address: A7-103 elita promenade J.P. nagar 7th phase A7-103 elita promenade J.P. nagar 7th phase bangalore 560078 " # No 77 Ramachandrappa Building 5th B Cross Near Mandha Bangalore North Peenya Small Industries Bangalore Ba"

prompt = "Given the following address add commas:Address: "+Address_given #RING MARATHAHALLI NEAR KLM FASHION MALL 96 OUTTER  /VARTHUR ROAD OUTTER" #and then parse this Indian address and label with appropriate tokens
#98 1st Floor 9th A Cross 3rd Main Road\n#98 1st Floor 9th A Cross 3rd Main Road\nPrasanthanagar\nPrasanthanagar 560078" # + Address  #No 77 Ramachandrappa Building 5th B Cross Near Mandha Bangalore North Peenya Small Industries Bangalore Ba" A7-103 elita promenade Apartments J.P. nagar 7th phase bangalore 560078


# Generate a response from the chatbot
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Print the response from the chatbot
# print(response.choices[0].text.strip())

AddressWithCommas = response.choices[0].text.strip()


prompt = "Given the following Indian address parse it:Address: "+AddressWithCommas

# Generate a response from the chatbot
response2 = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Print the response from the chatbot
# print(response.choices[0].text.strip())

Address_Parsed = response2.choices[0].text.strip()

address_lines = Address_Parsed.split('\n')

address_dict = {}
for line in address_lines:
    if ':' in line:
        key, value = line.split(':')
        address_dict[key.strip()] = value.strip()

print(address_dict)


col1, col2 = st.columns(2)

col1.subheader("Address with Commas:")
col1.write(AddressWithCommas)


col2.subheader("Parsed Address with tokens")

if address_dict.__len__()==0: 
	st.write("Cant Parse the address")
else: 
	for keys, values in address_dict.items():
		if keys == 'Parsed Address': 
			continue 
		else: 
			col2.write(keys)
			col2.write(values)

# st.write('Address with Commas inserted is:', AddressWithCommas)
# st.write('Parsed Address is :', Address_Parsed)
