"""Test the :mod:`weatherstation.receiver` module"""

from mock import Mock

from weatherstation.receiver import MicrochipReceiver

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
