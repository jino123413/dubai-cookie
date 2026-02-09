import React from 'react';

export const CookieIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 24,
  color = 'currentColor',
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <circle cx="12" cy="12" r="10" fill={color} opacity="0.9" />
    <circle cx="8" cy="9" r="1.5" fill="#5C4610" opacity="0.7" />
    <circle cx="14" cy="8" r="1.2" fill="#5C4610" opacity="0.6" />
    <circle cx="10" cy="14" r="1.3" fill="#5C4610" opacity="0.7" />
    <circle cx="15" cy="13" r="1" fill="#5C4610" opacity="0.5" />
    <circle cx="6" cy="13" r="0.8" fill="#5C4610" opacity="0.4" />
    <path
      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"
      fill="none"
      stroke={color}
      strokeWidth="0.5"
      opacity="0.3"
    />
  </svg>
);

export const KnifeIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 24,
  color = 'currentColor',
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M3 17L19 3"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
    />
    <path
      d="M19 3L21 5L7 19L3 17Z"
      fill={color}
      opacity="0.3"
    />
    <path
      d="M3 17L5 21L7 19"
      stroke={color}
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const ShareIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 24,
  color = 'currentColor',
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none">
    <path
      d="M12 3V15M12 3L8 7M12 3L16 7"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M4 14V18C4 19.1 4.9 20 6 20H18C19.1 20 20 19.1 20 18V14"
      stroke={color}
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

export const SparkleIcon: React.FC<{ size?: number; color?: string }> = ({
  size = 24,
  color = 'currentColor',
}) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill={color}>
    <path d="M12 2L13.5 8.5L20 10L13.5 11.5L12 18L10.5 11.5L4 10L10.5 8.5L12 2Z" />
    <path d="M19 15L19.75 17.25L22 18L19.75 18.75L19 21L18.25 18.75L16 18L18.25 17.25L19 15Z" opacity="0.6" />
  </svg>
);
