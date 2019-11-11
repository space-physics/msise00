function times = datetimerange(t0, t1, ts)
% ts: seconds

narginchk(3,3)
t0 = datenum(t0);
t1 = datenum(t1);

times = t0:ts/86400:t1;

end