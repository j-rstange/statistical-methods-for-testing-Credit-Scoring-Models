from methods import HMeasure as hm, BrierScore as bs, ProcentCorrectClassified as pcc, \
    KolmogorovSmirnov as ks, AreaUnderTheCurve as auc, PartialGiniCoefficient as pg

true_class = [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
probability = [0, 0.1, 0.1, 0.15, 0.2, 0.2, 0.25, 0.2, 0.3, 0.3,
               0.35, 0.4, 0.45, 0.5, 0.5, 0.55, 0.6, 0.6, 0.65, 0.7,
               0.7, 0.75, 0.8, 0.8, 0.85, 0.9, 0.9, 0.9, 0.95, 0.99]
threshold = 0.4

print(hm.h_measure(true_class, probability))
print(bs.brier_score(true_class, probability))
print(pcc.procent_correct_classified(true_class, probability, threshold))
print(ks.kolmogorov_smirnov_score_and_curve(true_class,probability))
print(auc.area_under_the_curve_and_roc_curve(true_class, probability))
print(pg.partial_gini_coefficient(true_class, probability, 1))



