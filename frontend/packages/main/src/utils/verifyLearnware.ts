import JSZip from "jszip";
import yaml from "js-yaml";

function getTopFolder(zip: JSZip): string {
  // return top folder when there is only one top folder
  // return '' else
  const topFolders = Object.keys(zip.files).filter((key) => {
    return key.indexOf("/") === key.length - 1;
  });
  const topFiles = Object.keys(zip.files).filter((key) => {
    return key.indexOf("/") === -1;
  });
  if (topFiles.length > 0) {
    return "";
  }
  if (topFolders.length !== 1) {
    return "";
  }
  return topFolders[0];
}

function verifyLearnware(file: ArrayBuffer): Promise<string | boolean> {
  return JSZip.loadAsync(file).then((zip) => {
    const topFolder = getTopFolder(zip);
    if (!zip.files[topFolder + "__init__.py"]) {
      return "No __init__.py file found";
    }
    if (!zip.files[topFolder + "learnware.yaml"]) {
      return "No learnware.yaml file found";
    }
    if (!zip.files[topFolder + "environment.yaml"] && !zip.files[topFolder + "requirements.txt"]) {
      return "No environment.yaml or requirements.txt file found";
    }

    const zipLearnwareYaml = zip.file(topFolder + "learnware.yaml");
    if (!zipLearnwareYaml) {
      return "No learnware.yaml file found";
    }
    return zipLearnwareYaml.async("string").then((yamlString) => {
      const learnware = yaml.load(yamlString) as {
        model: {
          class_name: string;
        };
        stat_specifications: {
          module_path: string;
          class_name: string;
          file_name?: string;
        }[];
      };

      if (!learnware.model) return "Key 'model' not found in learnware.yaml";
      if (!learnware.model.class_name) return "Key 'model.class_name' not found in learnware.yaml";
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
          if (!zip.files[topFolder + spec.file_name]) {
            return `File '${spec.file_name}' not found in zip file`;
          }
          const zipSpec = zip.file(topFolder + spec.file_name);
          if (!zipSpec) {
            return `File '${spec.file_name}' not found in zip file`;
          }
          return zipSpec
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
