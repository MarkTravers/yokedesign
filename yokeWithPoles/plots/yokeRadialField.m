clear all
close all

%% Plot magnetic field along pipe radius for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

radiusOuter = 0.5;
radiusInner = 0.4375;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    dataPerp = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialPerpendicular_0.txt", mur));
    dataPar = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialParallel_0.txt", mur));

    rho = vecnorm([dataPerp(:,1), dataPerp(:,3)], 2, 2);
    rho = [-rho(end:-1:2); rho];

    hTotMag = vecnorm((dataPerp(:,7:end) + dataPar(:,7:end))/2.0, 2, 2);
    hTotMag = [hTotMag(end:-1:2); hTotMag];

    pipeCenterIndices = find(abs(rho) < radiusInner);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.2f"}', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2), radiusInner))
    hold on

end

% Plot finalizations
plot([-radiusOuter -radiusOuter],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([-radiusInner -radiusInner],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([radiusOuter radiusOuter],[0.0 6e6], '--k', 'HandleVisibility', 'off')
plot([radiusInner radiusInner],[0.0 6e6], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'east')
xlabel('Pipe Radius (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Radius')
savefig('yokeRadialField.fig')
saveas(gcf, 'yokeRadialField.png')
