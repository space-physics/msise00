%% simple
time = datenum(2015,12,13,10,0,0);
glat = 65.1;
glon = -147.5;
f107a = 150.;
f107 = 150.;
Ap = 4;
altkm = 400.;

cwd = fileparts(mfilename('fullpath'));
addpath([cwd, filesep, '..', filesep, 'matlab'])

atmo = msise00(time, glat, glon, f107a, f107, Ap, altkm);

assert(abs(atmo.nN2 - 1900827.88) < 1e5, 'Ne error excessive')
