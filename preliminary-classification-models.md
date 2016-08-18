---
layout: page
title: Preliminary Classification Models
---

### Supervised Learning Evaluation

It is assumed that all code in the Text Data Processing section of the website has been run prior to any of the supervised learning code below. 

The code below evaluates multiple linear models, specifically, a logistic regression (with L1 and L2 penalization), linear support vector machine, and a ridge classifier.  All text in the reviews are evaluated as model features, and each definition of recall (review +/- 6 months from recall date, review +/- 1 year from recall date, review 1 year before recall date, review 6 months before recall date) is evaluated as the dependent variable.  Model accuracy, precision, recall, and F1-score is evaluated for each model/dependent variable combination using a 50% test/train split.


```python
from sklearn import svm
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

C=1  ##Note if C is too small percision/recall is zero
alpha = 1/C
classifiers = {'L1 logistic': LogisticRegression(C=C, \
                                    penalty='l1'),
               'L2 logistic (OvR)': LogisticRegression(C=C, \
                                    penalty='l2'),
               'Linear SVC': svm.SVC(kernel='linear', C=C, \
                            probability=True, random_state=0),
               'Ridge': RidgeClassifier(alpha=alpha)}

recall_defs = {'Review +/- 1 Year from recall': 'recalled_1y',
               'Review 1 year before recall' : 'recalled_1yb4', 
               'Review +/- 6 Months from recall' : 'recalled_6m', 
               'Review 6 months before recall' : 'recalled_6mb4'}


for index, (recall_descrip, recall_def) in enumerate(recall_defs.items()):
    target = np.array(Subset[recall_def])
    X_test, X_train, Y_test, Y_train = train_test_split(text_matrix, target, test_size=0.5, random_state=123)
    print("%s:" % recall_descrip)
    print("------------------------------------------------------")
    for index, (name, classifier) in enumerate(classifiers.items()):
        classifier.fit(X_train, Y_train)
        Y_pred = classifier.predict(X_test)
        print("%s:" % name)
        print("\tAccuracy: %1.3f" % accuracy_score(Y_test, Y_pred))
        print("\tPrecision: %1.3f" % precision_score(Y_test, Y_pred))
        print("\tRecall: %1.3f" % recall_score(Y_test, Y_pred))
        print("\tF1: %1.3f\n" % f1_score(Y_test, Y_pred))
```

    Review +/- 1 Year from recall:
    ------------------------------------------------------
    L2 logistic (OvR):
    	Accuracy: 0.853
    	Precision: 0.630
    	Recall: 0.371
    	F1: 0.467
    
    L1 logistic:
    	Accuracy: 0.849
    	Precision: 0.614
    	Recall: 0.343
    	F1: 0.440
    
    Linear SVC:
    	Accuracy: 0.818
    	Precision: 0.473
    	Recall: 0.442
    	F1: 0.457
    
    Ridge:
    	Accuracy: 0.840
    	Precision: 0.563
    	Recall: 0.353
    	F1: 0.434
    
    Review 6 months before recall:
    ------------------------------------------------------
    L2 logistic (OvR):
    	Accuracy: 0.948
    	Precision: 0.233
    	Recall: 0.056
    	F1: 0.091
    
    L1 logistic:
    	Accuracy: 0.947
    	Precision: 0.174
    	Recall: 0.045
    	F1: 0.072
    
    Linear SVC:
    	Accuracy: 0.923
    	Precision: 0.120
    	Recall: 0.107
    	F1: 0.113
    
    Ridge:
    	Accuracy: 0.942
    	Precision: 0.102
    	Recall: 0.034
    	F1: 0.051
    
    Review +/- 6 Months from recall:
    ------------------------------------------------------
    L2 logistic (OvR):
    	Accuracy: 0.920
    	Precision: 0.378
    	Recall: 0.129
    	F1: 0.193
    
    L1 logistic:
    	Accuracy: 0.920
    	Precision: 0.384
    	Recall: 0.133
    	F1: 0.197
    
    Linear SVC:
    	Accuracy: 0.896
    	Precision: 0.258
    	Recall: 0.220
    	F1: 0.238
    
    Ridge:
    	Accuracy: 0.919
    	Precision: 0.364
    	Recall: 0.126
    	F1: 0.187
    
    Review 1 year before recall:
    ------------------------------------------------------
    L2 logistic (OvR):
    	Accuracy: 0.888
    	Precision: 0.451
    	Recall: 0.210
    	F1: 0.287
    
    L1 logistic:
    	Accuracy: 0.887
    	Precision: 0.438
    	Recall: 0.203
    	F1: 0.277
    
    Linear SVC:
    	Accuracy: 0.860
    	Precision: 0.334
    	Recall: 0.319
    	F1: 0.326
    
    Ridge:
    	Accuracy: 0.881
    	Precision: 0.380
    	Recall: 0.184
    	F1: 0.248
    


### Key Words and Performance of Linear SVM

We mostly care about the recall measure (the % of recalled product reviews identified), given that our data are imbalanced. Therefore, Linear SVM with the review being +/- 1 year from the recall performed the best.  The code below explores the keywords that are coming out of the model and its overall performance.

The first step is to use cross validation with 20 folds.  Each fold contains different product IDs, which will tell us if the model is generalizable across products.  For each CV, we look at the top 10 most predictive words.


```python
##Cross validation with test/train samples that have different products to see if model is product specific
from sklearn.cross_validation import LabelKFold

model = svm.SVC(kernel='linear', C=C, probability=True, random_state=0)
target = np.array(Subset.recalled_1y)

term_names = vectorizer.get_feature_names()
term_names = pd.DataFrame(term_names, columns=['Term'])

labels = np.array(Subset.asin)
lkf_1 = LabelKFold(labels, n_folds=20)
recalled_asins = Subset[(Subset.recalled_1y == 1)].asin.unique()


for index, (test, train) in enumerate(lkf_1):
    results = model.fit(text_matrix[train], target[train])
    Y_pred = model.predict(text_matrix[test])
    
    results_coef_array = np.transpose(results.coef_).todense()
    results_df_coef = pd.DataFrame(results_coef_array,columns=['Coef'])
    results_df_coef = pd.concat([term_names, results_df_coef],axis = 1)
    results_df_coef = results_df_coef.sort_values(by='Coef',ascending=False)
    results_df_coef = results_df_coef[results_df_coef.Coef>0]
    
    print("CV #%d Train Set Stats" % (index+1))
    print("  Size of Train Set: %d" % len(target[train]))
    print("  Unique products in Train Set: %d" \
          % len(np.unique(labels[train])))
    print("  Unique recalled products in Train Set: %d" \
          % len(pd.merge(pd.DataFrame(recalled_asins, columns=['asin']), \
            pd.DataFrame(np.unique(labels[train]), columns=['asin']), \
            how = 'inner', on = ['asin'])))
    print("  Recalls in Train Set: %d" % target[train].sum())

    print(' ')
    print("CV #%d Test Set Stats" % (index+1))   
    print("  Size of Test Set: %d" % len(target[test]))
    print("  Unique products in Test Set: %d" \
          % len(np.unique(labels[test])))
    print("  Unique recalled products in Test Set: %d" \
          % len(pd.merge(pd.DataFrame(recalled_asins, columns=['asin']), \
            pd.DataFrame(np.unique(labels[test]), columns=['asin']), \
            how = 'inner', on = ['asin'])))
    print("  Predicted Recalls in Test Set: %d" % Y_pred.sum())
    print("  Actual Recalls in Test Set: %d" % target[test].sum())
    print(' ')
    print("CV #%d Performance" % (index+1))
    print("  Accuracy: %1.3f" % accuracy_score(target[test], Y_pred))
    print("  Precision: %1.3f" % precision_score(target[test], Y_pred))
    print("  Recall: %1.3f" % recall_score(target[test], Y_pred))
    print("  F1: %1.3f\n" % f1_score(target[test], Y_pred))
    print(' ')
    print("Top 10 words predictive words")
    print(results_df_coef.head(n=10))
    print(' ')
```

    CV #1 Train Set Stats
      Size of Train Set: 389
      Unique products in Train Set: 224
      Unique recalled products in Train Set: 4
      Recalls in Train Set: 166
     
    CV #1 Test Set Stats
      Size of Test Set: 7375
      Unique products in Test Set: 5062
      Unique recalled products in Test Set: 115
      Predicted Recalls in Test Set: 1064
      Actual Recalls in Test Set: 1118
     
    CV #1 Performance
      Accuracy: 0.754
      Precision: 0.174
      Recall: 0.165
      F1: 0.170
    
     
    Top 10 words predictive words
             Term      Coef
    6986    plain  0.643978
    1832  coconut  0.609174
    4773     item  0.556434
    9499    thumb  0.486011
    4564       in  0.484629
    6121      nat  0.477798
    3498     food  0.469390
    4597  individ  0.428531
    3108    evalu  0.411243
    9805      two  0.400804
     
    CV #2 Train Set Stats
      Size of Train Set: 389
      Unique products in Train Set: 230
      Unique recalled products in Train Set: 6
      Recalls in Train Set: 165
     
    CV #2 Test Set Stats
      Size of Test Set: 7375
      Unique products in Test Set: 5056
      Unique recalled products in Test Set: 113
      Predicted Recalls in Test Set: 998
      Actual Recalls in Test Set: 1119
     
    CV #2 Performance
      Accuracy: 0.760
      Precision: 0.174
      Recall: 0.155
      F1: 0.164
    
     
    Top 10 words predictive words
             Term      Coef
    2101   costco  0.769557
    7406    quino  0.742111
    2419    defin  0.733503
    7407   quinoa  0.636938
    2045     cook  0.574154
    7889      run  0.512086
    10264    wash  0.417549
    10038    valu  0.416317
    3498     food  0.379617
    8850     stil  0.374893
     
    CV #3 Train Set Stats
      Size of Train Set: 389
      Unique products in Train Set: 250
      Unique recalled products in Train Set: 5
      Recalls in Train Set: 123
     
    CV #3 Test Set Stats
      Size of Test Set: 7375
      Unique products in Test Set: 5036
      Unique recalled products in Test Set: 114
      Predicted Recalls in Test Set: 756
      Actual Recalls in Test Set: 1161
     
    CV #3 Performance
      Accuracy: 0.776
      Precision: 0.177
      Recall: 0.115
      F1: 0.140
    
     
    Top 10 words predictive words
              Term      Coef
    1996   consist  0.667266
    5834      milk  0.657472
    10284       we  0.620875
    1346       can  0.548840
    2176     cream  0.522619
    1083     brand  0.490847
    2465      dent  0.461844
    1832   coconut  0.449699
    3115     every  0.437067
    5619    market  0.434126
     
    CV #4 Train Set Stats
      Size of Train Set: 389
      Unique products in Train Set: 258
      Unique recalled products in Train Set: 4
      Recalls in Train Set: 103
     
    CV #4 Test Set Stats
      Size of Test Set: 7375
      Unique products in Test Set: 5028
      Unique recalled products in Test Set: 115
      Predicted Recalls in Test Set: 607
      Actual Recalls in Test Set: 1181
     
    CV #4 Performance
      Accuracy: 0.800
      Precision: 0.259
      Recall: 0.133
      F1: 0.176
    
     
    Top 10 words predictive words
            Term      Coef
    600     baby  0.996328
    8139     sel  0.629927
    4989     kid  0.598428
    5419     lov  0.588638
    6473    only  0.529569
    3626   fruit  0.495068
    6086      my  0.493271
    8222     she  0.473144
    7111   pouch  0.469734
    2347  daught  0.437825
     
    CV #5 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 258
      Unique recalled products in Train Set: 4
      Recalls in Train Set: 97
     
    CV #5 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5028
      Unique recalled products in Test Set: 115
      Predicted Recalls in Test Set: 720
      Actual Recalls in Test Set: 1187
     
    CV #5 Performance
      Accuracy: 0.793
      Precision: 0.263
      Recall: 0.159
      F1: 0.198
    
     
    Top 10 words predictive words
             Term      Coef
    600      baby  0.723933
    4038  grocery  0.609454
    8569      son  0.494482
    938     blend  0.479231
    4989      kid  0.469853
    8850     stil  0.464992
    6444      old  0.447676
    5331     list  0.418933
    6929     pict  0.405760
    6086       my  0.403557
     
    CV #6 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 267
      Unique recalled products in Train Set: 5
      Recalls in Train Set: 64
     
    CV #6 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5019
      Unique recalled products in Test Set: 114
      Predicted Recalls in Test Set: 239
      Actual Recalls in Test Set: 1220
     
    CV #6 Performance
      Accuracy: 0.810
      Precision: 0.126
      Recall: 0.025
      F1: 0.041
    
     
    Top 10 words predictive words
              Term      Coef
    6689    pancak  0.799270
    6682   pamelas  0.649828
    4887     joyce  0.617225
    10584      yes  0.617225
    7238   product  0.533800
    3582     freez  0.508464
    5149      larg  0.483808
    3848      glut  0.436407
    4000     great  0.423721
    7487      real  0.423318
     
    CV #7 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 269
      Unique recalled products in Train Set: 3
      Recalls in Train Set: 49
     
    CV #7 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5017
      Unique recalled products in Test Set: 116
      Predicted Recalls in Test Set: 274
      Actual Recalls in Test Set: 1235
     
    CV #7 Performance
      Accuracy: 0.817
      Precision: 0.285
      Recall: 0.063
      F1: 0.103
    
     
    Top 10 words predictive words
              Term      Coef
    4197  hazelnut  0.681813
    6344       nut  0.490479
    6462        on  0.443809
    8706     spoon  0.405532
    6346   nutella  0.399543
    6777       pay  0.397677
    3142     excel  0.344927
    3809      girl  0.339190
    8574       soo  0.325162
    5886   mislead  0.323780
     
    CV #8 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 270
      Unique recalled products in Train Set: 5
      Recalls in Train Set: 17
     
    CV #8 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5016
      Unique recalled products in Test Set: 114
      Predicted Recalls in Test Set: 75
      Actual Recalls in Test Set: 1267
     
    CV #8 Performance
      Accuracy: 0.821
      Precision: 0.133
      Recall: 0.008
      F1: 0.015
    
     
    Top 10 words predictive words
                Term      Coef
    6739       party  0.456949
    4078         gum  0.398979
    5789         mex  0.361307
    7398  quesodilla  0.361307
    9199        taco  0.356558
    4058    guacamol  0.352385
    6032         msg  0.349942
    9410       there  0.321707
    7362         put  0.309136
    8647   spearmint  0.278356
     
    CV #9 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 270
      Unique recalled products in Train Set: 7
      Recalls in Train Set: 58
     
    CV #9 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5016
      Unique recalled products in Test Set: 112
      Predicted Recalls in Test Set: 459
      Actual Recalls in Test Set: 1226
     
    CV #9 Performance
      Accuracy: 0.803
      Precision: 0.251
      Recall: 0.094
      F1: 0.136
    
     
    Top 10 words predictive words
              Term      Coef
    6433        oi  0.961564
    1260      busy  0.729098
    5946       mom  0.667707
    1261       but  0.651917
    226     almond  0.642181
    2231   crunchy  0.564158
    8961     stuff  0.507040
    10456     wish  0.504396
    2808       dry  0.500426
    5580      mapl  0.485255
     
    CV #10 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 271
      Unique recalled products in Train Set: 10
      Recalls in Train Set: 54
     
    CV #10 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5015
      Unique recalled products in Test Set: 109
      Predicted Recalls in Test Set: 401
      Actual Recalls in Test Set: 1230
     
    CV #10 Performance
      Accuracy: 0.804
      Precision: 0.229
      Recall: 0.075
      F1: 0.113
    
     
    Top 10 words predictive words
            Term      Coef
    1519     cer  0.643823
    613    bacon  0.591720
    8618     soy  0.496911
    5555     man  0.375558
    3241  fajita  0.366863
    2874     eat  0.364797
    8670    spic  0.351810
    5580    mapl  0.348224
    5899     mix  0.333764
    3819    glad  0.311509
     
    CV #11 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 271
      Unique recalled products in Train Set: 6
      Recalls in Train Set: 58
     
    CV #11 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5015
      Unique recalled products in Test Set: 113
      Predicted Recalls in Test Set: 360
      Actual Recalls in Test Set: 1226
     
    CV #11 Performance
      Accuracy: 0.806
      Precision: 0.211
      Recall: 0.062
      F1: 0.096
    
     
    Top 10 words predictive words
             Term      Coef
    1633     chil  0.660121
    9699      tri  0.473319
    1519      cer  0.461092
    2649   dislik  0.455082
    7344  purchas  0.422993
    1500   celery  0.419430
    1549    chang  0.389249
    2036  conveny  0.386536
    6493      opt  0.386505
    694       bas  0.377399
     
    CV #12 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 10
      Recalls in Train Set: 47
     
    CV #12 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 109
      Predicted Recalls in Test Set: 488
      Actual Recalls in Test Set: 1237
     
    CV #12 Performance
      Accuracy: 0.796
      Precision: 0.227
      Recall: 0.090
      F1: 0.129
    
     
    Top 10 words predictive words
               Term      Coef
    6032        msg  1.000000
    3145  excellent  0.745230
    8606      sourc  0.537998
    4779        its  0.531902
    2013    contain  0.524593
    7279    protein  0.520588
    3360        fin  0.450660
    1062        boy  0.412680
    3716       garl  0.406305
    63           ad  0.385837
     
    CV #13 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 4
      Recalls in Train Set: 25
     
    CV #13 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 115
      Predicted Recalls in Test Set: 102
      Actual Recalls in Test Set: 1259
     
    CV #13 Performance
      Accuracy: 0.823
      Precision: 0.275
      Recall: 0.022
      F1: 0.041
    
     
    Top 10 words predictive words
             Term      Coef
    8723   spread  0.465632
    6794   peanut  0.423991
    6344      nut  0.349848
    3279      fat  0.348197
    2445   delicy  0.343511
    10639   yummy  0.289524
    9523      tim  0.268430
    5702     mean  0.267854
    837    better  0.242513
    9727      tru  0.241437
     
    CV #14 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 6
      Recalls in Train Set: 41
     
    CV #14 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 113
      Predicted Recalls in Test Set: 244
      Actual Recalls in Test Set: 1243
     
    CV #14 Performance
      Accuracy: 0.816
      Precision: 0.266
      Recall: 0.052
      F1: 0.087
    
     
    Top 10 words predictive words
              Term      Coef
    6709    paprik  0.818070
    6515       org  0.729487
    4582    incred  0.651411
    2645      dish  0.634638
    1261       but  0.465584
    6794    peanut  0.431389
    7364      puts  0.388632
    8684      spin  0.388632
    6882     pesto  0.375296
    7969  sandwich  0.343811
     
    CV #15 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 5
      Recalls in Train Set: 32
     
    CV #15 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 114
      Predicted Recalls in Test Set: 152
      Actual Recalls in Test Set: 1252
     
    CV #15 Performance
      Accuracy: 0.825
      Precision: 0.375
      Recall: 0.046
      F1: 0.081
    
     
    Top 10 words predictive words
                Term      Coef
    7111       pouch  0.383170
    2347      daught  0.368011
    600         baby  0.363433
    6086          my  0.362551
    8606       sourc  0.308532
    9265       taste  0.305324
    517    astronaut  0.291228
    9514        tidy  0.291228
    10278     watery  0.268642
    10114       very  0.268244
     
    CV #16 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 7
      Recalls in Train Set: 44
     
    CV #16 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 112
      Predicted Recalls in Test Set: 305
      Actual Recalls in Test Set: 1240
     
    CV #16 Performance
      Accuracy: 0.804
      Precision: 0.167
      Recall: 0.041
      F1: 0.066
    
     
    Top 10 words predictive words
              Term      Coef
    4844     jerky  0.974670
    5261       lic  0.764621
    1633      chil  0.744819
    8551      some  0.514372
    5605   marinad  0.509972
    5530       mak  0.439006
    10586      yet  0.436447
    3342       fig  0.390573
    5342       liv  0.343880
    911      black  0.335236
     
    CV #17 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 7
      Recalls in Train Set: 33
     
    CV #17 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 112
      Predicted Recalls in Test Set: 263
      Actual Recalls in Test Set: 1251
     
    CV #17 Performance
      Accuracy: 0.808
      Precision: 0.186
      Recall: 0.039
      F1: 0.065
    
     
    Top 10 words predictive words
                 Term      Coef
    4762           it  0.513479
    8362          siz  0.486057
    8575         soon  0.435465
    3804  gingerbread  0.435182
    5940       molass  0.414538
    6378         oatm  0.396393
    5951          mon  0.394277
    630           bak  0.379725
    3360          fin  0.357671
    7889          run  0.353671
     
    CV #18 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 6
      Recalls in Train Set: 43
     
    CV #18 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 113
      Predicted Recalls in Test Set: 265
      Actual Recalls in Test Set: 1241
     
    CV #18 Performance
      Accuracy: 0.814
      Precision: 0.253
      Recall: 0.054
      F1: 0.089
    
     
    Top 10 words predictive words
             Term      Coef
    6929     pict  0.873416
    7437      ram  0.479302
    1519      cer  0.461457
    7755      ric  0.386548
    8575     soon  0.350860
    2115  couldnt  0.330907
    386     anywh  0.325157
    1887      com  0.322321
    586   awesome  0.321017
    4220  healthy  0.306886
     
    CV #19 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 6
      Recalls in Train Set: 33
     
    CV #19 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 113
      Predicted Recalls in Test Set: 195
      Actual Recalls in Test Set: 1251
     
    CV #19 Performance
      Accuracy: 0.814
      Precision: 0.195
      Recall: 0.030
      F1: 0.053
    
     
    Top 10 words predictive words
              Term      Coef
    3596    friend  0.576301
    3626     fruit  0.496235
    669        bar  0.404880
    1044    bought  0.372935
    10061      veg  0.372147
    7279   protein  0.297100
    6644      pack  0.287082
    5446     lucky  0.286845
    2128   country  0.279119
    2508   dessert  0.270367
     
    CV #20 Train Set Stats
      Size of Train Set: 388
      Unique products in Train Set: 272
      Unique recalled products in Train Set: 9
      Recalls in Train Set: 32
     
    CV #20 Test Set Stats
      Size of Test Set: 7376
      Unique products in Test Set: 5014
      Unique recalled products in Test Set: 110
      Predicted Recalls in Test Set: 367
      Actual Recalls in Test Set: 1252
     
    CV #20 Performance
      Accuracy: 0.813
      Precision: 0.324
      Recall: 0.095
      F1: 0.147
    
     
    Top 10 words predictive words
             Term      Coef
    2013  contain  0.762052
    669       bar  0.596065
    1056     bowl  0.459251
    6444      old  0.451831
    4139    handy  0.437437
    3866       go  0.418665
    7016     plum  0.414938
    5779     mess  0.398847
    2874      eat  0.391601
    2445   delicy  0.383769
     


We are getting some low recall values, and it looks like product-specific terms (e.g., coconut) are getting a lot of weight in the models.  This means that our model may have a hard time being generalizable - lets look at the full model (i.e., no cross validation) to see the terms that are getting the most weight when using all products    


```python
results = model.fit(text_matrix, target)
results_coef_array = np.transpose(results.coef_).todense()
results_df_coef = pd.DataFrame(results_coef_array, columns=['Coef'])
results_df_coef = pd.concat([term_names, results_df_coef], axis = 1)
results_df_coef = results_df_coef.sort_values(by='Coef', ascending=False)
results_df_coef[results_df_coef.Coef > 0].head(n=50)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Term</th>
      <th>Coef</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3804</th>
      <td>gingerbread</td>
      <td>1.697815</td>
    </tr>
    <tr>
      <th>4921</th>
      <td>justins</td>
      <td>1.639414</td>
    </tr>
    <tr>
      <th>6709</th>
      <td>paprik</td>
      <td>1.629455</td>
    </tr>
    <tr>
      <th>7407</th>
      <td>quinoa</td>
      <td>1.571956</td>
    </tr>
    <tr>
      <th>3951</th>
      <td>granddaught</td>
      <td>1.525153</td>
    </tr>
    <tr>
      <th>3241</th>
      <td>fajita</td>
      <td>1.496793</td>
    </tr>
    <tr>
      <th>288</th>
      <td>amino</td>
      <td>1.482580</td>
    </tr>
    <tr>
      <th>7504</th>
      <td>recal</td>
      <td>1.444783</td>
    </tr>
    <tr>
      <th>10264</th>
      <td>wash</td>
      <td>1.374378</td>
    </tr>
    <tr>
      <th>4066</th>
      <td>guav</td>
      <td>1.362638</td>
    </tr>
    <tr>
      <th>8381</th>
      <td>skippy</td>
      <td>1.324039</td>
    </tr>
    <tr>
      <th>701</th>
      <td>basil</td>
      <td>1.316200</td>
    </tr>
    <tr>
      <th>7406</th>
      <td>quino</td>
      <td>1.306519</td>
    </tr>
    <tr>
      <th>8095</th>
      <td>seam</td>
      <td>1.296897</td>
    </tr>
    <tr>
      <th>1955</th>
      <td>concoct</td>
      <td>1.280640</td>
    </tr>
    <tr>
      <th>6217</th>
      <td>newton</td>
      <td>1.277910</td>
    </tr>
    <tr>
      <th>4264</th>
      <td>hent</td>
      <td>1.277887</td>
    </tr>
    <tr>
      <th>6332</th>
      <td>nugo</td>
      <td>1.252936</td>
    </tr>
    <tr>
      <th>7437</th>
      <td>ram</td>
      <td>1.234634</td>
    </tr>
    <tr>
      <th>10201</th>
      <td>vs</td>
      <td>1.229726</td>
    </tr>
    <tr>
      <th>3543</th>
      <td>foul</td>
      <td>1.216128</td>
    </tr>
    <tr>
      <th>8410</th>
      <td>slightly</td>
      <td>1.190934</td>
    </tr>
    <tr>
      <th>5288</th>
      <td>lightn</td>
      <td>1.181437</td>
    </tr>
    <tr>
      <th>32</th>
      <td>accid</td>
      <td>1.172457</td>
    </tr>
    <tr>
      <th>7016</th>
      <td>plum</td>
      <td>1.166517</td>
    </tr>
    <tr>
      <th>2945</th>
      <td>eldest</td>
      <td>1.129980</td>
    </tr>
    <tr>
      <th>6433</th>
      <td>oi</td>
      <td>1.122017</td>
    </tr>
    <tr>
      <th>4009</th>
      <td>greek</td>
      <td>1.108895</td>
    </tr>
    <tr>
      <th>1170</th>
      <td>broth</td>
      <td>1.106454</td>
    </tr>
    <tr>
      <th>10050</th>
      <td>variety</td>
      <td>1.090841</td>
    </tr>
    <tr>
      <th>9354</th>
      <td>terrible</td>
      <td>1.082349</td>
    </tr>
    <tr>
      <th>6303</th>
      <td>note</td>
      <td>1.080769</td>
    </tr>
    <tr>
      <th>9199</th>
      <td>taco</td>
      <td>1.077790</td>
    </tr>
    <tr>
      <th>7780</th>
      <td>rins</td>
      <td>1.077001</td>
    </tr>
    <tr>
      <th>2697</th>
      <td>doct</td>
      <td>1.069091</td>
    </tr>
    <tr>
      <th>5261</th>
      <td>lic</td>
      <td>1.059215</td>
    </tr>
    <tr>
      <th>509</th>
      <td>assum</td>
      <td>1.049675</td>
    </tr>
    <tr>
      <th>8014</th>
      <td>sazon</td>
      <td>1.044622</td>
    </tr>
    <tr>
      <th>2868</th>
      <td>easiest</td>
      <td>1.030123</td>
    </tr>
    <tr>
      <th>917</th>
      <td>blackstrap</td>
      <td>1.027565</td>
    </tr>
    <tr>
      <th>1931</th>
      <td>completely</td>
      <td>1.026621</td>
    </tr>
    <tr>
      <th>9512</th>
      <td>tid</td>
      <td>1.019473</td>
    </tr>
    <tr>
      <th>281</th>
      <td>america</td>
      <td>1.016342</td>
    </tr>
    <tr>
      <th>1817</th>
      <td>co</td>
      <td>1.013590</td>
    </tr>
    <tr>
      <th>10569</th>
      <td>yay</td>
      <td>1.008432</td>
    </tr>
    <tr>
      <th>4197</th>
      <td>hazelnut</td>
      <td>1.007850</td>
    </tr>
    <tr>
      <th>2305</th>
      <td>daddy</td>
      <td>1.004679</td>
    </tr>
    <tr>
      <th>801</th>
      <td>belvita</td>
      <td>1.001835</td>
    </tr>
    <tr>
      <th>2033</th>
      <td>conv</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>10662</th>
      <td>zicos</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
</div>



Terms in the model are product specific - so let's take a look at how precision (ability of the model to NOT label non-recalled products as a recalled product) and information recall (ability of the model to detect all recalled product reviews) interact. Again, cross validation is used where sets include different product IDs.


```python
##Percision Recall Curve
from sklearn.metrics import precision_recall_curve, average_precision_score
import seaborn as sns
from sklearn.cross_validation import LabelKFold
import matplotlib.pyplot as plt
%matplotlib inline

labels = np.array(Subset.asin)
lkf = LabelKFold(labels, n_folds=10)
lr = LogisticRegression(C=C, penalty='l2')

plt.figure(figsize=(10,7))

for i, (train, test) in enumerate(lkf):
    y_score = lr.fit(text_matrix[train], \
                target[train]).decision_function(text_matrix[test])
    precision, recall, _ = precision_recall_curve(target[test], y_score)
    average_precision = average_precision_score(target[test], y_score)
    plt.plot(precision, recall, lw=1, label='Curve for fold %d (area = %0.2f)' \
             % (i+1, average_precision))
    
sns.set(style="darkgrid", color_codes=True, font_scale=1.25, palette='bright')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('Precision Recall Curve - Logistic Regression with 10 CVs')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
```


![png](https://github.com/mikemunsell/DSSG2016-UnsafeFoods/gh-pages/assets/images/PrecisionRecallCurve.png)


We see that precision is driven to zero with only a slight increase in information recall.  This means that in order to identify even 20% of recalled products across product-types, we must label almost all non-recalled products as being recalled (which is not what we want!)

### Evaluate Model with Generic Terms

Among all terms that were predictive of a recalled product review, there was a subset of terms that were in line with foodborne-illness symptoms and food-spoilage.  These terms were pulled out and the model was re-evaluated in order to see the performance with only these therms.


```python
##Create Word List that only includes non-product specific terms

word_list = ['detect', 'deceiv', 'recal', 'unus', 'foul', 'gassy', 'vomit', 'tummy', 'horr', 'horrend', 'disbeliev', 'hesit', 'annoy', \
'lie', 'distress', 'projectil', 'intestin', 'bitter',  'complaint', 'bad', 'urin', 'ridic', 'gross', \
'frust', 'rot', 'runny', 'terrible', 'unfortun', 'waste', 'throw', 'sour', 'batch', 'misl', 'mislead', 'unsatisfy', 'puk', \
'watery', 'lousy', 'wrong', 'undrinkable', 'stinky', 'bacter', 'wtf', 'celiac', 'parasit', 'discomfort' \
'nausea', 'naus', 'nause', 'pung', 'label', 'ingest', 'sick', 'throwing', 'dislik', 'defect', 'indescrib',\
'screwed', 'fridg', 'diogns', 'decad', 'flourless', 'dissatisfy', 'infect', 'disgruntl', 'disgusting', 'disgust',\
'rancid', 'cramp', 'nasty', 'underflav', 'allerg', 'nondairy', 'burnt', 'toss', 'yuck', 'awful', 'funny', 'victim', \
'queasy', 'mush', 'dissapoint', 'alarmingly', 'gluten', 'esophag', 'cloudy', 'unsuspect'] 

vectorizer_subset = CountVectorizer(binary=False, ngram_range=(1, 1), vocabulary=word_list)
text_matrix2 = vectorizer_subset.fit_transform(final_text)
```


```python
##Plot summation of features vs. classification
import scipy
from scipy.sparse import coo_matrix
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

vectorizer_excludeRecallkeywords = CountVectorizer(binary=False, ngram_range=(1, 1), stop_words=word_list)
food_review_text_sum = vectorizer_excludeRecallkeywords.fit_transform(final_text)
food_review_text_sum = scipy.sparse.coo_matrix.sum(food_review_text_sum, axis=1)
counts_recallwords = scipy.sparse.coo_matrix.sum(text_matrix2, axis=1)
df_for_graph = pd.concat([pd.DataFrame(counts_recallwords, columns=['recallWords']), \
                          pd.DataFrame(food_review_text_sum, columns=['otherWords']),\
                          pd.DataFrame(target, columns=['target'])], axis=1)


sns.set(style="darkgrid", color_codes=True, font_scale=1.25, palette='bright')
plt.xlim(-0.1,15)
plt.ylim(-0.1, 600)
plt.title('Recall Keywords vs. All Other Words')
plt.xlabel('Sum of Recall Keyword Frequency')
plt.ylabel('Sum of All Other Words Frequency')
plt.scatter(df_for_graph[df_for_graph.target==1].recallWords, df_for_graph[df_for_graph.target==1].otherWords,\
            marker='o', c='g', label='Recalled')
plt.scatter(df_for_graph[df_for_graph.target==0].recallWords, df_for_graph[df_for_graph.target==0].otherWords,\
            marker='o', c='b', label='Not Recalled')
plt.tight_layout()
plt.legend(bbox_to_anchor=(1, 1), loc=2)
```






![png](https://github.com/mikemunsell/DSSG2016-UnsafeFoods/gh-pages/assets/images/Classification.png)



```python
##Test model using cross validation 
from sklearn import cross_validation
target = np.array(Subset.recalled_1y)

scores = cross_validation.cross_val_score(model, text_matrix2, target, cv=50)
print("Mean Model Accuracy with 50 CV: %0.5f (+/- %0.5f)" % (scores.mean(), scores.std() * 2))

text_matrix2test, text_matrix2train, Y_test, Y_train = train_test_split(text_matrix2, target, test_size=0.5, random_state=123)
model.fit(text_matrix2train, Y_train)
Y_pred = model.predict(text_matrix2test)
print("Precision: %1.3f" % precision_score(Y_test, Y_pred))
print("Recall: %1.3f" % recall_score(Y_test, Y_pred))
print("F1: %1.3f\n" % f1_score(Y_test, Y_pred))
```

    Mean Model Accuracy with 50 CV: 0.83270 (+/- 0.01640)
    Precision: 0.378
    Recall: 0.025
    F1: 0.047
    



```python
from sklearn.metrics import roc_curve, auc
from scipy import interp
sns.set(style="darkgrid", color_codes=True, font_scale=1.25, palette='bright')

# Run classifier with cross-validation and plot ROC curves
mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(lkf):
    probas_ = lr.fit(text_matrix2[train], target[train]).predict_proba(text_matrix2[test])
    # Compute ROC curve and area the curve
    fpr, tpr, thresholds = roc_curve(target[test], probas_[:, 1])
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i+1, roc_auc))

plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

mean_tpr /= len(lkf)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

plt.xlim([0.0, 1.05])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic - Logistic Regression with 10 CVs')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.show()
```


![png](https://github.com/mikemunsell/DSSG2016-UnsafeFoods/gh-pages/assets/images/ROC.png)


The ROC curve demonstrates that the model with generic terms is only approximatley 50% accurate when evaluating across products.

### Non-linear Model

The code below tests whether the same challenges above (low identification of recall, product-specific terms occur with a non-linear model)


```python
##Random Forest
from sklearn.ensemble import RandomForestClassifier
target = np.array(Subset.recalled_1y)

rfc = RandomForestClassifier(n_estimators=200, criterion='entropy')
nonlinear_results = rfc.fit(text_matrix, target)
```


```python
##Find Important Terms
importance = np.transpose(nonlinear_results.feature_importances_)
importance_df = pd.DataFrame(importance, columns=['Importance'])
importance_df = pd.concat([term_names, importance_df], axis = 1)
importance_df = importance_df.sort_values(by='Importance', ascending=False)
importance_df[importance_df.Importance > 0].head(n=20)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Term</th>
      <th>Importance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1832</th>
      <td>coconut</td>
      <td>0.017936</td>
    </tr>
    <tr>
      <th>7406</th>
      <td>quino</td>
      <td>0.011562</td>
    </tr>
    <tr>
      <th>9297</th>
      <td>tea</td>
      <td>0.009681</td>
    </tr>
    <tr>
      <th>1840</th>
      <td>coff</td>
      <td>0.008188</td>
    </tr>
    <tr>
      <th>7111</th>
      <td>pouch</td>
      <td>0.006762</td>
    </tr>
    <tr>
      <th>10269</th>
      <td>wat</td>
      <td>0.005521</td>
    </tr>
    <tr>
      <th>5419</th>
      <td>lov</td>
      <td>0.005250</td>
    </tr>
    <tr>
      <th>3895</th>
      <td>good</td>
      <td>0.005139</td>
    </tr>
    <tr>
      <th>7407</th>
      <td>quinoa</td>
      <td>0.004978</td>
    </tr>
    <tr>
      <th>9264</th>
      <td>tast</td>
      <td>0.004937</td>
    </tr>
    <tr>
      <th>5294</th>
      <td>lik</td>
      <td>0.004822</td>
    </tr>
    <tr>
      <th>7237</th>
      <td>produc</td>
      <td>0.004637</td>
    </tr>
    <tr>
      <th>3419</th>
      <td>flav</td>
      <td>0.004578</td>
    </tr>
    <tr>
      <th>10006</th>
      <td>us</td>
      <td>0.004496</td>
    </tr>
    <tr>
      <th>3995</th>
      <td>gre</td>
      <td>0.004316</td>
    </tr>
    <tr>
      <th>2874</th>
      <td>eat</td>
      <td>0.003891</td>
    </tr>
    <tr>
      <th>6462</th>
      <td>on</td>
      <td>0.003863</td>
    </tr>
    <tr>
      <th>6794</th>
      <td>peanut</td>
      <td>0.003759</td>
    </tr>
    <tr>
      <th>9459</th>
      <td>this</td>
      <td>0.003620</td>
    </tr>
    <tr>
      <th>1261</th>
      <td>but</td>
      <td>0.003578</td>
    </tr>
  </tbody>
</table>
</div>




```python
##Statistics of the model
X_test, X_train, Y_test, Y_train = train_test_split(text_matrix, target, test_size=0.5, random_state=123)
rfc.fit(X_train, Y_train)
Y_pred = rfc.predict(X_test)
print("\tAccuracy: %1.3f" % accuracy_score(Y_test, Y_pred))
print("\tPrecision: %1.3f" % precision_score(Y_test, Y_pred))
print("\tRecall: %1.3f" % recall_score(Y_test, Y_pred))
print("\tF1: %1.3f\n" % f1_score(Y_test, Y_pred))
```

    	Accuracy: 0.841
    	Precision: 0.788
    	Recall: 0.116
    	F1: 0.202
    


As we can see, non-linear models also have the challenge of identifying product-specific terms and having a low proportion of recalls identified.
