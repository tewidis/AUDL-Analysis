#!/usr/bin/python

import pandas as pd
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
import math
import os
import operator

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
        new_score1, new_score2 = get_elo(team_data[team1][-1], team_data[team2][-1], df.loc[idx]['Win']);
        team_data[team1].append((df.loc[idx]['Date'], new_score1));
        team_data[team2].append((df.loc[idx]['Date'], new_score2));

    # plot elo scores over time
    pd.plotting.register_matplotlib_converters();
    years = [2014, 2015, 2016, 2017, 2018, 2019];
    fig1  = plt.figure();
    fig2  = plt.figure();

    fig = {};
    axs = {};
    legends = {};
    for year in years:
        fig[year] = plt.figure();
        axs[year] = fig[year].add_axes([0,0,1,1]);
        legends[year] = [];
    ax1 = fig1.add_axes([0,0,1,1]);
    ax2 = fig2.add_axes([0,0,1,1]);

    # make a unique colormap
    styles = ['-','--',':','-.'];
    num_styles = len(styles);
    num_lines = len(np.unique(df['Name']));
    num_colors = math.ceil(num_lines/num_styles);
    cmap = plt.cm.jet(np.matlib.repmat(np.linspace(0,1,num_colors),1,num_styles));
    styles = np.matlib.repmat(styles,1,num_colors);

    ax1.set_prop_cycle(plt.cycler('color',cmap[0]) + plt.cycler('linestyle',np.sort(styles[0])));
    ax2.set_prop_cycle(plt.cycler('color',cmap[0]) + plt.cycler('linestyle',np.sort(styles[0])));
    for year in years:
        axs[year].set_prop_cycle(plt.cycler('color',cmap[0]) + plt.cycler('linestyle',np.sort(styles[0])));

    # break the list of tuples into dates and scores
    for name in np.unique(df['Name']):
        sorted_list = sorted(team_data[name], key=lambda x: x[0])
        dates  = list(zip(*sorted_list))[0];
        scores = list(zip(*sorted_list))[1];
        ax1.plot(dates, scores);
        ax2.plot(scores);

        # plot elo scores year by year
        for year in years:
            indices = [];
            for count,date in enumerate(dates):
                if date.year == year:
                    indices.append(count);

            if not indices == []:
                indices = operator.itemgetter(indices);
                axs[year].plot(indices(np.array(dates)), indices(np.array(scores)));
                legends[year].append(name);


    # add legends, labels, make the plots prettier
    anchor_point = (0.,-0.85,1.,.102);
    ax1.legend(np.unique(df['Name']), bbox_to_anchor=anchor_point, loc='lower left', \
            ncol=2, mode='expand', borderaxespad=0.);
    ax2.legend(np.unique(df['Name']), bbox_to_anchor=anchor_point, loc='lower left', \
            ncol=2, mode='expand', borderaxespad=0.);

    for year in years:
        axs[year].set_xlabel('Time');
        axs[year].set_ylabel('Elo Rating');
        axs[year].set_title(str(year) + ' Season');
        axs[year].grid(b=True,which='major',axis='both');
        axs[year].legend(legends[year],bbox_to_anchor=anchor_point, loc='lower left', \
            ncol=2, mode='expand', borderaxespad=0.);
        plt.setp(axs[year].xaxis.get_majorticklabels(), rotation=45);
        filepath = '/home/twidis/ultianalytics/plots/elo_' + str(year) + '_season.png';
        os.remove(filepath);
        fig[year].savefig(filepath, bbox_inches='tight');
        plt.close(fig[year]);

    # set xlabels
    ax1.set_xlabel('Time');
    ax2.set_xlabel('Time');

    # set ylabels
    ax1.set_ylabel('Elo Rating');
    ax2.set_ylabel('Elo Rating');

    # set titles
    ax1.set_title('Elo Scores Across Seasons');
    ax2.set_title('Elo Scores');

    # turn on grids
    ax1.grid(b=True,which='major',axis='both');
    ax2.grid(b=True,which='major',axis='both');

    # save the figures
    filepath1 = '/home/twidis/ultianalytics/plots/elo_scores_over_time.png';
    filepath2 = '/home/twidis/ultianalytics/plots/elo_scores.png';
    os.remove(filepath1);
    os.remove(filepath2);

    fig1.savefig(filepath1, bbox_inches='tight');
    fig2.savefig(filepath2, bbox_inches='tight');

    plt.close(fig1);
    plt.close(fig2);

def get_elo(score1, score2, team1_win):
    # function that takes in two elo scores and who won and returns updated scores
    qa = 10**(score1[1]/400);
    qb = 10**(score2[1]/400);

    ea = qa/(qa+qb);
    eb = qb/(qa+qb);

    ra = score1[1] + 32*(team1_win - ea);
    #rb = score2[1] + 32*({"0":1, "1":0}[str(team1_win)] - eb);
    rb = score2[1] + 32*(~team1_win + 2 - eb);

    return ra, rb;

if __name__ == '__main__':
    main();
