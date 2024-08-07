# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
# from snowflake.snowpark.context import get_active_session



# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want in your custom smoothie"
)

name_on_order = st.text_input("Name of smoothie")
st.write("The name of your smoothie will be", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
st.text('fruityvice_response')

if ingredients_list:

    ingredients_string = ''

    for ingredient_choosen in ingredients_list:
        ingredients_string += ingredient_choosen + ' '

    # st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    # st.write(my_insert_stmt)

    time_to_insert = st.button('Submit order')

    if time_to_insert:
    
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
