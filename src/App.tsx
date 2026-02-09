import React, { useState, useCallback, useEffect } from 'react';
import { Screen, CookieResult } from './types';
import { getCookieForName, getDailyQuote } from './utils/cookie-engine';
import { saveTodayRecord, getTodayRecord, getStreak, getCollection } from './utils/storage';
import { useInterstitialAd } from './hooks/useInterstitialAd';
import { DeviceViewport } from './components/DeviceViewport';
import HomeScreen from './components/HomeScreen';
import RevealScreen from './components/RevealScreen';
import ResultScreen from './components/ResultScreen';

const AD_GROUP_ID = 'ait-ad-test-interstitial-id';

const App: React.FC = () => {
  const [screen, setScreen] = useState<Screen>('home');
  const [result, setResult] = useState<CookieResult | null>(null);
  const [streak, setStreak] = useState(0);
  const [collectionCount, setCollectionCount] = useState(0);
  const [dailyQuote, setDailyQuote] = useState('');
  const [isReady, setIsReady] = useState(false);
  const [isFirstVisit, setIsFirstVisit] = useState(true);

  const { loading: adLoading, showInterstitialAd } = useInterstitialAd(AD_GROUP_ID);

  useEffect(() => {
    const init = async () => {
      setDailyQuote(getDailyQuote());

      const streakData = await getStreak();
      setStreak(streakData.currentStreak);

      const collection = await getCollection();
      setCollectionCount(collection.discovered.length);

      const todayRecord = await getTodayRecord();
      if (todayRecord) {
        const cookieResult = getCookieForName(todayRecord.name);
        setResult(cookieResult);
        setIsFirstVisit(false);
        setScreen('result');
      }

      setIsReady(true);
    };
    init();
  }, []);

  const handleSubmitName = useCallback(async (name: string) => {
    const cookieResult = getCookieForName(name);
    setResult(cookieResult);
    setScreen('reveal');

    await saveTodayRecord(name, cookieResult.cookie.id);
    const streakData = await getStreak();
    setStreak(streakData.currentStreak);
    const collection = await getCollection();
    setCollectionCount(collection.discovered.length);
    setIsFirstVisit(false);
  }, []);

  const handleRevealComplete = useCallback(() => {
    setScreen('result');
  }, []);

  const handleRetry = useCallback(() => {
    showInterstitialAd({
      onDismiss: () => {
        setResult(null);
        setScreen('home');
      },
    });
  }, [showInterstitialAd]);

  if (!isReady) {
    return (
      <>
        <DeviceViewport />
        <div className="app">
          <div className="loading-screen">
            <div className="loading-cookie">
              <div className="loading-cookie-inner" />
            </div>
            <p className="loading-text">쿠키를 굽고 있어요...</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <DeviceViewport />
      <div className="app">
        {/* Floating crumbs background */}
        <div className="crumbs-bg">
          {Array.from({ length: 12 }).map((_, i) => (
            <div
              key={i}
              className={`floating-crumb ${i % 3 === 0 ? 'large' : ''}`}
              style={{
                left: `${(i * 27.3 + 8) % 100}%`,
                top: `${(i * 19.7 + 5) % 100}%`,
                '--delay': `${(i * 1.1) % 6}s`,
                '--duration': `${4 + (i * 1.3) % 5}s`,
                '--max-opacity': `${0.15 + (i * 0.05) % 0.2}`,
              } as React.CSSProperties}
            />
          ))}
        </div>

        {/* Header */}
        <header className="app-header">
          <h1 className="app-title">내가 두쫀쿠?</h1>
        </header>

        {/* Screens */}
        {screen === 'home' && (
          <HomeScreen
            streak={streak}
            collectionCount={collectionCount}
            dailyQuote={dailyQuote}
            onSubmitName={handleSubmitName}
          />
        )}

        {screen === 'reveal' && result && (
          <RevealScreen
            name={result.name}
            cookieName={result.cookie.name}
            onRevealComplete={handleRevealComplete}
          />
        )}

        {screen === 'result' && result && (
          <ResultScreen
            result={result}
            onRetry={handleRetry}
            adLoading={adLoading}
          />
        )}
      </div>
    </>
  );
};

export default App;
