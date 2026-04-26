import { useNavigate } from 'react-router-dom';
import HeartCanvas from '../components/HeartCanvas';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="relative flex flex-col items-center justify-center min-h-screen overflow-hidden bg-[#07070f]">

      {/* ambient background orbs */}
      <div className="absolute inset-0 pointer-events-none">
        <div
          className="glow-orb absolute rounded-full"
          style={{
            width: 520,
            height: 520,
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            background: 'radial-gradient(circle, rgba(180,14,47,0.28) 0%, transparent 70%)',
          }}
        />
        <div
          className="glow-orb absolute rounded-full"
          style={{
            width: 260,
            height: 260,
            top: '30%',
            left: '38%',
            animationDelay: '1.5s',
            background: 'radial-gradient(circle, rgba(239,68,68,0.12) 0%, transparent 70%)',
          }}
        />
      </div>

      {/* pulse rings + 3-D heart canvas */}
      <div className="relative flex items-center justify-center" style={{ width: 300, height: 300 }}>
        <div className="pulse-ring" style={{ width: 240, height: 240, position: 'absolute', top: 30, left: 30, borderRadius: '50%' }} />
        <div className="pulse-ring pulse-ring-2" style={{ width: 240, height: 240, position: 'absolute', top: 30, left: 30, borderRadius: '50%' }} />
        <div className="pulse-ring pulse-ring-3" style={{ width: 240, height: 240, position: 'absolute', top: 30, left: 30, borderRadius: '50%' }} />

        <HeartCanvas size={300} />
      </div>

      {/* brand + CTA */}
      <div className="mt-4 flex flex-col items-center gap-3 text-center px-6">
        <h1
          className="landing-fade-1 text-5xl font-bold tracking-tight"
          style={{
            background: 'linear-gradient(135deg, #ff6b8a 0%, #e8173a 60%, #ff6b8a 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
          }}
        >
          BeatBound
        </h1>

        {/* Hindi verse */}
        <p
          className="landing-fade-2 text-center leading-loose max-w-sm"
          style={{
            fontFamily: '"Noto Sans Devanagari", "Mangal", serif',
            fontSize: '1.15rem',
            background: 'linear-gradient(135deg, #fda4af 0%, #fb7185 50%, #fda4af 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            textShadow: 'none',
            letterSpacing: '0.01em',
          }}
        >
          हर धड़कन में एक कहानी है,<br />
          इसे संभालना ही ज़िंदगी की निशानी है।
        </p>

        <p className="landing-fade-3 text-base text-gray-500 max-w-xs leading-relaxed text-center" style={{ marginTop: '0.25rem' }}>
          Cardiac Decision Support System<br />
          <span className="text-gray-600 text-sm">AI-powered · Clinical-grade · Evidence-based</span>
        </p>

        <button
          onClick={() => navigate('/chat')}
          className="landing-fade-3 mt-4 px-8 py-3 rounded-full text-sm font-semibold text-white transition-all duration-200 hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:ring-offset-[#07070f]"
          style={{
            background: 'linear-gradient(135deg, #e8173a 0%, #9f0d25 100%)',
            boxShadow: '0 0 24px rgba(232,23,58,0.45)',
          }}
        >
          Get Started →
        </button>

        <p className="landing-fade-4 text-[11px] text-gray-700 mt-2">
          For educational &amp; research use only · Not a substitute for medical advice
        </p>
      </div>
    </div>
  );
}
