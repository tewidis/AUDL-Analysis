#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def main():
    df = pd.read_csv('/home/twidis/ultianalytics/data/cleaned_data.csv');
    df['Date'] = pd.to_datetime(df['Date']);

    # initialize all teams to a starting score of 1500
    team_data = {};
    for name in np.unique(df['Name']):
        team_data[name] = [(min(df[df['Name'] == name]['Date']), 1500)];

    # iterate over the data and update elo scores based on who wins and loses
    for idx in range(len(df)):
        team1 = df.loc[idx]['Name'];
        team2 = df.loc[idx]['Opponent'];
        new_score1, new_score2 = get_elo(team_data[team1][-1], team_data[team2][-1], 0);
        team_data[team1].append((df.loc[idx]['Date'], new_score1));
        team_data[team2].append((df.loc[idx]['Date'], new_score2));

    # plot elo scores over time
    pd.plotting.register_matplotlib_converters();
    fig1 = plt.figure();
    fig2 = plt.figure();
    ax1  = fig1.add_axes([0,0,1,1]);
    ax2  = fig2.add_axes([0,0,1,1]);

    # break the list of tuples into dates and scores
    for name in np.unique(df['Name']):
        sorted_list = sorted(team_data[name], key=lambda x: x[0])
        dates  = list(zip(*sorted_list))[0];
        scores = list(zip(*sorted_list))[1];
        ax1.plot(dates, scores);
        ax2.plot(scores);

    # add legends, labels, make the plots prettier
    ax1.legend(np.unique(df['Name']), bbox_to_anchor=(0.,1.02,1.,.102), loc='lower left', \
            ncol=2, mode='expand', borderaxespad=0.);
    ax2.legend(np.unique(df['Name']), bbox_to_anchor=(0.,1.02,1.,.102), loc='lower left', \
            ncol=2, mode='expand', borderaxespad=0.);
    ax1.set_xlabel('Time');
    ax2.set_xlabel('Time');
    ax1.set_ylabel('Elo Rating');
    ax2.set_ylabel('Elo Rating');

    # save the figures
    filepath1 = '/home/twidis/ultianalytics/plots/elo_scores_over_time.png';
    filepath2 = '/home/twidis/ultianalytics/plots/elo_scores.png';
    os.remove(filepath1);
    os.remove(filepath2);
    fig1.savefig(filepath1, bbox_inches='tight');
    fig2.savefig(filepath2, bbox_inches='tight');


def get_elo(score1, score2, team1_win):
    # function that takes in two elo scores and who won and returns updated scores
    qa = 10**(score1[1]/400);
    qb = 10**(score2[1]/400);

    ea = qa/(qa+qb);
    eb = qb/(qa+qb);

    ra = score1[1] + 32*(team1_win - ea);
    rb = score2[1] + 32*({"0":1, "1":0}[str(team1_win)] - eb);

    return ra, rb;

if __name__ == '__main__':
    main();
