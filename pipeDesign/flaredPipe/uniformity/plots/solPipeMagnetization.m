clear all
close all

%% Plot magnetization along pipe for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

% Plot initialization
pipeAxisColumnNumber = 1;
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

% Calculations and plotting
for mur = murList
    data = load(sprintf("..\\magstromOutput\\mur%s_prb_grp_cellLine_0.txt", mur));
    data = sortrows(data, pipeAxisColumnNumber);

    magMag = data(:,13);

    pipeCenterIndices = find(abs(data(:,pipeAxisColumnNumber)) <= 0.5);
    magMax = max(magMag(pipeCenterIndices));
    magMin = min(magMag(pipeCenterIndices));

    semilogy(data(:,pipeAxisColumnNumber), magMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaM(%.2f%%)_{\\pm 0.5"}', str2double(mur)-1, 100.0*(magMax-magMin)/((magMax+magMin)/2)))
    hold on
    
end

% Plot finalizations
plot([-0.5 -0.5],[1e4 1e7], '--k', 'HandleVisibility', 'off')
plot([0.5 0.5],[1e4 1e7], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'east')
xlabel('Pipe Length (in)')
ylabel('|\bfM\rm| (A/m)')
title('Magnetization Uniformity in Center Region of Pipe')
savefig('solMag.fig')
saveas(gcf, 'solMag.png')
