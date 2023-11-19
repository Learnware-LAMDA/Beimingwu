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
    variant: string;
    class: string;
  };
  children?: Route[];
  parent?: Route;
}
