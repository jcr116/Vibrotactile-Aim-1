#packages to import
import numpy as np
import scipy.io as sio
import plotly.plotly as py
import statistics as stat
import math as m
import plotly.graph_objs as go
import plotly.tools as tls

tls.set_credentials_file(username='cs1471', api_key='9xknhmjhas')

#################################################################################
#allows specified increments
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

#generates a list of frequencies that we test
def makeFrequency():
    frequencyList = [i for i in my_range(0, 2, 0.1)]

    for index,obj in enumerate(frequencyList):
        obj += m.log2(25)
        frequencyList[index] = round(2**obj)
    return frequencyList

#################################MAIN##########################################
# filename = input('Enter a filename: \n')
# fileDirectory = input('Enter the directory where you want your figure saved: /n')
# session = input('Enter the session number: \n')

#Use when debugging or manually editing
filename = ('MR1000_block1.144.mat')
fileDirectory = '/Users/courtneysprouse/GoogleDrive/Riesenhuber/05_2015_scripts/Vibrotactile/03_spatialLocalization/data/1000/'
session = 'post'

#load matfile
data = sio.loadmat(fileDirectory + filename, struct_as_record=True)

#make list of frequencies tested
frequencyList = makeFrequency()

#pull relevant data from structures
RT = data['trialOutput']['RT']
sResp = data['trialOutput']['sResp']
correctResponse = data['trialOutput']['correctResponse']
accuracy = data['trialOutput']['accuracy']
stimuli = data['trialOutput']['stimuli']
nTrials = data['exptdesign']['numTrialsPerSession'][0,0][0]
nBlocks = data['exptdesign']['numBlocks'][0,0][0]
subjectNumber = data['exptdesign']['number'][0,0][0]
subjectName = data['exptdesign']['subjectName'][0,0][0]


#############################################################################
#Calculations by category type
#############################################################################

#calculate accuracy by frequency
b_categoryA = []
b_categoryB = []
iTrial = iBlock = 0
for iBlock in range(sResp.size):
    categoryA = []
    categoryB = []
    for iTrial in range(sResp[0,iBlock].size):
        stimulus = round(stimuli[0,iBlock][1,iTrial])
        if accuracy[0,iBlock][0,iTrial]==1:
            if stimulus in frequencyList and stimulus < 47:
                categoryA.append(1)
            else:
                categoryB.append(1)
        else:
            if stimulus in frequencyList and stimulus < 47:
                categoryA.append(0)
            else:
                categoryB.append(0)
    b_categoryA.append(categoryA)
    b_categoryB.append(categoryB)

#calculate accuracy by block for category A
i = 0
mAcc_categoryA = []
for i in range(len(b_categoryA)):
    mAcc_categoryA.append(stat.mean(b_categoryA[i]))

#calculate accuracy by block for category B
i = 0
mAcc_categoryB = []
for i in range(len(b_categoryB)):
    mAcc_categoryB.append(stat.mean(b_categoryB[i]))

#calculate reaction time by category type
b_categoryA_RT = []
b_categoryB_RT = []
iTrial = iBLock = 0
for iBlock in range(sResp.size):
    categoryA_RT = []
    categoryB_RT = []
    for iTrial in range(len(RT[0,iBlock][0])):
        stimulus = round(stimuli[0,iBlock][1,iTrial])
        if stimulus in frequencyList and stimulus < 47:
            categoryA_RT.append(RT[0,iBlock][0,iTrial])
        else:
            categoryB_RT.append(RT[0,iBlock][0,iTrial])
    b_categoryA_RT.append(categoryA_RT)
    b_categoryB_RT.append(categoryB_RT)

#calculate RT by block for category A
iBlock = 0
mRT_categoryA = []
for iBlock, time in enumerate(b_categoryA_RT):
        mRT_categoryA.append(stat.mean(time))

#calculate RT by block for category B
iBlock = 0
mRT_categoryB = []
for iBlock, time in enumerate(b_categoryB_RT):
    mRT_categoryB.append(stat.mean(time))

#############################################################################
#Calculations by position
#############################################################################

#calculate the reaction time by position
iBlock = iTrial = 0
bD_wristPos_RT = []
bD_elbowPos_RT = []
bD_crossMidline_RT = []
bS_wristPos_RT = []
bS_elbowPos_RT = []
bS_midline_RT = []
for iBlock in range(sResp.size):
    D_wristPos_RT = []
    D_elbowPos_RT = []
    D_crossMidline_RT = []
    S_wristPos_RT = []
    S_elbowPos_RT = []
    S_midline_RT = []
    for iTrial in range(sResp[0,iBlock].size):
        pos1 = int(stimuli[0,iBlock][0,iTrial])
        pos2 = int(stimuli[0,iBlock][2,iTrial])
        if pos1 != pos2:
            if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4 or pos1 == 5 or pos1 == 6\
                    and pos2 == 1 or pos2 == 2 or pos2 == 3 or pos2 == 4 or pos2 == 5 or pos2 == 6:
                D_wristPos_RT.append(RT[0,iBlock][0,iTrial])
            elif pos1 == 9 or pos1 == 10 or pos1 == 11 or pos1 == 12 or pos1 == 13 or pos1 == 14\
                    and pos2 == 9 or pos2 == 10 or pos2 == 11 or pos2 == 12 or pos2 == 13 or pos2 == 14:
                 D_elbowPos_RT.append(RT[0,iBlock][0,iTrial])
            else:
                D_crossMidline_RT.append(RT[0,iBlock][0,iTrial])
        else:
            if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4:
                S_wristPos_RT.append(RT[0,iBlock][0,iTrial])
            elif pos1 == 5 or pos1 == 5 or pos1 == 9 or pos1 == 10:
                S_midline_RT.append(RT[0,iBlock][0,iTrial])
            else:
                S_elbowPos_RT.append(RT[0,iBlock][0,iTrial])

    bD_wristPos_RT.append(D_wristPos_RT)
    bD_elbowPos_RT.append(D_elbowPos_RT)
    bD_crossMidline_RT.append(D_crossMidline_RT)
    bS_wristPos_RT.append(S_wristPos_RT)
    bS_elbowPos_RT.append(S_elbowPos_RT)
    bS_midline_RT.append(S_midline_RT)

#calculate the mean RT by morph
D_wristPos_meanRT = []
iBlock = 0
for iBlock, rtDWP in enumerate(bD_wristPos_RT):
    if rtDWP != []:
        D_wristPos_meanRT.append(stat.mean(rtDWP))
    else:
        D_wristPos_meanRT.append(0)

#calculate the mean RT by morph
D_crossMidline_meanRT = []
iBlock = 0
for iBlock, rtDCM in enumerate(bD_crossMidline_RT):
    if rtDCM != []:
        D_crossMidline_meanRT.append(stat.mean(rtDCM))
    else:
        D_crossMidline_meanRT.append(0)

#calculate the mean RT by morph
D_elbowPos_meanRT = []
iBlock = 0
for iBlock, rtDEP in enumerate(bD_wristPos_RT):
    if rtDEP != []:
        D_elbowPos_meanRT.append(stat.mean(rtDEP))
    else:
        D_elbowPos_meanRT.append(0)

#calculate the mean RT by morph
S_wristPos_meanRT = []
iBlock = 0
for iBlock, rtSWP in enumerate(bS_wristPos_RT):
    if rtSWP != []:
        S_wristPos_meanRT.append(stat.mean(rtSWP))
    else:
        S_wristPos_meanRT.append(0)

#calculate the mean RT by morph
S_midline_meanRT = []
iBlock = 0
for iBlock, rtSM in enumerate(bS_midline_RT):
    if rtSM != []:
        S_midline_meanRT.append(stat.mean(rtSM))
    else:
        S_midline_meanRT.append(0)

#calculate the mean RT by morph
S_elbowPos_meanRT = []
iBlock = 0
for iBlock, rtSEP in enumerate(bS_elbowPos_RT):
    if rtSEP != []:
        S_elbowPos_meanRT.append(stat.mean(rtSEP))
    else:
        S_elbowPos_meanRT.append(0)

#calculate the accuracy by position
iBlock = iTrial = 0
bD_wristPos_accuracy = []
bD_elbowPos_accuracy = []
bD_crossMidline_accuracy = []
bS_wristPos_accuracy = []
bS_elbowPos_accuracy = []
bS_midline_accuracy = []
for iBlock in range(sResp.size):
    D_wristPos_accuracy = []
    D_elbowPos_accuracy = []
    D_crossMidline_accuracy = []
    S_wristPos_accuracy = []
    S_elbowPos_accuracy = []
    S_midline_accuracy = []
    for iTrial in range(sResp[0,iBlock].size):
        pos1 = int(stimuli[0,iBlock][0,iTrial])
        pos2 = int(stimuli[0,iBlock][2,iTrial])
        if accuracy[0,iBlock][0,iTrial]==1:
            if pos1 != pos2:
                if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4 or pos1 == 5 or pos1 == 6\
                        and pos2 == 1 or pos2 == 2 or pos2 == 3 or pos2 == 4 or pos2 == 5 or pos2 == 6:
                    D_wristPos_accuracy.append(1)
                elif pos1 == 9 or pos1 == 10 or pos1 == 11 or pos1 == 12 or pos1 == 13 or pos1 == 14\
                        and pos2 == 9 or pos2 == 10 or pos2 == 11 or pos2 == 12 or pos2 == 13 or pos2 == 14:
                    D_elbowPos_accuracy.append(1)
                else:
                    D_crossMidline_accuracy.append(1)
            else:
                if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4:
                    S_wristPos_accuracy.append(1)
                elif pos1 == 5 or pos1 == 5 or pos1 == 9 or pos1 == 10:
                    S_midline_accuracy.append(1)
                else:
                    S_elbowPos_accuracy.append(1)
        else:
            if pos1 != pos2:
                if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4 or pos1 == 5 or pos1 == 6\
                        and pos2 == 1 or pos2 == 2 or pos2 == 3 or pos2 == 4 or pos2 == 5 or pos2 == 6:
                    D_wristPos_accuracy.append(0)
                elif pos1 == 9 or pos1 == 10 or pos1 == 11 or pos1 == 12 or pos1 == 13 or pos1 == 14\
                        and pos2 == 9 or pos2 == 10 or pos2 == 11 or pos2 == 12 or pos2 == 13 or pos2 == 14:
                    D_elbowPos_accuracy.append(0)
                else:
                    D_crossMidline_accuracy.append(0)
            else:
                if pos1 == 1 or pos1 == 2 or pos1 == 3 or pos1 == 4:
                    S_wristPos_accuracy.append(0)
                elif pos1 == 5 or pos1 == 6 or pos1 == 9 or pos1 == 10:
                    S_midline_accuracy.append(0)
                else:
                    S_elbowPos_accuracy.append(0)

    bD_wristPos_accuracy.append(D_wristPos_accuracy)
    bD_elbowPos_accuracy.append(D_elbowPos_accuracy)
    bD_crossMidline_accuracy.append(D_crossMidline_accuracy)
    bS_wristPos_accuracy.append(S_wristPos_accuracy)
    bS_elbowPos_accuracy.append(S_elbowPos_accuracy)
    bS_midline_accuracy.append(S_midline_accuracy)

#calculate the mean accuracy by morph
D_wristPos_meanAcc = []
iBlock = 0
for iBlock, accDWP in enumerate(bD_wristPos_accuracy):
    if accDWP != []:
        D_wristPos_meanAcc.append(stat.mean(accDWP))
    else:
        D_wristPos_meanAcc.append(0)

#calculate the mean accuracy by morph
D_crossMidline_meanAcc = []
iBlock = 0
for iBlock, accDCM in enumerate(bD_crossMidline_accuracy):
    if accDCM != []:
        D_crossMidline_meanAcc.append(stat.mean(accDCM))
    else:
        D_crossMidline_meanAcc.append(0)

#calculate the mean accuracy by morph
D_elbowPos_meanAcc = []
iBlock = 0
for iBlock, accDEP in enumerate(bD_wristPos_accuracy):
    if accDEP != []:
        D_elbowPos_meanAcc.append(stat.mean(accDEP))
    else:
        D_elbowPos_meanAcc.append(0)

#calculate the mean accuracy by morph
S_wristPos_meanAcc = []
iBlock = 0
for iBlock, accSWP in enumerate(bS_wristPos_accuracy):
    if accSWP != []:
        S_wristPos_meanAcc.append(stat.mean(accSWP))
    else:
        S_wristPos_meanAcc.append(0)

#calculate the mean accuracy by morph
S_midline_meanAcc = []
iBlock = 0
for iBlock, accSM in enumerate(bS_midline_accuracy):
    if accSM != []:
        S_midline_meanAcc.append(stat.mean(accSM))
    else:
        S_midline_meanAcc.append(0)

#calculate the mean accuracy by morph
S_elbowPos_meanAcc = []
iBlock = 0
for iBlock, accSEP in enumerate(bS_elbowPos_accuracy):
    if accSEP != []:
        S_elbowPos_meanAcc.append(stat.mean(accSEP))
    else:
        S_elbowPos_meanAcc.append(0)

#############################################################################
#Calculating mean acc and RT overall
#############################################################################
#calculate the mean overall accuracy by block
O_accuracy = []
iBlock = 0
for iBlock in range(accuracy.size):
    O_accuracy.append([np.mean([accuracy[0,iBlock]])])

#calculate the mean RT overall by block
O_reactionTime = []
iBlock = 0
for iBlock in range(RT.size):
    O_reactionTime.append(np.mean(RT[0,iBlock]))

#x-axis label
x = []
i=0
for i in range(nBlocks):
            x.append("Block: " + str(i+1)),

#############################################################################
#Generating figures
#############################################################################

# (1.1) Define a trace-generating function (returns a Bar object)
def make_trace_bar(y, name):
    return go.Bar(
        x     = x,
        y     = y,            # take in the y-coords
        name  = name,      # label for hover
        xaxis = 'x1',                    # (!) both subplots on same x-axis
        yaxis = 'y1'
    )

# (1.1) Define a trace-generating function (returns a line object)
def make_trace_line(y, name):
    return go.Scatter(
        x     = x,
        y     = y,            # take in the y-coords
        name  = name,      # label for hover
        xaxis = 'x1',                    # (!) both subplots on same x-axis
        yaxis = 'y1'
    )


#make trace containing acc and RT by position for Different Condition
trace1 = make_trace_bar(D_wristPos_meanAcc, "Different wrist Accuracy")
trace2 = make_trace_bar(D_crossMidline_meanAcc, "Different Across Mid Accuracy")
trace3 = make_trace_bar(D_elbowPos_meanAcc, "Different Elbow Accuracy")
trace4 = make_trace_line(D_wristPos_meanRT, "Different wrist RT")
trace5 = make_trace_line(D_crossMidline_meanRT, "Different Across Mid RT")
trace6 = make_trace_line(D_elbowPos_meanRT, "Different Elbow RT")

#make trace containing overall acc and rt
trace7 = make_trace_line(O_accuracy, "Overall Accuracy")
trace8 = make_trace_line(O_reactionTime, "Overall RT")

#make trace containing acc and RT by position for Same Condition
trace9  = make_trace_bar(S_wristPos_meanAcc, "Same wrist Accuracy")
trace10 = make_trace_bar(S_midline_meanAcc, "Same Across Mid Accuracy")
trace11 = make_trace_bar(S_elbowPos_meanAcc, "Same Elbow Accuracy")
trace12 = make_trace_line(S_wristPos_meanRT, "Same wrist RT")
trace13 = make_trace_line(S_midline_meanRT, "Same Across Mid RT")
trace14 = make_trace_line(S_elbowPos_meanRT, "Same Elbow RT")

#make trace containing acc and RT by category
trace15 = make_trace_bar(mAcc_categoryA, "Accuracy Category A")
trace16 = make_trace_bar(mAcc_categoryB, "Accuracy Category B")
trace17 = make_trace_line(mRT_categoryA, "RT Category A")
trace18 = make_trace_line(mRT_categoryB, "RT Category B")

# matFileName = fileDirectory + filename
# dataFile = sio.savemat(matFileName, {'x':x, 'y':y, 'cp_mean': cp_mean, 'mm_mean': mm_mean, 'cb_mean': cb_mean)
# dataFile.write(x,y,cp_mean, mm_mean, cb_mean,)
# dataFile.close()


# Generate Figure object with 2 axes on 2 rows, print axis grid to stdout
fig = tls.make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=True,
)
fig2 = tls.make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=True,
)
fig3 = tls.make_subplots(
    rows=1,
    cols=1,
    shared_xaxes=True,
)

#set figure layout to hold mutlitple bars
fig['layout'].update(
    barmode='group',
    bargroupgap=0,
    bargap=0.25,
    title = "Accuracy by Position Same v Different"
)

fig2['layout'].update(
    barmode='group',
    bargroupgap=0,
    bargap=0.25,
    title = "RT by Position Same v Different"
)

fig3['layout'].update(
    barmode='group',
    bargroupgap=0,
    bargap=0.25,
    title = "Accurary and RT by Frequency"
)

fig['data']  = [trace1, trace2, trace3, trace9, trace10, trace11, trace7]
fig2['data'] = [trace4, trace5, trace6, trace12, trace13, trace14, trace8]
fig3['data'] = [trace15, trace16, trace17, trace18]

#get the url of your figure to embed in html later
first_plot_url = py.plot(fig, filename= subjectName + "AccByMorph" + session, auto_open=False,)
tls.get_embed(first_plot_url)
second_plot_url = py.plot(fig2, filename= subjectName + "RTbyMorph" + session, auto_open=False,)
tls.get_embed(second_plot_url)
third_plot_url = py.plot(fig3, filename= subjectName + "AccByCatgeory" + session, auto_open=False,)
tls.get_embed(third_plot_url)

#bread crumbs to make sure entered the correct information
print("Your graph will be saved in this directory: " + fileDirectory + "\n")
print("Your graph will be saved under: " + filename + "\n")
print("The session number you have indicated is: " + session + "\n")


#embed figure data in html
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <!-- *** FirstPlot *** --->
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="'''+ first_plot_url + '''.embed?width=800&height=550"></iframe>
        <!-- *** Second Plot *** --->
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="'''+ second_plot_url + '''.embed?width=800&height=550"></iframe>
        <!-- *** ThirdPlot *** --->
        <iframe width="1000" height="550" frameborder="0" seamless="seamless" scrolling="no" \
src="'''+ third_plot_url + '''.embed?width=800&height=550"></iframe>
</html>'''

#save figure data in location specific previously
f = open(fileDirectory + filename + '.html','w')
f.write(html_string)

#save images as png in case prefer compared to html
# py.image.save_as(first_plot_url, "/Users/courtneysprouse/Desktop" + filename + "CategoryTraining" + session + ".png")

#close all open files
f.close()

print("Done!")