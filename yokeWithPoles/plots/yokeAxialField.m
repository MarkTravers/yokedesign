clear all; 
close all;

%% Plot magnetic field along pipe axis for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

set(0,'DefaultTextFontName','Times',...
    'DefaultTextFontSize',14,...
    'DefaultAxesFontName','Times',...
    'DefaultAxesFontSize',14,...
    'DefaultLineLineWidth',1,...
    'DefaultLineMarkerSize',7.75)

centerRegionRadius = 0.5;
pipeLengthHalf = 5.0;

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
ax = nexttile;

hMaxOverall = 0.0;
% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_PipeCenterH_0.txt", mur));

    ycoord = data(:,2);

    hTotMag = vecnorm(data(:,7:end), 2, 2);

    if max(hTotMag) > hMaxOverall
        hMaxOverall = max(hTotMag);
    end

    pipeCenterIndices = find(abs(ycoord) <= centerRegionRadius);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(ycoord, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2)))
    hold on

end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / hMaxOverall;
end

% Plot finalizations
ylim([-0.1 1.1])
plot([-centerRegionRadius -centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([-pipeLengthHalf -pipeLengthHalf],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([pipeLengthHalf pipeLengthHalf],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
xlim([-pipeLengthHalf-0.5 pipeLengthHalf+0.5])
grid on
xlabel('Pipe Axis (in)')
ylabel('Normalized Magnetic Field')
title('Magnetic Field along Pipe Axis')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [0.585, 0.66, lgd.Position(3), lgd.Position(4)];
savefig('yokeAxialField.fig')
exportgraphics(gcf, ...
    'yokeAxialField.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')