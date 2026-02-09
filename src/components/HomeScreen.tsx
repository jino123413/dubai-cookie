import React, { useState } from 'react';
import { CookieIcon, SparkleIcon } from './BrandIcons';
import { cookieTypes } from '../data/cookie-types';

interface HomeScreenProps {
  streak: number;
  collectionCount: number;
  dailyQuote: string;
  onSubmitName: (name: string) => void;
}

const HomeScreen: React.FC<HomeScreenProps> = ({
  streak,
  collectionCount,
  dailyQuote,
  onSubmitName,
}) => {
  const [name, setName] = useState('');

  const handleSubmit = () => {
    const trimmed = name.trim();
    if (trimmed.length === 0) return;
    onSubmitName(trimmed);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  const totalCookies = cookieTypes.length;
  const progressPercent = Math.round((collectionCount / totalCookies) * 100);

  return (
    <div className="home-screen">
      {/* Streak chip */}
      {streak > 0 && (
        <div className="streak-chip">
          <CookieIcon size={14} color="#8B6914" />
          <span>연속 {streak}일째</span>
        </div>
      )}

      {/* Hero cookie illustration */}
      <div className="hero-section">
        <div className="hero-cookie-wrapper">
          <div className="hero-cookie">
            <CookieIcon size={80} color="#D4A574" />
            <div className="hero-cookie-sparkle sparkle-1">
              <SparkleIcon size={16} color="#DAA520" />
            </div>
            <div className="hero-cookie-sparkle sparkle-2">
              <SparkleIcon size={12} color="#D4A574" />
            </div>
            <div className="hero-cookie-sparkle sparkle-3">
              <SparkleIcon size={14} color="#DAA520" />
            </div>
          </div>
        </div>

        <h2 className="hero-title">이름 속에 숨은 감정,</h2>
        <h2 className="hero-title">쫀쿠로 태어나다</h2>
      </div>

      {/* Collection progress */}
      <div className="collection-section">
        <div className="collection-label">
          <span>{totalCookies}종 중 {collectionCount}종 발견</span>
          <span className="collection-percent">{progressPercent}%</span>
        </div>
        <div className="collection-bar">
          <div
            className="collection-bar-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Name input */}
      <div className="input-section">
        <input
          className="name-input"
          type="text"
          placeholder="이름을 입력하세요"
          value={name}
          onChange={(e) => setName(e.target.value)}
          onKeyDown={handleKeyDown}
          maxLength={10}
          autoComplete="off"
        />
      </div>

      {/* CTA Button */}
      <button
        className="btn-cta"
        onClick={handleSubmit}
        disabled={name.trim().length === 0}
      >
        <CookieIcon size={20} color="#FFF8F0" />
        <span>내 쫀쿠 확인하기</span>
      </button>

      {/* Daily quote */}
      <p className="daily-quote">"{dailyQuote}"</p>
    </div>
  );
};

export default HomeScreen;
