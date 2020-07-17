function iono = msise00(time, glat, glon, f107a, f107, Ap, altkm)
%% run MSIS E00
narginchk(7,7)
validateattributes(glat, {'numeric'}, {'scalar'}, mfilename, 'geodetic latitude',2)
validateattributes(glon, {'numeric'}, {'scalar'}, mfilename, 'geodetic longitude',3)
validateattributes(f107a, {'numeric'}, {'positive','scalar'},mfilename, '81 day AVERAGE OF F10.7 FLUX (centered on day)',4)
validateattributes(f107, {'numeric'}, {'positive','scalar'},mfilename, 'DAILY F10.7 FLUX FOR PREVIOUS DAY', 5)
validateattributes(Ap, {'numeric'}, {'positive','scalar'}, mfilename, 'MAGNETIC INDEX(DAILY)',6)
validateattributes(altkm, {'numeric'}, {'positive', 'scalar'},mfilename, 'altitude [km]',7)
%% binary MSISe00
cwd = fileparts(mfilename('fullpath'));
src_dir = fullfile(cwd,'../msise00');
build_dir = fullfile(src_dir, 'build');
exe = fullfile(build_dir, 'msise00_driver');
if ispc, exe = [exe, '.exe']; end
if ~is_file(exe), build('meson', src_dir, build_dir), end

doy = date2doy(time);
v = datevec(time);
hms = num2str(v(4:6));
iyd = int2str(v(1));
iyd = [iyd(3:4), num2str(floor(doy),'%03d')];


cmd = [exe, ' ', iyd, ' ', hms,...
       ' ',num2str(glat), ' ', num2str(glon),...
       ' ',num2str(f107a), ' ', num2str(f107), ' ', num2str(Ap),...
       ' ',num2str(altkm)];

[status,dat] = system(cmd);
if status ~= 0, error(dat), end


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
