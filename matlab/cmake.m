function cmake(srcdir, builddir)
% assumes CMake >= 3.13
narginchk(2,2)
validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

tail = [' -S ', srcdir, ' -B ', builddir];

ccmd = ['cmake ',tail];

runcmd(ccmd)

runcmd(['cmake --build ',builddir,' --parallel'])

end
