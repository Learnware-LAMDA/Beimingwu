import JSZip from "jszip";
import yaml from "js-yaml";

function verifyLearnware(file) {
  return JSZip.loadAsync(file).then((zip) => {
    if (!zip.files["__init__.py"]) {
      return "No __init__.py file found";
    }
    if (!zip.files["learnware.yaml"]) {
      return "No learnware.yaml file found";
    }
    if (!zip.files["environment.yaml"] && !zip.files["requirements.txt"]) {
      return "No environment.yaml or requirements.txt file found";
    }
    return zip
      .file("learnware.yaml")
      .async("string")
      .then((yamlString) => {
        const learnware = yaml.load(yamlString);

        if (!learnware.model) return "Key 'model' not found in learnware.yaml";
        if (!learnware.model.class_name)
          return "Key 'model.class_name' not found in learnware.yaml";
        if (!learnware.stat_specifications)
          return "Key 'stat_specification' not found in learnware.yaml";
        if (!learnware.stat_specifications.length)
          return "Key 'stat_specifications' must not be empty in learnware.yaml";

        for (const spec of learnware.stat_specifications) {
          // Should have stat_specifications[].module_path and stat_specifications[].class_name
          if (!spec) {
            return `Key 'stat_specifications[${learnware.stat_specifications.indexOf(
              spec,
            )}]' must not be empty in learnware.yaml`;
          }
          if (!spec.module_path) {
            return `Key 'stat_specifications[${learnware.stat_specifications.indexOf(
              spec,
            )}].module_path' not found in learnware.yaml`;
          }
          if (!spec.class_name) {
            return `Key 'stat_specifications[${learnware.stat_specifications.indexOf(
              spec,
            )}].class_name' not found in learnware.yaml`;
          }

          // Check file existence when using RKMEStatSpecification
          if (spec.class_name === "RKMEStatSpecification") {
            if (!spec.file_name) {
              return `Key 'stat_specifications[${learnware.stat_specifications.indexOf(
                spec,
              )}].file_name' not found in learnware.yaml`;
            }
            if (!zip.files[spec.file_name]) {
              return `File '${spec.file_name}' not found in zip file`;
            }
            return zip
              .file(spec.file_name)
              .async("string")
              .then(JSON.parse)
              .then((RKME) => {
                if (!RKME.z) return `Key 'z' not found or empty in ${spec.file_name}`;
                if (!Array.isArray(RKME.z) || RKME.z.length === 0)
                  return `Key 'z' must be a non-empty array in ${spec.file_name}`;
                if (!RKME.beta) return `Key 'beta' not found or empty in ${spec.file_name}`;
                if (!Array.isArray(RKME.beta) || RKME.beta.length === 0)
                  return `Key 'beta' must be a non-empty array in ${spec.file_name}`;
                if (!RKME.gamma) return `Key 'gamma' not found or empty in ${spec.file_name}`;
                if (!RKME.num_points)
                  return `Key 'num_points' not found or empty in ${spec.file_name}`;
                // cuda_idx can be empty
                if (RKME.cuda_idx === undefined)
                  return `Key 'cuda_idx' not found in ${spec.file_name}`;
                if (!RKME.device) return `Key 'device' not found or empty in ${spec.file_name}`;
                return true;
              });
          }
        }
        return true;
      });
  });
}

export { verifyLearnware };
