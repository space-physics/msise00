% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
f107a = 150;
f107 = 150;
Ap = 4;
alt_km = 200;
t0 = '2015-12-13 10:00:00';
t1 = '2015-12-14 10:00:00';

time = datetimerange(t0, t1, 3600);

for i = 1:length(time)
    atmos(i) = msise00(time(i), glat, glon, f107a, f107, Ap, alt_km); %#ok<SAGROW>
end

plottime(atmos, time, glat, glon)
