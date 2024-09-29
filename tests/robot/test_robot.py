import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from src.robot.robot import Robot
from src.schemas.robot import JobRequest, Command, Direction
from src.models.result import Result
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def mock_db_session():
    return MagicMock(spec=AsyncSession)


@pytest.fixture
def mock_result():
    return MagicMock(spec=Result)


@pytest.mark.asyncio
@patch("src.robot.robot.add_result_to_db")
@pytest.mark.parametrize(
    "job_request, expected_result, expected_commands",
    [
        # no overlapo
        (
            JobRequest(
                start={"x": 0, "y": 0},
                commands=[
                    Command(direction=Direction.EAST, steps=5),
                    Command(direction=Direction.NORTH, steps=3),
                ],
            ),
            9,
            2,
        ),
        # partial overlap
        (
            JobRequest(
                start={"x": 0, "y": 0},
                commands=[
                    Command(direction=Direction.EAST, steps=5),
                    Command(direction=Direction.NORTH, steps=5),
                    Command(direction=Direction.WEST, steps=5),
                ],
            ),
            16,
            3,
        ),
        # full overlap
        (
            JobRequest(
                start={"x": 0, "y": 0},
                commands=[
                    Command(direction=Direction.NORTH, steps=5),
                    Command(direction=Direction.SOUTH, steps=5),
                ],
            ),
            6,
            2,
        ),
        # no movement
        (
            JobRequest(
                start={"x": 0, "y": 0},
                commands=[],
            ),
            1,
            0,
        ),
        # movement over start
        (
            JobRequest(
                start={"x": 0, "y": 0},
                commands=[
                    Command(direction=Direction.NORTH, steps=2),
                    Command(direction=Direction.SOUTH, steps=4),
                ],
            ),
            5,
            2,
        ),
        # not starting at 0, 0
        (
            JobRequest(
                start={"x": 2, "y": 2},
                commands=[
                    Command(direction=Direction.NORTH, steps=5),
                    Command(direction=Direction.EAST, steps=3),
                    Command(direction=Direction.SOUTH, steps=2),
                ],
            ),
            11,
            3,
        ),
    ],
)
async def test_handle_job(
    mock_add_result_to_db,
    job_request,
    expected_result,
    expected_commands,
    mock_db_session,
    mock_result,
):
    robot = Robot()

    mock_add_result_to_db.return_value = mock_result
    mock_result.id = 1

    result = await robot.handle_job(job_request, mock_db_session)

    mock_add_result_to_db.assert_called_once()
    assert mock_add_result_to_db.call_args[0][1].commands == expected_commands

    assert result.id == mock_result.id
    assert isinstance(result.timestamp, datetime)
    assert result.commands == expected_commands
    assert result.result == expected_result
    assert result.duration > 0
