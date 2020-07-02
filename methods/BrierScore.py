def brier_score(true_class, probability):
    positives_true_class = []
    positives_score = []
    negatives_true_class = []
    negatives_score = []

    for k in range(len(true_class)):
        if true_class[k] == 0:
            positives_true_class.append(true_class[k])
            positives_score.append(probability[k])
        elif true_class[k] == 1:
            # 1 = default / negavtiv / schlecht
            negatives_true_class.append(true_class[k])
            negatives_score.append(probability[k])
        else:
            break

    dict = {}
    dict['positive_bs_score'] = brier_score_value(positives_true_class, positives_score)
    dict['negative_bs_score'] = brier_score_value(negatives_true_class, negatives_score)

    return dict

def brier_score_value(true_class, probability):
    sum = 0
    n = len(true_class)
    for i in range(n):
        difference = true_class[i] - probability[i]
        difference_square = difference * difference
        sum = sum + difference_square

    return sum/n




