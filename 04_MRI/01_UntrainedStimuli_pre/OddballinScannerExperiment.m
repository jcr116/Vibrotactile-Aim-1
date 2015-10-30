% Automaticity
function trialOutput = OddballinScannerExperiment(name,exptdesign)

try
    %dbstop if error;
    % following codes should be used when you are getting key presses using
    % fast routines like kbcheck.
    KbName('UnifyKeyNames');
    Priority(1)

    %settings so that Psychtoolbox doesn't display annoying warnings--DON'T CHANGE
    oldLevel = Screen('Preference', 'VisualDebugLevel', 1);
    %     oldEnableFlag = Screen('Preference', 'SuppressAllWarnings', 1);
    %     warning offc
    %HideCursor;

    WaitSecs(1); % make sure it is loaded into memory;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %		INITIALIZE EXPERIMENT
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    % open a screen and display instructions
    screens = Screen('Screens');
    screenNumber = min(screens)+1;

    % Open window with default settings:
    [w windowRect] = Screen('OpenWindow', screenNumber,[128 128 128]);
%     [w windowRect] = Screen('OpenWindow', screenNumber,[128 128 128], [0 0 800 800]); %for debugging
    white = WhiteIndex(w); % pixel value for white
    black = BlackIndex(w); % pixel value for black
    
    %  calculate the slack allowed during a flip interval
    refresh = Screen('GetFlipInterval',w);
    slack = refresh/2;

    % Select specific text font, style and size, unless we're on Linux
    % where this combo is not available:
    if IsLinux==0
        Screen('TextFont',w, 'Courier New');
        Screen('TextSize',w, 14);
        Screen('TextStyle', w, 1+2);
    end;
    
    % FIXATION IMAGE
    fixationImage = imread(exptdesign.fixationImage);

    % MAKE TEXTURES
    fixationTexture = Screen('MakeTexture', w, double(fixationImage));

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %		INTRO EXPERIMENT
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if exptdesign.responseBox
        %flush event cue
        evt=1;
        while ~isempty(evt)
            evt = CMUBox('GetEvent', exptdesign.boxHandle); %empty queue 
        end
        % Get the responses keyed in from subject
        drawAndCenterText(w,'Please press the button.',0);
        evt = CMUBox('GetEvent', exptdesign.boxHandle, 1); % get event for button pressed
        responseMapping.button1 = evt.state; % stores button box in variable
      
        % Let the scanner signal the scan to start
        drawAndCenterText(w,'Please get ready.\n\nThe experiment will begin shortly.',0);
        % WARNING: TRRIGGER CORRESPONDS TO A PRESS OF BUTTON 3!!!
        triggername=4;
        trigger=0;
        while ~isequal(triggername,trigger)
            evt = CMUBox('GetEvent', exptdesign.boxHandle, 1);
            trigger = evt.state;
            starttime = evt.time;
        end
        exptdesign.scanStart = starttime;
        exptdesign.responseMapping=responseMapping;
    else
        responseMapping=exptdesign.responseKeyChange;
        drawAndCenterText(w,'Hit Enter to Continue...',1);
        exptdesign.scanStart = GetSecs;
    end
    
    runCounter=1;


    %Display experiment instructions
    drawAndCenterText(w,['\nOn each trial, you will feel 6 vibrations \n'...
             'You will indicate the vibration that felt different from the other 5 vibrations\n'...
             'by pushing the button.'  ],1)
        
   response = exptdesign.response;

    %load training stimuli
%     [stimuliShuffled, oddball] = makeStimuli(response);
    load stimuliShuffled.mat
    stimuli = stimuliShuffled(:,:,runCounter);
  
    sResp = zeros(6,24);
    %generate a correctResponse map
    for i = 1:size(stimuli,2)
        for j = 1:size(stimuli,1)
            if (size(stimuli{j,i},2) > 1)
                correctResponse(j,i) = 1;
            else
                correctResponse(j,i) = 0;
            end
        end
    end
     
    for iBlock=1:size(stimuli,1)%how many blocks to run this training session
        stimulusTracking=[]; 
        
        for i = 1:size(stimuli,2)
            stimuliBlock{i} = stimuli{iBlock,i};
        end
        
        %iterate over trials
        for iTrial=1:size(stimuli,2)
            
            %clear event responses stored in cue
            while ~isempty(evt)
                evt = CMUBox('GetEvent', exptdesign.boxHandle);
            end
           
           %draw fixation
           Screen('DrawTexture', w, fixationTexture);
           [FixationVBLTimestamp FixationOnsetTime FixationFlipTimestamp FixationMissed] = Screen('Flip',w);
           
           %after 700 ms, present the vibrotactile stimulus
           wait1 = .7;
           %record response start time
           responseStartTime=GetSecs;
           
           constructStimuli(stimuliBlock, iTrial);
           
           drawAndCenterText(w, 'Break /n/n/n Press button if felt unique vibration pattern',0,wait1)
%            [RespVBLTimestamp RespOnsetTime RespFlipTimestamp RespMissed] = Screen('Flip', w, wait1);
            evt = CMUBox('GetEvent', exptdesign.boxHandle);
            if ~isempty(evt)
                sResp = 1;
            end
        
           %record end time of response
           responseFinishedTime=evt.time;
          
           %record parameters for the trial
           trialOutput(iBlock).responseStartTime(iTrial)=responseStartTime;
           trialOutput(iBlock).responseFinishedTime(iTrial)=responseFinishedTime;
           trialOutput(iBlock).RT(iTrial)=responseFinishedTime-responseStartTime;
           trialOutput(iBlock).sResp(iTrial)=sResp;
           trialOutput(iBlock).wait1(iTrial)=wait1;
           trialOutput(iBlock).FixationVBLTimestamp(iTrial)=FixationVBLTimestamp;
           trialOutput(iBlock).FixationOnsetTime(iTrial)=FixationOnsetTime;
           trialOutput(iBlock).FixationFlipTimestamp(iTrial)=FixationFlipTimestamp;
           trialOutput(iBlock).FixationMissed(iTrial)=FixationMissed;             
           runOutput(runCounter).trialStartTime(iTrial)= GetSecs;
           runOutput(runCounter).iBlocks(iTrial) = exptdesign.iBlocks;
           runOutput(runCounter).runIndex(iTrial) = runCounter;
           runOutput(runCounter).numTrials(iTrial) = exptdesign.numTrialsPerSession;
           runOutput(runCounter).trialIndex(iTrial) = iTrial;
           
        end
        %record parameters for the block
        %stimuli, order
        trialOutput.stimuli = stimuli;
    end
    
    Screen('DrawTexture', w, fixationTexture);
    Screen('Flip',w)
    
    ShowCursor;
  
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %		END
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    %  Write the trial specific data to the output file.
    tic;
     %save the session data in the data directory
        save(['./data_Oddball_Localizer_Pre/' exptdesign.number '/' datestr(now, 'yyyymmdd_HHMM') '-' exptdesign.subjectName '_block' num2str(iBlock) '/' exptdesign.run '.mat'], 'trialOutput', 'exptdesign');
        %save the history data (stimuli, last level passed)
    toc;

    WaitSecs('UntilTime',exptdesign.scanStart + 10*(numBlocks) + 6*(runCounter+1))
    % End of experiment, close window:
    Screen('CloseAll');
    Priority(0);
    % At the end of your code, it is a good idea to restore the old level.
    %     Screen('Preference','SuppressAllWarnings',oldEnableFlag);
    
    catch
    % This "catch" section executes in case of an error in the "try"
    % section []
    if exptdesign.netstationPresent
        % Tell Netstation to stop recording
        [status error] = NetStation('StopRecording');
        if status ==1 % there was an error!
            status;
            error;
            ME = MException('NETSTATION:CouldNotStopRecord', ['Could not tell Netstation to stop recording.  Please check the IP and connection and try again.\n  Error:' error]);
            %              throw(ME);
            disp('ERROR stopping recoring in Netstation!');
        end

        [status error] = NetStation('Disconnect');
        if status ==1 % there was an error!
            status;
            error;
            ME = MException('NETSTATION:CouldNotStopRecord', ['Could not tell Netstation to stop recording.  Please check the IP and connection and try again.\n  Error:' error]);
            %              throw(ME);
            disp('ERROR disconnecting from Netstation!');

        end
    end
    
    if exptdesign.responseBox
        CMUBox('Close',exptdesign.boxHandle);
    end
    
    % above.  Importantly, it closes the onscreen window if it's open.
    disp('Caught error and closing experiment nicely....');
    Screen('CloseAll');
    Priority(0);
    fclose('all');
    psychrethrow(psychlasterror);

end
end

function drawAndCenterText(window,message,wait, time)
    if nargin < 3
        wait = 1;
    end
    
    if nargin <4
        time =0;
    end
    
    % Now horizontally and vertically centered:
    [nx, ny, bbox] = DrawFormattedText(window, message, 'center', 'center', 0);
    black = BlackIndex(window); % pixel value for black               
    Screen('Flip',window, time);
    
    %KbWait(1) waits for a button press to continue
    
%     WaitSecs(0.2); %this is necessary on the windows XP machine to wait for mouse response -- DOES delay timing!
end

function constructStimuli(stimuliBlock,iTrial)
     f = stimuliBlock{1,iTrial}(1,:);
     p = stimuliBlock{1,iTrial}(2,:);

    if length(f) > 1 
        constructOddStimuli(stimuliBlock, iTrial)
    else
        stim = {...
            {'fixed',f,1,300},...
            {'fixchan',p},...
            };
        
        [t,s]=buildTSM_nomap(stim);
        
        stimGenPTB('load',s,t);
        rtn=-1;
        while rtn==-1
            rtn=stimGenPTB('start');
        end
    end
end

function constructOddStimuli(stimuliBlock, iTrial)
    f = stimuliBlock{1,iTrial}(1,:);
    p = stimuliBlock{1,iTrial}(2,:);
    
    stim = {...
            {'fixed',f(1),1,300},...
            {'durchannel',p(1),1, 90},...
            {'fixed',f(1),1,300},...
            {'durchannel',p(2), 100,190},...
            {'fixed',f(1),1,300},...
            {'durchannel',p(3), 200,290},...
           };

    [t,s]=buildTSM_nomap(stim);    
       
    stimGenPTB('load',s,t);
    rtn=-1;
    while rtn==-1
        rtn = stimGenPTB('start');
    end
    
end