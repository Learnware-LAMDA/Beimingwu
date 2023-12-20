export interface Filter {
  userName: string;
  email: string;
  verifyStatus?: boolean;
}

export interface User {
  id: number;
  username: string;
  email: string;
  role: number;
  unverified_learnware_count: number;
  verified_learnware_count: number;
}
