function test_msise00_matlab()

if verLessThan('matlab','9.3'), warning('Matlab >= R2017b required for Python 3.6'), end

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
He = xarrayDataArray2mat(atmos{'He'});
N2 = xarrayDataArray2mat(atmos{'N2'});
O = xarrayDataArray2mat(atmos{'O'});

assert_allclose(N2(13), 3.051389580214272e16)
%% plot

figure()
plot(t, N2)
ylabel('density [m^{-3}]')
title('N_2 vs. time')
end


function V = xarrayDataArray2mat(V)
  % convert xarray DataArray to Matlab matrix

  
V= V.values; 
S = V.shape;
V = cell2mat(cell(V.ravel('F').tolist()));
V = reshape(V,[int64(S{1}), int64(S{2})]);
    
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
