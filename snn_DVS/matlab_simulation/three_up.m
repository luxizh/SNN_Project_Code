function three_up(src, evt, stop)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    count=[0 0 0];
    while(strcmp(stop.Label,'Stop'))
        lane=unidrnd(3);
        car_pass(src,evt,lane);
        X=(lane-1)*40;% lane=1 2 3
        box=patch([X+5 X+35 X+35 X+5], [160 160 120 120], 'w');
        for y=140:-4:0
            %set(box,'XData',[x x+30 x+30 x]);
            set(box,'YData',[y y y-40 y-40]);
            pause(0.015);
        end
        count(lane)=count(lane)+1;
        set(box,'Xdata',[],'Ydata',[]);
    end
    
    %pause(1.1)
    count
    %set(box,'Xdata',[],'Ydata',[]);
    stop.Label='Stop';
    
return
    box=patch([5 35 35 5], [120 120 80 80], 'w');
    while(strcmp(stop.Label,'Stop'))
        for x=5:40:120
            for y=120:-10:0
                set(box,'XData',[x x+30 x+30 x]);
                set(box,'YData',[y y y-40 y-40]);
                pause(0.1);
                if(strcmp(stop.Label,'Stop')==0)
                    break
                end
            end
            if(strcmp(stop.Label,'Stop')==0)
                break
            end
        end
    end
    set(box,'Xdata',[],'Ydata',[]);
return
