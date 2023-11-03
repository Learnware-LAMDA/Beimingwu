import context
import lib.engine as engine_utils
import yaml
import os
import json
import zipfile


if __name__ == "__main__":
    context.init_engine()

    engine = context.engine

    for learnware_id, learnware in engine.learnware_organizer.learnware_list.items():
        print(f"processing learnware: {learnware_id}")
        zip_path = engine.learnware_organizer.learnware_zip_list[learnware_id]
        unzip_path = engine.learnware_organizer.learnware_folder_list[learnware_id]

        with zipfile.ZipFile(zip_path, "w") as f:
            for root, dirs, files in os.walk(unzip_path):
                for file in files:
                    if file.endswith(".pyc"):
                        os.remove(os.path.join(root, file))
                    else:
                        f.write(os.path.join(root, file), arcname=file)
