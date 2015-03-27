FC = gfortran
FCFLAGS = -O2 -mtune=native

all: libnrlmsis.a testgtd7

LIBOBJS = physics_constants.o utils_spline.o physics_msis.o utils_constants.o

%.o: %.f90
	$(FC) $(FCFLAGS) -c $<

%.o: %.F90
	$(FC) $(CPPFLAGS) $(FCFLAGS) -c $<

libnrlmsis.a: $(LIBOBJS)
	$(AR) $(ARFLAGS) $@ $(LIBOBJS)

testgtd7: testgtd7.f90 libnrlmsis.a
	$(FC) $(FCFLAGS) $(LDFLAGS) -o $@ $< libnrlmsis.a

utils_constants.o: utils_constants.f90
physics_constants.o: physics_constants.f90 utils_constants.o
utils_spline.o: utils_spline.f90 utils_constants.o
physics_msis.o: physics_msis.f90 physics_constants.o physics_msis.o utils_constants.o
