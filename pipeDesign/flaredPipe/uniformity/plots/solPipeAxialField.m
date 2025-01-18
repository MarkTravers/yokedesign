clear all; 
close all;

%% Plot magnetic field along pipe axis for varying X
% List of susceptibilities to plot
murList = ["00002", "00100", "01000", "10000"];

centerRegionRadius = 0.5;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_Haxial_0.txt", mur));

    ycoord = data(:,1) / 0.0254;

    % hTotMag = vecnorm(data(:,7:end), 2, 2);
    hTotMag = data(:,7);

    pipeCenterIndices = find(abs(ycoord) <= centerRegionRadius);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(ycoord, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.1f"}', mur, 100.0*(hMax-hMin)/((hMax+hMin)/2), centerRegionRadius))
    hold on

end

% Plot finalizations
plot([-centerRegionRadius -centerRegionRadius],[0.0 35], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[0.0 35], '--k', 'HandleVisibility', 'off')
% xlim([-5.0 5.0])
grid on
legend('Location', 'north')
xlabel('Pipe Axis (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Axis')