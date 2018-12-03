function iono = msise00(time, glat, glon, f107a, f107, Ap, altkm)

validateattributes(glat, {'numeric'}, {'scalar'})
validateattributes(glon, {'numeric'}, {'scalar'})
validateattributes(f107a, {'numeric'}, {'positive','scalar'})
validateattributes(f107, {'numeric'}, {'positive','scalar'})
validateattributes(Ap, {'numeric'}, {'positive','scalar'})
validateattributes(altkm, {'numeric'}, {'positive', 'scalar'})
%% binary MSISe00
cwd = fileparts(mfilename('fullpath'));
exe = [cwd,filesep,'..', filesep, 'bin', filesep, 'msise00_driver'];
if ispc, exe = [exe,'.exe']; end
if ~exist(exe,'file'), error('compile MSISE00 via setup_msise00.m'), end

doy = date2doy(time);
v = datevec(time);
hms = num2str(v(4:6));


cmd = [exe, ' ', int2str(doy), ' ', hms,...
       ' ',num2str(glat), ' ', num2str(glon),...
       ' ',num2str(f107a), ' ', num2str(f107), ' ', num2str(Ap),...
       ' ',num2str(altkm)];
[status,dat] = system(cmd);
if status ~= 0, error(dat), end


D = cell2mat(textscan(dat, '%f %f %f %f %f %f %f %f %f', 1, 'ReturnOnError', false));

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


T = cell2mat(textscan(dat, '%f %f', 1, 'HeaderLines', 1, 'ReturnOnError', false));
iono.Texospheric = T(1);
iono.Tn = T(2);
end
