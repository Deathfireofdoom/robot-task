import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
from src.main import app
from src.models.result import Result


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
@patch("src.core.database.get_db_session", new_callable=AsyncMock)
@patch("src.robot.robot.Robot.handle_job", new_callable=AsyncMock)
@pytest.mark.parametrize(
    "job_request, handle_job_side_effect, expected_status_code",
    [
        # happy
        (
            {
                "start": {"x": 0, "y": 0},
                "commands": [
                    {"direction": "east", "steps": 5},
                    {"direction": "north", "steps": 3},
                ],
            },
            None,
            200,
        ),
        # bad request input
        (
            {
                "start": {"x": 0, "y": 0},
                "commands": [
                    {"direction": "invalid", "steps": 5},
                    {"direction": "north", "steps": 3},
                ],
            },
            None,
            422,
        ),
        # exception
        (
            {
                "start": {"x": 0, "y": 0},
                "commands": [
                    {"direction": "east", "steps": 5},
                    {"direction": "north", "steps": 3},
                ],
            },
            Exception("Error during job processing"),
            500,
        ),
    ],
)
async def test_post_job(
    mock_handle_job,
    mock_get_db_session,
    client,
    job_request,
    handle_job_side_effect,
    expected_status_code,
):
    mock_db = AsyncMock()
    mock_get_db_session.return_value = mock_db

    if handle_job_side_effect is None:
        mock_result = Result(
            id=1, timestamp="1994-12-16T00:00:00", commands=0, result=0, duration=0.0
        )
        mock_handle_job.return_value = mock_result
    else:
        mock_handle_job.side_effect = handle_job_side_effect

    if handle_job_side_effect is not None:
        with pytest.raises(Exception, match="Error during job processing"):
            response = client.post(
                "/tibber-developer-test/enter-path", json=job_request
            )
            assert response.status_code == expected_status_code
    else:
        response = client.post("/tibber-developer-test/enter-path", json=job_request)

        assert response.status_code == expected_status_code
        if response.status_code == 200:
            result = response.json()
            assert result["id"] == 1
            assert result["commands"] == 0
            assert result["result"] == 0
            assert result["duration"] == 0.0
