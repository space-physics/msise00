function build(build_sys, srcdir, builddir)
% build with 'meson' or 'cmake'

validateattributes(build_sys, {'char'}, {'vector'})

if nargin < 3
cwd = fileparts(mfilename('fullpath'));
srcdir =   [cwd, filesep,'..', filesep, 'src'];
builddir = [cwd, filesep,'..',filesep,'build'];
end

assert(exist(srcdir,'dir')==7, ['source directory ',srcdir,' does not exist'])
assert(exist(builddir,'dir')==7, ['build directory ',builddir,' does not exist'])

switch build_sys
  case 'meson', build_meson(srcdir, builddir)
  case 'cmake', build_cmake(srcdir, builddir)
  otherwise error('Specifiy "meson" or "cmake" to build this project.')
end

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
