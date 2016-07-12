function tactileSweep%(stimulus)
    
%     f1=stimulus(1);
%     f2=stimulus(2);
%     p1=stimulus(3);
%     p2=stimulus(4);

    stim = {...
        {'fixed',100,1,300},...
        {'fixchan',14}%,...
%         {'fixed',100,51,100},...
%         {'fixchan',3},...
%         {'fixed',100,101,150},...
%         {'fixchan',5},...
%         {'fixed',100,151,200},...
%         {'fixchan',7},...
%         {'fixed',100,201,250},...
%         {'fixchan',9},...
%         {'fixed',100,251,300},...
%         {'fixchan',11},...
%         {'fixed',100,301,350},...
%         {'fixchan',13},...
        };
    [t,s]=buildTSM_nomap(stim);
    
    stimGen('load',s,t);
    rtn=-1;
    while rtn==-1
        rtn=stimGen('start');
    end
end