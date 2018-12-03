function atmos = msise00(time, alt_km, glat, glon)
%% call MSISE00 model from Matlab.
% https://www.scivision.co/matlab-python-user-module-import/
assert(~verLessThan('matlab', '9.5'), 'Matlab >= R2018b required')

narginchk(4,4)
validateattributes(alt_km, {'numeric'}, {'positive', 'vector'})
validateattributes(glat, {'numeric'}, {'scalar'})
validateattributes(glon, {'numeric'}, {'scalar'})

switch class(time)
    case {'datetime', 'double'}, time = datestr(time, 30);
end

atmos = py.msise00.run(time, alt_km, glat, glon);
end
