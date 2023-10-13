import JSZip from "jszip";
import yaml from "js-yaml";
import { ComposerTranslation } from "vue-i18n";

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

function verifyLearnware(file: ArrayBuffer, t: ComposerTranslation): Promise<string> {
  return JSZip.loadAsync(file).then((zip) => {
    const topFolder = getTopFolder(zip);
    if (!zip.files[topFolder + "__init__.py"]) {
      return t("Submit.File.Error.FileNotFound", { filename: "__init__.py" });
    }
    if (!zip.files[topFolder + "learnware.yaml"]) {
      return t("Submit.File.Error.FileNotFound", { filename: "learnware.yaml" });
    }
    if (!zip.files[topFolder + "environment.yaml"] && !zip.files[topFolder + "requirements.txt"]) {
      return t("Submit.File.Error.FileNotFound", { filename: "environment.yaml/requirements.txt" });
    }

    // For type check
    const zipLearnwareYaml = zip.file(topFolder + "learnware.yaml");
    if (!zipLearnwareYaml) {
      return t("Submit.File.Error.FileNotFound", { filename: "learnware.yaml" });
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

      if (!learnware.model) {
        return t("Submit.File.Error.KeyNotFoundInFile", {
          filename: "learnware.yaml",
          key: "model",
        });
      }
      if (!learnware.model.class_name) {
        return t("Submit.File.Error.KeyNotFoundInFile", {
          filename: "learnware.yaml",
          key: "model.class_name",
        });
      }
      if (!learnware.stat_specifications) {
        return t("Submit.File.Error.KeyNotFoundInFile", {
          filename: "learnware.yaml",
          key: "stat_specifications",
        });
      }
      if (!learnware.stat_specifications.length) {
        return t("Submit.File.Error.KeyEmptyInFile", {
          filename: "learnware.yaml",
          key: "stat_specifications",
        });
      }

      for (const spec of learnware.stat_specifications) {
        // Should have stat_specifications[].module_path and stat_specifications[].class_name
        if (!spec) {
          return t("Submit.File.Error.KeyEmptyInFile", {
            filename: "learnware.yaml",
            key: `stat_specifications[${learnware.stat_specifications.indexOf(spec)}]`,
          });
        }
        if (!spec.module_path) {
          return t("Submit.File.Error.KeyNotFoundInFile", {
            filename: "learnware.yaml",
            key: `stat_specifications[${learnware.stat_specifications.indexOf(spec)}].module_path`,
          });
        }
        if (!spec.class_name) {
          return t("Submit.File.Error.KeyNotFoundInFile", {
            filename: "learnware.yaml",
            key: `stat_specifications[${learnware.stat_specifications.indexOf(spec)}].class_name`,
          });
        }

        // Check file existence when using RKMEStatSpecification
        if (spec.class_name === "RKMEStatSpecification") {
          if (!spec.file_name) {
            return t("Submit.File.Error.KeyNotFoundInFile", {
              filename: "learnware.yaml",
              key: `stat_specifications[${learnware.stat_specifications.indexOf(spec)}].file_name`,
            });
          }
          if (!zip.files[topFolder + spec.file_name]) {
            return t("Submit.File.Error.FileNotFound", { filename: spec.file_name });
          }
          const zipSpec = zip.file(topFolder + spec.file_name);
          if (!zipSpec) {
            return t("Submit.File.Error.FileNotFound", { filename: spec.file_name });
          }
          return zipSpec
            .async("string")
            .then(JSON.parse)
            .then((RKME) => {
              if (!RKME.z) {
                return t("Submit.File.Error.KeyNotFoundOrEmptyInFile", {
                  filename: spec.file_name,
                  key: "z",
                });
              }
              if (!Array.isArray(RKME.z) || RKME.z.length === 0) {
                return t("Submit.File.Error.KeyNotNonEmptyArrayInFile", {
                  filename: spec.file_name,
                  key: "z",
                });
              }
              if (!RKME.beta) {
                return t("Submit.File.Error.KeyNotFoundOrEmptyInFile", {
                  filename: spec.file_name,
                  key: "beta",
                });
              }
              if (!Array.isArray(RKME.beta) || RKME.beta.length === 0) {
                return t("Submit.File.Error.KeyNotNonEmptyArrayInFile", {
                  filename: spec.file_name,
                  key: "beta",
                });
              }
              if (!RKME.gamma) {
                return t("Submit.File.Error.KeyNotFoundOrEmptyInFile", {
                  filename: spec.file_name,
                  key: "gamma",
                });
              }
              if (!RKME.num_points) {
                return t("Submit.File.Error.KeyNotFoundOrEmptyInFile", {
                  filename: spec.file_name,
                  key: "num_points",
                });
              }
              // cuda_idx can be empty
              if (RKME.cuda_idx === undefined) {
                return t("Submit.File.Error.KeyNotFoundInFile", {
                  filename: spec.file_name,
                  key: "cuda_idx",
                });
              }
              if (!RKME.device) {
                return t("Submit.File.Error.KeyNotFoundOrEmptyInFile", {
                  filename: spec.file_name,
                  key: "device",
                });
              }
              return "";
            });
        }
      }
      return "";
    });
  });
}

export { verifyLearnware };
