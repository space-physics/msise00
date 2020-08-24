function plotalt(atmos, times, glat, glon)
arguments
  atmos struct
  times datetime
  glat (1,1) double
  glon (1,1) double
end
%% Density profiles
hp = figure;
sgtitle(hp, {[datestr(times),' deg.  (',num2str(glat),', ', num2str(glon),')']})
t = tiledlayout(hp, 1,2);
ax = nexttile(t);
set(ax, 'nextplot','add')

altkm = [atmos.altkm];

semilogx(ax, [atmos.nHe], altkm, 'DisplayName', 'N_{He}')
semilogx(ax, [atmos.nO], altkm, 'DisplayName', 'N_{O^+}')
semilogx(ax, [atmos.nN2], altkm, 'DisplayName', 'N_{N_2}')
semilogx(ax, [atmos.nO2], altkm, 'DisplayName', 'N_{O_2}')
semilogx(ax, [atmos.nAr], altkm, 'DisplayName', 'N_{Ar}')
semilogx(ax, [atmos.nTotal], altkm, 'DisplayName', 'N_{Total}')
semilogx(ax, [atmos.nH], altkm, 'DisplayName', 'N_H')
semilogx(ax, [atmos.nN], altkm, 'DisplayName', 'N_N')

title(ax, 'Number Densities')
xlabel(ax, 'Density [m^-3]')
ylabel(ax, 'altitude [km]')
xlim(ax, [1,1e17])

set(ax,'xscale','log')
grid(ax, 'on')
legend(ax, 'show','location','northeast')

%% Temperature Profiles

ax = nexttile(t);
set(ax, 'nextplot','add')

plot(ax, [atmos.Tn], altkm, 'DisplayName', 'T_n')
plot(ax, [atmos.Texospheric], altkm, 'DisplayName', 'T_{exo}')

title(ax, 'Temperature')
xlabel(ax, 'Temperature [K]')
ylabel(ax, 'altitude [km]')

grid(ax, 'on')
legend(ax, 'show','location','northwest')

end
