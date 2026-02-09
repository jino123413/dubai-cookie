import { CookieResult } from '../types';
import { cookieTypes } from '../data/cookie-types';
import { dailyQuotes } from '../data/daily-quotes';

function hashCode(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return Math.abs(hash);
}

function getTodayString(): string {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

export function getCookieForName(name: string): CookieResult {
  const today = getTodayString();
  const trimmed = name.trim();
  const hash = hashCode(today + trimmed + 'dubai-cookie');
  const cookieIndex = hash % cookieTypes.length;
  const cookie = cookieTypes[cookieIndex];

  return {
    cookie,
    name: trimmed,
    date: today,
  };
}

export function getDailyQuote(): string {
  const today = getTodayString();
  const idx = hashCode(today + 'cookie-quote') % dailyQuotes.length;
  return dailyQuotes[idx];
}
