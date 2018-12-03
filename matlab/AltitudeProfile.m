% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
f107a = 150;
f107 = 150;
Ap = 4;
alt_km = 50:20:1000;
time = '2015-12-13 10:00:00';

for i = 1:length(alt_km)
    atmos(i) = msise00(time, glat, glon, f107a, f107, Ap, alt_km(i)); %#ok<SAGROW>
end

plotalt(atmos, time, glat, glon)
