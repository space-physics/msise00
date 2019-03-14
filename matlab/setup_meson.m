function setup_meson(srcdir, builddir)
%% setup using Meson + Ninja

validateattributes(srcdir,{'char'},{'vector'})
validateattributes(builddir,{'char'},{'vector'})

fprintf('Meson: ')
runcmd('meson --version')

fprintf('Ninja: ')
runcmd('ninja --version')


if ~exist([builddir,filesep,'build.ninja'], 'file')
  runcmd(['meson setup ',builddir,' ',srcdir])
end

runcmd(['ninja -C ',builddir])

disp('Build complete!')
end
