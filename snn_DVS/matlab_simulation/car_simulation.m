close all
clear all
clc
f = figure('MenuBar','None');
menu = uimenu(f,'Label','Start simulation');
stop=uimenu(f,'Label','Stop','Callback',{@stop_func},... 
           'Separator','on','Accelerator','X');
%stop.Accelerator = '4';
%quit=uimenu(f,'Label','Quit','Callback',{@exit_func},... 
%           'Separator','on','Accelerator','Q');
%arrows=uimenu(menu,'Label','Arrows', 'Callback',{@arrow_func, stop}); 
box=uimenu(menu,'Label','three_lanes up', 'Callback',{@three_up,stop});
box.Accelerator = '0';
box1=uimenu(menu,'Label','three_lanes_mul up', 'Callback',{@three_up_mul,stop}); 
box1.Accelerator = '1';
%box2=uimenu(menu,'Label','six_lanes_mul up', 'Callback',{@six_up_mul,stop});
box2=uimenu(menu,'Label','six_lanes_mul up', 'Callback',{@three_mul_sp,stop});
box2.Accelerator = '2';
box3=uimenu(menu,'Label','six_lanes_mul up', 'Callback',{@six_up_mul_1,stop}); 
box3.Accelerator = '3';
hold all;
 axis([0,120,0,120]); 
%axis square;
 set(gcf, 'color', [0 0 0]);
 set(gca, 'color', [0 0 0]);
 set(gca,'xtick',[]);
 set(gca,'xticklabel',[]);
 set(gca,'ytick',[])
 set(gca,'yticklabel',[]);

