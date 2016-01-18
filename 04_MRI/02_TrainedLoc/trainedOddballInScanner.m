% get subject info
%name = '915';
%number = name;

number = input('\n\nEnter Subject ID:\n\n','s');
exptdesign.number = number;
if isempty(number)
    name = [datestr(now,'yyyy-mm-dd-HH-MM') 'MR000'];
else
    name = [datestr(now,'yyyy-mm-dd-HH-MM') number];
end
WaitSecs(0.25);

%check if subject has data on file
exptdesign.saveDir = ['./data_Trained_Localizer/' number];
if ~exist(exptdesign.saveDir,'dir')
    mkdir(exptdesign.saveDir)
end

exptdesign.subjectName = name;

%Trial/Block/Run lengths
exptdesign.numBlocks = 24;              
exptdesign.numTrialsPerSession = 6;    
exptdesign.numRuns = 6;

%fixation location/duration
exptdesign.fixationDuration =0.700;
exptdesign.trialDuration = 16;
exptdesign.fixationImage = 'imgsscaled/fixation.bmp';  
exptdesign.imageDirectory = 'imgsscaled/';   

% Decide which response mapping you are using
% if exptdesign.debugmode
%     exptdesign.response = 1;
%     exptdesign.responseBox = 0;
%     exptdesign.boxHandle = 2; % we still need this variable in the debug mode. 
% else
%     exptdesign.response = input('\n\nEnter response key profile (option 0 or 1):\n\n');
%     exptdesign.responseBox = 1;             % Controls whether we are using the keyboard or the response box for subj. responses.
% end

exptdesign.interTrialInterval = 0.7;                % amount of time between trials
exptdesign.usespace=0;                  % use space bar to start each trial?

%open com3 port for button boxes
if exptdesign.responseBox
    % Ensure button-box configuration is correct
    disp('Ensure dip switches are set to E-PRIME and 5+');
    input('Hit Enter to Continue...');
    exptdesign.boxHandle = CMUBox('Open', 'pst', 'COM3', 'norelease');
end

%open com2 port for stimulator
stimGenPTB('open')

%run all 6 runs right after the last 
for iRuns = 1:exptdesign.numRuns
    exptdesign.iRuns=iRuns;
    [trialOutput.run] = trainedOddballExperimentInScanner(name,exptdesign);
end

%close com3 port
if exptdesign.responseBox
    CMUBox('Close',exptdesign.boxHandle);
    disp('Ensure dip switches are set back to 4');
end

%close com2 port 
stimGenPTB('close')