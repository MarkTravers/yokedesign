clear all; close all;
data = load('yoke_prb_grp_PipeCenterH_0.txt');
y = data(:,2);
Hy = data(:,5);

plot(y,Hy,'linewidth',2)
xlabel('y (inches)');
ylabel('Hy (A/m)')
title('Axial H-field along the pipe');