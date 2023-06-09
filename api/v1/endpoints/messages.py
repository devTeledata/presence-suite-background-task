from typing import Any

from fastapi import APIRouter
from fastapi import BackgroundTasks

from schema.PresenceSuite import PresenceSuite
from tasks.PresenceSuite import PresenceSuiteTask

router = APIRouter()

@router.post("/presencesuite-task")
@router.post("/presencesuite-task/", include_in_schema=False)
def get_pubsub_message(presencesuite: PresenceSuite, background_tasks: BackgroundTasks) -> Any:

    task = PresenceSuiteTask()

    background_tasks.add_task(task.task, presencesuite)

    #task.task(presencesuite)
    return 'OK'


