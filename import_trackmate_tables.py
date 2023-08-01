import pandas as pd
from collections import Counter

# Path to directory (needs to be specified by user)

datadir = "/g/schwab/Beckwith_MSB/Analysis/Live_LM_dataAnalysis/Trackmate_csvFiles/"

for ds in ['MSB26_2', 'MSB30_4']:
    tracks = pd.read_csv(datadir + ds + "_tracks.csv", \
                         usecols=['NUMBER_SPOTS', 'NUMBER_GAPS', 'LONGEST_GAP', 'NUMBER_SPLITS', 'TRACK_ID', \
                                  'TRACK_MEAN_SPEED', 'TRACK_MAX_SPEED', 'TRACK_MIN_SPEED', 'TRACK_MEDIAN_SPEED', \
                                  'TRACK_STD_SPEED', 'TOTAL_DISTANCE_TRAVELED', 'MAX_DISTANCE_TRAVELED', \
                                  'MEAN_STRAIGHT_LINE_SPEED', 'LINEARITY_OF_FORWARD_PROGRESSION', \
                                  'MEAN_DIRECTIONAL_CHANGE_RATE'])
    links = pd.read_csv(datadir + ds + "_edges.csv", \
                        usecols=['LABEL', 'TRACK_ID', 'SPOT_SOURCE_ID', 'SPOT_TARGET_ID', 'EDGE_X_LOCATION', \
                                 'EDGE_Y_LOCATION', 'DIRECTIONAL_CHANGE_RATE','SPEED', 'DISPLACEMENT'])
    spots = pd.read_csv(datadir + ds + "_spots.csv", \
                        usecols=['LABEL', 'ID', 'TRACK_ID', 'POSITION_X', 'POSITION_Y', 'POSITION_T', 'FRAME', \
                                 'ELLIPSE_ASPECTRATIO', 'AREA', 'PERIMETER', 'CIRCULARITY', 'SOLIDITY'
                                 ])

    # Generate a list of spot_ids that correspond to a splitting event
    # (SOURCE_IDs of splitting event appear twice)

    source_ids = list(links["SPOT_SOURCE_ID"])
    source_id_counts = Counter(source_ids)
    # splitting_event_ids = [id for id in source_id_counts if source_id_counts[id] > 1]

    # Add Boolean to Spots and Links Dataframes

    # spots["Splitting_event"] = spots["ID"].apply(lambda x: \
    #                                                  False if x not in splitting_event_ids \
    #                                                      else True)
    #
    # links["Splitting_event"] = links["SPOT_SOURCE_ID"].apply(lambda x: \
    #                                                              False if x not in splitting_event_ids \
    #                                                                  else True)
    # Rename link dataframe columns

    links.columns = ['LABEL',
                     'TRACK_ID',
                     'SOURCE_ID',
                     'TARGET_ID',
                     'DIRECTIONAL_CHANGE_RATE',
                     'SPEED',
                     'DISPLACEMENT',
                     'EDGE_X_LOCATION',
                     'EDGE_Y_LOCATION']


    # Get lineages
    #
    # def get_lineage(x, links_df):
    #     num = x.SOURCE_ID
    #     if x.SPLITTING_EVENT:
    #         lineage = [str(num)]
    #     else:
    #         lineage = []
    #     while True:
    #         y = links_df.loc[links_df['TARGET_ID'] == num, :]
    #         if y.empty:
    #             break
    #         if y.SPLITTING_EVENT.values[0]:
    #             lineage.append(str(y.SOURCE_ID.values[0]))
    #         num = y.SOURCE_ID.values[0]
    #     if lineage:
    #         return ".".join(reversed(lineage))
    #     else:
    #         return None
    #
    #
    # links['LINEAGE'] = links.apply(get_lineage, links_df=links, axis=1)

    # Exclude intermediate spots and links
    #
    # links = links[links["SPLITTING_EVENT"] == True]
    #
    # spots = spots[spots["Splitting_event"] == True]
    spots.rename(columns={"ID": "SOURCE_ID"}, inplace=True)

    # merging

    df_merged = pd.merge(links, spots, how="outer", on=["SOURCE_ID", "TRACK_ID"])


    # Add column containing the SOURCE_ID of the mother cell

    # def get_mother(x):
    #     lineage_list = x.split(".")
    #     if len(lineage_list) == 1:
    #         pass
    #     else:
    #         return lineage_list[-2]
    #

    # df_merged["MOTHER_ID"] = df_merged["LINEAGE"].apply(lambda x: get_mother(x))

    # remove multi-header rows
    df_m1=df_merged.drop([0,1,2,len(links),len(links)+1])

    mobietable=pd.read_csv('data/'+ ds + '/tables/' + ds + '_spotIDs/default.tsv', delimiter='\t')

    mt1=mobietable.sort_values('label_id')

    df_m1.rename(columns={"SOURCE_ID": "label_id"}, inplace=True)

    df_m1.label_id = df_m1.label_id.astype(int)
    df_m1.label_id += 1

    fulltable = pd.merge(df_m1, mt1, how="outer", on="label_id")

    fulltable.to_csv('data/'+ ds + '/tables/' + ds + '_spotIDs/trackmate/default.tsv',sep='\t')