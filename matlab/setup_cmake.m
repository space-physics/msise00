function setup_cmake(srcdir, builddir)
%% setup using CMake

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

runcmd('cmake --version')

if ispc
  wopts = '-G "MinGW Makefiles" -DCMAKE_SH="CMAKE_SH-NOTFOUND"';
else
  wopts = '';
end

ccmd = ['cmake ', wopts, ' -S ', srcdir, ' -B ', builddir];

runcmd(ccmd)

runcmd(['cmake --build ',builddir])

disp('Build complete!')
end
