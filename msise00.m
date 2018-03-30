function msise00()
% quick demo calling MSISE00 model from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/

% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 10:10:1000;
t = '2015-12-13T10';


dt = py.msise00.rungtd7(t,alt_km,glat,glon);

dens = xarray2mat(dt(1));
temp = xarray2mat(dt(2));
species = xarrayind2vector(dt(1),'species');

plotmsis(alt_km,dens,temp,species,t,glat,glon)
end

function plotmsis(alt_km,dens,temp,species,t,glat,glon)
  figure(1), clf(1)
  ax = axes('nextplot','add');

  for i = 1:size(dens,2)
    semilogx(ax,dens(:,i), alt_km, 'DisplayName',species{i})
  end

  set(ax,'xscale','log')
  title({[t,' deg.  (',num2str(glat),',', num2str(glon),')']})
  xlabel('Density [m^-3]')
  ylabel('altitude [km]')

  xlim([1e6,1e20])
  grid('on')
  legend('show')

end

function V = xarray2mat(V)
  % convert xarray 2-D array to Matlab matrix


V= V{1}.values;
S = V.shape;
V = cell2mat(cell(V.ravel('F').tolist()));
V = reshape(V,[int64(S{1}), int64(S{2})]);

end

function I = xarrayind2vector(V,key)

C = cell(V{1}.indexes{key}.values.tolist);  % might be numeric or cell array of strings

if iscellstr(C) || any(class(C{1})=='py.str')
    I=cellfun(@char,C, 'uniformoutput',false);
else
    I = cell2mat();
end % if

end % function