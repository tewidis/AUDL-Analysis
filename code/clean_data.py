#!/usr/bin/python

import pandas as pd
import numpy as np

def main():
    # read in the processed data
    df = pd.read_csv('/home/twidis/ultianalytics/data/all_data.csv');

    df.Date = df.Date.str.slice(0,10);

    # there are some major inconsistencies in how opponents are named, standardize them
    for idx in range(len(df)):
        if 'atlanta' in df.loc[idx]['Opponent'] or 'hustle' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'atlanta_hustle';
        elif 'austin' in df.loc[idx]['Opponent'] or 'sol' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'austin_sol';
        elif 'charlotte' in df.loc[idx]['Opponent'] or 'express' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'charlotte_express';
        elif 'chicago' in df.loc[idx]['Opponent'] or 'wildfire' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'chicago_wildfire';
        elif 'cin' in df.loc[idx]['Opponent'] or 'revolution' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'cincinnati_revolution';
        elif 'dallas' in df.loc[idx]['Opponent'] or 'roughnecks' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'dallas_roughnecks';
        elif 'dc' in df.loc[idx]['Opponent'] or 'breeze' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'dc_breeze';
        elif 'detroit' in df.loc[idx]['Opponent'] or 'mechanix' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'detroit_mechanix';
        elif 'indi' in df.loc[idx]['Opponent'] or 'alley' in df.loc[idx]['Opponent'] or 'indy' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'indianapolis_alleycats';
        elif 'jacksonville' in df.loc[idx]['Opponent'] or 'cannons' in df.loc[idx]['Opponent']  or 'tampa_bay' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'tampa_bay_cannons';
        elif 'los_angeles' in df.loc[idx]['Opponent'] or 'aviators' in df.loc[idx]['Opponent'] or df.loc[idx]['Opponent'] == 'la':
            df.loc[idx,'Opponent'] = 'los_angeles_aviators';
        elif 'madison' in df.loc[idx]['Opponent'] or 'radicals' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'madison_radicals';
        elif 'minnesota' in df.loc[idx]['Opponent'] or 'chill' in df.loc[idx]['Opponent'] or 'mn' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'minnesota_wind_chill';
        elif 'montreal' in df.loc[idx]['Opponent'] or 'royal' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'montreal_royal';
        elif 'nashville' in df.loc[idx]['Opponent'] or 'nightwatch' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'nashville_nightwatch';
        elif 'york' in df.loc[idx]['Opponent'] or 'emp' in df.loc[idx]['Opponent'] :
            df.loc[idx,'Opponent'] = 'new_york_empire';
        elif 'ottawa' in df.loc[idx]['Opponent'] or 'outlaws' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'ottawa_outlaws';
        elif 'phil' in df.loc[idx]['Opponent'] or 'phoenix' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'philadelphia_phoenix';
        elif 'pitt' in df.loc[idx]['Opponent'] or 'thunderbirds' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'pittsburgh_thunderbirds';
        elif 'ral' in df.loc[idx]['Opponent'] or 'flyers' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'raleigh_flyers';
        elif 'rochester' in df.loc[idx]['Opponent'] or 'dragons' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'rochester_dragons';
        elif 'salt_lake' in df.loc[idx]['Opponent'] or 'lions' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'salt_lake_lions';
        elif 'san_diego' in df.loc[idx]['Opponent'] or 'growlers' in df.loc[idx]['Opponent']  or 'sd' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'san_diego_growlers';
        elif 'san_fran' in df.loc[idx]['Opponent'] or 'flame' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'san_francisco_flamethrowers';
        elif 'san_jose' in df.loc[idx]['Opponent'] or 'spiders' in df.loc[idx]['Opponent']  or 'sj' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'san_jose_spiders';
        elif 'seattle' in df.loc[idx]['Opponent'] or 'cascades' in df.loc[idx]['Opponent']  or 'raptors' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'seattle_cascades';
        elif 'toronto' in df.loc[idx]['Opponent'] or 'rush' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'toronto_rush';
        elif 'vancouver' in df.loc[idx]['Opponent'] or 'riptide' in df.loc[idx]['Opponent']:
            df.loc[idx,'Opponent'] = 'vancouver_riptide';

        if 'raptors' in df.loc[idx]['Name']:
            df.loc[idx,'Name'] = 'seattle_cascades';

    # for some reason, there's an opponent named test. drop this from the dataset
    df.drop(df[df['Opponent'] == 'test'].index, inplace=True);

    # drop the duplicate cases
    for idx in range(len(df)):
        try:
            df.drop(df[ (df['Opponent'] == df.loc[idx,'Name']) & (df['Name'] == df.loc[idx,'Opponent']) & (df['Date'] == df.loc[idx,'Date']) ].index, inplace=True);
        except:
            print('Row not in dataframe');

    # write out to a different file
    df.to_csv('/home/twidis/ultianalytics/data/cleaned_data.csv',index=False);

if __name__ == "__main__":
    main();
