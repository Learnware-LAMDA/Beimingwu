export interface Filter {
  userName: string;
  email: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  unverified_learnware_count: number;
  verified_learnware_count: number;
}
