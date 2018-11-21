function assert_allclose(actual, desired, atol,rtol)
narginchk(2,4)

if nargin<3 || isempty(atol), atol=0; end
if nargin<4 || isempty(rtol), rtol=1e-7; end

measdiff = abs(actual-desired);
tol = atol + rtol * abs(desired);
assert(all(measdiff(:) <= tol))

end