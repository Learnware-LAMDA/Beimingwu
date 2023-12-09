import { marked } from "marked";
import DOMPurify from "dompurify";

const purify = DOMPurify(window);

export default function html2Markdown(html: string): string {
  return purify.sanitize(marked(html, { async: false }) as string);
}
