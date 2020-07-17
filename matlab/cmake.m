function cmake(srcdir)
% build project with CMake
narginchk(1,1)
validateattributes(srcdir,{'char'},{'vector'},1)

ccmd = ['ctest -S ', srcdir, '/setup.cmake -VV'];

runcmd(ccmd)

end
