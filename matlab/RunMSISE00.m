% geographic WGS84 lat,lon,alt
glat = 65.1;
glon = -147.5;
alt_km = 10:10:1000;
time = '2015-12-13T10:00:00';

A = msise00(time, alt_km, glat, glon);

plotmsis(A)