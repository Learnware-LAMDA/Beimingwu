import CODE_COLOR from "./codeColor";
import { computed, type ComputedRef } from "vue";
import { useI18n } from "vue-i18n";

const { green, purple, yellow, gray } = CODE_COLOR;

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

function fromImport(from: string, _import: string): string[] {
  return [
    ...addColorAndSplit("from ", green),
    ...addColorAndSplit(from, purple),
    ...addColorAndSplit(" import ", green),
    ..._import,
  ];
}

function importAs(_import: string, _as: string): string[] {
  return [
    ...addColorAndSplit("import ", green),
    ...addColorAndSplit(_import, purple),
    ...addColorAndSplit(" as ", green),
    ...addColorAndSplit(_as, purple),
  ];
}

function lineContinue(): string {
  return `<br />&nbsp;&nbsp;&nbsp;<span style="color: ${green}">...:</span>&nbsp;`;
}

function tab(): string {
  return "&nbsp;&nbsp;&nbsp;&nbsp;";
}

// python list
const result = [
  "[",
  ...[
    "00001987",
    "00001986",
    "00001982",
    "00001981",
    "00001980",
    "00001979",
    "00001978",
    "00001975",
    "00001974",
    "00001973",
  ].reduce(
    (acc: string[], cur: string, index: number): string[] => [
      ...acc,
      "'",
      ...Array.from(cur),
      "'",
      index < 9 ? "," : "",
      index < 9 ? "<br />" : "",
    ],
    [],
  ),
  "]<br />",
];

export function getCoverCode(): ComputedRef<CodeFragment[]> {
  const { t } = useI18n();

  return computed(() => [
    {
      index: 0,
      name: "Simplified",
      import: [
        startWithIn(1),
        ...fromImport("learnware", "LearnwareClient"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.SearchLearnware"), gray),
        lineContinue(),
        ..."learnware_ids = client.search_learnware(user_info)",
      ],
      result: [..."...", "<br />"],
      reuse: [
        "<br />" + startWithIn(3),
        ...addColorAndSplit("# " + t("CodeFragments.LoadLearnware"), gray),
        lineContinue(),
        ..."learnware_list = client.load_learnware(learnware_ids)",
        "<br />",

        "<br />" + startWithIn(4),
        ...addColorAndSplit("# " + t("CodeFragments.ReuseLearnware"), gray),
        lineContinue(),
        ..."y_predict = Reuser(learnware_list).predict(X)",
      ],
    },
    {
      index: 1,
      name: "Single",
      import: [
        startWithIn(1),
        ...importAs("numpy", "np"),
        lineContinue(),
        ...fromImport("learnware.market", "BaseUserInfo"),
        lineContinue(),
        ...fromImport("learnware.specification", "generate_stat_spec"),
        lineContinue(),
        ...fromImport("learnware.client", "LearnwareClient"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.UserPrepare"), gray),
        lineContinue(),
        ..."client = LearnwareClient()",
        lineContinue(),
        ..."client.login(your_email, your_token)",
        ..."data = np.random.randn(",
        ...addColorAndSplit("10000", green),
        ...", ",
        ...addColorAndSplit("10", green),
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
      result: [..."single_demo_output: ", ..."00001987"],
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
        ..."y_predict = learnware.predict(data)",
      ],
    },
    {
      index: 2,
      name: "Multiple",
      import: [
        startWithIn(1),
        ...importAs("numpy", "np"),
        lineContinue(),
        ...fromImport("learnware.market", "BaseUserInfo"),
        lineContinue(),
        ...fromImport("learnware.specification", "generate_stat_spec"),
        lineContinue(),
        ...fromImport("learnware.client", "LearnwareClient"),
        lineContinue(),
        ...fromImport("learnware.reuse", "AveragingReuser"),

        `<br /><br />${startWithIn(2)}`,
        ...addColorAndSplit("# " + t("CodeFragments.UserPrepare"), gray),
        lineContinue(),
        ..."client = LearnwareClient()",
        lineContinue(),
        ..."client.login(your_email, your_token)",
        ..."data = np.random.randn(",
        ...addColorAndSplit("10000", green),
        ...", ",
        ...addColorAndSplit("10", green),
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
        ...addColorAndSplit('"multiple"', yellow),
        ..."][",
        ...addColorAndSplit('"learnware_ids"', yellow),
        ..."][",
        ...addColorAndSplit("0", green),
        ..."]",
      ],
      result: [..."multi_demo_output: ", ...result],
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
        ..."pred_y = AveragingReuser(learnware_list).predict(data)",
      ],
    },
  ]);
}

export function getFeatureCode(): ComputedRef<
  { index: number; name: string; load: string[]; reuse: string[] }[]
> {
  const { t } = useI18n();

  return computed(() => [
    {
      index: 0,
      name: "Load learnware",
      load: [
        startWithIn(1),
        ...addColorAndSplit("# " + t("CodeFragments.LoadLearnware"), gray),
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
        ...addColorAndSplit("# " + t("CodeFragments.ReuseLearnware"), gray),
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
  ]);
}
