function six_up_mul(src, evt, stop)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    X=[];
    Y=[];
    lane=unidrnd(8,[1,6])+4;
    X=[0 0 0 0];
    Y=[0 0 0 0];
    box=patch(X,Y,'w');
    while(strcmp(stop.Label,'Stop'))
    %while(1)
        Y=Y-10;
        lane=lane-1;
        for i=1:6
            if lane(i)==0
                lane(i)=unidrnd(9)+3;
                X=[(i-1)*20+2 (i-1)*20+18 (i-1)*20+18 (i-1)*20+2;X];
                Y=[144 144 120 120;Y];
            end
        end
        if size(Y,1)
            del=find(Y(:,1)<=0);
            X(del,:)=[];
            Y(del,:)=[];
        end
        set(box,'Xdata',X','Ydata',Y');
        %patch(X',Y','w');
        pause(0.1);
        %pause(1.1)
    end
    set(box,'Xdata',[],'Ydata',[]);
    stop.Label='Stop';