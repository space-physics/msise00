function plotmsis(atmos)
  arguments
    atmos struct
  end

species = cellfun(@char, cell(atmos.attrs{'species'}), 'uniformoutput', false);
alt_km = xarrayind2vector(atmos, 'alt_km');
times = xarrayind2vector(atmos, 'time');
glat = xarrayind2vector(atmos, 'lat');
glon = xarrayind2vector(atmos, 'lon');

figure
ax = axes('nextplot','add');

for i = 1:length(species)
dens = xarray2mat(atmos{species{i}});
semilogx(ax, dens, alt_km, 'DisplayName', species{i})
end


title(ax, {[times,' (',num2str(glat),', ', num2str(glon),')']})
xlabel(ax,'Density [m^-3]')
ylabel(ax,'altitude [km]')

set(ax,'xscale','log')
xlim(ax,[1e6,1e20])
grid(ax,'on')
legend('show')

end
