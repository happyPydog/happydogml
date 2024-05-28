import pytest

from happydogml.utilities import track


def test_track_success(test_logger, mocker):
    mock_info = mocker.patch.object(test_logger, "info")

    @track(logger=test_logger)
    def add(x: int, y: int) -> int:
        return x + y

    result = add(5, 10)
    assert result == 15
    mock_info.assert_called_once()
    log_data = mock_info.call_args[0][0]
    assert log_data["function"] == "add"
    assert log_data["args"] == (5, 10)
    assert log_data["kwargs"] == {}
    assert log_data["status"] == "success"
    assert log_data["result"] == 15
    assert "execution_time" in log_data


def test_track_error(test_logger, mocker):
    mock_info = mocker.patch.object(test_logger, "info")

    @track(logger=test_logger)
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
    mock_info.assert_called_once()
    log_data = mock_info.call_args[0][0]
    assert log_data["function"] == "divide"
    assert log_data["args"] == (5, 0)
    assert log_data["kwargs"] == {}
    assert log_data["status"] == "error"
    assert log_data["error"] == "division by zero"
    assert "execution_time" in log_data
