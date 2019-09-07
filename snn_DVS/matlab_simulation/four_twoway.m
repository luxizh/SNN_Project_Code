function four_twoway(src, evt, stop)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    count=[0 0 0 0];
    while(strcmp(stop.Label,'Stop'))
        lane=unidrnd(4);
        tp=rand(1);
        pause(tp/10)
        %car_pass(src,evt,lane);
        X=(lane-1)*30;% lane=1 2 3
        if lane<3
            box=patch([X+5 X+25 X+25 X+5], [150 150 120 120], 'w');
            for y=150:-4:0
                set(box,'YData',[y y y-30 y-30]);
                pause(0.015);
            end
        else
            box=patch([X+5 X+25 X+25 X+5], [0 0 -30 -30], 'w');
            for y=0:4:150
                set(box,'YData',[y y y-30 y-30]);
                pause(0.015);
            end            
        end
        count(lane)=count(lane)+1;
        set(box,'Xdata',[],'Ydata',[]);
    end
    
    %pause(1.1)
    count
    %set(box,'Xdata',[],'Ydata',[]);
    stop.Label='Stop';
    
return