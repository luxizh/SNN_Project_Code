function car_pass(src, evt, lane)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    X=(lane-1)*40;% lane=1 2 3
    box=patch([X+5 X+35 X+35 X+5], [160 160 120 120], 'w');
    for y=140:-4:0
        %set(box,'XData',[x x+30 x+30 x]);
        set(box,'YData',[y y y-40 y-40]);
        pause(0.01);
    end
    set(box,'Xdata',[],'Ydata',[]);
return