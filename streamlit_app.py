import streamlit as st
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

try:
  # user choice
  fruit_choice = st.text_input('What fruit would you like information about?')
  # st.write('The user entered ', fruit_choice)
  
  if not fruit_choice:
    st.error('Please select a fruit to get information.')
  else:
    # fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # st.text(fruityvice_response.json())
    # normalize api response (json) and pass it to a df
    # fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    back_from_func = get_fruityvice_data(fruit_choice)
    st.dataframe(back_from_func)
except URLError as e:
    st.error()

# break
# st.stop()

# my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
# my_data_rows = my_cur.fetchall()

st.header("Fruit Load List contains:")
# st.dataframe(my_data_rows)

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
    return my_cur.fetchall()

if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)

# st.stop()

# add choice
# add_my_fruit = st.text_input('What fruit would you like to add?', 'Kiwi')
# st.write('Thanks for adding ', add_my_fruit)

# # my_cur.execute("insert into fruit_load_list values ('from streamlit')")

def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
    return 'Thanks for adding ' + new_fruit

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_func = insert_row_snowflake(add_my_fruit)
  st.text(back_from_func)

