function three_up_mul(src, evt, stop)
%     vidObj = VideoWriter('vertical.avi');
%     open(vidObj);
    X=[];
    Y=[];
    lane=unidrnd(50,[1,3])+10;%20 10
    count=zeros(1,3);
    X=[0 0 0 0];
    Y=[0 0 0 0];
    box=patch(X,Y,'w');
    while(strcmp(stop.Label,'Stop'))
    %while(1)
        Y=Y-4;
        lane=lane-1;
        for i=1:3
            if lane(i)==0
                count(i)=count(i)+1;
                lane(i)=unidrnd(50)+15;%20 10
                X=[(i-1)*40+5 (i-1)*40+35 (i-1)*40+35 (i-1)*40+5;X];
                Y=[160 160 120 120;Y];
            end
        end
        if size(Y,1)
            del=find(Y(:,1)<=0);
            X(del,:)=[];
            Y(del,:)=[];
        end
        set(box,'Xdata',X','Ydata',Y');
        %patch(X',Y','w');
        pause(0.015);
        %pause(1.1)
    end
    set(box,'Xdata',[],'Ydata',[]);
    stop.Label='Stop';
    count
    return