import subprocess
import csv
import pandas as pd
import numpy as np

def main():
    seasons = [2014, 2015, 2016, 2017, 2018, 2019];
    for season in seasons:
        process_season("/home/twidis/ultianalytics/data/" + str(season) + "/", season);
        print("{} season completed".format(str(season)));

    # combine all of the seasons into one csv
    df = [];
    for season in seasons:
        df.append(pd.read_csv("/home/twidis/ultianalytics/data/" + str(season) + "/combined_data.csv"));

    all_data = pd.concat(df, ignore_index=True);
    all_data.to_csv('/home/twidis/ultianalytics/data/all_data.csv',mode='a',index=False);

def process_season(filepath, year):
    # get a list of the csv files
    files = subprocess.check_output(["find", filepath, "-iname", "*csv"]);
    files = files.split();

    # loop over the files and process the data
    write_header = True;
    for curr_file in files:
        curr_file = str(curr_file);
        curr_file = curr_file[2:len(curr_file)-1];

        if curr_file == filepath + 'combined_data.csv':
            continue;

        data = pd.read_csv(curr_file, usecols=['Date/Time','Opponent','Line','Our Score - End of Point','Their Score - End of Point', 'Action', 'Hang Time (secs)'], index_col=False);
        data.columns = ['Date','Opponent','Line','TeamScore','OppScore','Action','HangTime'];
        game_dates = data.Date.unique();

        for ii in range(len(game_dates)):
            game_data = process_game_dataframe(data[data.Date==game_dates[ii]], curr_file[len(filepath):-4], year);
            if ii == 0:
                season_data = game_data;
            else:
                season_data = pd.concat([season_data, game_data]);

        # write the data to a combined file so we don't have to reread all data
        if write_header:
            season_data.to_csv(filepath + 'combined_data.csv',mode='a',index=False);
            write_header = False;
        else:
            season_data.to_csv(filepath + 'combined_data.csv',mode='a',index=False,header=False);


def process_game_dataframe(df, name, year):
    # initialize some variables
    goals = df.TeamScore.iloc[-1];
    goals_against = df.OppScore.iloc[-1];
    opponent = df.Opponent.iloc[-1].replace(' ', '_').lower();
    hang_times = [];
    catches = 0;
    turns = 0;
    forced_turns = 0;
    drops = 0;
    throwaways = 0;

    # loop over the actions in the game to classify them
    for ii in range(len(df)):
        idx = ii + df.index[0];
        if df.Action[idx] == 'Pull':
            if not np.isnan(df.HangTime[idx]):
                hang_times.append(df.HangTime[idx]);
        elif df.Action[idx] == 'Throwaway':
            throwaways = throwaways + 1;
        elif df.Action[idx] == 'Catch':
            catches = catches + 1;
        elif df.Action[idx] == 'D':
            forced_turns = forced_turns + 1;
        elif df.Action[idx] == 'Drop':
            drops = drops + 1;

    # calculate the derived statistics
    throws = catches + drops + forced_turns + throwaways;
    turns = throwaways + drops;
    if not hang_times == []:
        avg_hangtime = np.mean(hang_times);
    else:
        avg_hangtime = 6;

    avg_throws_per_score  = throws/goals;
    completion_percentage = catches/throws;
    throwing_percentage   = throws/(throws+throwaways);
    catching_percentage   = catches/(catches+drops);

    if goals > goals_against:
        win = 1;
    else:
        win = 0;

    # build up a new dataframe to return with the statistics for this game
    game_data = pd.DataFrame(columns=['Year','Name','Opponent','Goals','GoalsAgainst','Throws','Catches','Turnovers','Forced_Turns','AvgHangTime','AvgThrowsPerScore','CompletionPct','ThrowingPct','CatchingPct','Win']);
    game_data.loc[0] = [year,name,opponent,goals,goals_against,throws,catches,turns,forced_turns,avg_hangtime,avg_throws_per_score,completion_percentage,throwing_percentage,catching_percentage,win];

    return game_data;

if __name__ == "__main__":
    main();
