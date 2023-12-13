import CODE_COLOR from "./codeColor";
import { computed, type ComputedRef } from "vue";
import { useI18n } from "vue-i18n";

const { green, purple, yellow, gray, red } = CODE_COLOR;

export interface CodeFragment {
  index: number;
  name: string;
  import: string[];
  result: string[];
  reuse: string[];
}

function addColorAndSplit(str: string, color: string): string[] {
  return str.split("").map((c) => `<span style="color: ${color}">${c}</span>`);
}

function startWithIn(index: number): string {
  return `<b style='color: ${green}'>In [${index}]:&nbsp;</b>`;
}

function startWithOut(index: number): string {
  return `<b style='color: ${red}'>Out[${index}]:&nbsp;</b>`;
}

function fromImport(from: string, _import: string): string[] {
  return [
    ...addColorAndSplit("from ", green),
    ...addColorAndSplit(from, purple),
    ...addColorAndSplit(" import ", green),
    ..._import,
  ];
}

/*
function importAs(_import: string, _as: string): string[] {
  return [
    ...addColorAndSplit("import ", green),
    ...addColorAndSplit(_import, purple),
    ...addColorAndSplit(" as ", green),
    ...addColorAndSplit(_as, purple),
  ];
}
*/

function lineContinue(): string {
  return `<br />&nbsp;&nbsp;&nbsp;<span style="color: ${green}">...:</span>&nbsp;`;
}

function tab(): string {
  return "&nbsp;&nbsp;&nbsp;&nbsp;";
}

export function getCoverCode(): ComputedRef<CodeFragment[]> {
  const { t } = useI18n();

  return computed(() => [
    {
      index: 0,
      name: "Simplified",
      import: [
        startWithIn(1),
        ...fromImport("learnware", "LearnwareClient, BaseUserInfo, Reuser"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.UserPrepare"), gray),
        lineContinue(),
        ..."client = LearnwareClient()",
        lineContinue(),
        ..."user_info = BaseUserInfo(...)",

        `<br /><br />${startWithIn(3)}`,
        ...addColorAndSplit("# " + t("CodeFragments.SearchLearnware"), gray),
        lineContinue(),
        ..."learnware_ids = client.search_learnware(user_info)",
      ],
      result: [""],
      reuse: [
        "<br />" + startWithIn(4),
        ...addColorAndSplit("# " + t("CodeFragments.LoadLearnware"), gray),
        lineContinue(),
        ..."learnware_list = client.load_learnware(learnware_ids)",
        "<br />",

        "<br />" + startWithIn(5),
        ...addColorAndSplit("# " + t("CodeFragments.ReuseLearnware"), gray),
        lineContinue(),
        ..."y_pred = Reuser(learnware_list).predict(X)",
      ],
    },
    {
      index: 1,
      name: "Single",
      import: [
        startWithIn(1),
        ...fromImport("learnware.market", "BaseUserInfo"),
        lineContinue(),
        ...fromImport("learnware.specification", "generate_stat_spec"),
        lineContinue(),
        ...fromImport("learnware.client", "LearnwareClient"),
        lineContinue(),
        ...fromImport("sklearn.datasets", "load_iris"),
        lineContinue(),
        ...fromImport("sklearn.metrics", "accuracy_score"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.UserPrepare"), gray),
        lineContinue(),
        ..."client = LearnwareClient()",
        lineContinue(),
        ..."client.login(your_email, your_token)",
        lineContinue(),
        ..."data, target = load_iris(return_X_y=",
        ...addColorAndSplit("True", green),
        ...")",
        lineContinue(),
        ..."rkme = generate_stat_spec(",
        ...addColorAndSplit("type", green),
        ..."=",
        ...addColorAndSplit('"table"', yellow),
        ...", X=data)",
        lineContinue(),
        ..."user_info = BaseUserInfo(stat_info={rkme.type: rkme})",

        `<br /><br />${startWithIn(3)}`,
        ...addColorAndSplit("# " + t("CodeFragments.SearchLearnware"), gray),
        lineContinue(),
        ..."learnware_id = client.search_learnware(user_info)[",
        ...addColorAndSplit('"single"', yellow),
        ..."][",
        ...addColorAndSplit('"learnware_ids"', yellow),
        ..."][",
        ...addColorAndSplit("0", green),
        ..."]",
      ],
      result: [startWithOut(3), ..."Search result: '00001987'"],
      reuse: [
        "<br />" + startWithIn(4),
        ...addColorAndSplit("# " + t("CodeFragments.LoadLearnware"), gray),
        lineContinue(),
        ..."learnware = client.load_learnware(learnware_id=learnware_id, runnable_option=",
        ...addColorAndSplit('"conda"', yellow),
        ...")",
        "<br /><br />",

        startWithIn(5),
        ...addColorAndSplit("# " + t("CodeFragments.ReuseLearnware"), gray),
        lineContinue(),
        ..."y_pred = learnware.predict(data)",
        lineContinue(),
        ..."accuracy_score(y_pred, target)",
        "<br />",

        startWithOut(5),
        ..."Classification accuracy: 100%",
      ],
    },
    {
      index: 2,
      name: "Multiple",
      import: [
        startWithIn(1),
        ...fromImport("learnware.market", "BaseUserInfo"),
        lineContinue(),
        ...fromImport("learnware.specification", "generate_stat_spec"),
        lineContinue(),
        ...fromImport("learnware.client", "LearnwareClient"),
        lineContinue(),
        ...fromImport("learnware.reuse", "AveragingReuser"),
        lineContinue(),
        ...fromImport("sklearn.datasets", "load_digits"),
        lineContinue(),
        ...fromImport("sklearn.metrics", "accuracy_score"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.UserPrepare"), gray),
        lineContinue(),
        ..."client = LearnwareClient()",
        lineContinue(),
        ..."client.login(your_email, your_token)",
        lineContinue(),
        ..."data, target = load_digits(return_X_y=",
        ...addColorAndSplit("True", green),
        ...")",
        lineContinue(),
        ..."rkme = generate_stat_spec(",
        ...addColorAndSplit("type", green),
        ..."=",
        ...addColorAndSplit('"table"', yellow),
        ...", X=data)",
        lineContinue(),
        ..."user_info = BaseUserInfo(stat_info={rkme.type: rkme})",

        `<br /><br />${startWithIn(3)}`,
        ...addColorAndSplit("# " + t("CodeFragments.SearchLearnware"), gray),
        lineContinue(),
        ..."learnware_ids = client.search_learnware(user_info)[",
        ...addColorAndSplit('"multiple"', yellow),
        ..."][",
        ...addColorAndSplit('"learnware_ids"', yellow),
        ..."]",
      ],
      result: [startWithOut(3), ..."Search Result: ['00002018', '00002016', '00002017']"],
      reuse: [
        "<br />" + startWithIn(4),
        ...addColorAndSplit("# " + t("CodeFragments.LoadLearnware"), gray),
        lineContinue(),
        ..."learnware_list = client.load_learnware(learnware_id=learnware_ids, runnable_option=",
        ...addColorAndSplit('"conda"', yellow),
        ...")",
        "<br /><br />",

        startWithIn(5),
        ...addColorAndSplit("# " + t("CodeFragments.ReuseLearnware"), gray),
        lineContinue(),
        ..."y_pred = AveragingReuser(learnware_list, mode=",
        ...addColorAndSplit('"vote_by_label"', yellow),
        ...").predict(data)",
        lineContinue(),
        ..."accuracy_score(y_pred, target)",
        "<br />",

        startWithOut(5),
        ..."Classification accuracy: 100%",
      ],
    },
  ]);
}

export const featureCode = [
  {
    index: 0,
    name: "Load learnware",
    load: [
      startWithIn(1),
      ...addColorAndSplit("# Load learnwares", gray),
      lineContinue(),
      ...fromImport("learnware.client", "LearnwareClient"),
      lineContinue(),
      ..."learnware_list = LearnwareClient().load_learnware(",
      lineContinue() + tab(),
      ..."leanrware_id=id_list, runnable_option=",
      ...addColorAndSplit('"docker"', yellow),
      lineContinue(),
      ...")",
    ],
    reuse: [
      `<br /><br />${startWithIn(2)}`,
      ...addColorAndSplit("# Reuse learnwares", gray),
      lineContinue(),
      ...fromImport("learnware.reuse", "AveragingReuser"),
      lineContinue(),
      ..."y_pred = AveragingReuser(",
      lineContinue() + tab(),
      ..."learnware_list=learnware_list, mode=",
      ...addColorAndSplit('"vote_by_label"', yellow),
      lineContinue(),
      ...").predict(X)",
    ],
  },
];
