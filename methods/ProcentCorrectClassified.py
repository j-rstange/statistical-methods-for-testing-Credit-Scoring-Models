def procent_correct_classified(true_class, probability, threshold):

    predicted_class = get_predicted_class(true_class, probability, threshold)

    TP, FP, FN, TN = confusion_matrix(predicted_class, true_class)

    PCC = (TP+TN)/(TP+TN+FP+FN)

    return PCC

def confusion_matrix(predicted_class, true_class):
    TP, FP, FN, TN = 0, 0, 0, 0

    for k in range(len(true_class)):
        if predicted_class[k] == 1:
            if predicted_class[k] == true_class[k]:
                # 1 = default / negativ / schlecht
                TN += 1
            else:
                FN += 1
        else:
            if predicted_class[k] == true_class[k]:
                TP += 1
            else:
                FP += 1
    return TP, FP, FN, TN

def get_predicted_class(true_class, probability, threshold):
    predicted_class = []

    for i in range(len(probability)):
        if probability[i] >= threshold:
            predicted_class.append(1)
        else:
            predicted_class.append(0)

    return predicted_class