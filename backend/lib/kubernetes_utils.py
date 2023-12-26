from kubernetes import client, config, utils
import yaml
import time
import shortuuid
import os


def run_check(env_path, learnware_path, checker_name):
    config.load_incluster_config()

    k8s_client = client.ApiClient()
    v1 = client.CoreV1Api()

    template_file = os.path.join("learnware-check.yaml")
    with open(template_file) as fin:
        template_content = fin.read()
        pass

    current_pod_name = os.environ["HOSTNAME"]
    current_pod_image = v1.read_namespaced_pod(name=current_pod_name, namespace="learnware").spec.containers[0].image

    pod_name = str(shortuuid.uuid()).lower()
    template_content = template_content.replace("{{NAME}}", pod_name)
    template_content = template_content.replace("{{LEARNWARE_PATH}}", learnware_path)
    template_content = template_content.replace("{{CHECKER_NAME}}", checker_name)
    template_content = template_content.replace("{{ENV_PATH}}", env_path)
    template_content = template_content.replace("{{IMAGE}}", current_pod_image)

    template_dict = yaml.safe_load(template_content)

    pod = utils.create_from_dict(k8s_client, template_dict)[0]

    # wait for pod end
    while True:
        pod = v1.read_namespaced_pod(name=pod.metadata.name, namespace="learnware")
        print(f"Pod status: {pod.status.phase}")
        if pod.status.phase not in ["Pending", "Running"]:
            break

        time.sleep(1)
        pass

    if pod.status.phase == "Succeeded":
        v1.delete_namespaced_pod(name=pod.metadata.name, namespace="learnware")
        return True, "Success"
    else:
        # read logs of the pod
        logs = v1.read_namespaced_pod_log(name=pod.metadata.name, namespace="learnware")
        v1.delete_namespaced_pod(name=pod.metadata.name, namespace="learnware")
        return False, logs
    pass
