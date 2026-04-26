import { cn } from "../../lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: "default" | "success" | "warning" | "danger" | "info";
}

const variantMap: Record<string, string> = {
  default: "bg-gray-100 text-gray-700",
  success: "bg-success-50 text-success-600",
  warning: "bg-warning-50 text-warning-600",
  danger:  "bg-danger-50 text-danger-600",
  info:    "bg-primary-50 text-primary-700",
};

export function Badge({ variant = "default", className, children, ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
        variantMap[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
