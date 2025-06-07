clear all
close all

%% Plot magnetic field along pipe radius for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

set(0,'DefaultTextFontName','Times',...
    'DefaultTextFontSize',14,...
    'DefaultAxesFontName','Times',...
    'DefaultAxesFontSize',14,...
    'DefaultLineLineWidth',1,...
    'DefaultLineMarkerSize',7.75)

radiusOuter = 0.5;
radiusInner = 0.4375;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
ax = nexttile;

hMaxOverall = 0.0;
% Calculations and plotting
for mur = murList
    dataPerp = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialPerpendicular_0.txt", mur));
    dataPar = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadialParallel_0.txt", mur));

    rho = vecnorm([dataPerp(:,1), dataPerp(:,3)], 2, 2);
    rho = [-rho(end:-1:2); rho];

    hTotMag = vecnorm((dataPerp(:,7:end) + dataPar(:,7:end))/2.0, 2, 2);
    hTotMag = [hTotMag(end:-1:2); hTotMag];

    if max(hTotMag) > hMaxOverall
        hMaxOverall = max(hTotMag);
    end

    pipeCenterIndices = find(abs(rho) < radiusInner);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2)))
    hold on

end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / hMaxOverall;
end

% Plot finalizations
ylim([-0.1 1.1])
plot([-radiusOuter -radiusOuter],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([-radiusInner -radiusInner],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([radiusOuter radiusOuter],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([radiusInner radiusInner],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
grid on
xlabel('Pipe Radius (in)')
ylabel('Normalized Magnetic Field')
title('Magnetic Field along Pipe Radius')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [ax.InnerPosition(1) + ax.InnerPosition(3)/2 - lgd.Position(3)/2, 0.5, lgd.Position(3), lgd.Position(4)];
savefig('yokeRadialField.fig')
exportgraphics(gcf, ...
    'yokeRadialField.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')
