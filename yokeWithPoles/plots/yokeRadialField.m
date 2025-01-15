clear all
close all

%% Plot magnetization along pipe for varying X
% List of susceptibilities to plot
murList = ["00002", "00100", "01000", "10000"];

% radiusInner = 0.437500;
radiusInner = 0.419922;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    dataPerp = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialPerpendicular_0.txt", mur));

    rho = vecnorm([dataPerp(:,1), dataPerp(:,3)], 2, 2);
    rho = [-rho(end:-1:2); rho];

    hTotMag = vecnorm(dataPerp(:,7:end), 2, 2);
    hTotMag = [hTotMag(end:-1:2); hTotMag];

    pipeCenterIndices = find(abs(rho) < radiusInner);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.2f"}', mur, 100.0*(hMax-hMin)/((hMax+hMin)/2), radiusInner))
    hold on

end

% Plot finalizations
plot([-0.5 -0.5],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([-0.437500 -0.437500],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([0.5 0.5],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([0.437500 0.437500],[0.0 6e6], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'east')
xlabel('Pipe Radius (in)')
ylabel('|\bfH\rm| (A/m)')
title('Magnetic Field Uniformity along Pipe Radius')
