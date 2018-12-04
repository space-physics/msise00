function plotalt(atmos, times, glat, glon)

validateattributes(atmos, {'struct'}, {})
%% Density profiles
hp = figure;
try
sgtitle(hp, {[datestr(times),' deg.  (',num2str(glat),', ', num2str(glon),')']})
end
ax = subplot(1,2,1, 'parent', hp);
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
xlabel(ax, 'Density [cm^-3]')
ylabel(ax, 'altitude [km]')
xlim(ax, [1,1e17])

set(ax,'xscale','log')
grid(ax, 'on')
legend(ax, 'show','location','northeast')

%% Temperature Profiles

ax = subplot(1,2,2, 'parent', hp);
set(ax, 'nextplot','add')

plot(ax, [atmos.Tn], altkm, 'DisplayName', 'T_n')
plot(ax, [atmos.Texospheric], altkm, 'DisplayName', 'T_{exo}')

title('Temperature')
xlabel(ax, 'Temperature [K]')
ylabel(ax, 'altitude [km]')

grid(ax, 'on')
legend(ax, 'show','location','northwest')

end
