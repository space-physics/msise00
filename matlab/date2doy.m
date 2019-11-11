function doy = date2doy(adate)
%% from https://github.com/scivision/sciencedates
narginchk(1,1)
v = datevec(adate);
n = datenum(v);

doy = n - datenum(v(:,1), 1,0);

end
