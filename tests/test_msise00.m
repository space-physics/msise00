%% environment
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')
v = ver('matlab');
mv = v.Version;
pv = pyversion;
switch(mv)
  case '9.5', assert(pv=="3.6", 'Matlab <-> Python version mismatch')
end

%% simple
cwd = fileparts(mfilename('fullpath'));
addpath([cwd,'/../matlab'])

time = {'2013-03-31', '2013-04-01'}; 
altkm = 150.;
glat = 65;
glon = -148.;

atmos = py.msise00.run(time, altkm, glat, glon);

t = xarrayind2vector(atmos, 'time');

assert(t(1) == datetime(time{1}))

He = xarray2mat(atmos{'He'});
N2 = xarray2mat(atmos{'N2'});
O = xarray2mat(atmos{'O'});

assert_allclose(N2(13), 3.051389580214272e16)
