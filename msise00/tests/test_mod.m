%% simple
time = datenum(2001,2,2,8,0,0);
glat = 60;
glon = -70;
f107a = 163.6666;
f107 = 146.7;
Ap = 7;
altkm = 400.;

cwd = fileparts(mfilename('fullpath'));
matlab_root = [cwd, '/../../matlab'];
assert(isfolder(matlab_root), ['Matlab directory does not exist: ', matlab_root])
addpath(matlab_root)

atmo = msise00(time, glat, glon, f107a, f107, Ap, altkm);
%% read CCMC output
fid = fopen([cwd,filesep,'ccmc.log']);

A = cell2mat(textscan(fid, '%f %f %f %f %f %f %f %f %f %f %f %f', 1, ...
  'ReturnOnError', false, 'HeaderLines', 25));

A(2:4) = A(2:4) * 1e6;  % cm^-3 => m^-3
A(5) = A(5) * 1000; % gram cm^-3 => kg m^-3
A(8:end) = A(8:end) * 1e6;

fclose(fid);
%% compare
assert(abs(atmo.altkm - A(1)) < 0.1, 'wrong altitude?')
assert(abs(atmo.nO - A(2)) < A(2)*0.05, 'O error')
assert(abs(atmo.nN2 - A(3)) < A(3)*0.25, 'N2 error')
assert(abs(atmo.nO2 - A(4)) < A(4)*0.3, 'O2 error')
assert(abs(atmo.nTotal - A(5)) < A(5)*0.1, 'total mass density')
assert(abs(atmo.Tn - A(6)) < A(6)*0.035, ['Tn: ', num2str(atmo.Tn), ' ', num2str(A(6))])
assert(abs(atmo.Texospheric - A(7)) < A(7)*0.035, 'Texo')
assert(abs(atmo.nHe - A(8)) < A(8)*0.25, 'He')
assert(abs(atmo.nAr - A(9)) < A(9)*0.4, 'Ar')
assert(abs(atmo.nH - A(10)) < A(10)*0.15, 'H')
assert(abs(atmo.nN - A(11)) < A(11)*0.3, 'N')
assert(abs(atmo.nOanomalous - A(12)) < A(12)*0.3, 'AO')

disp(['OK: MSISE00: ',version])
