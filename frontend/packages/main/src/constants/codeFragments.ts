import CODE_COLOR from "./codeColor";

const { green, purple, yellow, pink } = CODE_COLOR;

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
  return "<br />&nbsp;&nbsp;&nbsp;...:&nbsp;";
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

export default [
  {
    index: 0,
    name: "Concept demo",
    import: [
      startWithIn(1),
      ...fromImport("learnware.client", "LearnwareClient"),

      `<br /><br />${startWithIn(2)}`,
      ..."learnware_ids = client.search_learnware(user_info)[",
      ...addColorAndSplit('"single"', yellow),
      "][",
      ...addColorAndSplit('"learnware_ids"', yellow),
      "]",
    ],
    result,
    reuse: [
      "<br />" + startWithIn(3),
      ..."learnware_list = client.load_learnware(learnware_ids)",
      "<br /><br />",
      startWithIn(4),
      ..."y_predict = Reuser(learnware_list).predict(X)",
    ],
  },
  {
    index: 1,
    name: "Single demo",
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
      ...addColorAndSplit("def ", green),
      ...addColorAndSplit("single_demo", purple),
      ..."(client, data):",
      lineContinue() + tab(),
      ..."rkme = generate_stat_spec(",
      ...addColorAndSplit("type", green),
      ...addColorAndSplit("=", green),
      ...addColorAndSplit('"table"', yellow),
      ...", X=data)",

      lineContinue() + tab(),
      ..."user_info = BaseUserInfo(stat_info={rkme.type: rkme})",

      lineContinue() + tab() + lineContinue() + tab(),
      ..."learnware_id = client.search_learnware(user_info)[",
      ...addColorAndSplit('"single"', yellow),
      ..."][",
      ...addColorAndSplit('"learnware_ids"', yellow),
      ..."][",
      ...addColorAndSplit("0", green),
      ..."]",

      lineContinue() + tab(),
      ..."learnware = client.load_learnware(learnware_id=learnware_id, runnable_option=",
      ...addColorAndSplit('"conda"', yellow),
      ...")",

      lineContinue() + tab(),
      ..."pred_y = learnware.predict(data)",

      lineContinue() + tab() + lineContinue() + tab(),
      ...addColorAndSplit("print", green),
      ..."(",
      ...addColorAndSplit('f"single_demo_output: ', yellow),
      ...addColorAndSplit("{", pink),
      ..."pred_y",
      ...addColorAndSplit("}", pink),
      ...addColorAndSplit('"', yellow),
      ...")",
      `<br /><br />${startWithIn(3)}`,

      ...addColorAndSplit("if ", green),
      ...addColorAndSplit(" __name__ ", purple),
      ..."== ",
      ...addColorAndSplit('"__main__"', yellow),

      lineContinue() + tab(),
      ..."client = LearnwareClient()",

      lineContinue() + tab(),
      ..."client.login(",
      ...addColorAndSplit('"liujd@lamda.nju.edu.cn"', yellow),
      ...", ",
      ...addColorAndSplit('"963357f500144a9cb0dde58fa4fd98f6"', yellow),
      ...")",

      lineContinue() + tab(),
      ...addColorAndSplit("data", purple),
      ..." = np.random.randn(",
      ...addColorAndSplit("10000", yellow),
      ...", ",
      ...addColorAndSplit("100", yellow),
      ...")",

      lineContinue() + tab(),
      ..."single_demo(client, data)",
    ],
    result: [..."single_demo_output: ", ...result],
    reuse: [
      "<br />" + startWithIn(4),
      ..."learnware_list = client.load_learnware(learnware_ids)",
      "<br /><br />",
      startWithIn(5),
      ..."y_predict = Reuser(learnware_list).predict(X)",
    ],
  },
  {
    index: 2,
    name: "Multiple demo",
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
      ...addColorAndSplit("def ", green),
      ...addColorAndSplit("multi_demo", purple),
      ..."(client, data):",
      lineContinue() + tab(),
      ..."rkme = generate_stat_spec(",
      ...addColorAndSplit("type", green),
      ...addColorAndSplit("=", green),
      ...addColorAndSplit('"table"', yellow),
      ...", X=data)",

      lineContinue() + tab(),
      ..."user_info = BaseUserInfo(stat_info={rkme.type: rkme})",

      lineContinue() + tab() + lineContinue() + tab(),
      ..."learnware_id = client.search_learnware(user_info)[",
      ...addColorAndSplit('"multiple"', yellow),
      ..."][",
      ...addColorAndSplit('"learnware_ids"', yellow),
      ..."][",
      ...addColorAndSplit("0", green),
      ..."]",

      lineContinue() + tab(),
      ..."learnware = client.load_learnware(learnware_id=learnware_id, runnable_option=",
      ...addColorAndSplit('"conda"', yellow),
      ...")",

      lineContinue() + tab(),
      ..."pred_y = learnware.predict(data)",

      lineContinue() + tab() + lineContinue() + tab(),
      ...addColorAndSplit("print", green),
      ..."(",
      ...addColorAndSplit('f"multi_demo_output: ', yellow),
      ...addColorAndSplit("{", pink),
      ..."pred_y",
      ...addColorAndSplit("}", pink),
      ...addColorAndSplit('"', yellow),
      ...")",
      `<br /><br />${startWithIn(3)}`,

      ...addColorAndSplit("if ", green),
      ...addColorAndSplit(" __name__ ", purple),
      ..."== ",
      ...addColorAndSplit('"__main__"', yellow),

      lineContinue() + tab(),
      ..."client = LearnwareClient()",

      lineContinue() + tab(),
      ..."client.login(",
      ...addColorAndSplit('"liujd@lamda.nju.edu.cn"', yellow),
      ...", ",
      ...addColorAndSplit('"963357f500144a9cb0dde58fa4fd98f6"', yellow),
      ...")",

      lineContinue() + tab(),
      ...addColorAndSplit("data", purple),
      ..." = np.random.randn(",
      ...addColorAndSplit("10000", yellow),
      ...", ",
      ...addColorAndSplit("100", yellow),
      ...")",

      lineContinue() + tab(),
      ..."multi_demo(client, data)",
    ],
    result: [..."multi_demo_output: ", ...result],
    reuse: [
      "<br />" + startWithIn(4),
      ..."learnware_list = client.load_learnware(learnware_ids)",
      "<br /><br />",
      startWithIn(5),
      ..."y_predict = Reuser(learnware_list).predict(X)",
    ],
  },
];
