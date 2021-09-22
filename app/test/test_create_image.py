from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

INVALID_DOCKERFILE = bytes("SOME\nINVALID\nDOCKERFILE", "utf-8")

DOCKERFILE_BUILD_ERR = bytes("FROM python:3.8-alpine\nCOPY notexisting.file .", "utf-8")


def test_invalid_dockerfile():
    response = client.post(
        "/create_image?name=test&tag=test",
        files={
            "file": INVALID_DOCKERFILE,
        },
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "dockerfile parse error line 1: unknown instruction: SOME"
    }


def test_not_existing_resource_in_dockerfile():
    response = client.post(
        "/create_image?name=test&tag=test",
        files={
            "file": DOCKERFILE_BUILD_ERR,
        },
    )
    print(response.json())
    assert response.status_code == 400
    assert response.json() == {
        "detail": "COPY failed: file not found in build context or excluded by .dockerignore: stat notexisting.file: file does not exist"
    }


def test_no_dockerfile():
    response = client.post("/create_image?name=test&tag=test", files={})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "file"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_missing_params():
    response = client.post(
        "/create_image?=test&tag=", files={"file": INVALID_DOCKERFILE}
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["query", "name"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["query", "tag"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
                "ctx": {"limit_value": 1},
            },
        ]
    }
