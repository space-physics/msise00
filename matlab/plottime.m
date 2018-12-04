function plottime(atmos, times, glat, glon)

figure(1); clf(1)
ax1 = subplot(2,1,1);
set(ax1,'nextplot','add')

semilogy(ax1,times, [atmos.nN2], 'DisplayName','N_{N_2}')
semilogy(ax1,times, [atmos.nO2], 'DisplayName','N_{O_2}')


datetick(ax1,'x',13)
title(ax1,[datestr(times(1), 29), ' (',num2str(glat),',',num2str(glon),')'])
ylabel(ax1,'cm^{-3}')

legend(ax1,'show','location','southwest')


%% smaller quantities
ax = subplot(2,1,2);
set(ax,'nextplot','add')
semilogy(ax,times, [atmos.nAr], 'DisplayName','N_{Ar}')

datetick(ax,'x',13)
ylabel(ax,'cm^{-3}')
xlabel(ax, 'time [UTC]')

legend(ax,'show')
end
