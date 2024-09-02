# Lawen(Large **L**anguage Model **A**gent for **W**eb **En**vironment)

## Getting Started

### Install from pypi(unfinished)

If you want to use poetry to manage your project, you can follow the instruction [here](https://python-poetry.org/docs/basic-usage/). Otherwise, you can use `pip` to install the package.

#### Option 1: Install the basic package

```bash
# The basic package can be installed with pip
pip install lawen

# or poetry
poetry add lawen
```

#### Option 2: Install the basic package with extra package

```bash
# These extra package can be installed with pip, you can choose one or more of them.
pip install lawen[miniwob, mongodb, mysql, orjson, postgresql, redis, ujson, mind2web, webarena]

# poetry version
poetry add lawen --extras "miniwob mongodb mysql orjson postgresql redis ujson mind2web webarena"
```

#### Option 3: Install the basic package with all environment extra package

`mysql|mongodb|postgresql|redis` are used to store the log.
`orjson|ujson` are used to fasten the serialization and deserialization of json data.

```bash

# envs can be combined with other json or database extra packages.
pip install lawen[envs]

# poetry version
poetry add lawen --extras "envs"
```

### Install from source

Since the project is managed by `poetry`, you should install `poetry` first.

```bash
# poetry can be installed with conda
conda install poetry
```

Or you can follow the instruction [here](https://python-poetry.org/docs/#installation)

```bash
# Clone the repository
git clone --recursive https://github.com/1746104160/lawen.git

# To install the library
poetry install --all-extras
```

> If you want to use `mysql|mongodb|postgresql|redis` to store the log, you should install the corresponding database first.

## Environment

> Since `MiniWoB++` environment is based on selenium, you should install `Chrome/Chromium` and `chromedriver` manually.
> Since `WebArena` environment is based on playwright, you should run `playright install` command after installation.

The code has already been tested on Python > 3.10, < 3.12 in `Ubuntu 22.04` , `Windows 11` and `WSL2 Ubuntu 22.04` platforms.

> Since chromedriver is depend on `chromium`, which can be easily installed with command `sudo snap install chromium`, it's suggested to enable `systemd` in `WSL2` environment. Please follow the instruction [here](https://learn.microsoft.com/en-us/windows/wsl/systemd)

## Basic Usage

```python
"""This is a simple example of using the SimpleLLMAgent."""
from logging import info

from lawen.agents import SimpleLLMAgent
from lawen.envs.miniwob import MiniWoBEnv

env: MiniWoBEnv = MiniWoBEnv(
    name="miniwob/click-test-2-v1",
    env_type="static",
    render_mode="human",
)
agent = SimpleLLMAgent(
    name="llm_agent",
    env=env,
    api_base="your-api-base",
    api_key="your-api-key",
    model_name="your-model-name",
    template="prompts/templates/test.txt",
    task="click-test",
    proxy="your-proxy",
)
try:
    for _ in range(10):
        # Start a new episode.
        obs, infos = env.reset()

        # choose action.
        action, input_action_args = agent.next_action(obs)
        obs, reward, terminated, truncated, infos = env.step(
            action,
            **input_action_args,
        )

        # print info.
        action_info = f"Action: {action.name}, Args: {input_action_args}"
        info(action_info)
        reward_info = f"Reward: {reward}"
        info(reward_info)
        terminated_info = f"Terminated: {terminated}"
        info(terminated_info)
        truncated_info = f"Truncated: {truncated}"
        info(truncated_info)
        infos_info = f"Info: {infos}"
        info(infos_info)

finally:
    env.close()
```

## Development

### dataClass

Dataclass is a decorator which is used to create a class with some special features, such as:

* `__init__` method automatically generated
* `__repr__` method automatically generated
* `__post_init__` method after `__init__` method
* `field` method to specify the type of the field, which can be used to validate the type of the field(especially for the usage of marshmallow)

## marshmallow

Marshmallow is a library which is used to serialize and deserialize json data. It can be used to validate the type of the field.

## orjson

It is current the fastest json library in python, while it does not support load and dump method. It only supports loads and dumps method.

## encapsulation

The `make_instance` method is used to encapsulate the `__init__` method of the dataclass. It can be used to create an instance of the dataclass with the given json data, or simply keyword arguments.

The `dump_instance` method is used to encapsulate the `dump` method of the marshmallow schema class. It can be used to dump the instance of the dataclass to json data, which is better for data transmission during the llm process.

## code lint and format

The `ruff` package is used to lint the code. It is a wrapper of `flake8` and `black`. It can be used to lint the code and format the code efficiently.

## code test

The `pytest` package is used to automately test the code. It can be used to test the code efficiently.
