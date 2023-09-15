import context
import lib.engine as engine_utils
import yaml
import os
import json
import zipfile


if __name__ == "__main__":
    context.init_engine()

    engine = context.engine

    for learnware_id, learnware in engine.learnware_list.items():
        print(f"processing learnware: {learnware_id}")
        zip_path = engine.learnware_zip_list[learnware_id]
        unzip_path = engine.learnware_folder_list[learnware_id]

        semantic_specification = learnware.get_specification().get_semantic_spec()

        yaml_path = engine_utils.learnware_config.learnware_folder_config["yaml_file"]
        yaml_path = os.path.join(unzip_path, yaml_path)

        with open(yaml_path, "r") as f:
            learnware_info = yaml.safe_load(f)
            pass
        learnware_info["id"] = learnware_id
        learnware_info["semantic_specification"] = {"file_name": "semantic_specification.json"}
        with open(yaml_path, "w") as f:
            yaml.safe_dump(learnware_info, f)
            pass

        with open(os.path.join(unzip_path, "semantic_specification.json"), "w") as f:
            json.dump(semantic_specification, f, indent=4)
            pass

        os.remove(zip_path)

        with zipfile.ZipFile(zip_path, "w") as f:
            for root, dirs, files in os.walk(unzip_path):
                for file in files:
                    f.write(os.path.join(root, file), arcname=file)
                    pass
                pass
            pass
        pass
    pass
