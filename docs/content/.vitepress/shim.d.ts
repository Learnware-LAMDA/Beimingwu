declare module "*.vue" {
  import { ComponentOptions } from "vue";
  const component: ComponentOptions;
  export default component;
}

declare module "segmentit" {
  export function useDefault(segmentInstance: Segment): Segment;
  export class Segment {
    doSegment(text: string, option: { simple: boolean }): string[];
    loadStopwordDict(dict: string): void;
  }
}

declare module "vitepress/dist/client/app/utils" {
  export function pathToFile(path: string): string;
}

declare module "vitepress/dist/client/theme-default/support/translate.js" {
  export function createTranslate(
    themeObject: any,
    defaultTranslations: Record<string, any>,
  ): (key: string) => string;
}

declare module "@localSearchIndex" {
  const data: Record<string, () => Promise<{ default: string }>>;
  export default data;
}

declare module "mark.js/src/vanilla.js" {
  import type Mark from "mark.js";
  const mark: typeof Mark;
  export default mark;
}

declare module "url" {
  export function fileURLToPath(url: URL): string;
}
