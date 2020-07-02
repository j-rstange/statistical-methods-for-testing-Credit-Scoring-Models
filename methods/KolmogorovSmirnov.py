import pandas as pd
import matplotlib
import matplotlib.pyplot as plt



# not the best algorithm but
# its easy and I can sort two lists in the same time
def insertion_sort(input_list, second_list):
    input_list = input_list.copy()
    second_list = second_list.copy()
    for i in range(1, len(input_list)):
        j = i - 1
        nxt_element = input_list[i]
        second_nxt_elemnt = second_list[i]
        # Compare the current element with next one

        while (input_list[j] > nxt_element) and (j >= 0):
            input_list[j + 1] = input_list[j]
            second_list[j+1] = second_list[j]
            j = j - 1
        input_list[j + 1] = nxt_element
        second_list[j+1] = second_nxt_elemnt

    return input_list, second_list


def kolmogorov_smirnov_score_and_curve(true_class, probability):
    scores = []
    for i in range(len(probability)):
        score = int(1000-probability[i]*1000)
        scores.append(score)

    scores, true_class = insertion_sort(scores, true_class)

    df_main = pd.DataFrame({"score": [], "count_bad":[], "count_good":[]})

    for i in range(len(scores)):
        if len(df_main) >0:
            last_score = df0['score'].iloc[-1]
            if last_score == scores[i]:
                if true_class[i] == 1:
                    df_main['count_bad'].iloc[-1]+=1
                else:
                    df_main['count_good'].iloc[-1]+=1
            else:
                df1 = pd.DataFrame({"score": [scores[i]], "count_bad": [df_main["count_bad"].iloc[-1] +1], "count_good": [df_main["count_good"].iloc[-1]]})
                df0 = pd.DataFrame({"score": [scores[i]], "count_bad": [df_main["count_bad"].iloc[-1]], "count_good": [df_main["count_good"].iloc[-1] +1]})

                if true_class[i] == 1:
                    df_main = df_main.append(df1, ignore_index = True)
                else:
                    df_main = df_main.append(df0, ignore_index = True)
        else:
            df1 = pd.DataFrame({"score": [scores[i]], "count_bad": [1], "count_good": [0]})
            df0 = pd.DataFrame({"score": [scores[i]], "count_bad": [0] , "count_good": [1]})

            if true_class[i] == 1:
                df_main = df_main.append(df1, ignore_index = True)
            else:
                df_main = df_main.append(df0, ignore_index = True)

    number_of_good = true_class.count(0)
    number_of_bad = len(true_class)-number_of_good

    def calculation_cum_good_pcn(row):
        return row['count_good'] / number_of_good
    def calculation_cum_bad_pcn(row):
        return row['count_bad'] /number_of_bad
    df_main['cum_bad_pcn'] = df_main.apply (lambda row: calculation_cum_bad_pcn(row), axis=1)
    df_main['cum_good_pcn'] = df_main.apply (lambda row: calculation_cum_good_pcn(row), axis=1)

    def sepeartion(row):
        return row['cum_bad_pcn'] - row['cum_good_pcn']

    df_main['seperation'] =  df_main.apply(lambda row: sepeartion(row), axis=1)

    #plot_ks_graphic(df_main)
    x = df_main['score']
    y_1 = df_main['cum_bad_pcn']
    y_2 = df_main['cum_good_pcn']
    max_seperation = df_main.loc[df_main['seperation'].idxmax()]
    x_ks = max_seperation['score']
    y_top = max_seperation['cum_bad_pcn']
    y_bottom = max_seperation['cum_good_pcn']
    return df_main['seperation'].max(), x, y_1, y_2, x_ks, y_top, y_bottom

def plot_ks_graphic(df_main):
    max_seperation = df_main.loc[df_main['seperation'].idxmax()]

    # Data for plotting
    x = df_main['score']
    y_1 = df_main['cum_bad_pcn']
    y_2 = df_main['cum_good_pcn']

    fig, ax = plt.subplots()
    ax.plot(x, y_1, color='tab:red')
    ax.plot(x, y_2, color='tab:blue')
    ax.vlines(ymin=max_seperation['cum_good_pcn'], ymax=max_seperation['cum_bad_pcn'], x=max_seperation['score'], color='black')

    ax.set(xlabel='scores', ylabel='cum %',
           title='KS Statistik')
    ax.grid()

    plt.show()