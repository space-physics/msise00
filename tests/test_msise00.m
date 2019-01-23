%% simple
time = datenum(2001,2,2,8,0,0);
glat = 60;
glon = -70;
f107a = 163.6666;
f107 = 146.7;
Ap = 7;
altkm = 400.;

cwd = fileparts(mfilename('fullpath'));
addpath([cwd, filesep, '..', filesep, 'matlab'])

atmo = msise00(time, glat, glon, f107a, f107, Ap, altkm);

fid = fopen([cwd,filesep,'ccmc.log']);
while ~feof(fid)
  d = fgetl(fid);
  if ~isempty(d), dat = d; end
end

A = cell2mat(textscan(dat, '%f %f %f %f %f %f %f %f %f %f %f %f', 1, 'ReturnOnError', false));

assert(abs(atmo.altkm - A(1)) < 0.1, 'wrong altitude?')
assert(abs(atmo.nO - A(2)) < A(2)*0.005, 'O error')
assert(abs(atmo.nN2 - A(3)) < A(3)*0.01, 'N2 error')
assert(abs(atmo.nO2 - A(4)) < A(4)*0.01, 'O2 error')
assert(abs(atmo.nTotal - A(5)) < A(5)*0.01, 'total mass density')
assert(abs(atmo.Tn - A(6)) < A(6)*0.001, 'Tn')
assert(abs(atmo.Texospheric - A(7)) < A(7)*0.001, 'Texo')
assert(abs(atmo.nHe - A(8)) < A(8)*0.005, 'He')
assert(abs(atmo.nAr - A(9)) < A(9)*0.01, 'Ar')
assert(abs(atmo.nH - A(10)) < A(10)*0.005, 'H')
assert(abs(atmo.nN - A(11)) < A(11)*0.01, 'N')
assert(abs(atmo.nOanomalous - A(12)) < A(12)*0.001, 'AO')
