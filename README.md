# AUDL Analysis
> Predicting Performance of American Ultimate Disc League Teams

Inspired by the FiveThirtyEight model developed to rank and predict MLB teams,
I wanted to develop a similar model that could be applied to ultimate teams,
specifically teams in the AUDL. I found that
[ultianalytics.com](www.ultianalytics.com) has recorded
statistics on each team since the genesis of the league in 2014, so there was
plenty of data for training and testing models.

The FiveThirtyEight model uses a modified Elo algorithm (created to rank chess
players)for rating teams and predicting winners. Their model incorporates
additional features, such as home field advantage, distance the team travels,
amount of rest, and the starting pitcher, to award and deduct additional points
before each game. For example, their analysis suggests that home field
advantage is worth 24 additional points. A complete explanation of their model
is available at
[fivethirtyeight.com/methodology/how-our-mlb-predictions-work](fivethirtyeight.com/methodology/how-our-mlb-predictions-work).

## Gathering and Cleaning Data
After writing bash scripts that used cURL to download all of the data from
ultianalytics, I realized that many of the csv files referred to the same teams
by slightly different names (new_york_empire vs ny_empire) which would make
analysis difficult. I wrote a script to clean the data that resolved all of
these naming issues. Additionally, I used pandas to create a dataframe capturing
statistics not present in the raw data, such as average pull time, number of
turnovers, drops, completion percentage, average throws per score, etc.

## Developing Models to Predict a Winner
Once the data had been cleaned and combined into one file, I wanted to
experiment with different models that used the statistics I calculated to
classify the game as a win or a loss. I created linear, logistic, lasso,
XGBoost, and SVM models that predicted based on the following set of input
features:
* Throws
* Catches
* Turnovers
* Forced Turnovers
* Average Pull Hang Time
* Average Throws per Score
* Completion Percentage
* Throwing Percentage
* Catching Percentage
Throwing and catching percentage are used to capture whether a turnover was
attributed to a throwaway or a dropped pass.
I found that my XGBoost model performed the best, successfully classifying a
game as a win or loss 81.42% of the time. The feature importances for the model
are shown below.
![alt text](https://github.com/tewidis/AUDL-Analysis/blob/master/plots/feature_importances_xgboost.png
"Features Importances")
The relative importance of different features used in the decision trees can be
used to inform my Elo model later. For example, teams that generate many
turnovers might be awarded additional points going into a game since forced
turnovers is of high importance in the model.

## Creating an Elo Ranking System
Elo Scores
![alt text](https://github.com/tewidis/AUDL-Analysis/blob/master/plots/elo_scores.png
"Elo Scores")

Elo Scores Over Time
![alt
text](https://github.com/tewidis/AUDL-Analysis/blob/master/plots/elo_scores_over_time.png
"Elo Scores Over Time")

Plots of Elo scores for each season are also included in the plots folder of
this repository.

## Future Work
* Incorpoate mean reversion calculation after each season
* Calculate a predicted winner before each game and evaluate how often the
  model is correct
* Begin incorporating other features into the model (home field advantage, etc)

## Conclusion
Through this project, I became more familiar with using common data science
libraries such as pandas, numpy, and scikit-learn for processing data and
developing models. Additionally, I learned about some of the math behind the
Elo algorithm and how the difference in rating between two opponents translates
to a probability. This project also served as an exercise in data visualization
using matplotlib's plotting features.
