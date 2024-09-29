from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.robot import JobRequest, JobResult, Command, Direction
from src.models.result import Result
from src.crud.result import add_result_to_db
from src.robot.memory import Memory


class Robot:
    def __init__(self):
        self.memory = Memory()
        self.x, self.y = 0, 0

    async def handle_job(self, job: JobRequest, db: AsyncSession) -> JobResult:
        start_time = datetime.now()
        self.x, self.y = job.start.x, job.start.y

        self.memory.add_movement(self.x, self.y, self.x, self.y)

        for command in job.commands:
            self._act_on_command(command)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        result = await self._calculate_result(duration, len(job.commands), db)
        return result

    def _act_on_command(self, command: Command):
        x_start, y_start = self.x, self.y

        self._move_robot(command)

        self.memory.add_movement(
            x_start=x_start, x_end=self.x, y_start=y_start, y_end=self.y
        )

    def _move_robot(self, command: Command):
        match command.direction:
            case Direction.NORTH:
                self.y += command.steps

            case Direction.SOUTH:
                self.y -= command.steps

            case Direction.EAST:
                self.x += command.steps

            case Direction.WEST:
                self.x -= command.steps

            case _:
                raise Exception("Unexpected direction")

    async def _calculate_result(
        self, duration: float, n_commands: int, db: AsyncSession
    ) -> JobResult:
        visited = self.memory.calculate_visited()

        result_data = Result(
            timestamp=datetime.now(),
            commands=n_commands,
            result=visited,
            duration=duration,
        )

        # TODO(oe): Not sure if I am super happy with this part being here
        # maybe the database-action should be more isolated making testing
        # easier.
        result = await add_result_to_db(db, result_data)

        return JobResult(
            id=result.id,
            timestamp=result_data.timestamp,
            commands=result_data.commands,
            result=result_data.result,
            duration=result_data.duration,
        )
