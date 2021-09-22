import docker


class DockerService:

    USERNAME = "testbuildandpush"

    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, file, name: str, tag: str) -> str:
        assert len(name.strip()) > 0, "name cannot be empty"
        assert len(tag.strip()) > 0, "tag cannot be empty"

        repo = "{}/{}:{}".format(DockerService.USERNAME, name, tag)

        self.client.images.build(fileobj=file, tag=repo, rm=True)
        print("BUILT IMAGE:", repo)

        return repo

    def push_image(self, repo: str):
        assert len(repo.strip()) > 0

        msg = self.client.images.push(repo)
        print("PUSHED IMAGE:", repo)

        return msg

    def build_and_push(self, file, name: str, tag: str):
        repo = self.build_image(file, name, tag)
        _ = self.push_image(repo)

        return repo
