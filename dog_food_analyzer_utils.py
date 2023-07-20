## There are two functions in the file
## The first function will create a json file having variables upto the Dog Exclusive Input section (The part where we take name, age, etc.)
## inputs from the user
## The second function will add the variables of remaining parts in the same json.

# importing libraries
import re
import pandas as pd
import json

# importing utils files
import dog_food_analyzer_dictionaries
from dog_food_analyzer_dictionaries import *

def co2_emissions_from_ingredients(ing_str, diet_category):
    '''
    This function will clean and preprocess the ingredient panel and do the categorization of ingredients.
    Input: Ingredient Panel of the product, Diet category chosen by user - "Dry" or "Wet"
    
    This function will create the json file first.
    '''
    try:
    # taking care of flavors
        if ": " in ing_str:
            ing_str_2 = ing_str.split(': ')[1].strip()
        else:
            ing_str_2 = ing_str
    # First level cleaning
        ing_str_2 = re.sub(r"vitamins & minerals", "", ing_str_2, flags = re.IGNORECASE).strip()
        ing_str_2 = ing_str_2.replace("Premium chicken (20%, including back and breast)", "chicken")
        ing_str_2 = re.sub(r"\)\s*([a-zA-Z])", r"), \1", ing_str_2).strip()
        ing_str_2 = re.sub(r"\]\s*([a-zA-Z])", r"], \1", ing_str_2).strip()
        ing_str_2 = re.sub(r'\s*[-–]\s*|\s*\(\d+(\.\d+)?%\s*[^)]*\)',
                ' ',
                ing_str_2).strip()
        ing_str_2 = re.sub(r'\s*[-–]\s*|\s*\(\s*[^)]+\d+%[^)]*\)',
                ' ',
                ing_str_2).strip()
        ing_str_2 = ing_str_2.replace(" poultry in total", "").replace("’", "").replace("'", "")
        ing_str_2 = re.sub(r"\(\d+%?\)", "", ing_str_2).strip()
        

        # creating a list of ingredients directly without preprocessing in order to highlight them properly. This will be used further
        # as keys to highlight the ingredients in app
        unprocessed_ing_list = ing_str_2.split(", ")

        # replacing vitamins and minerals keywords along with extra other keywords
        ing_str_3 = ing_str_2.lower().replace('vitamins', '').replace('trace minerals', '').replace('minerals', '').replace('new:', '').replace('original:', '').replace('caloric content', '')

        # iteration for each category (cat wellness dry, dog raw food, etc.) of product to clean and preprocess the ingredient panel
        for cate, values in cleaning_dictionary.items():

            # iterating for cleaning each ingredient string
            for unc, clean in values.items():
                ing_str_3 = ing_str_3.replace(unc, clean)

            # removing extra noises
            ing_str_4 = ing_str_3.replace('[', '')
            ing_str_5 = re.sub('\n', ' ', ing_str_4)
            ing_str_6 = re.sub(r'\s+', ' ', ing_str_5)
            ing_str_7 = re.sub('\xa0', '', ing_str_6).strip()

            for unc, clean in replace_dict.items():
                ing_str_7 = ing_str_7.replace(unc, clean)

            # splitting each ingredient from the ingredient string and storing it in list
            split_ingredients = ing_str_7.split(',')
            split_ingredients = [i.strip() for i in split_ingredients]
            # iterating each ingredient and removing useless parantheses
            ingredients_tokenized = []
            for each in split_ingredients:
                if '(' in each and ')' not in each:
                    s = each.replace('(', '')
                    ingredients_tokenized.append(s)
                elif ')' in each and '(' not in each:
                    s = each.replace(')', '')
                    ingredients_tokenized.append(s)
                else:
                    ingredients_tokenized.append(each)

            # removing trailing fullstops
            new_ingredients = []
            for each in ingredients_tokenized:
                if len(each) != 0 and each[-1] == '.':
                    item = each[:-1].strip()
                    new_ingredients.append(item)
                elif len(each) != 0 and each[0] == ':':
                    item = each[2:].strip()
                    new_ingredients.append(item)
                else:
                    new_ingredients.append(each)

            # removing extra noises from ingredients (Z68980, D80987, etc)
            # for this, splitting ingredients by fullstop
            new_ingredients_split = [each.split('.') for each in new_ingredients]

            # checking pattern of those noises and removing it
            new_ingredients_2 = []
            for each in new_ingredients_split:
                if len(each) == 2:
                    if len(each[1]) == 8 or len(each[1]) == 7:
                        new_ingredients_2.append(each[0].strip())
                    else:
                        new_ingredients_2.append(each)
                else:
                    new_ingredients_2.append(each)

            # Joining again with fullstops as that was the separator for splitting for previous step
            new_product_wise_ingredients = []
            for each in new_ingredients_2:
                if type(each) == list:
                    new_product_wise_ingredients.append(('.').join(each).lower().strip().replace("))", ")").replace("((", "(").strip())
                else:
                    new_product_wise_ingredients.append(each.lower().strip().replace("))", ")").replace("((", "(").strip())

            if '' in new_product_wise_ingredients:
                new_product_wise_ingredients.remove('')

            # converting the list of ingredient panel into dataframe to check if each
            # ingredient belongs to dictionary of standardized ingredients
            ingredients_dict_df = pd.DataFrame(new_product_wise_ingredients,
                                               columns=['Ingredient']).drop_duplicates()

            set_of_already_corrected_ingredient_names = set(
                ingredient_and_sub_and_parent_category.keys())

            set_of_current_ingredients = set(
                ingredients_dict_df['Ingredient'].str.lower())

            remaining_set = (set_of_current_ingredients -
                             set_of_already_corrected_ingredient_names.intersection(set_of_current_ingredients))

            # this will break the loop if the remaining unmatched ingredient is nan or empty string
            if ('nan' in remaining_set and '' in remaining_set and len(remaining_set) <= 3) or\
                    (('nan' in remaining_set or '' in remaining_set) and len(remaining_set) == 1):

                break

        # removing trailing fullstops
        unprocessed_ing_list_2 = []
        for each in unprocessed_ing_list:
            if len(each) != 0 and each[-1] == '.':
                item = each[:-1].strip()
                unprocessed_ing_list_2.append(item)
            elif len(each) != 0 and each[0] == ':':
                item = each[2:].strip()
                unprocessed_ing_list_2.append(item)
            else:
                unprocessed_ing_list_2.append(each)

        # removing extra noises from ingredients (Z68980, D80987, etc)
        # for this, splitting ingredients by fullstop
        unprocessed_ing_split = [each.split('.') for each in unprocessed_ing_list_2]

        # checking pattern of those noises and removing it
        unprocessed_ing_list_5 = []
        for each in unprocessed_ing_split:
            if len(each) == 2:
                if len(each[1]) == 8 or len(each[1]) == 7:
                    unprocessed_ing_list_5.append(each[0].strip())
                else:
                    unprocessed_ing_list_5.append(each)
            else:
                unprocessed_ing_list_5.append(each)

        # Joining again with fullstops as that was the separator for splitting for previous step
        unprocessed_ing_list_6 = []
        for each in unprocessed_ing_list_5:
            if type(each) == list:
                unprocessed_ing_list_6.append(('.').join(each).strip().replace("))", ")").replace("((", "(").strip())
            else:
                unprocessed_ing_list_6.append(each.strip().replace("))", ")").replace("((", "(").strip())

        unprocessed_ing_list_7 = [re.sub(r"(vitamins|trace minerals|minerals)", "", each, flags=re.IGNORECASE).replace(":", "").strip() for each in unprocessed_ing_list_6]
        unprocessed_ing_list_8 = []
        for ingre in unprocessed_ing_list_7:
            if "(" in ingre and ")" not in ingre:
                ingre = ingre.replace(r"(", "")
            elif ")" in ingre and "(" not in ingre:
                ingre = ingre.replace(r")", "")
            elif "[" in ingre and "]" not in ingre:
                ingre = ingre.replace(r"[", "")
            elif "]" in ingre and "[" not in ingre:
                ingre = ingre.replace(r"]", "")
            elif "]" not in ingre and "[" not in ingre and ")" not in ingre and "(" not in ingre:
                ingre = ingre
            unprocessed_ing_list_8.append(ingre)

# ---------------------------------------------------------------------------------------------------------------------------------

        if diet_category == 'Dry' and len(new_product_wise_ingredients) > 5:

            ingredient_list = new_product_wise_ingredients[0:11]
            
            not_in_sub_category_list = [each for each in ingredient_list if each.lower() not in ingredient_and_sub_and_parent_category.keys()]

            sub_category_list = [ingredient_and_sub_and_parent_category[each.lower()][0]
                                 for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]

            parent_category_list = [ingredient_and_sub_and_parent_category[each.lower()][1] 
                                    for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]


            proprotions = proportion_division_dict[diet_category]

            top_5_df = pd.DataFrame(zip(parent_category_list[0:5], sub_category_list[0:5],
                                        proprotions[0:5]), columns = ['parent_category','sub_category', 'proportions'])


        elif diet_category == 'Wet' and len(new_product_wise_ingredients) > 5:

            ingredient_list = new_product_wise_ingredients[0:8]
            
            not_in_sub_category_list = [each for each in ingredient_list if each.lower() not in ingredient_and_sub_and_parent_category.keys()]


            sub_category_list = [ingredient_and_sub_and_parent_category[each.lower()][0]
                                 for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]

            parent_category_list = [ingredient_and_sub_and_parent_category[each.lower()][1] 
                                    for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]


            proprotions = proportion_division_dict[diet_category]

            top_5_df = pd.DataFrame(zip(parent_category_list[0:5], sub_category_list[0:5],
                                        proprotions[0:5]), columns = ['parent_category','sub_category', 'proportions'])



        elif len(new_product_wise_ingredients) <= 5:

            ingredient_list = new_product_wise_ingredients
            
            not_in_sub_category_list = [each for each in ingredient_list if each.lower() not in
                                        ingredient_and_sub_and_parent_category.keys()]


            sub_category_list = [ingredient_and_sub_and_parent_category[each.lower()][0]
                                 for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]

            parent_category_list = [ingredient_and_sub_and_parent_category[each.lower()][1] 
                                    for each in ingredient_list if each.lower() in ingredient_and_sub_and_parent_category.keys()]
            
            proprotions = proportion_division_dict[len(sub_category_list)]

            top_5_df = pd.DataFrame(zip(parent_category_list, sub_category_list,
                                        proprotions), columns = ['parent_category','sub_category', 'proportions'])


        else: 

            total_co2 = 0
            print(err)
            return_dict = {"Error: ":"Please enter diet category properly!"}
            # Write the dictionary to a JSON file 
            with open('json_output.json', 'w') as f:
            # saving dictionary into json file
                json.dump(return_dict, f, indent = 1)

            return return_dict, total_co2

        
        emission_df = pd.DataFrame.from_dict(emission_dict,
                                             orient = 'index',
                                             columns = ['CO2 Emission Percentile']).reset_index().rename(columns= {'index' :
                                                                                                                   'sub_category'})


        top_5_df_merged = top_5_df.merge(emission_df, how= 'inner').sort_values(by = 'proportions', ascending = False)
        
        top_5_df_merged['multiplier'] = [i/top_5_df_merged['proportions'].iloc[-1] for i in top_5_df_merged['proportions']]
        
        
        total_co2_list = []
        
        for i, j, k in zip(top_5_df_merged['CO2 Emission Percentile'], top_5_df_merged['multiplier'], top_5_df_merged['parent_category']):
#             total_co2_list.append((i/100) * j)
            if k == 'animal products' or k == 'marine products' or k == 'dairy products':
                total_co2_list.append((i/100) * j)
            else:
                total_co2_list.append(j * (0 - (1-(i/100))))
                


        total_co2 = sum(total_co2_list)         

        co2_index = total_co2 + dict_diet_category_emission_value[diet_category][0]
        
        if diet_category == 'Dry' and co2_index > 9:
            co2_index = 9
        elif diet_category == 'Dry' and co2_index < 0: 
            co2_index = 0
        elif diet_category == 'Wet' and co2_index > 42:
            co2_index = 42
        elif diet_category == 'Wet' and co2_index < 22: 
            co2_index = 22         
        
    #       mapping the ingredients with their parent category using ingredient dictionary and storing it in dictionary
        mapping_df = pd.DataFrame(zip(new_product_wise_ingredients[0:5], unprocessed_ing_list_8[0:5]),
                                 columns=['lower', 'as_in'])

        dict_df = pd.DataFrame(zip(ingredient_and_sub_and_parent_category.keys(), 
                                   [i[0] for i in ingredient_and_sub_and_parent_category.values()], 
                                   [i[1] for i in ingredient_and_sub_and_parent_category.values()]),
                                        columns=['lower', 'sub_category', 'parent_category'])

        merged_df = mapping_df.merge(dict_df, how='inner')

    #     print(merged_df)

        merged_grouped_df = merged_df.groupby("parent_category",
                         as_index=False).agg({"as_in": lambda x: list(x)})

        merged_grouped_df = merged_grouped_df[(merged_grouped_df['parent_category'] == 'animal products') |
                                             (merged_grouped_df['parent_category'] == 'marine products') |
                                             (merged_grouped_df['parent_category'] == 'dairy products')]

        merged_grouped_df['parent_category'] = merged_grouped_df['parent_category'].str.title()

        final_dict = [k for k in merged_grouped_df['as_in']]
        
        final_dict_1 = []
        
        for i in final_dict:
            
            final_dict_1.extend(i)
            
        
        co2_index_per_year = co2_index * 365
        
        co2_index_in_tons = co2_index_per_year / 1000
        
        miles =  int(round(co2_index_in_tons / other_factors_of_co2_in_metric_tons['miles_of_gasoline_vehicle'][0], 0))
                         
        
        return_dict = {'highlighting_ingredients' : final_dict_1,
                       'co2_emission_from_ingredients_per_day' : round(co2_index, 2),
                       'co2_emission_from_ingredients_per_year' : round(co2_index_per_year, 2),
                       'min_threshold' : threshold_of_ingredient_dict[diet_category][0],
                       'max_threshold' : threshold_of_ingredient_dict[diet_category][1],
                       'miles' : miles,
                       'not_in_our_sub_category_list' : not_in_sub_category_list}
                       
        
        
        # with open('json_output.json', 'w') as f:
        # # saving dictionary into json file
        #     json.dump(return_dict, f, indent = 1)

    except Exception as err:
        co2_index = 0
        print(err)
        return_dict = {"Error: ":"Please Enter Ingredients Properly!"}
        # Write the dictionary to a JSON file 
        # with open('json_output.json', 'w') as f:
        # # saving dictionary into json file
        #     json.dump(return_dict, f, indent = 1)
    return return_dict                                                                                      

def co2_emissions_by_calorie_requirements(ingredients, years, months, weight, condition, diet_category, breed):
    '''This function is for the pet exclusive section where we take user inputs such as years, months, etc.
        years: Should be an integer not less than 0.
        months: Should be an integer from 1 to 12
        weight: Should be an integer or decimal value.
        breed: Should strictly be a text from the keys of "dog_breed_lifespan" dictionary in dictionaries.py.
        condition: Should be strictly from "Intact", "Neutered", "Obese".
        
        This will update the already created json file where it will add the new variables.
    '''
    
    values_from_ingredients = co2_emissions_from_ingredients(ingredients, diet_category)
    
    try:
        kcal_per_day = 0
        fat_per_day = 0
        protein_per_day = 0
        co2_in_kg = 0
        rer = int(round(70 * (weight ** 0.75)))
        age_in_months = years*12 + months
        lifespan = dog_breed_lifespan[breed]
#         print(lifespan)
#         print(age_in_months)
        if 0 < age_in_months < 9:
            if age_in_months <= 4:
                kcal_per_day = 3 * rer
                protein_per_day = (45/1000)*kcal_per_day
                fat_per_day = (kcal_per_day*21.3)/1000

            elif age_in_months > 4:
                kcal_per_day = 2 * rer
                protein_per_day = (35/1000)*kcal_per_day
                fat_per_day = (kcal_per_day*21.3)/1000


        elif age_in_months >= (0.75 * lifespan)*12:
            kcal_per_day = 0.8 * rer
            protein_per_day = (20/1000)*kcal_per_day
            fat_per_day = (10/1000)*kcal_per_day

        elif 9 < age_in_months < (0.75 * lifespan)*12:

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
        
                       
        kcal_per_day = round(kcal_per_day, 2)
        fat_per_day = round(fat_per_day, 2)
        protein_per_day = round(protein_per_day, 2)

#         with open('json_output.json', 'r') as f:
#             # saving dictionary into json file
#                 data = json.load(f)  
        
        
        co2_in_kg_per_day0 = round(values_from_ingredients['co2_emission_from_ingredients_per_day'] * kcal_per_day / 1000, 2)
        
        if values_from_ingredients['min_threshold'] > co2_in_kg_per_day0 and values_from_ingredients['max_threshold'] > co2_in_kg_per_day0:
            co2_in_kg_per_day = values_from_ingredients['min_threshold'] + 0.09
        elif values_from_ingredients['min_threshold'] < co2_in_kg_per_day0 and values_from_ingredients['max_threshold'] > co2_in_kg_per_day0:
            co2_in_kg_per_day = co2_in_kg_per_day0
        elif values_from_ingredients['min_threshold'] < co2_in_kg_per_day0 and values_from_ingredients['max_threshold'] < co2_in_kg_per_day0:
            co2_in_kg_per_day = values_from_ingredients['max_threshold'] - 0.09
        else:
            co2_in_kg_per_day = co2_in_kg_per_day0
        
        
        co2_in_kg_per_year = co2_in_kg_per_day0 * 365                 
                 
        reducing_co2_per_day = co2_in_kg_per_day0 / reducing_co2_dict[diet_category]
        
        if values_from_ingredients['min_threshold'] > reducing_co2_per_day and values_from_ingredients['max_threshold'] > reducing_co2_per_day:
            reduced_co2_per_day_black_bar = values_from_ingredients['min_threshold'] + 0.09
        elif values_from_ingredients['min_threshold'] < reducing_co2_per_day and values_from_ingredients['max_threshold'] > reducing_co2_per_day:
            reduced_co2_per_day_black_bar = reducing_co2_per_day
        elif values_from_ingredients['min_threshold'] < reducing_co2_per_day and values_from_ingredients['max_threshold'] < reducing_co2_per_day:
            reduced_co2_per_day_black_bar = values_from_ingredients['max_threshold'] - 0.09
        else:
            reduced_co2_per_day_black_bar = reducing_co2_per_day
        
#         reducing_co2_per_year = co2_in_kg_per_year / reducing_co2_dict[diet_category]
        
#         reduced_co2_per_year = co2_in_kg_per_year - reducing_co2_per_year
        
        number_of_trees =  (co2_in_kg_per_year - (co2_in_kg_per_year / reducing_co2_dict[diet_category]))  / (other_factors_of_co2_in_metric_tons['number_of_urban_tree_seedlings_grown'][0] * 1000)
         
        data = {}
        data['calories_per_day_in_kcal'] = round(kcal_per_day, 2)
        data['fat_per_day_in_gms'] = round(fat_per_day, 2)
        data['protein_per_day_in_gms'] = round(protein_per_day, 2)
        data['dog_exclusive_co2_emission_per_day_value'] = round(co2_in_kg_per_day0, 2)
        data['dog_exclusive_co2_emission_per_day_black_bar'] = round(co2_in_kg_per_day, 2)
#         data['dog_exclusive_co2_emission_per_year'] = round(co2_in_kg_per_year, 2)
        data['final_co2_per_day_after_reducing_value'] = round(reducing_co2_per_day, 2)
        data['final_co2_per_day_after_reducing_black_bar'] = round(reduced_co2_per_day_black_bar, 2)
        
#         data['final_co2_per_year_after_reducing'] = round(reducing_co2_per_year, 2)
        data['number_of_trees'] = int(round(number_of_trees, 0))
        data['min_threshold'] = values_from_ingredients['min_threshold']
        data['max_threshold'] = values_from_ingredients['max_threshold']

        # with open('json_output.json', 'w') as f:
        #     # saving dictionary into json file
        #         json.dump(data, f, indent = 1)

    except Exception as err:
        print(err)
        data = {"Error: ":"Please enter informations properly!"}
        # Write the dictionary to a JSON file 
        # with open('json_output.json', 'w') as f:
        # # saving dictionary into json file
        #     json.dump(data, f, indent = 1)
        
    return data