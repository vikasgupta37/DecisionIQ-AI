import { cn } from "@/lib/utils";

interface StatusBadgeProps {
  status: string;
  className?: string;
}

const statusConfig: Record<string, { label: string; className: string }> = {
  pending: {
    label: "Pending",
    className: "bg-amber-500/15 text-amber-400 border-amber-500/20",
  },
  processing: {
    label: "Processing",
    className: "bg-blue-500/15 text-blue-400 border-blue-500/20",
  },
  completed: {
    label: "Completed",
    className: "bg-emerald-500/15 text-emerald-400 border-emerald-500/20",
  },
  failed: {
    label: "Failed",
    className: "bg-red-500/15 text-red-400 border-red-500/20",
  },
  trend: {
    label: "Trend",
    className: "bg-violet-500/15 text-violet-400 border-violet-500/20",
  },
  anomaly: {
    label: "Anomaly",
    className: "bg-orange-500/15 text-orange-400 border-orange-500/20",
  },
  recommendation: {
    label: "Recommendation",
    className: "bg-cyan-500/15 text-cyan-400 border-cyan-500/20",
  },
  system: {
    label: "System",
    className: "bg-slate-500/15 text-slate-400 border-slate-500/20",
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = statusConfig[status] || {
    label: status,
    className: "bg-slate-500/15 text-slate-400 border-slate-500/20",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium",
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  );
}
