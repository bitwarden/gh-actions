import sys
import anyio
import dagger


async def test():
    config = dagger.Config(log_output=sys.stderr)

    async with dagger.Connection(config) as client:

        # get reference to the local project
        src_id = await client.host().directory("").id()

        python = (
            client.container()
            # pull python container
            .from_("python:3.10-slim-buster")
            # mount cloned repository into image
            .with_mounted_directory("/src", src_id)
            # set working directory
            .with_workdir("/src")
            # install test dependencies
            .exec(["pip", "install", "pipenv"]).exec(["pipenv", "install", "-d"])
            # run tests
            .exec(["pipenv", "run", "pytest", "tests/"])
        )

        # execute
        await python.exit_code()

        print("Tests Successful")


if __name__ == "__main__":
    anyio.run(test)
