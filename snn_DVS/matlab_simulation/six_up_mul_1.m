function six_up_mul_1(src, evt, stop)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    X=[];
    Y=[];
    lane=unidrnd(80,[1,6])+8;%24，6
    count=zeros(1,6);
    X=[0 0 0 0];
    Y=[0 0 0 0];
    box=patch(X,Y,'w');
    while(strcmp(stop.Label,'Stop'))
    %while(1)
        Y=Y-4;
        lane=lane-1;
        for i=1:6
            if lane(i)==0
                count(i)=count(i)+1;
                lane(i)=unidrnd(80)+8;% 60 8%24 6
                X=[(i-1)*20+2 (i-1)*20+18 (i-1)*20+18 (i-1)*20+2;X];
                Y=[144 144 120 120;Y];
            end
        end

        set(box,'Xdata',X','Ydata',Y');
        if size(Y,1)
            del=find(Y(:,1)<=0);
            X(del,:)=[];
            Y(del,:)=[];
        end
        %patch(X',Y','w');
        pause(0.015);
        %pause(1.1)
    end
    set(box,'Xdata',[],'Ydata',[]);
    stop.Label='Stop';
    count
    return