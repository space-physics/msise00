classdef TestLint < matlab.unittest.TestCase

methods (Test)

function test_linter(tc)
cwd = fileparts(mfilename('fullpath'));

fail = checkcode_recursive(fullfile(cwd, '..'), tc, fullfile(cwd, "MLint.txt"));

tc.verifyFalse(fail)
end

end

end
