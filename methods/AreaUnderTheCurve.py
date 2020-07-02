from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt



def area_under_the_curve_and_roc_curve(true_class, probability):
    auc = roc_auc_score(true_class, probability)
    #fpr = x, tpr = y
    fpr, tpr, thresholds = roc_curve(true_class, probability)

    # plt.plot(fpr,tpr, color = 'orange', label='ROC curve (area =)' + str(auc))
    # plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic example')
    # plt.legend(loc="lower right")
    # plt.show()
    return auc, fpr, tpr

# true_class = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
# probability = [0, 0.1, 0.1, 0.15, 0.2, 0.2, 0.25, 0.2, 0.3, 0.3,
#                0.35, 0.4, 0.45, 0.5, 0.5, 0.55, 0.6, 0.6, 0.65, 0.7,
#                0.7, 0.75, 0.8, 0.8, 0.85, 0.9, 0.9, 0.9, 0.95, 0.99]
# area_under_the_curve_and_roc_curve(true_class, probability)