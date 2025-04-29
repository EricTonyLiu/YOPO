from ruamel.yaml import YAML
import random

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = None

envs = {}
env_num = 5
for i in range(env_num):
    name = f"quadrotor_env_{i + 1}"
    envs[name] = {
        "collect_data": "yes",
        "bounding_box": [round(random.uniform(0, 100), 2) for _ in range(3)],
        "bounding_box_origin": [round(random.uniform(0, 100), 2) for _ in range(3)],
        "sim_dt": round(random.uniform(0.1, 1.0), 2),
    }

# 顶层结构：添加一个环境数量字段
data = {
    "env_count": env_num,
    "envs": envs
}

# 保存 YAML 文件
with open("multi_env_dict_config.yaml", "w") as f:
    yaml.dump(data, f)
