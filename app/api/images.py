from fastapi import APIRouter, File, UploadFile, Depends, Query, HTTPException
from ..service.docker_service import DockerService
from docker.errors import APIError, BuildError


router = APIRouter()


@router.post("/create_image")
def create_image(
    name: str = Query(..., min_length=2),
    tag: str = Query(..., min_length=1),
    docker_service: DockerService = Depends(DockerService),
    file: UploadFile = File(...),
):
    try:
        repo = docker_service.build_and_push(file=file.file, name=name, tag=tag)
    except APIError as error:
        raise HTTPException(status_code=400, detail=error.explanation)
    except BuildError as error:
        raise HTTPException(status_code=400, detail=error.msg)

    return {"msg": "Successfully published repository '{}'".format(repo)}
