import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import UpdateLocale from "dayjs/plugin/updateLocale";
import zhCn from "dayjs/locale/zh-cn";

dayjs.extend(relativeTime);

dayjs.extend(UpdateLocale);
dayjs.updateLocale("zh-cn", zhCn);

const language =
  JSON.parse(localStorage.getItem("vuex") || "{}")?.i18n?.locale ||
  (navigator.language || "en").toLocaleLowerCase();
dayjs.locale(language);
