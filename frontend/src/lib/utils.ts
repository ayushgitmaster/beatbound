import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Returns Tailwind color class based on risk category string. */
export function riskColor(category: string): string {
  const c = category.toLowerCase();
  if (c.includes("low"))        return "text-success-600";
  if (c.includes("border"))     return "text-blue-500";
  if (c.includes("inter") || c.includes("moderate")) return "text-warning-600";
  if (c.includes("high") || c.includes("critical"))  return "text-danger-600";
  return "text-gray-600";
}

export function riskBgColor(category: string): string {
  const c = category.toLowerCase();
  if (c.includes("low"))        return "bg-success-50 border-success-500";
  if (c.includes("border"))     return "bg-blue-50 border-blue-400";
  if (c.includes("inter") || c.includes("moderate")) return "bg-warning-50 border-warning-500";
  if (c.includes("high") || c.includes("critical"))  return "bg-danger-50 border-danger-500";
  return "bg-gray-50 border-gray-300";
}

export function riskBarColor(category: string): string {
  const c = category.toLowerCase();
  if (c.includes("low"))        return "bg-success-500";
  if (c.includes("border"))     return "bg-blue-400";
  if (c.includes("inter") || c.includes("moderate")) return "bg-warning-500";
  return "bg-danger-500";
}

/** Format a number to 1 decimal place, returning "—" for null/undefined. */
export function fmt(val: number | undefined | null, unit = ""): string {
  if (val == null) return "—";
  return `${val.toFixed(1)}${unit ? " " + unit : ""}`;
}

/** Confidence → colour */
export function confColor(conf: number): string {
  if (conf >= 0.85) return "text-success-600";
  if (conf >= 0.65) return "text-warning-600";
  return "text-danger-600";
}
