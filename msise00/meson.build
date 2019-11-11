project('msise00', 'fortran',
  default_options : ['default_library=static', 'buildtype=release'])

driver = executable('msise00_driver',
  sources: ['fortran/nrlmsise00_sub.for', 'fortran/msise00_driver.f90']
)

test('MSISdriver', driver,
  args: ['30', '12', '1', '2', '65', '0', '100', '100', '4', '100'],
  timeout: 15)