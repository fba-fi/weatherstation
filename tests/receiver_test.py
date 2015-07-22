"""Test the :mod:`weatherstation.receiver` module"""

from mock import Mock

from weatherstation.receiver import MicrochipReceiver

import pytest

import time

def test_read_data():
    """Test reading from the device

    :returns: None

    """

    receiver = MicrochipReceiver()

    attrs = {'read.return_value': []}
    receiver.device = Mock(**attrs)

    data = receiver.read_data()
    assert data == []

    expected_data = ['foo']
    attrs = {'read.return_value': expected_data}
    receiver.device = Mock(**attrs)

    data = receiver.read_data()
    assert data == expected_data


def test_write_data():
    """Test writing to the device

    :returns: None

    """

    receiver = MicrochipReceiver()

    expected_data = ['foo']
    attrs = {'write.return_value': 4}

    device = Mock(**attrs)

    receiver.device = device

    data = receiver.write_data(expected_data)

    device.write.assert_called_once_with(1, [2, 1, 1, 'foo'], 0)


@pytest.mark.display_integration
def test_display_integration(receiver):
    """@todo: Docstring for test_display_control.

    :arg1: @todo
    :returns: @todo

    """

    for direction in range(0, 10000, 10):

        measurement = {
            "direction_min": (direction) % 360,
            "direction_avg": (direction + 15) % 360,
            "direction_max": (direction + 30) % 360,
            "speed_min": 22.2,
            "speed_avg": 25.0,
            "speed_max": 34.2,
            "temperature": 27.7
        }

        display_address = [80,80,80]

        base = ord("0")

        data_text = "%03.0f,%03.0f,%03.0f,%0.1f,%0.1f,%0.1f,%0.1f" % (
            measurement["direction_min"],
            measurement["direction_avg"],
            measurement["direction_max"],
            measurement["speed_min"],
            measurement["speed_avg"],
            measurement["speed_max"],
            measurement["temperature"])

        for char in data_text:
            data_payload.append(ord(char))

        data_packet = display_address + data_payload + [0]

        num = receiver.write_data(data_packet)

        print 'Wrote %s bytes' % str(num)

        time.sleep(0.2)
