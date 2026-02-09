export type Screen = 'home' | 'reveal' | 'result';

export interface CookieType {
  id: number;
  name: string;
  emotion: string;
  decoDescription: string;
  themeColor: string;
  personality: string;
  quote: string;
  fluxPrompt: string;
}

export interface CookieResult {
  cookie: CookieType;
  name: string;
  date: string;
}

export interface TodayRecord {
  date: string;
  name: string;
  cookieId: number;
}

export interface CollectionData {
  discovered: number[];
}

export interface StreakData {
  currentStreak: number;
  lastDate: string;
}
