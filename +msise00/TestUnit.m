classdef TestUnit < matlab.unittest.TestCase

methods (Test)

function test_ccmc(tc)
time = datetime(2001,2,2,8,0,0);
glat = 60;
glon = -70;
ind = struct("f107s", 163.6666, "f107", 146.7, "Ap", 7);
altkm = 400.;

cwd = fileparts(mfilename('fullpath'));

atmo = msise00.msise00(time, glat, glon, ind, altkm);
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
tc.assertEqual(ind.f107, atmo.f107)
tc.assertEqual(ind.f107s, atmo.f107s)
tc.assertEqual(ind.Ap, atmo.Ap)

tc.verifyEqual(A(1), atmo.altkm)
tc.verifyEqual(A(2), atmo.nO, 'RelTol', 0.01)
tc.verifyEqual(A(3), atmo.nN2, 'RelTol', 0.01)
tc.verifyEqual(A(4), atmo.nO2, 'RelTol', 0.01)
tc.verifyEqual(A(5), atmo.nTotal, 'RelTol', 0.01)
tc.verifyEqual(A(6), atmo.Tn, 'RelTol', 0.01)
tc.verifyEqual(A(7), atmo.Texo, 'RelTol', 0.01)
tc.verifyEqual(A(8), atmo.nHe, 'RelTol', 0.01)
tc.verifyEqual(A(9), atmo.nAr, 'RelTol', 0.01)
tc.verifyEqual(A(10), atmo.nH, 'RelTol', 0.01)
tc.verifyEqual(A(11), atmo.nN, 'RelTol', 0.01)
tc.verifyEqual(A(12), atmo.nOanomalous, 'RelTol', 0.01)

end


function test_ccmc2(tc)
time = datetime(2018,5,17,21,0,0);
glat = 55;
glon = 120;
ind = struct("f107s", 72.6, "f107", 71.5, "Ap", 9.5);
altkm = 300.;

atmo = msise00.msise00(time, glat, glon, ind, altkm);

tc.verifyEqual(4.874e7, atmo.nN2 / 1e6, "RelTol", 0.01)
tc.verifyEqual(1.622e6, atmo.nO2 / 1e6, "RelTol", 0.01)

tc.verifyEqual(794.1, atmo.Tn, "RelTol", 0.01)
tc.verifyEqual(800, atmo.Texo, "RelTol", 0.01)

end


function test_plot_alt(tc)
time = datetime(2018,5,17,21,0,0);
glat = 55;
glon = 120;
ind = struct("f107s", 72.6, "f107", 71.5, "Ap", 9.5);
altkm = 300.;

atmo = msise00.msise00(time, glat, glon, ind, altkm);

hf = msise00.plotalt(atmo, time, glat, glon);

tc.verifyClass(hf, "matlab.ui.Figure")

close(hf)

end

function test_plot_time(tc)
time = datetime(2018,5,17,21,0,0);
glat = 55;
glon = 120;
ind = struct("f107s", 72.6, "f107", 71.5, "Ap", 9.5);
altkm = 300.;

atmo = msise00.msise00(time, glat, glon, ind, altkm);

hf= msise00.plottime(atmo, time, glat, glon);

tc.verifyClass(hf, "matlab.ui.Figure")

close(hf)

end

end
end
