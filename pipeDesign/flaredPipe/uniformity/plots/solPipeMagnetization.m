clear all
close all

%% Plot magnetization along pipe for varying X
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
pipeAxisColumnNumber = 1;
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
ax = nexttile;

maxMag = 0.0;
% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_cellLine_0.txt", mur));
    data = sortrows(data, pipeAxisColumnNumber);

    magMag = data(:,13);

    if max(magMag) > maxMag
        maxMag = max(magMag);
    end

    pipeCenterIndices = find(abs(data(:,pipeAxisColumnNumber)) <= 0.5);
    magMax = max(magMag(pipeCenterIndices));
    magMin = min(magMag(pipeCenterIndices));

    plot(data(:,pipeAxisColumnNumber), magMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaM(%.2f%%)', str2double(mur)-1, 100.0*(magMax-magMin)/((magMax+magMin)/2)))
    hold on
    
end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / maxMag;
end

% Plot finalizations
ylim([-0.1 1.1])
xlim([-4.5 4.5])
plot([-centerRegionRadius -centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([centerRegionRadius centerRegionRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([-pipeLengthRadius -pipeLengthRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
plot([pipeLengthRadius pipeLengthRadius],[-0.1 1.1], '--k', 'HandleVisibility', 'off')
grid on
xlabel('Pipe Length (in)')
ylabel('Normalized Magnetization')
title('Magnetization along Pipe Axis')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [ax.InnerPosition(1) + ax.InnerPosition(3)/2 - lgd.Position(3)/2, 0.45, lgd.Position(3), lgd.Position(4)];
savefig('solMag.fig')
exportgraphics(gcf, ...
    'solMag.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')
