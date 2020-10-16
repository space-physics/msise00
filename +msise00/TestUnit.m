classdef TestUnit < matlab.unittest.TestCase

methods (Test)

function test_exe(tc)
time = datetime(2001,2,2,8,0,0);
glat = 60;
glon = -70;
f107a = 163.6666;
f107 = 146.7;
Ap = 7;
altkm = 400.;

cwd = fileparts(mfilename('fullpath'));

atmo = msise00.msise00(time, glat, glon, f107a, f107, Ap, altkm);
%% read CCMC output
ref_fn = fullfile(cwd, "../src/msise00/tests/ccmc.log");
fid = fopen(ref_fn);

A = cell2mat(textscan(fid, '%f %f %f %f %f %f %f %f %f %f %f %f', 1, ...
  'ReturnOnError', false, 'HeaderLines', 25));

A(2:4) = A(2:4) * 1e6;  % cm^-3 => m^-3
A(5) = A(5) * 1000; % gram cm^-3 => kg m^-3
A(8:end) = A(8:end) * 1e6;

fclose(fid);

%% compare
tc.verifyEqual(A(1), atmo.altkm, 'AbsTol', 0.1)
tc.verifyEqual(A(2), atmo.nO, 'RelTol', 0.05)
tc.verifyEqual(A(3), atmo.nN2, 'RelTol', 0.3)
tc.verifyEqual(A(4), atmo.nO2, 'RelTol', 0.4)
tc.verifyEqual(A(5), atmo.nTotal, 'RelTol', 0.1)
tc.verifyEqual(A(6), atmo.Tn, 'RelTol', 0.035)
tc.verifyEqual(A(7), atmo.Texospheric, 'RelTol', 0.035)
tc.verifyEqual(A(8), atmo.nHe, 'RelTol', 0.25)
tc.verifyEqual(A(9), atmo.nAr, 'RelTol', 0.6)
tc.verifyEqual(A(10), atmo.nH, 'RelTol', 0.15)
tc.verifyEqual(A(11), atmo.nN, 'RelTol', 0.3)
tc.verifyEqual(A(12), atmo.nOanomalous, 'RelTol', 0.3)

end
end
end
