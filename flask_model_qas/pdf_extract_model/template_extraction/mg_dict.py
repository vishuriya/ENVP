import pandas as pd
import re

# Gets the mapping of which column to fit where into the template
def fetch(df_final, cur_index, dict_of_val, list_of_list, no_header_count, indices, ficticious_header):
    template_header_limited = list(dict_of_val.keys())

    l_of_l = list_of_list
    df_updated_list = pd.DataFrame(list_of_list)
   
    # df_template = pd.read_excel(r'C:\Users\PN665UT\OneDrive - EY\Desktop\flask_app\flask_app\pdf_keras_model\26062020_120058.xlsx', sheet_name='Sheet1')

    header = 0
    col_to_be_transported = []
    blank = 0

    for i in range(0, len(l_of_l[0])):
        for j in range(0, len(template_header_limited)):
            if l_of_l[header][i] in dict_of_val[template_header_limited[j]]:
                l_of_l[0][i] = template_header_limited[j]
                col_to_be_transported.append([i, j])

                break
        else:
            col_to_be_transported.append([i, len(template_header_limited) + no_header_count + blank])
            blank = blank + 1

    l=[]
    print("#############################Column to be transported")
    print(l_of_l)
    # Returns the mapping from list to template for columns
    return cur_index, col_to_be_transported, l_of_l


# Identifies top row of the list
def return_top_row(list_of_list):
    list_expected = ['Description*','Quantity*']
    final_list = []
    for i in list_of_list:
        for j in list_expected:
            for k in i:
                if re.match(j,k):
                    pos_of_col = list_of_list.index(i)
                    if pos_of_col > 0:
                        del list_of_list[0:pos_of_col]
                        final_list = list_of_list
                    else:
                        final_list = list_of_list
                else:
                    final_list = list_of_list

    for i in range(len(final_list[0])):
        final_list[0][i] = final_list[0][i].strip().replace('.','').replace('\n','').replace('  ',' ')
    
    return final_list