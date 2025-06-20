clear all; 
close all;

%% Plot magnetic field along pipe axis for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

centerRegionRadius = 0.5;
pipeLengthRadius = 4.0;

set(0,'DefaultTextFontName','Times',...
    'DefaultTextFontSize',14,...
    'DefaultAxesFontName','Times',...
    'DefaultAxesFontSize',14,...
    'DefaultLineLineWidth',1,...
    'DefaultLineMarkerSize',7.75)

% Plot initialization
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
ax = nexttile;

maxH = 0.0;
% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_Haxial_0.txt", mur));

    % hTotMag = vecnorm(data(:,7:end), 2, 2);
    hTotMag = data(:,7);

    if max(hTotMag) > maxH
        maxH = max(hTotMag);
    end

    pipeCenterIndices = find(abs(data(:,1)) <= centerRegionRadius);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(data(:,1), hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2)))
    hold on

end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / maxH;
end
    

% Plot finalizations
ylim([-0.1 1.1])
xlim([-4.5 4.5])
plot([-centerRegionRadius -centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([-pipeLengthRadius -pipeLengthRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([pipeLengthRadius pipeLengthRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')

grid on
xlabel('Pipe Axis (in)')
ylabel('Normalized Magnetic Field')
title('Magnetic Field along Pipe Axis')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [ax.InnerPosition(1) + ax.InnerPosition(3)/2 - lgd.Position(3)/2, 0.55, lgd.Position(3), lgd.Position(4)];
savefig('solAxialField.fig')
exportgraphics(gcf, ...
    'solAxialField.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')