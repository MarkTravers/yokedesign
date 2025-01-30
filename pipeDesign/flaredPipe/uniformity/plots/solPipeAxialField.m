clear all; 
close all;

%% Plot magnetic field along pipe axis for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

centerRegionRadius = 0.5;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_Haxial_0.txt", mur));

    % hTotMag = vecnorm(data(:,7:end), 2, 2);
    hTotMag = data(:,7);

    pipeCenterIndices = find(abs(data(:,1)) <= centerRegionRadius);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(data(:,1), hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.1f"}', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2), centerRegionRadius))
    hold on

end

% Plot finalizations
plot([-centerRegionRadius -centerRegionRadius],[0.0 8e4], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[0.0 8e4], '--k', 'HandleVisibility', 'off')
xlim([-5.0 5.0])
grid on
legend('Location', 'north')
xlabel('Pipe Axis (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Axis')
savefig('solAxialField.fig')
saveas(gcf, 'solAxialField.png')