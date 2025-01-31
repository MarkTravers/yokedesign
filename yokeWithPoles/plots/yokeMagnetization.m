clear all
close all

%% Plot magnetization along pipe for varying X
% List of susceptibilities to plot
murList = ["00002", "00101", "01001", "10001"];

% Plot initialization
pipeAxisColumnNumber = 2;
tiledlayout(1,1, "TileSpacing","tight","Padding","tight")
nexttile

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

    pipeCenterIndices = find(abs(averagedData(:,pipeAxisColumnNumber)) <= 0.5);
    magMax = max(magMag(pipeCenterIndices));
    magMin = min(magMag(pipeCenterIndices));

    semilogy(averagedData(:,pipeAxisColumnNumber), magMag, 'DisplayName', sprintf('\\chi = %.0f; \\DeltaM(%.2f%%)_{\\pm 0.5"}', str2double(mur)-1, 100.0*(magMax-magMin)/((magMax+magMin)/2)))
    hold on
    % semilogy(averagedData(:,pipeAxisColumnNumber), abs(averagedData(:,5)), 'DisplayName', sprintf('\\chi = %.0f', mur))
    
end

% Plot finalizations
plot([-0.5 -0.5],[1e4 1e10], '--k', 'HandleVisibility', 'off')
plot([0.5 0.5],[1e4 1e10], '--k', 'HandleVisibility', 'off')
grid on
legend('Location', 'south')
xlabel('Pipe Length (in)')
ylabel('|\bfM\rm| (A/m)')
title('Magnetization Uniformity in Center Region of Pipe')
savefig('yokeMagnetization.fig')
saveas(gcf, 'yokeMagnetization.png')
