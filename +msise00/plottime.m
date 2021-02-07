function fig = plottime(atmos, times, glat, glon)
arguments
  atmos struct
  times datetime
  glat (1,1) double
  glon (1,1) double
end

fig = figure(1);
clf(fig)
t = tiledlayout(fig, 2, 1);
ax1 = nexttile(t);
set(ax1,'nextplot','add')

semilogy(ax1,times, [atmos.nN2], 'DisplayName','N_{N_2}')
semilogy(ax1,times, [atmos.nO2], 'DisplayName','N_{O_2}')

title(ax1,[datestr(times(1), 29), ' (',num2str(glat),',',num2str(glon),')'])
ylabel(ax1,'m^{-3}')

legend(ax1,'show','location','southwest')

%% smaller quantities
ax = nexttile(t);
set(ax,'nextplot','add')
semilogy(ax,times, [atmos.nAr], 'DisplayName','N_{Ar}')

ylabel(ax,'m^{-3}')
xlabel(ax, 'time [UTC]')

legend(ax,'show')
end
