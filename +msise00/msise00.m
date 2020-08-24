function iono = msise00(time, glat, glon, f107a, f107, Ap, altkm)
%% run MSISe00
arguments
  time (1,1) datetime
  glat (1,1) {mustBeNumeric,mustBeFinite}
  glon (1,1) {mustBeNumeric,mustBeFinite}
  f107a (1,1) {mustBeNumeric,mustBeFinite,mustBeNonnegative}
  f107 (1,1) {mustBeNumeric,mustBeFinite,mustBeNonnegative}
  Ap (1,1) {mustBeNumeric,mustBeFinite,mustBeNonnegative}
  altkm (1,1) {mustBeNumeric,mustBeFinite,mustBeNonnegative}
end
%% binary MSISe00
cwd = fileparts(mfilename('fullpath'));
src_dir = fullfile(cwd,'../src/msise00');
exe = fullfile(src_dir, 'msise00_driver');
if ispc, exe = [exe, '.exe']; end
if ~isfile(exe)
  msise00.cmake(src_dir)
end

doy = day(time, 'dayofyear');
year2 = int2str(year(time));
year2 = year2(3:4);
iyd = sprintf('%s%03d', year2, doy);
hms = sprintf('%02d %02d %02d', hour(time), minute(time), second(time));

cmd = [exe, ' ', iyd, ' ', hms,...
       ' ',num2str(glat), ' ', num2str(glon),...
       ' ',num2str(f107a), ' ', num2str(f107), ' ', num2str(Ap),...
       ' ',num2str(altkm)];

[ret,dat] = system(cmd);
assert(ret == 0, dat)

D = cell2mat(textscan(dat, '%f', 'ReturnOnError', false));
if length(D)~=11
  disp(dat)
  error(['unexpected output from MSISe00 using ', exe])
end

iono.altkm = altkm;
iono.nHe = D(1);
iono.nO = D(2);
iono.nN2 = D(3);
iono.nO2 = D(4);
iono.nAr = D(5);
iono.nTotal = D(6);
iono.nH = D(7);
iono.nN = D(8);
iono.nOanomalous = D(9);

iono.Texospheric = D(10);
iono.Tn = D(11);
end
