# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
    """choose the fruits you want in your custom Smoothie!
    """
)
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your smoothie wil be:", name_on_order)

cnx=st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)


ingredients_list = st.multiselect(
    "choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    #st.write(ingredients_string)
     
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                values ('""" + ingredients_string + """','""" +name_on_order+ """')"""
    
    st.write(my_insert_stmt)
    
    if ingredients_string:
        session.sql(my_insert_stmt).collect()
        #st.success('Your Smoothie is ordered!', icon="✅")
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your smoothie is ordered!', icon="✅")
       st.write(f"✅ Your smoothie is ordered, {name_on_order}!")

import requests

# Attempt to fetch data from the API
try:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
    
    # Check if the request was successful
    if fruityvice_response.status_code == 200:
        st.text(fruityvice_response.json())  # Display the JSON data if successful
    else:
        st.text(f"Error: Received a {fruityvice_response.status_code} status code.")
        st.text(f"Response: {fruityvice_response.text}")

except requests.exceptions.RequestException as e:
    # Handle any network errors
    st.text(f"Request failed: {e}")
