function doy = date2doy(adate)
%% from https://github.com/scivision/sciencedates

v = datevec(adate);
n = datenum(v);

doy = n - datenum(v(:,1), 1,0);

end
