import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import tz from "dayjs/plugin/timezone";
import relativeTime from "dayjs/plugin/relativeTime";
import UpdateLocale from "dayjs/plugin/updateLocale";
import zhCn from "dayjs/locale/zh-cn";
import i18n from "@main/i18n";

dayjs.extend(utc);
dayjs.extend(tz);

dayjs.extend(relativeTime);

dayjs.extend(UpdateLocale);
dayjs.updateLocale("zh-cn", zhCn);

const language = i18n.global.locale;
dayjs.locale(language.value);
