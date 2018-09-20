function msise00()
% quick demo calling MSISE00 model from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/

assert(~verLessThan('matlab', '8.4'), 'Matlab >= R2014b required')

% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 10:10:1000;
t = '2015-12-13T10';


atmos = py.msise00.run(t, alt_km, glat, glon);

plotmsis(atmos)
end

function plotmsis(atmos)

  species = cellfun(@char, cell(atmos.attrs{'species'}), 'uniformoutput', false);
  alt_km = xarrayind2vector(atmos, 'alt_km');
  times = xarrayind2vector(atmos, 'time');
  glat = xarrayind2vector(atmos, 'lat');
  glon = xarrayind2vector(atmos, 'lon');

  figure(1), clf(1)
  ax = axes('nextplot','add');
  
  for i = 1:size(species)
    dens = xarray2mat(atmos{species{i}});
    semilogx(ax, dens, alt_km, 'DisplayName', species{i})
  end

  set(ax,'xscale','log')
  title({[times,' (',num2str(glat),', ', num2str(glon),')']})
  xlabel('Density [m^-3]')
  ylabel('altitude [km]')

  xlim([1e6,1e20])
  grid('on')
  legend('show')

end

function V = xarray2mat(V)
  % convert xarray 2-D array to Matlab matrix


V = V.values;
S = V.shape;
V = cell2mat(cell(V.ravel('F').tolist()));
V = reshape(V,[int64(S{1}), int64(S{2})]);

end

function I = xarrayind2vector(V, key)

C = cell(V.indexes{key}.values.tolist);  % might be numeric or cell array of strings

if iscellstr(C) || (length(C) > 1 && isa(C{1}, 'py.str'))
    I = cellfun(@char,C, 'uniformoutput',false);
elseif isa(C{1}, 'py.datetime.datetime')
    I = char(C{1}.isoformat());
else
    I = cell2mat(C);
end % if

end % function