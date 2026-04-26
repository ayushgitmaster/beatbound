import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "../../lib/utils";

const btn = cva(
  "inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 select-none cursor-pointer",
  {
    variants: {
      variant: {
        default:   "bg-primary-600 text-white hover:bg-primary-700 active:bg-primary-800 shadow-sm",
        secondary: "bg-primary-50 text-primary-700 hover:bg-primary-100 border border-primary-200",
        outline:   "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50",
        ghost:     "text-gray-600 hover:bg-gray-100 hover:text-gray-900",
        danger:    "bg-danger-600 text-white hover:bg-danger-700 shadow-sm",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-sm",
        lg: "h-11 px-6 text-base",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: { variant: "default", size: "md" },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof btn> {
  loading?: boolean;
}

export function Button({ className, variant, size, loading, children, disabled, ...props }: ButtonProps) {
  return (
    <button className={cn(btn({ variant, size }), className)} disabled={disabled || loading} {...props}>
      {loading && (
        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
      )}
      {children}
    </button>
  );
}
