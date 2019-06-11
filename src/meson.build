
driver = executable('msise00_driver', 'nrlmsise00_sub.for', 'msise00_driver.f90')

testexe = executable('test_msise00', 'nrlmsise00_sub.for', 'reference/nrlmsise00_driver.for')

test('MSISprint', testexe)
