import pandas as pd
from methods import KolmogorovSmirnov as ks
import matplotlib.pyplot as plt

def partial_gini_coefficient(true_class, probability, partial_gini_cut_off):
    n = len(true_class)
    # find the position of the cut_off
    n_cut_off = n

    n = len(true_class)
    n_10 = int(n/10)
    n_remaining = n%10
    n_bad = true_class.count(1)
    probability, true_class = ks.insertion_sort(probability, true_class)
    for l in range(len(probability)):
        if probability[l] > partial_gini_cut_off:
            n_cut_off = l
            break;

    df_main = pd.DataFrame({"decile": [0,1,2,3,4,5,6,7,8,9,10],
                            "number": [0,n_10,n_10,n_10,n_10,n_10,n_10,n_10,n_10,n_10,n_10]})

    for i in range(n_remaining):
        df_main['number'][i+1]+=1

    def number_in_percent(column_name,row, n):
        return row[column_name] / n
    def cumulative_number(column):
        cum_column = [0]
        for i in range(len(column)-1):
            cum_column.append(cum_column[i]+column[i+1])
        return cum_column



    #get number ob bad for each decile +
    #add one quantile if the position of the cut_off is not at the end of one existing decile
    # this changes the overall Gini coefficient but is needed for the partial
    number_of_bad_list = [0]
    previous_number = 0
    boolean = False
    skipp = 1
    for k in range(10):
        number = df_main['number'][k+skipp] + previous_number
        if number > n_cut_off and k !=0 and boolean == False:
            boolean = True
            if previous_number != n_cut_off:
                extraordinary_number = n_cut_off-previous_number
                extra = extraordinary_number / n_10
                line = pd.DataFrame({"decile": k+extra, "number": extraordinary_number}, index=[k])
                df_main = pd.concat([df_main.iloc[:k+1], line, df_main.iloc[k+1:]]).reset_index(drop=True)
                df_main['number'][k+2]-=extraordinary_number
                # might not be the most elegant solution but it works, sry
                slice = true_class[previous_number:previous_number+extraordinary_number]
                number_of_bad_list.append(slice.count(1))
                previous_number = previous_number+extraordinary_number
                slice = true_class[previous_number:number]
                number_of_bad_list.append(slice.count(1))
                previous_number = number
                skipp = 2
            else:
                slice = true_class[previous_number:number]
                number_of_bad_list.append(slice.count(1))
                previous_number = number
        else:
            slice = true_class[previous_number:number]
            number_of_bad_list.append(slice.count(1))
            previous_number = number

    df_main['number_perc'] = df_main.apply(lambda row: number_in_percent('number',row, n), axis=1)
    df_main['cum_number'] = cumulative_number(df_main['number'])
    df_main['cum_number_perc'] = cumulative_number(df_main['number_perc'])

    df_main['number_of_bad'] = number_of_bad_list
    df_main['number_of_bad_perc'] = df_main.apply(lambda row: number_in_percent('number_of_bad',row, n_bad), axis=1)
    df_main['cum_number_of_bad_perc'] = cumulative_number(df_main['number_of_bad_perc'])

    #calculate the area for each trapeze
    def area(df):
        area_list = [0]
        for i in range(len(df['decile'])-1):
            area = (df['cum_number_of_bad_perc'][i]+df['cum_number_of_bad_perc'][i+1])*0.5*df['number_perc'][i+1]
            area_list.append(area)
        return area_list

    df_main['area'] = area(df_main)
    #find cut_off qunatile (decile)
    for i in range(len(df_main['number'])):
        if df_main['cum_number'][i] == n_cut_off:
            cut_off_decile = i

    # area under the curve to cut_off
    sum_area = sum(df_main['area'][:cut_off_decile+1])
    area_under_diagonal=0.5*df_main['cum_number_perc'][cut_off_decile]*df_main['cum_number_of_bad_perc'][cut_off_decile]
    # area between diagonal and lorenz_curve
    A1 = area_under_diagonal-sum_area
    PG = A1 / (sum_area+A1)
    x = df_main['decile']
    y = df_main['cum_number_of_bad_perc']
    x_partial = df_main['decile'][cut_off_decile]
    y_partial = df_main['cum_number_perc'][cut_off_decile]

    #plt.plot(df_main['decile'], df_main['cum_number_of_bad_perc'], color = 'orange')
    #plt.plot(df_main['decile'], df_main['cum_number_perc'], color = 'blue')
    #plt.show()
    return PG, x, y, x_partial, y_partial

