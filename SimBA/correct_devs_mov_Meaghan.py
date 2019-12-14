import os
import pandas as pd
import math
import numpy as np
import statistics

trackingFilesList = []
trackingFilesDir = r"Z:\DeepLabCut\OpenField_analysis\tracking_data"
criterion = 2
loopy = 0


def add_correction_prefix(col, bpcorrected_list):
    colc = 'Corrected_' + col
    bpcorrected_list.append(colc)
    return bpcorrected_list

def correct_value_position(df, colx, coly, col_corr_x, col_corr_y, dict_pos):

    dict_pos[colx] = dict_pos.get(colx, 0) 
    dict_pos[coly] = dict_pos.get(coly, 0)

    animalSize = mean1size

    currentCriterion = mean1size * criterion
    list_x = []
    list_y = []
    prev_x = df.iloc[0][colx]
    prev_y = df.iloc[0][coly]
    ntimes = 0
    live_prevx = df.iloc[0][colx]
    live_prevy = df.iloc[0][coly]
    NT = 6
    for index, row in df.iterrows():

        if index == 0:
            continue

        if (math.hypot(row[colx] - prev_x, row[coly] - prev_y) < (animalSize/4)): #the mouse is standing still
            currentCriterion = animalSize * 2
            
        if ((math.hypot(row[colx] - prev_x, row[coly] - prev_y) < currentCriterion) or (ntimes > NT and \
                                      math.hypot(row[colx] - live_prevx, row[coly] - live_prevy) < currentCriterion)):

            list_x.append(row[colx])
            list_y.append(row[coly])

            prev_x = row[colx]
            prev_y = row[coly]

            ntimes = 0
            
        else:
            #out of range
            list_x.append(prev_x)
            list_y.append(prev_y)
            dict_pos[colx] += 1
            dict_pos[coly] += 1
            ntimes += 1
            
        live_prevx = row[colx]
        live_prevy = row[coly]
        
    df[col_corr_x] = list_x
    df[col_corr_y] = list_y

    return df

########### FIND CSV FILES ###########
for i in os.listdir(trackingFilesDir):
    if i.__contains__(".csv"):
        file = os.path.join(trackingFilesDir, i)
        trackingFilesList.append(file)

########### CREATE PD FOR RAW DATA AND PD FOR MOVEMENT BETWEEN FRAMES ###########
for i in trackingFilesList:
    loopy += 1
    currentFile = i
    csv_df = pd.read_csv(currentFile,
                            names=["Mouse1_left_ear_x", "Mouse1_left_ear_y","Mouse1_left_ear_p","Mouse1_right_ear_x", "Mouse1_right_ear_y", "Mouse1_right_ear_p", "Mouse1_left_hand_x", "Mouse1_left_hand_y", "Mouse1_left_hand_p", \
                                   "Mouse1_right_hand_x", "Mouse1_right_hand_y", "Mouse1_right_hand_p", "Mouse1_left_foot_x", "Mouse1_left_foot_y", "Mouse1_left_foot_p", "Mouse1_right_foot_x", "Mouse1_right_foot_y", "Mouse1_right_foot_p",
                                   "Mouse1_nose_x", "Mouse1_nose_y", "Mouse1_nose_p", "Mouse1_tail_x", "Mouse1_tail_y", "Mouse1_tail_p", "Mouse1_back_x", "Mouse1_back_y", "Mouse1_back_p"])

    csv_df = csv_df.drop(csv_df.index[[0, 1, 2]])
    csv_df = csv_df.apply(pd.to_numeric)
    ########### CREATE SHIFTED DATAFRAME FOR DISTANCE CALCULATIONS ###########################################
    csv_df_shifted = csv_df.shift(periods=1)
    csv_df_shifted = csv_df_shifted.rename(columns={'Mouse1_left_ear_x': 'Mouse1_left_ear_x_shifted', 'Mouse1_left_ear_y': 'Mouse1_left_ear_y_shifted',
                     'Mouse1_left_ear_p': 'Mouse1_left_ear_p_shifted', 'Mouse1_right_ear_x': 'Mouse1_right_ear_x_shifted', \
                     'Mouse1_right_ear_y': 'Mouse1_right_ear_y_shifted', 'Mouse1_right_ear_p': 'Mouse1_right_ear_p_shifted',
                     'Mouse1_left_hand_x': 'Mouse1_left_hand_x_shifted', 'Mouse1_left_hand_y': 'Mouse1_left_hand_y_shifted', \
                     'Mouse1_left_hand_p': 'Mouse1_left_hand_p_shifted', 'Mouse1_right_hand_x': 'Mouse1_right_hand_x_shifted',
                     'Mouse1_right_hand_y': 'Mouse1_right_hand_y_shifted', 'Mouse1_right_hand_p': 'Mouse1_right_hand_p_shifted', 'Mouse1_left_foot_x': \
                     'Mouse1_left_foot_x_shifted', 'Mouse1_left_foot_y': 'Mouse1_left_foot_y_shifted',
                     'Mouse1_left_foot_p': 'Mouse1_left_foot_p_shifted', 'Mouse1_right_foot_x': 'Mouse1_right_foot_x_shifted',
                     'Mouse1_right_foot_y': 'Mouse1_right_foot_y_shifted', \
                     'Mouse1_right_foot_p': 'Mouse1_right_foot_p_shifted', 'Mouse1_nose_x': 'Mouse1_nose_x_shifted',
                     'Mouse1_nose_y': 'Mouse1_nose_y_shifted', 'Mouse1_nose_p': 'Mouse1_nose_p_shifted', 'Mouse1_tail_x': 'Mouse1_tail_x_shifted',
                     'Mouse1_tail_y': 'Mouse1_tail_y_shifted', 'Mouse1_tail_p': 'Mouse1_tail_p_shifted',
                     'Mouse1_back_x': 'Mouse1_back_x_shifted', 'Mouse1_back_y': 'Mouse1_back_y_shifted',
                     'Mouse1_back_p': 'Mouse1_back_p_shifted'})
    csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner')

    ########### EUCLIDEAN DISTANCES ###########################################
    csv_df_combined['Mouse_nose_to_tail'] = np.sqrt((csv_df_combined.Mouse1_nose_x - csv_df_combined.Mouse1_tail_x) ** 2 + (csv_df_combined.Mouse1_nose_y - csv_df_combined.Mouse1_tail_y) ** 2)
    csv_df_combined = csv_df_combined.fillna(0)

    ########### MEAN MOUSE SIZES ###########################################
    mean1size = (statistics.mean(csv_df_combined['Mouse_1_nose_to_tail']))

    bps = ['Mouse1_left_ear', 'Mouse1_right_ear', 'Mouse1_left_hand', 'Mouse1_right_hand', 'Mouse1_left_foot', 'Mouse1_tail', 'Mouse1_right_foot', 'Mouse1_back', 'Mouse1_nose']
    bplist1x = []
    bplist1y = []
    bpcorrected_list1x = []
    bpcorrected_list1y = []

    for bp in bps:
        colx = bp + '_x'
        coly = bp + '_y'
        bplist1x.append(colx)
        bplist1y.append(coly)
        bpcorrected_list1x = add_correction_prefix(colx, bpcorrected_list1x)
        bpcorrected_list1y = add_correction_prefix(coly, bpcorrected_list1y)

    # this dictionary will count the number of times each body part position needs to be corrected
    dict_pos = {}
    
    for idx, col1x in enumerate(bplist1x):
        # apply function to all body part data
        col1y = bplist1y[idx]
        col_corr_1x = bpcorrected_list1x[idx]
        col_corr_1y = bpcorrected_list1y[idx]
        csv_df_combined = correct_value_position(csv_df_combined, col1x, col1y, col_corr_1x, col_corr_1y, dict_pos)

    scorer = pd.read_csv(currentFile).scorer.iloc[2:]
    scorer = pd.to_numeric(scorer)
    scorer = scorer.reset_index()
    scorer = scorer.drop(['index'], axis=1)
    csv_df_combined['scorer'] = scorer.values.astype(int)
    csv_df_combined = csv_df_combined[
        ["scorer", "Corrected_Mouse1_left_ear_x", "Corrected_Mouse1_left_ear_y", "Corrected_Mouse1_left_ear_p", "Corrected_Mouse1_right_ear_x", "Corrected_Mouse1_right_ear_y", "Corrected_Mouse1_right_ear_p", "Corrected_Mouse1_left_hand_x",
         "Corrected_Mouse1_left_hand_y", "Corrected_Mouse1_left_hand_p", "Corrected_Mouse1_right_hand_x", "Corrected_Mouse1_right_hand_y", "Corrected_Mouse1_right_hand_p", "Corrected_Mouse1_left_foot_x", "Corrected_Mouse1_left_foot_y", "Corrected_Mouse1_left_foot_p",
         "Corrected_Mouse1_right_foot_x", "Corrected_Mouse1_right_foot_y", "Corrected_Mouse1_right_foot_p", "Corrected_Mouse1_nose_x", "Corrected_Mouse1_nose_y", "Corrected_Mouse1_nose_p", "Corrected_Mouse1_tail_x", "Corrected_Mouse1_tail_y", "Corrected_Mouse1_tail_p",  "Corrected_Mouse1_back_x", "Corrected_Mouse1_back_y", "Corrected_Mouse1_back_p"]]
         
    #csv_df_combined = csv_df_combined.drop(csv_df_combined.index[0:2])
    df_headers = pd.read_csv(currentFile, nrows=0)
    csv_df_combined.columns = df_headers.columns
    csv_df_combined = pd.concat([df_headers, csv_df_combined])
    fileName = os.path.basename(currentFile)
    fileName, fileEnding = fileName.split('.')
    fileOut = str(fileName) + str('.csv')
    pathOut = os.path.join(trackingFilesDir, fileOut)
    csv_df_combined.to_csv(pathOut, index=False)
