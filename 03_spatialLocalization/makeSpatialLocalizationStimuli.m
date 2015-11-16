f1=2.^([0:.1:2]+log2(25));

frequency = [f1(2) f1(20)];

channels = [1 3 5 9; 5 9 11 13];

%channels = [2 4 6 10; 6 10 12 14];
pair1 = [repmat(channels(1),1,4), repmat(channels(2),1,4), repmat(channels(3),1,4), repmat(channels(4),1,4), repmat(channels(2,3),1,4), repmat(channels(2,4),1,4),...
         repmat(channels(1),1,4), repmat(channels(2),1,4), repmat(channels(3),1,4), repmat(channels(4),1,4), repmat(channels(2,3),1,4), repmat(channels(2,4),1,4);
         repmat(frequency(1),1,24), repmat(frequency(2),1,24)];
         
pair2 = [repmat(channels(1,:),1,3), repmat(channels(2,:),1,3),...
         repmat(channels(1,:),1,3), repmat(channels(2,:),1,3);
         repmat(frequency(1),1,24), repmat(frequency(2),1,24)];   
pair3 = [repmat(channels(1,:),1,4), repmat(channels(2,3:4),1,4) ; repmat(frequency(1),1,8), repmat(frequency(2),1,8), repmat(frequency(1),1,4), repmat(frequency(2),1,4);
         repmat(channels(1,:),1,4), repmat(channels(2,3:4),1,4) ; repmat(frequency(1),1,8), repmat(frequency(2),1,8), repmat(frequency(1),1,4), repmat(frequency(2),1,4)];
    
%combine frequency combinations with position pairs 
stimuli = [pair1; pair2];
stimuli = [stimuli,pair3];
stimuli = [repmat(stimuli,1,2)]; 

% populate trial structure with 2 instances of the same stimulus
save ('spatialLocalizationStimuli_0.mat','stimuli')

%save ('spatialLocalizationStimuli_1.mat','stimuli')