export interface Route {
  name: string;
  path: string;
  meta: {
    showInNavBar: boolean;
    hideWhenLoggedIn: boolean;
    requiredLogin: boolean;
    showWhenNotLoggedIn?: boolean;
    icon: string;
    title: string;
    variant?: "flat" | "text" | "elevated" | "tonal" | "outlined" | "plain";
    class: string;
  };
  children?: Route[];
  parent?: Route;
}
