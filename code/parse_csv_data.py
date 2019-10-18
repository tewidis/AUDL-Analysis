import subprocess
import csv
import pandas as pd
import numpy as np

def main():
    # get a list of the csv files
    files = subprocess.check_output(["find", "/home/twidis/ultianalytics/data/", "-iname", "*csv"]);
    files = files.split();

    # loop over the files and process the data
    write_header = True;
    for curr_file in files:
        curr_file = str(curr_file);
        curr_file = curr_file[2:len(curr_file)-1];

        if curr_file == '/home/twidis/ultianalytics/data/combined_data.csv':
            continue;

        data = pd.read_csv(curr_file, usecols=['Date/Time','Opponent','Line','Our Score - End of Point','Their Score - End of Point', 'Action', 'Hang Time (secs)'], index_col=False);
        data.columns = ['Date','Opponent','Line','TeamScore','OppScore','Action','HangTime'];
        game_dates = data.Date.unique();

        for ii in range(len(game_dates)):
            game_data = process_game_dataframe(data[data.Date==game_dates[ii]], curr_file[len('/home/twidis/ultianalytics/data/'):-4]);
            if ii == 0:
                season_data = game_data;
            else:
                season_data = pd.concat([season_data, game_data]);

        # write the data to a combined file so we don't have to reread all data
        if write_header:
            season_data.to_csv('/home/twidis/ultianalytics/data/combined_data.csv',mode='a',index=False);
            write_header = False;
        else:
            season_data.to_csv('/home/twidis/ultianalytics/data/combined_data.csv',mode='a',index=False,header=False);


def process_game_dataframe(df, name):
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
    throws = catches + drops;
    turns = throwaways + drops;
    if not hang_times == []:
        avg_hangtime = np.mean(hang_times);
    else:
        avg_hangtime = 6;
    avg_throws_per_score = throws/goals;
    completion_percentage = catches/throws;
    throwing_percentage = (throws-throwaways)/throws;
    catching_percentage = (catches-drops)/catches;

    if goals > goals_against:
        win = 1;
    else:
        win = 0;

    # build up a new dataframe to return with the statistics for this game
    game_data = pd.DataFrame(columns=['Name','Opponent','Goals','GoalsAgainst','Throws','Catches','Turnovers','Forced_Turns','AvgHangTime','AvgThrowsPerScore','CompletionPct','ThrowingPct','CatchingPct','Win']);
    game_data.loc[0] = [name,opponent,goals,goals_against,throws,catches,turns,forced_turns,avg_hangtime,avg_throws_per_score,completion_percentage,throwing_percentage,catching_percentage,win];

    return game_data;

if __name__ == "__main__":
    main();
