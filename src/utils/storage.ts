import { Storage } from '@apps-in-toss/web-framework';
import { TodayRecord, CollectionData, StreakData } from '../types';

const TODAY_KEY = 'dubai-cookie-today';
const COLLECTION_KEY = 'dubai-cookie-collection';
const STREAK_KEY = 'dubai-cookie-streak';

function getTodayString(): string {
  const now = new Date();
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
}

function getYesterdayString(): string {
  const d = new Date();
  d.setDate(d.getDate() - 1);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

export async function getTodayRecord(): Promise<TodayRecord | null> {
  try {
    const stored = await Storage.getItem(TODAY_KEY);
    if (stored) {
      const parsed: TodayRecord = JSON.parse(stored);
      if (parsed.date === getTodayString()) {
        return parsed;
      }
    }
  } catch {}
  return null;
}

export async function saveTodayRecord(name: string, cookieId: number): Promise<void> {
  const today = getTodayString();
  const record: TodayRecord = { date: today, name, cookieId };

  try {
    await Storage.setItem(TODAY_KEY, JSON.stringify(record));
  } catch {}

  await addToCollection(cookieId);
  await updateStreak();
}

async function addToCollection(cookieId: number): Promise<void> {
  try {
    const collection = await getCollection();
    if (!collection.discovered.includes(cookieId)) {
      collection.discovered.push(cookieId);
      await Storage.setItem(COLLECTION_KEY, JSON.stringify(collection));
    }
  } catch {}
}

export async function getCollection(): Promise<CollectionData> {
  try {
    const stored = await Storage.getItem(COLLECTION_KEY);
    if (stored) {
      return JSON.parse(stored);
    }
  } catch {}
  return { discovered: [] };
}

export async function getStreak(): Promise<StreakData> {
  try {
    const stored = await Storage.getItem(STREAK_KEY);
    if (stored) {
      const data: StreakData = JSON.parse(stored);
      const today = getTodayString();
      const yesterday = getYesterdayString();

      if (data.lastDate === today) {
        return data;
      }
      if (data.lastDate === yesterday) {
        return { currentStreak: data.currentStreak, lastDate: data.lastDate };
      }
    }
  } catch {}
  return { currentStreak: 0, lastDate: '' };
}

async function updateStreak(): Promise<void> {
  try {
    const current = await getStreak();
    const today = getTodayString();
    const yesterday = getYesterdayString();

    let newStreak: number;
    if (current.lastDate === today) {
      return;
    } else if (current.lastDate === yesterday) {
      newStreak = current.currentStreak + 1;
    } else {
      newStreak = 1;
    }

    await Storage.setItem(
      STREAK_KEY,
      JSON.stringify({ currentStreak: newStreak, lastDate: today }),
    );
  } catch {}
}
