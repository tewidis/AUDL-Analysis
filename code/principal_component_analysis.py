import pandas as pd
import matplotlib as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def main():
    # read in the processed data
    df = pd.read_csv('/home/twidis/ultianalytics/data/combined_data.csv');

    # split into features and values
    X = df.iloc[:,4:13];
    Y = df.iloc[:,13];

    # normalize the data to mean 0 standard deviation 1
    X = StandardScaler().fit_transform(X);

    # use principal component analysis to reduce to the top 2 principal components
    pca = PCA(0.95);

    principal_components = pca.fit_transform(X);

    #principal_df = pd.DataFrame(data = principal_components, columns = ['principal component 1', 'principal component 2']);

    #final_df = pd.concat([principal_df, df.iloc[:,13]], axis=1);

    #print(pca.explained_variance_ratio_);
    print(pca.n_components_);

if __name__ == '__main__':
    main();
