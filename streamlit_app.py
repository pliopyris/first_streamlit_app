import streamlit as st
import pandas
import requests

st.title('My parents new healthy diner')

st.header('Breakfast Menu')
st.text('🥣 Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Lime'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# st.dataframe(my_fruit_list)
st.dataframe(fruits_to_show)

# Display FruityVice API response
st.header('Fruityvice Fruit Advice')

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text(fruityvice_response.json())

# normalize api response (json) and pass it to a df
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
st.dataframe(fruityvice_normalized)

