# importing libraries
import re
import pandas as pd
import json

# importing utils files
import ingredient_analyzer_dictionaries
from ingredient_analyzer_dictionaries import *

# Defining the main function that will clean and categorize ingredients
def preprocess_ingredients(ing_str):
    
    '''
    This function will clean and preprocess the ingredient panel and do the categorization of ingredients.
    Input: Ingredient Panel of the product
    Returns: Nested Dictionary and json file of {Category : {preprocessed ingredient name:ingredient name as entered}}
    '''
    try:
        # taking care of flavors
        if ": " in ing_str:
            ing_str_2 = ing_str.split(': ')[1].strip()
        else:
            ing_str_2 = ing_str

        ing_str_2 = re.sub(r"vitamins & minerals", "", ing_str_2, flags = re.IGNORECASE).strip()
        ing_str_2 = re.sub(r"\)\s*([a-zA-Z])", r"), \1", ing_str_2).strip()
        ing_str_2 = re.sub(r"\]\s*([a-zA-Z])", r"], \1", ing_str_2).strip()

        # creating a list of ingredients directly without preprocessing in order to highlight them properly.
        unprocessed_ing_list = ing_str_2.split(", ")

        # replacing vitamins and minerals keywords along with extra other keywords
        ing_str_3 = ing_str_2.lower().replace('vitamins', '').replace('minerals', '').replace('new:', '').replace('original:', '').replace('caloric content', '')

        # iteration for each category (cat wellness dry, dog raw food, etc.) of product to clean and preprocess the ingredient panel
        for cate, values in cleaning_dictionary.items():

            # converting each ingredient panel into string type
            # ingredients_list = [str(i) for i in ingr_list]

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
            split_ingredients = ing_str_7.split(', ')

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

            # removing tailing fullstops
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

            # converting the list of ingredient panel into dataframe to check if each
            # ingredient belongs to dictionary of standardized ingredients
            ingredients_dict_df = pd.DataFrame(new_product_wise_ingredients,
                                               columns=['Ingredient']).drop_duplicates()

            set_of_already_corrected_ingredient_names = set(
                ingredient_dictionary.keys())

            set_of_current_ingredients = set(
                ingredients_dict_df['Ingredient'].str.lower())

            remaining_set = (set_of_current_ingredients -
                             set_of_already_corrected_ingredient_names.intersection(set_of_current_ingredients))

            # this will break the loop if the remaining unmatched ingredient is nan or empty string
            if ('nan' in remaining_set and '' in remaining_set and len(remaining_set) <= 3) or\
                    (('nan' in remaining_set or '' in remaining_set) and len(remaining_set) == 1):

                break

        # Before we map the ingredients i.e. the preprocessed ingredient to the ingredient as entered, we need to some of the cleaning for that unprocessed ingredient as
        # well.
        # Inconsistent use of the parantheses in the data is to be removed.
        # unprocessed_ing_list_2 = []

#         # iterating each ingredient and removing useless parantheses
#         for each in unprocessed_ing_list:
#             if '(' in each and ')' not in each:
#                 s = each.replace('(', '')
#                 unprocessed_ing_list_2.append(s)
#             elif ')' in each and '(' not in each:
#                 s = each.replace(')', '')
#                 unprocessed_ing_list_2.append(s)
#             else:
#                 unprocessed_ing_list_2.append(each)

#         # Inconsistent use of the square brackets in the data is to be removed.
#         unprocessed_ing_list_3 = []

#         # iterating each ingredient and removing useless parantheses
#         for each in unprocessed_ing_list_2:
#             if '[' in each and ']' not in each:
#                 s = each.replace('[', '')
#                 unprocessed_ing_list_3.append(s)
#             elif ']' in each and '[' not in each:
#                 s = each.replace(']', '')
#                 unprocessed_ing_list_3.append(s)
#             else:
#                 unprocessed_ing_list_3.append(each)

        # removing tailing fullstops
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

        unprocessed_ing_list_7 = [re.sub(r"(vitamins|minerals)", "", each, flags=re.IGNORECASE).replace(":", "").strip() for each in unprocessed_ing_list_6]

        # mapping the ingredients with their parent category using ingredient dictionary and storing it in dictionary with its flavor
        mapping_dict = {k:v for k,v in zip(new_product_wise_ingredients, unprocessed_ing_list_7)}
        
        d = {}
        for each in new_product_wise_ingredients:
            if each in set(ingredient_dictionary.keys()):
                parent_cat = ingredient_dictionary[each]
                d[each] = parent_cat.capitalize()
            elif each not in set(ingredient_dictionary.keys()) and each!="":
                d[each] = "Undefined"


        # converting the flavor : ingredient : parent_category dictionary to 
        # parent_category : ingredient dictionary
        category_dict = {}
        for ingredient, category in d.items():
            if category not in category_dict:
                category_dict[category] = {}
            category_dict[category].update({ingredient.replace(r")", "").replace(r"(", ""): mapping_dict[ingredient]})
            
            
        
        sorted_dict = dict(sorted(category_dict.items()))
    
#         print(sorted_dict)
        
        # mapping the description of categories in the sorted dictionary
        new_sorted_dict = {}
        
        for cate, ingredients in sorted_dict.items():
            for cate_for_desc, desc in description_dictionary.items():
                if cate_for_desc == cate:
                    d = {}
                    d['Description'] = desc
                    for each, ingre in ingredients.items():
                        if "(" in ingre and ")" not in ingre:
                            ingre = ingre.replace(r"(", "")
                        elif ")" in ingre and "(" not in ingre:
                            ingre = ingre.replace(r")", "")
                        elif "[" in ingre and "]" not in ingre:
                            ingre = ingre.replace(r"[", "")
                        elif "]" in ingre and "[" not in ingre:
                            ingre = ingre.replace(r"]", "")
                            
                        d[each] = ingre
                    new_sorted_dict[cate] = d


        # sorted_dict = {k:list(v.values()) for k, v in sorted_dict.items()}
        
        # Write the dictionary to a JSON file 
        # with open('json_output.json', 'w') as f:
        # # saving dictionary into json file
        #     json.dump(new_sorted_dict, f)
        
    except Exception as err:
        print(err)
        new_sorted_dict = {"Error: ":"Please Enter Ingredients Properly!"}
        # Write the dictionary to a JSON file 
        # with open('json_output.json', 'w') as f:
        # # saving dictionary into json file
        #     json.dump(new_sorted_dict, f)

    return new_sorted_dict