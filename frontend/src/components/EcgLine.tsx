/**
 * Animated ECG waveform strip — realistic PQRST morphology.
 * Uses a 2-cycle SVG path scrolled left continuously for a seamless loop.
 */

interface EcgLineProps {
  className?: string
  color?: string
  opacity?: number
}

// Single PQRST cycle (200 viewBox units wide, baseline y=20, height 40):
//  flat → P wave (gentle bump) → PR → QRS (sharp spike) → ST → T wave → flat
const C1 =
  'M0,20 L28,20 Q38,20 43,14 Q48,9 53,20 L67,20 L69,25 L73,1 L77,26 L81,20 L98,20 Q108,12 118,10 Q128,8 136,20 L200,20'

// Identical copy shifted 200 units right for seamless scroll loop
const C2 =
  'M200,20 L228,20 Q238,20 243,14 Q248,9 253,20 L267,20 L269,25 L273,1 L277,26 L281,20 L298,20 Q308,12 318,10 Q328,8 336,20 L400,20'

export function EcgLine({ className = '', color = '#e11d48', opacity = 0.6 }: EcgLineProps) {
  return (
    <div
      className={`overflow-hidden ${className}`}
      style={{ height: 40 }}
      aria-hidden="true"
    >
      {/*
        SVG is 200% wide (two cycles) → left-50% translation = exact one cycle scroll.
        preserveAspectRatio="none" lets the path stretch to fill the width.
      */}
      <svg
        width="200%"
        height="40"
        viewBox="0 0 400 40"
        preserveAspectRatio="none"
        style={{
          display: 'block',
          animation: 'ecgScroll 3.6s linear infinite',
        }}
      >
        <path
          d={`${C1} ${C2}`}
          stroke={color}
          strokeWidth="1.8"
          fill="none"
          opacity={opacity}
          vectorEffect="non-scaling-stroke"
        />
      </svg>
    </div>
  )
}
