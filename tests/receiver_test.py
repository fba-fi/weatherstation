"""Test the :mod:`weatherstation.receiver` module"""

from mock import Mock

from weatherstation.receiver import MicrochipReceiver

import pytest

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

    measurement = {
        "direction_min": 170,
        "direction_avg": 185,
        "direction_max": 240,
        "speed_min": 7.2,
        "speed_avg": 9.9,
        "speed_max": 13.2,
        "temperature": 23.3
    }

    display_address = [80,80,80]

    base = ord("0")

    data_text = "%s,%s,%s,%s,%s,%s,%s" % (
        measurement["direction_min"],
        measurement["direction_avg"],
        measurement["direction_max"],
        measurement["speed_min"],
        measurement["speed_avg"],
        measurement["speed_max"],
        measurement["temperature"])

    data_payload = []

    for char in data_text:
        data_payload.append(ord(char) - ord("0"))

    data_packet = display_address + data_payload

    data_packet = display_address + [
        48,54,53,44,49,57,48,44,50,48,48,44,51,46,
        50,44,53,46,56,44,49,48,46,52,44,49,57,46,54]

    num = receiver.write_data(data_packet)

    print 'Wrote %s bytes' % str(num)



