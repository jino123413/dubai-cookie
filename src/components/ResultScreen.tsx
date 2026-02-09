import React, { useCallback } from 'react';
import { CookieResult } from '../types';
import { ShareIcon, CookieIcon, SparkleIcon } from './BrandIcons';

interface ResultScreenProps {
  result: CookieResult;
  onRetry: () => void;
  adLoading: boolean;
}

const ResultScreen: React.FC<ResultScreenProps> = ({
  result,
  onRetry,
  adLoading,
}) => {
  const { cookie, name } = result;

  const handleShare = useCallback(async () => {
    const shareText = `${name}님은 "${cookie.name}"이래! 🍪\n이름 속에 숨은 감정, 쫀쿠로 태어나다`;

    try {
      const { share, getTossShareLink } = await import('@apps-in-toss/web-framework');
      const tossLink = await getTossShareLink('intoss://dubai-cookie/');
      await share({ message: `${shareText}\n${tossLink}` });
    } catch {
      try {
        if (navigator.share) {
          await navigator.share({
            title: '내가 두쫀쿠?',
            text: shareText,
          });
        }
      } catch {}
    }
  }, [name, cookie.name]);

  const cookieImageSrc = `/cookies/${cookie.id}.png`;

  return (
    <div className="result-screen">
      {/* Cookie image hero */}
      <div className="result-hero">
        <div className="result-image-frame">
          <img
            src={cookieImageSrc}
            alt={cookie.name}
            className="result-cookie-image"
            onError={(e) => {
              (e.target as HTMLImageElement).style.display = 'none';
              const fallback = (e.target as HTMLImageElement).nextElementSibling;
              if (fallback) (fallback as HTMLElement).style.display = 'flex';
            }}
          />
          <div className="result-cookie-fallback" style={{ display: 'none' }}>
            <CookieIcon size={80} color={cookie.themeColor} />
            <div className="fallback-deco" style={{ color: cookie.themeColor }}>
              {cookie.emotion}
            </div>
          </div>
        </div>

        {/* Sparkle decorations around image */}
        <div className="result-sparkle s1">
          <SparkleIcon size={18} color={cookie.themeColor} />
        </div>
        <div className="result-sparkle s2">
          <SparkleIcon size={14} color="#DAA520" />
        </div>
        <div className="result-sparkle s3">
          <SparkleIcon size={16} color={cookie.themeColor} />
        </div>
      </div>

      {/* Cookie name badge - overlapping with image */}
      <div className="result-name-badge" style={{ backgroundColor: cookie.themeColor }}>
        <span>{cookie.name}</span>
      </div>

      {/* Personality description - narrative style */}
      <div className="result-personality">
        <p className="personality-text">{cookie.personality}</p>
      </div>

      {/* Today's message */}
      <div className="result-quote-section">
        <div className="quote-divider">
          <span className="quote-divider-line" />
          <span className="quote-divider-label">오늘의 한마디</span>
          <span className="quote-divider-line" />
        </div>
        <p className="result-quote">"{cookie.quote}"</p>
      </div>

      {/* Share button */}
      <button className="btn-share" onClick={handleShare}>
        <ShareIcon size={18} color="#FFF8F0" />
        <span>친구에게 공유하기</span>
      </button>

      {/* AD retry button */}
      <div className="retry-section">
        <button
          className="btn-retry"
          onClick={onRetry}
          disabled={adLoading}
        >
          <span className="ad-badge">AD</span>
          <span>다른 이름으로 보기</span>
        </button>
        <p className="ad-notice">광고 시청 후 다른 이름의 쫀쿠를 확인합니다</p>
      </div>
    </div>
  );
};

export default ResultScreen;
