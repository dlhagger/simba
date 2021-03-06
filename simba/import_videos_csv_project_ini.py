import os
import shutil
import cv2
import subprocess
import sys

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def extract_frames_ini(directory):
    filesFound = []

    def execute(command):
        print(command)
        subprocess.call(command, shell=True, stdout=subprocess.PIPE)

    ########### FIND FILES ###########
    for i in os.listdir(directory):
        # if i.__contains__(".mp4"):
        filesFound.append(i)


    for i in filesFound:
        pathDir1 = str(i[:-4])
        pathDir0 =str(str(os.path.dirname(directory)) +'\\frames\\input' )
        pathDir = str(str(pathDir0)+'\\' + pathDir1)

        if not os.path.exists(pathDir):
            os.makedirs(pathDir)
            picFname = '%d.png'

            saveDirFilenames = os.path.join(pathDir, picFname)

            fname = str(directory)+'\\' + str(i)
            cap = cv2.VideoCapture(fname)
            fps = cap.get(cv2.CAP_PROP_FPS)
            amount_of_frames = cap.get(7)
            print('The number of frames in this video = ',amount_of_frames)
            print('Extracting frames... (Might take awhile)')
            command = str('ffmpeg -i ' + str(fname) + ' ' + '-q:v 1' + ' ' + '-start_number 0' + ' ' + str(saveDirFilenames))
            print(command)
            subprocess.call(command, shell=True)
            print('Frames were extracted for',os.path.basename(pathDir))


        else:
            print(os.path.basename(pathDir),'existed, no action taken, frames should be in there')

    print('All frames were extracted.')

def copy_frame_folders(source,inifile):
    source = str(source) + '\\'
    dest = str(os.path.dirname(inifile))
    dest1 = str((dest) + '\\frames\\input')
    files = []

    ########### FIND FILES ###########
    for i in os.listdir(source):
        files.append(i)

    for f in files:
        filetocopy = source + f
        if os.path.exists(dest1 + '\\' + f):
            print(f, 'already exist in', dest1)

        elif not os.path.exists(dest1 + '\\' + f):
            print('Copying frames of',f)
            shutil.copytree(filetocopy, dest1+'\\'+f)
            nametoprint = os.path.join('',*(splitall(dest1)[-4:]))
            print(f, 'copied to', nametoprint)

    print('Finished copying frames.')

def copy_singlevideo_DPKini(inifile,source):
    try:
        print('Copying video...')
        dest = str(os.path.dirname(inifile))
        dest1 = str((dest) + '\\videos\\input')

        if os.path.exists(dest1+'\\'+os.path.basename(source)):
            print(os.path.basename(source), 'already exist in', dest1)
        else:
            shutil.copy(source, dest1)
            nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
            print(os.path.basename(source),'copied to',nametoprint)

        print('Finished copying video.')
    except:
        pass

def copy_singlevideo_ini(inifile,source):
    try:
        print('Copying video...')
        dest = str(os.path.dirname(inifile))
        dest1 = str((dest) + '\\' + 'videos')

        if os.path.exists(dest1+'\\'+os.path.basename(source)):
            print(os.path.basename(source), 'already exist in', dest1)
        else:
            shutil.copy(source, dest1)
            nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
            print(os.path.basename(source),'copied to',nametoprint)

        print('Finished copying video.')
    except:
        pass

def copy_multivideo_DPKini(inifile,source,filetype):
    try:
        print('Copying videos...')
        source = str(source)+'\\'
        dest = str(os.path.dirname(inifile))
        dest1 = str((dest)+ '\\videos\\input')
        files = []

        ########### FIND FILES ###########
        for i in os.listdir(source):
            if i.__contains__(str('.'+filetype)):
                files.append(i)

        for f in files:
            filetocopy=source +'\\'+f
            if os.path.exists(dest1+'\\'+f):
                print(f, 'already exist in', dest1)

            elif not os.path.exists(dest1+'\\'+f):
                shutil.copy(filetocopy, dest1)
                nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
                print(f, 'copied to', nametoprint)

        print('Finished copying videos.')
    except:
        print('Please select a folder and enter in the file type')


def copy_multivideo_ini(inifile,source,filetype):
    try:
        print('Copying videos...')
        source = str(source)+'\\'
        dest = str(os.path.dirname(inifile))
        dest1 = str((dest)+ '\\' + 'videos')
        files = []

        ########### FIND FILES ###########
        for i in os.listdir(source):
            if i.__contains__(str('.'+filetype)):
                files.append(i)

        for f in files:
            filetocopy=source +'\\'+f
            if os.path.exists(dest1+'\\'+f):
                print(f, 'already exist in', dest1)

            elif not os.path.exists(dest1+'\\'+f):
                shutil.copy(filetocopy, dest1)
                nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
                print(f, 'copied to', nametoprint)

        print('Finished copying videos.')
    except:
        print('Please select a folder and enter in the file type')

def copy_allcsv_ini(inifile,source):
    print('Copying csv files...')
    source = str(source)+'\\'
    dest = str(os.path.dirname(inifile))
    dest1 = str((dest)+ '\\' + 'csv'+ '\\'+ 'input_csv'+'\\original_filename')
    dest2 = str((dest) + '\\' + 'csv' + '\\' + 'input_csv\\')
    files = []

    if not os.path.exists(dest1):
        os.makedirs(dest1)

    ########### FIND FILES ###########
    for i in os.listdir(source):
        if i.__contains__(".csv"):
            files.append(i)
    ###copy files to project_folder/csv/raw_tracking_csv
    for f in files:
        filetocopy = source +'\\'+f
        if os.path.exists(dest1+'\\'+f):
            print(f, 'already exist in', dest1)

        elif not os.path.exists(dest1+'\\'+f):
            shutil.copy(filetocopy, dest1)
            nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
            print(f, 'copied to', nametoprint)
    ### copy files to input_csv
    for f in files:
        filetocopy = source +'\\'+f
        if os.path.exists(dest2+'\\'+f):
            print(f, 'already exist in', dest2)

        elif not os.path.exists(dest2+'\\'+f):
            shutil.copy(filetocopy, dest2)
            nametoprint = os.path.join('', *(splitall(dest2)[-4:]))
            print(f, 'copied to', nametoprint)

    ##rename files in input csv
    for i in os.listdir(dest2):
        if ('.csv') and ('DeepCut') in i:
            finali = i.split('DeepCut')[0]
            os.rename(dest2+i,dest2+finali+'.csv')
        else:
            pass
    print('Finished importing tracking data.')


# def copy_allcsv_ini_patternmatch(inifile,source):
#     print('Copying csv files...')
#     source = str(source)+'\\'
#     dest = str(os.path.dirname(inifile))
#     dest2 = str((dest) + '\\' + 'csv' + '\\' + 'input_csv\\')
#     destvid = str(dest) + '\\videos\\'
#     files = []
#     videos=[]
#
#     ########### FIND FILES ###########
#     for i in os.listdir(source):
#         if i.__contains__(".csv"):
#             files.append(i)
#
#     ### find videos
#     for i in os.listdir(destvid):
#         if i.__contains__('.mp4'):
#             i = i.split('.')[0]
#             videos.append(i)
#
#     for f in files:
#         for i in videos:
#             if i in f:
#                 shutil.copy(source +'\\'+f,dest2)
#                 os.rename(dest2+f,dest2+i+'.csv')
#
#     print('Finished importing tracking data.')

def copy_singlecsv_ini(inifile,source):
    print('Copying csv file...')
    dest = str(os.path.dirname(inifile))
    dest1 = str((dest) + '\\' + 'csv' + '\\' + 'input_csv\\original_filename\\')
    dest2 = str((dest) + '\\' + 'csv' + '\\' + 'input_csv\\')

    if not os.path.exists(dest1):
        os.makedirs(dest1)

    if os.path.exists(dest1+'\\'+os.path.basename(source)):
        print(os.path.basename(source), 'already exist in', dest1)
    else:
        shutil.copy(source, dest1)
        nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
        print(os.path.basename(source), 'copied to', nametoprint)

    if os.path.exists(dest2+'\\'+os.path.basename(source)):
        print(os.path.basename(source), 'already exist in', dest1)
    else:
        shutil.copy(source, dest2)
        nametoprint = os.path.join('', *(splitall(dest2)[-4:]))
        print(os.path.basename(source), 'copied to', nametoprint)

    ##rename files in input csv
    for i in os.listdir(dest2):
        if ('.csv') and ('DeepCut') in i:
            finali = i.split('DeepCut')[0]
            os.rename(dest2+i,dest2+finali+'.csv')
        else:
            pass

    print('Finished importing tracking data.')