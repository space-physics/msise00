%% MacOS PATH workaround
% Matlab does not seem to load .zshrc or otherwise pickup shell "export" like
% Matlab on Linux or Windows does, so we apply these MacOS-specific workaround

function fix_macos()

if ~ismac
  return
end

sys_path = getenv("PATH");
needed_paths = ["/opt/homebrew/bin", "/usr/local/bin"];
for np = needed_paths
  if isfolder(np)
    if contains(sys_path, np)
      return
    else
      sys_path = np + pathsep + sys_path;
      break
    end
  end
end

setenv('PATH', sys_path)

end
