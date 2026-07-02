import { cn } from "@/lib/utils";

interface KpiCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  trend?: string;
  className?: string;
}

export function KpiCard({ title, value, icon, trend, className }: KpiCardProps) {
  return (
    <div
      className={cn(
        "group relative overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-br from-slate-900 to-slate-800 p-6 transition-all duration-300 hover:border-violet-500/30 hover:shadow-lg hover:shadow-violet-500/5",
        className
      )}
    >
      {/* Ambient glow */}
      <div className="absolute -right-6 -top-6 h-24 w-24 rounded-full bg-violet-500/10 blur-2xl transition-all duration-500 group-hover:bg-violet-500/20" />

      <div className="relative flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-bold tracking-tight text-white">
            {value}
          </p>
          {trend && (
            <p className="mt-1 text-xs font-medium text-emerald-400">{trend}</p>
          )}
        </div>
        <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-violet-500/15 text-violet-400">
          {icon}
        </div>
      </div>
    </div>
  );
}
