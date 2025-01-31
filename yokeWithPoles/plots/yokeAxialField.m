clear all; 
close all;

%% Plot magnetic field along pipe axis for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

centerRegionRadius = 0.5;
pipeLengthHalf = 5.0;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_PipeCenterH_0.txt", mur));

    ycoord = data(:,2);

    hTotMag = vecnorm(data(:,7:end), 2, 2);

    pipeCenterIndices = find(abs(ycoord) <= centerRegionRadius);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(ycoord, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.1f"}', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2), centerRegionRadius))
    hold on

end

% Plot finalizations
plot([-centerRegionRadius -centerRegionRadius],[0.0 7e6], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[0.0 7e6], '--k', 'HandleVisibility', 'off')
xlim([-pipeLengthHalf pipeLengthHalf])
grid on
legend('Location', 'northeast')
xlabel('Pipe Axis (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Axis')
savefig('yokeAxialField.fig')
saveas(gcf, 'yokeAxialField.png')