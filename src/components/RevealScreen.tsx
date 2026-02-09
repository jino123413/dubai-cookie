import React, { useState, useEffect } from 'react';

interface RevealScreenProps {
  name: string;
  cookieName: string;
  onRevealComplete: () => void;
}

const RevealScreen: React.FC<RevealScreenProps> = ({
  name,
  cookieName,
  onRevealComplete,
}) => {
  const [phase, setPhase] = useState<'cutting' | 'reveal'>('cutting');

  useEffect(() => {
    const timer1 = setTimeout(() => {
      setPhase('reveal');
    }, 1400);

    const timer2 = setTimeout(() => {
      onRevealComplete();
    }, 2800);

    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [onRevealComplete]);

  return (
    <div className="reveal-screen">
      <div className="reveal-cookie-area">
        {/* Cookie being cut */}
        <div className={`reveal-cookie ${phase === 'cutting' ? 'cutting' : 'cut-done'}`}>
          <div className="cookie-left-half">
            <div className="cookie-surface" />
          </div>
          <div className="cookie-right-half">
            <div className="cookie-surface" />
          </div>

          {/* Cutting line */}
          <div className={`cutting-line ${phase === 'cutting' ? 'animate-cut' : 'cut-complete'}`} />

          {/* Cross section glow */}
          {phase === 'reveal' && (
            <div className="cross-section-glow" />
          )}
        </div>

        {/* Crumbs */}
        {phase === 'reveal' && (
          <div className="cookie-crumbs">
            {Array.from({ length: 6 }).map((_, i) => (
              <div
                key={i}
                className="crumb"
                style={{
                  '--crumb-x': `${(i - 3) * 20 + Math.random() * 10}px`,
                  '--crumb-delay': `${i * 0.08}s`,
                  '--crumb-size': `${3 + Math.random() * 4}px`,
                } as React.CSSProperties}
              />
            ))}
          </div>
        )}
      </div>

      {/* Text */}
      <div className="reveal-text">
        <p className="reveal-name">
          <span className="reveal-name-highlight">{name}</span>님의 쫀쿠는...
        </p>
        {phase === 'reveal' && (
          <p className="reveal-cookie-name">{cookieName}</p>
        )}
      </div>
    </div>
  );
};

export default RevealScreen;
