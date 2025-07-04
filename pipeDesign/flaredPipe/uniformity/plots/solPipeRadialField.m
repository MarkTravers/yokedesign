clear all
close all

%% Plot magnetic field along pipe radius for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

radiusOuter = 0.413;
radiusInner = 0.354;

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
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_HRadial_0.txt", mur));

    rho = vecnorm(data(:,2:3), 2, 2) .* sign(data(:,2));

    hTotMag = vecnorm(data(:,7:end), 2, 2);

    if max(hTotMag) > maxH
        maxH = max(hTotMag);
    end

    pipeCenterIndices = find(abs(rho) < radiusInner-0.01);
    hMax = max(hTotMag(pipeCenterIndices));
    hMin = min(hTotMag(pipeCenterIndices));

    plot(rho, hTotMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaH(%.2f%%)', str2double(mur)-1, 100.0*(hMax-hMin)/((hMax+hMin)/2)))
    hold on

end

% Normalize data in plot
plots = findall(gca, 'Type', 'Line');
for i = 1:length(plots)
    plots(i).YData = plots(i).YData / maxH;
end

% Plot finalizations
ylim([0.0 1.1])
plot([-radiusOuter -radiusOuter],[0.0 1.1], '--k', 'HandleVisibility', 'off')
plot([-radiusInner -radiusInner],[0.0 1.1], '--k', 'HandleVisibility', 'off')
plot([radiusOuter radiusOuter],[0.0 1.1], '--k', 'HandleVisibility', 'off')
plot([radiusInner radiusInner],[0.0 1.1], '--k', 'HandleVisibility', 'off')
grid on
xlabel('Pipe Radius (in)')
ylabel('Normalized Magnetic Field')
title('Magnetic Field along Pipe Radius')
drawnow
lgd = legend(ax,"Location","none","Units","normalized");
lgd.Position = [ax.InnerPosition(1) + ax.InnerPosition(3)/2 - lgd.Position(3)/2, 0.40, lgd.Position(3), lgd.Position(4)];
savefig('solRadialField.fig')
exportgraphics(gcf, ...
    'solRadialField.pdf', ...
    'ContentType','vector', ...
    'BackgroundColor','none')
