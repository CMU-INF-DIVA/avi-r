# Version History

## AVI-R v1.3.8

* Add back timeout.
* More robust during iteration initialization.
* Limit seek retries based on frame id.

## AVI-R v1.3.7

* Remove default timeout.
* Bypass kwargs to _init.

## AVI-R v1.3.6

* Add timeout for PyAV.

## AVI-R v1.3.5

* More robust extraction of frame size.

## AVI-R v1.3.4

* Ignore errors in metadata decoding.

## AVI-R v1.3.3

* Fix seek retry.

## AVI-R v1.3.2

* More robust seek.

## AVI-R v1.3.1

* Optimized reorder buffer for faster random access.

## AVI-R v1.3

* Fix memory leak with explicit `close` method.

## AVI-R v1.2.1

* Update video properties.

## AVI-R v1.1.1

* Consistent action for `seek(0)`.

## AVI-R v1.1

* Optimized stability and efficiency for bidirectional frame.

## AVI-R v1.0.1

* Optimized random access.
* Deprecate annotation converter.
* Release on PyPI.

## DIVA IO v0.3

* Optimized random access and fix missing.
* Robustness improvement.
* Speed test.

## DIVA IO v0.2 (Deprecated)

* Real random access in video loader.
* Add annotation converter.
* Warning control option.

## DIVA IO v0.1

* Initial release of video loader.
