import { NavLink } from "react-router-dom";
import { useEffect, useState } from "react";
import {
  MessageSquareHeart,
  Activity,
  FlaskConical,
  BarChart3,
  BookOpen,
  Layers,
  Info,
  Cpu,
  Calculator,
  TestTube2,
  Wifi,
  WifiOff,
} from "lucide-react";
import { cn } from "../lib/utils";

const navItems = [
  { to: "/chat",      icon: MessageSquareHeart, label: "Chat Assistant" },
  { to: "/symptom",   icon: Activity,           label: "Symptom Checker" },
  { to: "/lab",       icon: FlaskConical,        label: "Upload Lab Report" },
  { to: "/risk",      icon: BarChart3,           label: "Risk Dashboard" },
  { to: "/explain",   icon: Layers,             label: "Explainability" },
  { to: "/resources", icon: BookOpen,           label: "Resources" },
  { to: "/about",     icon: Info,               label: "About" },
];

const kpis = [
  { icon: Cpu,         label: "LLM",         value: "Gemini 2.5" },
  { icon: Calculator,  label: "Calculators", value: "4 Models"   },
  { icon: TestTube2,   label: "Lab Markers", value: "9 Params"   },
  { icon: Layers,      label: "Reasoning",   value: "Explainable"},
];

function useApiStatus() {
  const [online, setOnline] = useState<boolean | null>(null);
  useEffect(() => {
    fetch("/api/health", { method: "GET" })
      .then((r) => setOnline(r.ok))
      .catch(() => setOnline(false));
  }, []);
  return online;
}

export function Sidebar() {
  const online = useApiStatus();

  return (
    <aside className="fixed top-0 left-0 h-full w-60 bg-white border-r border-gray-200 flex flex-col z-20 shadow-sm">
      {/* Brand */}
      <div className="px-5 py-5 border-b border-gray-100">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
            <MessageSquareHeart size={18} className="text-white" />
          </div>
          <div>
            <p className="text-sm font-bold text-gray-900 leading-tight">BeatBound</p>
            <p className="text-[10px] text-gray-400 leading-tight">Cardiac DSS v3.0</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-3 py-4 space-y-0.5 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors duration-150",
                isActive
                  ? "bg-primary-50 text-primary-700"
                  : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
              )
            }
          >
            {({ isActive }) => (
              <>
                <Icon
                  size={17}
                  className={cn("shrink-0", isActive ? "text-primary-600" : "text-gray-400")}
                />
                {label}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* ── System KPIs ─────────────────────────────────────────────────── */}
      <div className="px-3 pb-3 border-t border-gray-100 pt-3 space-y-2.5">

        {/* API status badge */}
        <div className="flex items-center justify-between px-2">
          <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-wide">System Status</span>
          <span
            className={cn(
              "flex items-center gap-1 text-[10px] font-medium rounded-full px-2 py-0.5",
              online === null  ? "bg-gray-100 text-gray-400" :
              online           ? "bg-green-50 text-green-600" :
                                 "bg-red-50   text-red-500"
            )}
          >
            {online === null ? (
              <span className="w-1.5 h-1.5 rounded-full bg-gray-300 inline-block" />
            ) : online ? (
              <>
                <span className="relative flex h-1.5 w-1.5">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-green-500" />
                </span>
                <Wifi size={9} />
                API Online
              </>
            ) : (
              <>
                <WifiOff size={9} />
                API Offline
              </>
            )}
          </span>
        </div>

        {/* KPI 2×2 grid */}
        <div className="grid grid-cols-2 gap-1.5">
          {kpis.map(({ icon: Icon, label, value }) => (
            <div
              key={label}
              className="flex flex-col gap-0.5 bg-gray-50 rounded-xl px-2.5 py-2 border border-gray-100"
            >
              <div className="flex items-center gap-1 text-primary-500">
                <Icon size={11} />
                <span className="text-[9px] font-semibold uppercase tracking-wide text-gray-400">{label}</span>
              </div>
              <span className="text-[11px] font-bold text-gray-800 leading-tight">{value}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Footer */}
      <div className="px-4 py-3 border-t border-gray-100">
        <p className="text-[11px] text-gray-400 text-center leading-relaxed">
          Designed by Ayush Sharma &amp; Janvi Chauhan
        </p>
        <p className="text-[10px] text-gray-300 text-center mt-0.5">For educational use only</p>
      </div>
    </aside>
  );
}
