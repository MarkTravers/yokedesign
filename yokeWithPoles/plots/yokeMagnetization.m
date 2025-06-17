clear all
close all

%% Plot magnetization along pipe for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

set(0,'DefaultTextFontName','Times',...
    'DefaultTextFontSize',14,...
    'DefaultAxesFontName','Times',...
    'DefaultAxesFontSize',14,...
    'DefaultLineLineWidth',1,...
    'DefaultLineMarkerSize',7.75)

% Plot initialization
pipeAxisColumnNumber = 2;
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
ax = nexttile;

maxMagOverall = 0.0;
% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_PipeMag_0.txt", mur));
    data = sortrows(data, pipeAxisColumnNumber);
    changeIndices = [1; find(diff(data(:,pipeAxisColumnNumber)) ~= 0) + 1];

    averagedData = zeros(length(changeIndices)-1, size(data,2));

    for i = 1:length(changeIndices)-1
        averagedData(i,:) = mean(data(changeIndices(i):changeIndices(i+1),:),1);
    end

    magMag = vecnorm(averagedData(:,4:end),2,2);

    if max(magMag) > maxMagOverall
        maxMagOverall = max(magMag);
    end

    pipeCenterIndices = find(abs(averagedData(:,pipeAxisColumnNumber)) <= 0.5);
    magMax = max(magMag(pipeCenterIndices));
    magMin = min(magMag(pipeCenterIndices));

    semilogy(averagedData(:,pipeAxisColumnNumber), magMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaM(%.2f%%)', str2double(mur)-1, 100.0*(magMax-magMin)/((magMax+magMin)/2)))
    hold on
    % semilogy(averagedData(:,pipeAxisColumnNumber), abs(averagedData(:,5)), 'DisplayName', sprintf('\\chi = %.0f', mur))
    
end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / maxMagOverall;
end

% Plot finalizations
ylim([1e-5 2.0])
xlim([-5.5 5.5])
plot([-0.5 -0.5],[1e-5 2.0], '--k', 'HandleVisibility', 'off')
plot([0.5 0.5],[1e-5 2.0], '--k', 'HandleVisibility', 'off')
plot([-5.0 -5.0],[1e-5 2.0], '--k', 'HandleVisibility', 'off')
plot([5.0 5.0],[1e-5 2.0], '--k', 'HandleVisibility', 'off')
grid on
xlabel('Pipe Length (in)')
ylabel('Normalized Magnetization')
title('Magnetization along Pipe Axis')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [ax.InnerPosition(1) + ax.InnerPosition(3)/2 - lgd.Position(3)/2, 0.15, lgd.Position(3), lgd.Position(4)];
savefig('yokeMagnetization.fig')
exportgraphics(gcf, ...
    'yokeMagnetization.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')
