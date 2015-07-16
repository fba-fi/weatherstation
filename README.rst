Weather Station
===============

This software receives weather data from USB radio receiver (add model),
calculates statistics and produces some pretty graphics.

Requirements
------------

    * pyusb - https://github.com/walac/pyusb

Testing
-------

Run tests with pytest::

    py.test -sv tests

Or continously with pytest-xdist module::

    py.test -sv tests --looponfail

Integration tests with real hardware::

    py.test -sv test --hardware-integration

Installation
------------

Install software with command::

    python setup.py install

Configuration
-------------

Usage
-----

License
-------

Copyright (C) 2015  Mikko Vatanen <mikko@vapaatyyli.fi>, Kaale Nieminen

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

