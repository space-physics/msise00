function build(fc)

if nargin < 1
  fc = 'gfortran';
end
validateattributes(fc, {'char'}, {'vector'})

cwd = fileparts(mfilename('fullpath'));
builddir = [cwd, filesep, '..', filesep, 'msise00'];
srcdir = [builddir, filesep, 'fortran'];

if strcmp(fc, 'ifort') && ispc
  opt = '/O2';
else
  opt = '-O2';
end

cmd = [fc, ' ', opt, ' ',...
       srcdir,filesep,'nrlmsise00_sub.for', ' ', ...
       srcdir,filesep,'msise00_driver.f90', ' ',...
       '-o ',builddir,filesep,'msise00_driver'];

disp(cmd)
runcmd(cmd)

end


function build_cmake(srcdir, builddir)
%% build using CMake

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

runcmd(['cmake --build ',builddir, ' --parallel'])

end


function build_meson(srcdir, builddir)
%% build using Meson + Ninja

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

disp('Meson: ')
runcmd('meson --version')

disp('Ninja: ')
runcmd('ninja --version')

if ~exist([builddir,filesep,'build.ninja'], 'file')
  runcmd(['meson setup ',builddir,' ',srcdir])
end

runcmd(['ninja -C ',builddir])

end
