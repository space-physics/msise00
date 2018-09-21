function test_msise00_matlab()
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

time = {'2013-03-31', '2013-04-01'}; 
altkm = 150.;
glat = 65;
glon = -148.;

%% run MSISE00
atmos = py.msise00.run(time, altkm, glat, glon);
%% Extract time
t = datetime(xarrayInd2vector(atmos, 'time') / 1e9, 'convertfrom', 'posixtime');

assert(t(1) == datetime(time{1}))
%% extract values
He = xarray2mat(atmos{'He'});
N2 = xarray2mat(atmos{'N2'});
O = xarray2mat(atmos{'O'});

assert_allclose(N2(13), 3.051389580214272e16)
%% plot

figure()
plot(t, N2)
ylabel('density [m^{-3}]')
title('N_2 vs. time')
end


function M = xarray2mat(V)
M = double(py.numpy.asfortranarray(V));
end

function I = xarrayInd2vector(V,key)

Iv = V{key}.indexes{key}.values.tolist();

I = cellfun(@double, cell(Iv));

end

function assert_allclose(actual, desired, atol,rtol)
narginchk(2,4)

if nargin<3 || isempty(atol), atol=0; end
if nargin<4 || isempty(rtol), rtol=1e-7; end

measdiff = abs(actual-desired);
tol = atol + rtol * abs(desired);
assert(all(measdiff(:) <= tol))

end
