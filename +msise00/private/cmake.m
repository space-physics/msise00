function cmake(src_dir)
% build program using CMake
arguments
  src_dir (1,1) string
end

assert(isfolder(src_dir), "source directory not found: %s", src_dir)

build_dir = fullfile(src_dir, "build");

fix_macos()

assert(system("cmake --version") == 0, 'CMake not found')

cmd = "cmake -B" + build_dir + "-S" + src_dir;
assert(system(cmd) == 0, 'error building with CMake')

cmd = "cmake --build " + build_dir;
assert(system(cmd) == 0, 'error building with CMake')

end


function fix_macos()

%% MacOS PATH workaround
% Matlab does not seem to load .zshrc or otherwise pickup shell "export" like
% Matlab on Linux or Windows does, so we apply these MacOS-specific workaround
if ~ismac
  return
end

sys_path = getenv("PATH");
needed_paths = ["/usr/local/bin", "/opt/homebrew/bin"];
for np = needed_paths
  if isfolder(np) && ~contains(sys_path, np)
    sys_path = np + pathsep + sys_path;
  end
end

setenv('PATH', sys_path)

end % function
