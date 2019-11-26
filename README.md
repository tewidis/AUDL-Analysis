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

## Continued Efforts
* Incorpoate mean reversion calculation after each season
* Incorporate home team advantage adjustment
* Calculate a predicted winner before each game and evaluate how often the
  model is correct
* Begin incorporating other features into the model

## Conclusion
Through this project, I became more familiar with using common data science
libraries such as pandas, numpy, and scikit-learn for processing data and
developing models. Additionally, I learned about some of the math behind the
Elo algorithm and how the difference in rating between two opponents translates
to a probability. This project
