# Toxic comment analysis I
In this project, I implemented the Long-short-term-memory (LSTM) Neural network to analysis half million Wikipedia comments' toxicity, which was originaly raised up by Jigsaw and Google through this kaggle competition:
(https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge#description)  
Detailed explainations for each section are written in the notebooks.

## 1. Notebook of LSTM implementation and exploratory data analysis
https://github.com/hhzzxx957/toxic_comment/blob/master/codes/improved-lstm-baseline-glove-dropout.ipynb

## 2. Examples about Ensemble modeling
Here are the example codes used in the kaggle competition, input files are not included.
### (1) Out-of-fold (OOF) stacking
https://github.com/hhzzxx957/toxic_comment/blob/master/codes/oof_stack_regime.ipynb
### (2) Geomean and wighted average
https://github.com/hhzzxx957/toxic_comment/blob/master/codes/geomean.ipynb

## 3. A simple website to test comment's toxicity
http://hzx957.pythonanywhere.com/  
This is a test website built by python Flask, the toxicity prediction is based on the pretrained LSTM model. All source codes about the website is included in the websitecode folder.

# Toxic comment analysis II
To solve the identity bias problem, Jigsaw and Google proposed another competition on Kaggle in 2019, the number of comments has increased to 2 million.  
(https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification/overview/description)  
In this project, I used state-of-art NLP technique BERT to analysis Wikipedia comments' toxicity.

## 1. Notebook of BERT implementation
https://github.com/hhzzxx957/toxic_comment/blob/master/codes/toxic-bert.ipynb
## 2. Blender
Blender of BERT, GPT2 and LSTM for final submission
https://github.com/hhzzxx957/toxic_comment/blob/master/codes/BERT%20%2BGPT2%2B%20LSTM%20(final%20blender).ipynb

# Disclaimer
The codes and content are purely informative and none of the information provided constitutes any recommendation regarding any security, transaction or investment strategy for any specific person. The implementation described in the notebook could be risky and the market condition could be volatile and differ from the period covered above. All trading strategies and tools are implemented at the users’ own risk.
