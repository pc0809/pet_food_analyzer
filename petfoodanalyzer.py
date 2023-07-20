from st_aggrid import AgGrid, ColumnsAutoSizeMode, GridOptionsBuilder
from IPython.display import HTML, display
from fractions import Fraction
import re
import ingredient_analyzer_dictionaries
import ingredient_analyzer_utils
from ingredient_analyzer_utils import *
from ingredient_analyzer_dictionaries import *
import dog_food_analyzer_dictionaries
import dog_food_analyzer_utils
from dog_food_analyzer_utils import *
from dog_food_analyzer_dictionaries import *
import numpy as np
import pandas as pd
import plotly
import st_aggrid
import streamlit as st
import streamlit.components.v1 as components
from IPython.core.display import HTML
from PIL import Image
from plotly import *
from st_aggrid import *

# HTML("<style>.rendered_html th {max-width: 10.9em;}</style>")


# show screen in wide mode while launching the app
st.set_page_config(layout="wide")

# styling with css for margin and padding
st.markdown("""
        <style>
               .css-18e3th9 {
                    padding-top: 1rem;
                    padding-bottom: 1rem;
                    padding-left: 1rem;
                    padding-right: 1rem;
                }
        </style>
        """, unsafe_allow_html=True)

# defining a function to read data in minimum time
@st.cache(allow_output_mutation=True)
def data_read(file):
    return pd.read_csv(file, sep='|', encoding='utf-8')


main_data = data_read(
    "data_for_streamlit_reduced_20_07_23.csv")


tabs = ['Ingredient Analyzer', 'Environment Impact',
        'Pet Information', 'Preferences', 'Best Products']
whitespace = 23
ingredient_analyzer, environment_impact, pet_information, preferences, best_products = st.tabs(
    [s.center(whitespace, "\u2001") for s in tabs])



with ingredient_analyzer:

    space, diet_category_col, space_1, ingredient_col, space_2 = st.columns([0.2, 1, 0.1, 3, 0.2])
    
    with diet_category_col:
        st.markdown('#### Select Food Category:')
        diet_category = st.radio('Selected Category:', [
                                'Dry', 'Wet'], label_visibility='collapsed', horizontal=True)
    
    
    with ingredient_col:
        st.markdown('#### Enter Ingredient List:')
        ing_str = st.text_area('Enter Ingredient List:', height= 220,  label_visibility = 'collapsed', key='ia') 
        
        if ing_str == '':
            st.error('Please enter the ingredient list.')
            ing_str ='.'
            
            
        ing_result = preprocess_ingredients(ing_str)
        # st.write(ing_result)
        
        
    with diet_category_col:
    
        if len(ing_result) != 0:
            
            st.markdown('#### Select Category:')
            selected_p_c = st.radio('Selected Category:', ing_result.keys(), label_visibility = 'collapsed')
            
                
    with ingredient_col:
    
        if len(ing_result) != 0:
        
            if list(ing_result[selected_p_c].values())[0] != '':
                st.markdown('#### Selected category definition:')
                st.markdown(f"###### {list(ing_result[selected_p_c].values())[0]}")
                
            st.markdown('#### Ingredients from selected categories:')
            
            if list(ing_result[selected_p_c].keys())[0] != 'Description':
                st.write(', '.join(list(ing_result[selected_p_c].values())))
            else:
                st.write(', '.join(list(ing_result[selected_p_c].values())[1:]))
                

with environment_impact:
    
    space_1, ingredient_text_col, space_2, ingredients_res_col = st.columns([0.1, 1, 0.1, 0.6])
    
    with ingredient_text_col:
        
        st.markdown('#### Enter Ingredient List:')
        ing_str_2 = st.text_area('Enter Ingredient List:', height= 220,  label_visibility = 'collapsed', key ='dfa') 
        
    with ingredients_res_col:
        
        dfa_result_1 = co2_emissions_from_ingredients(ing_str_2, diet_category)
        
        if len(dfa_result_1) > 1:
            
            st.markdown('#### Major Emitters:')
            st.markdown(f"###### {', '.join(dfa_result_1['highlighting_ingredients'])}")
            
    with ingredient_text_col:
        
        st.markdown('#### Environmental Impact:')
        
        progress_bar = st.progress(0.0)
        
        if len(dfa_result_1) > 1:
        
            for i in range(threshold_of_ingredient_dict[diet_category][1]):
                
                progress_bar.progress(dfa_result_1['co2_emission_from_ingredients_per_day'] /threshold_of_ingredient_dict[diet_category][1])
                
            st.markdown(f"###### This is equivalant to {dfa_result_1['miles']} miles driven by an average gasoline passenger vehicle\n")
            
    with ingredients_res_col:
        
        if len(dfa_result_1) > 1:
            st.markdown('#### CO2 emission in kg:')   
            st.markdown(f"###### Daily threshold: {threshold_of_ingredient_dict[diet_category][1]} kg")
            st.markdown(f"###### Daily emision: {dfa_result_1['co2_emission_from_ingredients_per_day']} kg")
            st.markdown(f"###### Yearly emission: {dfa_result_1['co2_emission_from_ingredients_per_year']} kg\n")
        
        
with pet_information:
    
    
    space_1, head_1 ,space_2, head_2, \
                    head_3 ,space_3 = st.columns([0.2, 3,0.2,  1.3, 1.3, 0.2])
    
    with head_1:
        
        st.markdown('#### Enter you pet\'s details:')
        
    with head_2:
        
        st.markdown(f'#### Pet\'s Profile:')
        
    with head_3:
        
        st.markdown(f'#### Requirements:')
        
    with space_3:
        
        bool_a = st.button('i')
        
     
    
    space_1, first_info_col, second_info_col ,space_2, profile_col_1, profile_col_2, \
                    requirement_col_1, requirement_col_2 ,space_3 = st.columns([0.2, 1.5, 1.5,0.2,  0.6, 0.7, 0.6, 0.7, 0.2])
        
    with first_info_col:
        
        st.markdown("<p style='font-size:0.9em;'>What is the name of your pet?</p>", unsafe_allow_html=True)
        name = st.text_input('What is the name of your pet?', value = 'Pet' , label_visibility = 'collapsed')
        name = name.capitalize()
    
        # gender
        st.markdown(f"<p style='font-size:0.9em;'>What is {name}'s gender?</p>", unsafe_allow_html=True)
        gender = st.radio(f"What is {name}'s gender?",('Male', 'Female'),  horizontal = True , label_visibility = 'collapsed')

        # species
        st.markdown(f"<p style='font-size:0.9em;'>Is it a dog or a cat?</p>", unsafe_allow_html=True)
        species = st.radio(f"He is a", ('Cat', 'Dog'), horizontal = True , label_visibility = 'collapsed')
        
        # breed (if species is dog)
        if species == 'Dog':
            st.markdown(f"<p style='font-size:0.9em;'>What breed is your dog?</p>",
                            unsafe_allow_html=True)

            breed=st.selectbox("Select your dog's breed", list(dog_breed_lifespan.keys()),
                            label_visibility = 'collapsed')    
            
                        
        years_months = '00/00'
        
        # age of pet
        st.markdown(f"<p style='font-size:0.9em;'>Tell us {name}'s age in YY/MM format:</p>", unsafe_allow_html=True)
        years_months = st.text_input(' ', label_visibility = 'collapsed', placeholder = 'YY/MM', max_chars  = 5)
        
        # converting age of pet in months and years
        
        pattern = re.compile(r"^[0-9][0-9]\/[0-1][0-9]$")
            
        # if age is entered properly
        if pattern.match(years_months) != None and years_months.split("/")[1] < "12" and years_months != '00/00':

            years = int(years_months.split("/")[0])
            months = int(years_months.split("/")[1])

            age_in_months = (int(years)*12) + int(months)

        # if age is not written in proper format
        else:
            years = 0
            months = 0
            age_in_months = 0
            
            # shows error
            st.error("Enter valid age!")
            
    
    with second_info_col:
        
        # default lifestage and condition
        lifestage = 'Adult'
        condition = 'Intact'
        
        # if species is cat
        if species == 'Cat':

            if  age_in_months <= 12:
                
                # lifestage
                lifestage = 'Kitten'
                # condition
                condition = 'Kitten'

            elif 12 < age_in_months < 120:
                
                # lifestage
                lifestage = 'Adult'
                if gender == 'Male':
                    st.markdown(f"<p style='font-size:0.9em;'>He is:</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='font-size:0.9em;'>She is:</p>", unsafe_allow_html=True)

                # condition
                condition = st.selectbox(' ', ('Intact', 'Neutered', 'Obese Prone') , label_visibility = 'collapsed')

            elif age_in_months >= 120:

                # lifestage
                lifestage = 'Senior'
                # condition
                condition = 'Senior'
                
        
        # if species is dog:
        elif species == 'Dog':
            
            # dog's breed lifespan
            lifespan = int(dog_breed_lifespan[breed])

            if 0 < age_in_months < 9:

                # lifestage
                lifestage = 'Puppy'
                # condition
                condition = 'Puppy'

            elif 9 < age_in_months < (0.75 * lifespan)*12:

                # lifestage
                lifestage = 'Adult'

                if gender == 'Male':
                    st.markdown(f"<p style='font-size:0.9em;'>He is:</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='font-size:0.9em;'>She is:</p>", unsafe_allow_html=True)

                # condition
                condition = st.selectbox(' ', ('Intact', 'Neutered', 'Obese Prone') , label_visibility = 'collapsed')

            elif age_in_months >= (0.75 * lifespan)*12:

                # lifestage
                lifestage = 'Senior'
                # condition
                condition = 'Senior'
        
        # weight of the pet
        if gender == 'Male':

            st.markdown("<p style='font-size:0.9em;'>How much does he weigh (in kg)?</p>", unsafe_allow_html=True)

            weight = st.number_input(label = 'Weight?',
                                step=1, min_value = 0, label_visibility = 'collapsed')

        elif gender == 'Female':

            st.markdown("<p style='font-size:0.9em;'>How much does she weigh (in kg)?</p>", unsafe_allow_html=True)

            weight = st.number_input(label = 'Weight?',
                                step=1, min_value =0, label_visibility = 'collapsed')
            

        main_data=main_data[main_data['Category'].str.contains(species)]
        
        # st.write(main_data['Health_Segment'].unique())
        dic = {'Dental Health': ['Dental & Breath Care', 'Dental Care'],
                'Diabetes or other such issues': ['Diabetic Support', 'Low Glycemic'],
                'Digestion': ['Digestive Health', 'Sensitive Digestion'],
                'Hairballs': ['Hairball Control'],
                'Heart and Liver': ['Heart & Liver Care'],
                'Hip and Joint': ['Hip & Joint Support'],
                'Kidneys': ['Kidney Care'],
                'Skin and Coat': ['Skin & Coat Health'],
                'Urinary Tract Health': ['Urinary Tract Health'],
                'None of the above': None}
        
        
        # data grouped by health conditions
        health_segments_grouped = main_data.groupby(['Health_Condition'], as_index=False).agg({'Product':'nunique'})
        health_segments_grouped_filtered = health_segments_grouped[health_segments_grouped['Product']>1]
        # list of health conditions
        health_segments_filtered_list=health_segments_grouped_filtered['Health_Condition'].unique().tolist()
        # converting the above defined dictionary into exploded dataframe
        hc_exploded=pd.DataFrame(dic.items(),columns=['Selected_Segment',
                                                      'Actual_Segment']).explode('Actual_Segment')
        # finding common segments from dictionary and main data
        hc_list_of_segments=list(hc_exploded[hc_exploded['Actual_Segment'].isin(health_segments_filtered_list)]['Selected_Segment'].unique())
        hc_list_of_segments.extend(['None of the above'])
        
        # health segment
        st.markdown(f"<p style='font-size:0.9em;'>Does {name} have health problems related to any of these?</p>", unsafe_allow_html=True)
        hc = st.radio("Select Health Condition", hc_list_of_segments, label_visibility = 'collapsed')
        
    # calculations of kcal, fat and protien 
    rer = 70 * (weight ** 0.75)
    bw = weight ** 0.75
    
    # for kitten
    if lifestage == 'Kitten':
        kcal_per_day = 2.5 * rer
        protein_per_day = (45/1000)*kcal_per_day
        fat_per_day = (22.5/1000)*kcal_per_day

    # for puppy
    elif lifestage == 'Puppy':

        if age_in_months <= 4:
            kcal_per_day = 3 * rer
            protein_per_day = (45/1000)*kcal_per_day
            fat_per_day = (kcal_per_day*21.3)/1000

        elif age_in_months > 4:
            kcal_per_day = 2 * rer
            protein_per_day = (35/1000)*kcal_per_day
            fat_per_day = (kcal_per_day*21.3)/1000

    # for senior cat
    elif lifestage == 'Senior' and species == 'Cat':
        kcal_per_day = 1 * rer
        protein_per_day = (40/1000)*kcal_per_day
        fat_per_day = (22.5/1000)*kcal_per_day

    # for senior dog
    elif lifestage == 'Senior' and species == 'Dog':
        kcal_per_day = 0.8 * rer
        protein_per_day = (20/1000)*kcal_per_day
        fat_per_day = (10/1000)*kcal_per_day
        
    # for adult cat
    elif lifestage == 'Adult' and species == 'Cat':

        if condition == 'Intact':
            kcal_per_day = 1.4 * rer
            protein_per_day = (40/1000)*kcal_per_day
            fat_per_day = (22.5/1000)*kcal_per_day
        elif condition == 'Neutered':
            kcal_per_day = 1.2 * rer
            protein_per_day = (40/1000)*kcal_per_day
            fat_per_day = (22.5/1000)*kcal_per_day
        elif condition == 'Obese Prone':
            kcal_per_day = rer
            protein_per_day = (40/1000)*kcal_per_day
            fat_per_day = (22.5/1000)*kcal_per_day

    # for adult dog
    elif lifestage == 'Adult' and species == 'Dog':

        if condition == 'Intact':
            kcal_per_day = 1.8 * rer
            protein_per_day = (20/1000)*kcal_per_day
            fat_per_day = (10/1000)*kcal_per_day
        elif condition == 'Neutered':
            kcal_per_day = 1.6 * rer
            protein_per_day = (20/1000)*kcal_per_day
            fat_per_day = (10/1000)*kcal_per_day
        elif condition == 'Obese Prone':
            kcal_per_day = 1.4 * rer
            protein_per_day = (20/1000)*kcal_per_day
            fat_per_day = (10/1000)*kcal_per_day

    with profile_col_1:
        
        # markdowns for details
        if weight != 0 and 0 <= int(months) < 13 and int(years) >= 0 and age_in_months != 0:

            st.markdown(f'###### Name:')
            st.markdown(f'###### Species:')
            st.markdown(f'###### Gender:')
            st.markdown(f'###### Age:')
            st.markdown(f'###### Lifestage:')
            if lifestage == 'Adult':
                st.markdown(f'###### Condition:')
            st.markdown(f'###### Weight:')
            st.markdown(f'###### Health Issue:')

        else:
            st.markdown('')
            
            
    with profile_col_2:
        
        # pets' details
        if weight != 0 and 0 <= int(months) < 13 and int(years) >= 0 and age_in_months != 0:

            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {name}</p>', unsafe_allow_html=True)
            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {species}</p>', unsafe_allow_html=True)
            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {gender}</p>', unsafe_allow_html=True)
            
            if years == '00':
                st.markdown(f'###### <p style="color:#fe9a0a; display:inline;">{int(months)} months</p>', unsafe_allow_html=True)
            elif months == '00':
                st.markdown(f'###### <p style="color:#fe9a0a; display:inline;">{int(years)} years</p>', unsafe_allow_html=True)
            else:
                st.markdown(f'###### <p style="color:#fe9a0a; display:inline;">{int(years)} years {int(months)} months</p>', unsafe_allow_html=True)
            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {lifestage}</p>', unsafe_allow_html=True)
            if lifestage == 'Adult':
                st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {condition}</p>', unsafe_allow_html=True)
            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {weight} kg</p>', unsafe_allow_html=True)
            st.markdown(f'###### <p style="color:#fe9a0a; display:inline;"> {hc}</p>', unsafe_allow_html=True)

        else:
            st.markdown('')             
            
    with requirement_col_1:
        
        # markdowns for requirements text
        st.markdown(f'###### <i>Energy (MER)*:</i>',
                unsafe_allow_html=True)
        st.markdown(f'###### <i>Fat:</i>',
                unsafe_allow_html=True)
        st.markdown(f'###### <i>Fat (oz):</i>',
                unsafe_allow_html=True)
        st.markdown(f'###### <i>Protein:</i>',
                unsafe_allow_html=True)
        st.markdown(f'###### <i>Protein (oz):</i>',
                unsafe_allow_html=True)
        
    with requirement_col_2:

        # requirements of pets
        
        fat_per_day_in_oz = round(0.0352 * fat_per_day, 2)
        protein_per_day_in_oz = round(0.0352 * protein_per_day, 2)
        st.markdown(f'###### <p style="color:#00aaff; display:inline;"><i><b>{str(round(kcal_per_day,0))}</b> kcal/day</i></p>', unsafe_allow_html=True)
        st.markdown(f'###### <p style="color:#00aaff; display:inline;"><i><b>{str(round(fat_per_day,0))}</b> g/day</i></p>', unsafe_allow_html=True)
        st.markdown(f'###### <p style="color:#00aaff; display:inline;"><i><b>{str(round(fat_per_day_in_oz,2))}</b> oz/day</i></p>', unsafe_allow_html=True)
        st.markdown(f'###### <p style="color:#00aaff; display:inline;"><i><b>{str(round(protein_per_day,0))}</b> g/day</i></p>', unsafe_allow_html=True)
        st.markdown(f'###### <p style="color:#00aaff; display:inline;"><i><b>{str(round(protein_per_day_in_oz,2))}</b> oz/day</i></p>', unsafe_allow_html=True)
        

    
if bool_a == True:
    # additional information
    st.markdown(f'<p style="display:inline; color:grey; font-size:0.9em;"><i>The above calculations are based on NRC guidelines for \
        nutritional requirements of dogs and cats. For more information please refer to these sources:<br>\
    1. <a href = "https://www.merckvetmanual.com/management-and-nutrition/nutrition-small-animals/nutritional-requirements-and-related-diseases-of-small-animals">Daily Maintenance Energy Requirements for Dogs and Cats</a><br>\
    2. <a href = "https://www.aaha.org/globalassets/02-guidelines/2021-nutrition-and-weight-management/resourcepdfs/new-2021-aaha-nutrition-and-weight-management-guidelines-with-ref.pdf">AAHA - Energy Requirement Calculations</a><br>\
    3. <a href = "https://www.aaha.org/aaha-guidelines/life-stage-feline-2021/feline-life-stage-home/">2021 AAHA/AAFP Feline Life Stage Guidelines</a><br>\
    4. <a href = "https://www.aaha.org/your-pet/pet-owner-education/aaha-guidelines-for-pet-owners/life-stage-canine/">8 THINGS YOU NEED TO KNOW ABOUT AAHA’S CANINE LIFE STAGE GUIDELINES</a></i></p>',
    unsafe_allow_html=True) 
    
    bool_a = False  
        
with preferences:
    
    
    space, col_for_texture_contents, col_for_spacing_2, col_for_ingre_table, col_for_spacing_3 = st.columns([0.2, 1.2,0.2,4.5, 0.2])    

    # texture and content column starts here (first column)
    with col_for_texture_contents:
        
        # filtering data based on species and health conditions
        if hc == 'None of the above':
            data = main_data[(~main_data['Category'].str.contains('Veterinary')) &
                            (main_data['Category'].str.contains(species))]
        else:
            data = main_data[main_data['Health_Condition'].isin(dic[hc])&
                            (main_data['Category'].str.contains(species))]
        
        # st.write(data['Product'].unique())
        # st.markdown(f"<p style='font-size:0.8em;'>Select Food Texture:</p>", unsafe_allow_html=True)
        
        st.markdown(f'#### Select Food Texture:')
        
        # now, we need unique list of contents, so we are splitting the contents column to make a list of contents to give selection to a user
        data['Contents_Split'] = data['Content'].str.split(", ")
        data_exploded_by_contents = data.explode('Contents_Split')
        data_exploded_by_contents = data_exploded_by_contents[data_exploded_by_contents['Contents_Split']!='']
        
        # grouping the data by texture and content to find the nuber of products for each texture and content
        data_t_c_grouped = data_exploded_by_contents.groupby(['Texture', 'Contents_Split'],
                                                            as_index=False).agg({'Product':'nunique'})
        
        # removing the specific content and texture which has zero products because we are not giving those contents as option which has zero products to go on with.
        data_t_c_grouped_filtered = data_t_c_grouped[data_t_c_grouped['Product']>0] 
        # texture selection
        texture = st.radio('',data_t_c_grouped_filtered['Texture'].unique(), horizontal=True, 
                           label_visibility = 'collapsed')
        
        # content selection                                                            
        # st.markdown(f"<p style='font-size:0.8em;'>Select Category:</p>", unsafe_allow_html=True) 
        st.markdown(f'#### Select Category:')
                                                                      
        contents = st.selectbox('',data_t_c_grouped_filtered[data_t_c_grouped_filtered['Texture']==texture]['Contents_Split'].unique(), 
                           label_visibility = 'collapsed')
        
        # st.write(contents)
        # filtering data by texture and contents                                                               
        filtered_data = data_exploded_by_contents[(data_exploded_by_contents['Texture']==texture) &
                                                 (data_exploded_by_contents['Contents_Split']==contents)]
    
    # texture and content column ends here (first column)
    
    # second column used for spacing

    # condition to show the ingredients only if the remaining products are more than two
    if filtered_data['Product'].nunique() > 2:

    # ingredient table column starts here
        with col_for_ingre_table:
            
            
            st.markdown(f'#### Deselect the ingredients from the below table:')
            
            # preparing data to show ingredients
            # a user can deselect the ingredients as per his choice  
            
            # grouping data by ingredients categories to find the number of product for each ingredient
            filtered_for_ing = filtered_data.groupby(['Split_Individual_Ingredient',
            'parent_category',
            'sub_category'], as_index=False).agg({'Product':"nunique"}).rename(columns={'Split_Individual_Ingredient':"Ingredient",
            'Product':'Products containing the ingredient'})

            filtered_for_ing = filtered_for_ing[filtered_for_ing['Products containing the ingredient']<filtered_data['Product'].nunique()-2]
                

            # table of ingredients with its parent category and sub-category
            gb0 = GridOptionsBuilder.from_dataframe(filtered_for_ing)
            gb0.configure_pagination(paginationAutoPageSize=True) #Add pagination
            gb0.configure_side_bar() #Add a sidebar
            gb0.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
            gridOptions = gb0.build()

            grid_response = AgGrid(
                filtered_for_ing,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
                gridOptions=gridOptions,
                data_return_mode='AS_INPUT', 
                update_mode='MODEL_CHANGED', 
                fit_columns_on_grid_load=True,
                enable_enterprise_modules=True,
                height=450,
                theme='balham',
                reload_data=False,
                allow_unsafe_jscode=True,
                unsafe_allow_html = True
            )

            data0 = grid_response['data']
            selected0 = grid_response['selected_rows']
            main_data0 = pd.DataFrame(selected0)
            
            # ingredient table column ends here
    
    # if the remaining products is less tha two, we will show this statement    
    else:
        data0 = filtered_data
        selected0 = []
        main_data0 = main_data
        with col_for_ingre_table:
            st.markdown(f"<p style='font-size:1em;'>Only 2 products remaining, if you deselect any ingredient from those products, \
                then you can't compare any products.</p>", unsafe_allow_html=True)
            
     
    # fourth column used for spacing
    
    # filtering data after deselecting ingredients
    # if user has deselected zero ingredients
    if selected0 == []:
        deselected_ing_list = ['']
    # if user has deselected more than zero ingredients
    else:

        deselected_ing_list = list(main_data0['Ingredient'])
    product_name_final = list(
        filtered_data[
            filtered_data['Split_Individual_Ingredient'].isin([each for each in deselected_ing_list])]['Product'].unique())
    
    
    with col_for_texture_contents:
        
        if '' not in deselected_ing_list:
            st.markdown(f'#### Deselected ingredients:')
            st.markdown(f'###### {", ".join(deselected_ing_list)}')
    
    # final filtered data after removing products which contains the user's deselected ingredients
    final_filtered_data = filtered_data[~filtered_data['Product'].isin(product_name_final)]
    if len(final_filtered_data)==0:
        st.error('No products left', icon='🚩')     
        
    
    
        

    
    final_filtered_data['Calories (kcal)'] = [(kcal_per_day) for each in final_filtered_data['Product']]
    # daily feeding in grams
    final_filtered_data['Daily Feeding (oz)'] = ((kcal_per_day/final_filtered_data['kcal_per_oz']))
    # daily feeding in 8-oz cups
    final_filtered_data['Daily Feeding (8-oz cups)'] = round(final_filtered_data['Daily Feeding (oz)'] / 8, 2)
    # product's price per day
    final_filtered_data['Price/Day ($)'] = ((final_filtered_data['Daily Feeding (oz)'] * final_filtered_data['Price Per Oz']) )
    # fat per day
    final_filtered_data['Fat (oz)'] = ((final_filtered_data['Fat oz per lb'] * final_filtered_data['Daily Feeding (oz)'] )/ 16)
    # protein per day
    final_filtered_data['Protein (oz)'] = ((final_filtered_data['Protein oz per lb'] * final_filtered_data['Daily Feeding (oz)'] )/16)
    # difference between required fat and fat in daily feeding proportion
    final_filtered_data['fat_abs_diff_perc'] = abs(final_filtered_data['Fat (oz)'] - fat_per_day_in_oz)*100/((final_filtered_data['Fat (oz)'] + fat_per_day_in_oz)/2)
    # difference between required protein and protein in daily feeding proportion
    final_filtered_data['protein_abs_diff_perc'] = abs(final_filtered_data['Protein (oz)'] - protein_per_day_in_oz)*100/((final_filtered_data['Protein (oz)'] + protein_per_day_in_oz)/2)
    # total difference in fat and protein
    final_filtered_data['abs_prot_fat'] = (final_filtered_data['fat_abs_diff_perc'] + final_filtered_data['protein_abs_diff_perc'])/2

    final_filtered_data = final_filtered_data.round(2)
    # single pack of product will last
    # final_filtered_data['Single pack will last'] = round(
    #     final_filtered_data['final_size_of_pack_in_kg']*1000/final_filtered_data['Daily Feeding (g)'], 0).astype(str).replace({".0":''},
    #     regex=True) + ' days'
    if 'inf' in list(round(
            final_filtered_data['final_size_of_pack_in_oz']/final_filtered_data['Daily Feeding (oz)'], 0).astype(str))[0]:
        final_filtered_data['Single pack will last']  = '0' + ' days'    
    else: 
        final_filtered_data['Single pack will last'] = round(
            final_filtered_data['final_size_of_pack_in_oz']/final_filtered_data['Daily Feeding (oz)'], 0).astype(int).astype(str) + ' days' 
        
    # final data to show
    final_data = final_filtered_data.sort_values(by=['abs_prot_fat',
    'Price/Day ($)'])[['Product',
    'Price/Day ($)',
    'Fat (oz)',
    'fat_abs_diff_perc',
    'Protein (oz)',
    'protein_abs_diff_perc',
    'Daily Feeding (oz)',
    'Daily Feeding (8-oz cups)',
    'Single pack will last']].rename(columns={'fat_abs_diff_perc':'Deviation in Fat (%)',
    'protein_abs_diff_perc':'Deviation in Protein (%)'}).drop_duplicates()  
    
    
with best_products:
    
    space, main_table_col, space_2 = st.columns([0.1,1,0.1])
    
    with main_table_col:
    
        # table of remaining products
        # a user can select products from this table to compare it on the next screen
        st.markdown(f'<p style="color:#2A5782; display:inline; "><b><h5>Select products for comparison</h5></b></p>', unsafe_allow_html=True)
        
        gb = GridOptionsBuilder.from_dataframe(final_data)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
        gridOptions = gb.build()

        grid_response = AgGrid(
            final_data,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS,
            gridOptions=gridOptions,
            data_return_mode='AS_INPUT', 
            update_mode='MODEL_CHANGED', 
            fit_columns_on_grid_load=True,
            enable_enterprise_modules=True,
            height=275,
            theme = 'balham',
            reload_data=False,
            allow_unsafe_jscode=True,
            unsafe_allow_html = True
        )

        # filtering data based on selected products
        data = grid_response['data']
        selected = grid_response['selected_rows']
        main_data = pd.DataFrame(selected)
        
        # st.write(final_filtered_data)
        
        if len(main_data)<2:
            list_of_final_products = []
        elif len(main_data)>1:
            list_of_final_products = list(main_data['Product'].unique()) 
            
        if len(list_of_final_products) != 0:
            
            st.markdown(f'<p style="color:#2A5782; display:inline; "><b><h5>Comparison of ingredients for selected products</h5></b></p>', unsafe_allow_html=True)
            pd.set_option('display.max_colwidth', None)


            final_filtered_data_1 = final_filtered_data[final_filtered_data['Product'].isin(list_of_final_products)][['Product', 'standardized_ingredient_panel']].drop_duplicates()
            
            ing_list = []
            for each in final_filtered_data_1['standardized_ingredient_panel'].str.split(', '):
                for each_2 in each:
                    ing_list.append((', '.join(each), each_2, standard_ingredient_dict[each_2]))
                    
            ing_df = pd.DataFrame(ing_list, columns = ['standardized_ingredient_panel', 'ingredient', 'category'])
            ing_df_2 = ing_df.merge(final_filtered_data_1)
            
            ing_df_2_grouped = ing_df_2.groupby(by = ['Product','category'], as_index = False).agg({
                                                                                    'ingredient':
                                                                                    lambda x : ', '.join(x)})
            

                   
            sorting_list = [
                'animal products'           
                'marine products'
                'grains'
                'vitamins'
                'minerals'
                'natural flavors'
                'artificial flavors'
                'natural additives'
                'artificial preservatives'
                'natural colors',
                'artificial colors',
                'amino acids'
                'fats and oils'
                'legumes'
                'oilseeds'
                'roughage fiber'
                'nuts'
                'fruits' 
                'vegetables'
                'dairy products'
                'human food'
                'herbs' 
                'spices'
                'enzymes'
                'microorganisms or fermentation products'
                'unknown']

            # sorting_dict_df = pd.DataFrame({v: i for i, v in enumerate(sorting_list)}, columns = ['category', 'order'])
            # ing_df_2_grouped['ordered_category'] = pd.Categorical(ing_df_2_grouped['category'], categories = sorting_list, ordered =True)
            # ing_df_2_grouped = ing_df_2_grouped.sort_values('ordered_category')
            
            pivot_df = ing_df_2_grouped.pivot_table(index='category', columns='Product', values='ingredient', aggfunc=lambda x: ' '.join(x)).replace(np.nan, '')
            
            # pivot_df_reset = pivot_df.reset_index()
            
            # pivot_df_reset.map(column = 'category', sorting_dict)
            
            # pivot_df_reset['category'] = pd.Categorical(pivot_df_reset['category'], categories = sorting_list, ordered =True)
            
            # pivot_df_sorted = pivot_df_reset.sort_values(by='category', key=lambda x: x.map({v: i for i, v in enumerate(sorting_list)}))
            
            # st.write(type(pivot_df_reset))
            # st.write(sorting_dict_df)
            # st.write(pivot_df.reindex(sorting_list))
            
            st.dataframe(pivot_df.style.set_properties(**{'color':
            '#00aaff'}).applymap(lambda x: 'color: grey' if pd.isna(x) else '').hide_index(),
            width=800, use_container_width=True)    
        
    
        
        
    
