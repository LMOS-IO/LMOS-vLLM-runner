import asyncio
import subprocess

from lmos_config.runner_instance import InstanceConfig
from lmos_config import config
from lmos_config.ConfigTypes.llm_runner.vllm import vLLMArgs

def get_own_config() :
    for llm_runner in config.services.llm_runner:
        if InstanceConfig.type == llm_runner.name:
            return llm_runner
        
    print(f"ERROR: INVALID CANNOT FIND CONFIG FOR RUNNER TYPE `{InstanceConfig.type}`")
    raise Exception(f"ERROR: INVALID CANNOT FIND CONFIG FOR RUNNER TYPE `{InstanceConfig.type}`")

asyncio.run(config.load_config_data())

config = get_own_config()

include = set(vLLMArgs.model_fields) & set(config.model_fields_set)

CMD = ["--model", config.location]

for field in include:
    print(f"{field=}", flush=True)
    CMD.append(f"--{field}")
    CMD.append(getattr(config, field))

CMD = list(map(str, CMD))

vllm = subprocess.run(
    ["python3", "-m", "vllm.entrypoints.openai.api_server"] + CMD
)
