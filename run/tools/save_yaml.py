from ruamel.yaml import YAML
import random

yaml = YAML()
yaml.preserve_quotes = True
yaml.default_flow_style = None
envs = []
env_num = 5
for i in range(env_num):
    envs.append(
        {
            "name": f"quadrotor_env_{i + 1}",
            "collect_data": "yes",
            "bounding_box": [round(random.uniform(0, 100), 2) for _ in range(3)],
            "bounding_box_origin": [round(random.uniform(0, 100), 2) for _ in range(3)],
            "sim_dt": round(random.uniform(0.1, 1.0), 2),
        }
    )

# 构造顶层数据结构
data = {"envs": envs}

# 保存 YAML 文件
with open("multi_env_list_config.yaml", "w") as f:
    yaml.dump(data, f)