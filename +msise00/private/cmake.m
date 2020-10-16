function cmake(src_dir)
% build program using CMake and default generator
% to specify generator with CMake >= 3.15 set environment variable CMAKE_GENERATOR
arguments
  src_dir (1,1) string
end

ccmd = "ctest -S " + fullfile(src_dir, "setup.cmake") +  " -VV";

ret = system('cmake --version');
if ret ~= 0
  error('cmake:environment_error', 'CMake not found')
end

if ~isfolder(src_dir)
  error("cmake:file_not_found", "source directory not found: " + src_dir)
end

ret = system(ccmd);
if ret ~= 0
  error('cmake:runtime_error', 'error building with CMake')
end

end
