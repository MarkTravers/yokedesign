clear all
close all

%% Plot magnetic field along pipe radius for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

radiusOuter = 0.413;
radiusInner = 0.354;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadial_0.txt", mur));

    rho = vecnorm(data(:,2:3), 2, 2) .* sign(data(:,2));

    hTotMag = vecnorm(data(:,7:end), 2, 2);

    pipeCenterIndices = find(abs(rho) < radiusInner-0.01);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)_{\\pm %0.2f"}', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2), radiusInner))
    hold on

end

% Plot finalizations
ylim([0.0 2.2e4])
plot([-radiusOuter -radiusOuter],[0.0 2.2e4], '--k', 'HandleVisibility', 'off')
plot([-radiusInner -radiusInner],[0.0 2.2e4], '--k', 'HandleVisibility', 'off')
plot([radiusOuter radiusOuter],[0.0 2.2e4], '--k', 'HandleVisibility', 'off')
plot([radiusInner radiusInner],[0.0 2.2e4], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'east')
xlabel('Pipe Radius (in)')
ylabel('|\bfH\rm| (A/m)')
title('Axial Magnetic Field Uniformity along Pipe Radius')
savefig('solRadialField.fig')
saveas(gcf, 'solRadialField.png')
