import { marked } from "marked";
import DOMPurify from "dompurify";

const purify = DOMPurify(window);

const renderer = new marked.Renderer();
renderer.image = (): string => "";

export default function html2Markdown(html: string): string {
  return purify.sanitize(marked(html, { async: false, renderer }) as string);
}
