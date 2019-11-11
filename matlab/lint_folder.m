function results = lint_folder(folder, verbose)
%% lints each Matlab .m file in folder.
% distinct from mlintrpt() in that this function is all CLI instead of GUI

narginchk(1,2)
assert(is_folder(folder), [folder, ' is not a folder'])

matfiles = dir([folder, '/*.m']);

for i = 1:length(matfiles)
  file = [folder, '/', matfiles(i).name];
  res = checkcode(file);
  if ~isempty(res)
    [~, stem] = fileparts(file);
    results.(stem) = res;
    if verbose
      disp([file, ' has ', int2str(length(res)), ' lint messages.'])
    end
  end
end % for

if ~nargout, clear('results'), end

end % function