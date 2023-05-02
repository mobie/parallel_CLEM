import pandas as pd
from collections import Counter

# Path to directory (needs to be specified by user)

datadir = "/g/schwab/Beckwith_MSB/Analysis/Live_LM_dataAnalysis/Trackmate_csvFiles/"

tracks = pd.read_csv(datadir + "MSB30_4_tracks.csv", \
                     usecols=['NUMBER_SPOTS', 'NUMBER_GAPS', 'LONGEST_GAP', 'NUMBER_SPLITS', 'TRACK_ID'])
links = pd.read_csv(datadir + "MSB30_4_edges.csv", \
                    usecols=['LABEL', 'TRACK_ID', 'SPOT_SOURCE_ID', 'SPOT_TARGET_ID', 'EDGE_X_LOCATION', \
                             'EDGE_Y_LOCATION'])
spots = pd.read_csv(datadir + "MSB30_4_spots.csv", \
                    usecols=['LABEL', 'ID', 'TRACK_ID', 'POSITION_X', 'POSITION_Y', 'FRAME'])

# Generate a list of spot_ids that correspond to a splitting event
# (SOURCE_IDs of splitting event appear twice)

source_ids = list(links["SPOT_SOURCE_ID"])
source_id_counts = Counter(source_ids)
splitting_event_ids = [id for id in source_id_counts if source_id_counts[id] > 1]

# Add Boolean to Spots and Links Dataframes

spots["Splitting_event"] = spots["ID"].apply(lambda x: \
                                                 False if x not in splitting_event_ids \
                                                     else True)

links["Splitting_event"] = links["SPOT_SOURCE_ID"].apply(lambda x: \
                                                             False if x not in splitting_event_ids \
                                                                 else True)
# Rename link dataframe columns

links.columns = ['LABEL', \
                 'TRACK_ID', \
                 'SOURCE_ID', \
                 'TARGET_ID', \
                 'EDGE_X_LOCATION', \
                 'EDGE_Y_LOCATION', \
                 'SPLITTING_EVENT']


# Get lineages

def get_lineage(x, links_df):
    num = x.SOURCE_ID
    if x.SPLITTING_EVENT:
        lineage = [str(num)]
    else:
        lineage = []
    while True:
        y = links_df.loc[links_df['TARGET_ID'] == num, :]
        if y.empty:
            break
        if y.SPLITTING_EVENT.values[0]:
            lineage.append(str(y.SOURCE_ID.values[0]))
        num = y.SOURCE_ID.values[0]
    if lineage:
        return ".".join(reversed(lineage))
    else:
        return None


links['LINEAGE'] = links.apply(get_lineage, links_df=links, axis=1)

# Exclude intermediate spots and links
#
# links = links[links["SPLITTING_EVENT"] == True]
#
# spots = spots[spots["Splitting_event"] == True]
spots.rename(columns={"ID": "SOURCE_ID"}, inplace=True)

# merging

df_merged = pd.merge(links, spots, how="outer", on=["SOURCE_ID", "TRACK_ID"])
df_merged = df_merged.drop(['Splitting_event', 'LABEL_x', 'LABEL_y'], axis=1)
df_merged["Generation"] = df_merged["LINEAGE"].apply(lambda x: x.count(".") + 1)


# Add column containing the SOURCE_ID of the mother cell

def get_mother(x):
    lineage_list = x.split(".")
    if len(lineage_list) == 1:
        pass
    else:
        return lineage_list[-2]


df_merged["MOTHER_ID"] = df_merged["LINEAGE"].apply(lambda x: get_mother(x))

df_m1=df_merged.drop([0,1,2,len(links),len(links)+1])

df_m1.to_csv('data/MSB30_4/tables/trackmate1.tsv',sep='\t')