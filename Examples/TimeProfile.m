% geographic WGS84 lat,lon,alt
function TimeProfile()

glat = 65.1;
glon = -147.5;

gi = struct;
gi.f107s = 150;
gi.f107 = 150;
gi.Ap = 4;

alt_km = 200;
t0 = datetime(2015, 12, 13, 10, 1, 2);
t1 = datetime(2015, 12, 14, 10, 3, 4);

cwd = fileparts(mfilename('fullpath'));
addpath(fullfile(cwd, '..'));

time = t0:seconds(3600):t1;

for i = 1:length(time)
  atmos(i) = msise00.msise00(time(i), glat, glon, gi, alt_km); %#ok<AGROW>
end

msise00.plottime(atmos, time, glat, glon);

end
