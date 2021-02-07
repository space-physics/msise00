function atmos = msise00(time, glat, glon, indices, altkm)
%% run MSISe00
arguments
  time (1,1) datetime
  glat (1,1) {mustBeNumeric,mustBeFinite}
  glon (1,1) {mustBeNumeric,mustBeFinite}
  indices (1,1) struct
  altkm (1,1) {mustBeNumeric,mustBeFinite,mustBeNonnegative}
end
%% binary MSISe00
cwd = fileparts(mfilename('fullpath'));
src_dir = fullfile(cwd, "../src/msise00");
exe = fullfile(src_dir, "msise00_driver");
if ispc, exe = exe + ".exe"; end
if ~isfile(exe)
  cmake(src_dir)
end

doy = day(time, 'dayofyear');
hms = sprintf('%02d %02d %02d', hour(time), minute(time), second(time));

cmd = exe + " " + doy + " " + hms +...
       " " + num2str(glat) + " " + num2str(glon) + ...
       " " + num2str(indices.f107s) + " " + num2str(indices.f107) + " " + num2str(indices.Ap) + ...
       " " + num2str(altkm);

[ret,dat] = system(cmd);
if ret ~= 0
  error("msise00:runtimeError", "MSISE00 failure %s", dat)
end

D = cell2mat(textscan(dat, '%f', 'ReturnOnError', false));
if length(D)~=11
  disp(dat)
  error("unexpected output from MSISe00 using " + exe)
end

atmos = struct("altkm", altkm, "f107s", indices.f107s, "f107", indices.f107, "Ap", indices.Ap,...
  "nHe", D(1), "nO", D(2), "nN2", D(3), "nO2", D(4), "nAr", D(5), ...
  "nTotal", D(6), "nH", D(7), "nN",  D(8),  "nOanomalous", D(9), "Texo", D(10), "Tn", D(11));

end
