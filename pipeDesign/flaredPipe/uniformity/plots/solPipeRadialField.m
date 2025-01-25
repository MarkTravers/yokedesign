clear all
close all

%% Plot magnetic field along pipe radius for varying X
% List of susceptibilities to plot
murList = ["00002", "00100", "01000", "10000"];

% radiusInner = 0.437500;
radiusInner = 0.419922;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = [load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialInside_0.txt", mur)); load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialOutside_0.txt", mur))];

    rho = vecnorm([data(:,2), data(:,3)], 2, 2) / 0.0254;
    rho = [-rho(end:-1:2); rho];

    hTotMag = vecnorm(data(:,7:end), 2, 2);
    hTotMag = [hTotMag(end:-1:2); hTotMag];

    pipeCenterIndices = find(abs(rho) < radiusInner);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.2f"}', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2), radiusInner))
    hold on

end

% Plot finalizations
plot([-0.5 -0.5],[0.0 9.0], '--k', 'HandleVisibility', 'off')
plot([-0.437500 -0.437500],[0.0 9.0], '--k', 'HandleVisibility', 'off')
plot([0.5 0.5],[0.0 9.0], '--k', 'HandleVisibility', 'off')
plot([0.437500 0.437500],[0.0 9.0], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'east')
xlabel('Pipe Radius (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Radius')
