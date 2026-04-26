import { cn } from "../../lib/utils";

interface ProgressProps {
  value: number;        // 0–100
  max?: number;
  color?: string;       // Tailwind bg-* class
  className?: string;
  showLabel?: boolean;
}

export function Progress({ value, max = 100, color = "bg-primary-500", className, showLabel = false }: ProgressProps) {
  const pct = Math.min(100, Math.max(0, (value / max) * 100));
  return (
    <div className={cn("relative w-full h-2.5 bg-gray-100 rounded-full overflow-hidden", className)}>
      <div
        className={cn("h-full rounded-full transition-all duration-500", color)}
        style={{ width: `${pct}%` }}
      />
      {showLabel && (
        <span className="absolute right-0 -top-5 text-xs text-gray-500">
          {Math.round(pct)}%
        </span>
      )}
    </div>
  );
}
