"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { AppShell } from "@/components/layout/app-shell";
import { KpiCard } from "@/components/kpi-card";
import { StatusBadge } from "@/components/status-badge";
import { formatBytes, formatRelativeTime } from "@/lib/utils";

interface DashboardData {
  kpis: {
    total_uploads: number;
    processed_datasets: number;
    active_insights: number;
    storage_used_bytes: number;
  };
  upload_status: Array<{
    id: number;
    name: string;
    file_type: string;
    file_size: number;
    status: string;
    created_at: string;
  }>;
  insights: Array<{
    id: number;
    title: string;
    content: string;
    insight_type: string;
    created_at: string;
  }>;
  recent_activities: Array<{
    id: number;
    user_name: string;
    action: string;
    details: string | null;
    created_at: string;
  }>;
}

export default function DashboardPage() {
  const { data, isLoading } = useQuery<DashboardData>({
    queryKey: ["dashboard"],
    queryFn: () => api.get<DashboardData>("/dashboard"),
  });

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">
            Platform overview and real-time intelligence metrics
          </p>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <KpiCard
            title="Total Uploads"
            value={isLoading ? "—" : data?.kpis.total_uploads ?? 0}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
            }
          />
          <KpiCard
            title="Processed"
            value={isLoading ? "—" : data?.kpis.processed_datasets ?? 0}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            }
          />
          <KpiCard
            title="AI Insights"
            value={isLoading ? "—" : data?.kpis.active_insights ?? 0}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="16" y2="12"/><line x1="12" x2="12.01" y1="8" y2="8"/></svg>
            }
          />
          <KpiCard
            title="Storage Used"
            value={isLoading ? "—" : formatBytes(data?.kpis.storage_used_bytes ?? 0)}
            icon={
              <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>
            }
          />
        </div>

        <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Recent Uploads */}
          <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <h3 className="mb-4 text-base font-semibold text-white">Recent Uploads</h3>
            {isLoading ? (
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-12 animate-pulse rounded-lg bg-white/5" />
                ))}
              </div>
            ) : data?.upload_status.length === 0 ? (
              <p className="text-sm text-slate-500 py-8 text-center">No uploads yet</p>
            ) : (
              <div className="space-y-2">
                {data?.upload_status.map((file) => (
                  <div
                    key={file.id}
                    className="flex items-center justify-between rounded-xl bg-white/[0.03] border border-white/5 px-4 py-3"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-500/10 text-xs font-bold text-violet-400 uppercase">
                        {file.file_type}
                      </div>
                      <div>
                        <p className="text-sm font-medium text-white">{file.name}</p>
                        <p className="text-xs text-slate-500">{formatBytes(file.file_size)}</p>
                      </div>
                    </div>
                    <StatusBadge status={file.status} />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* AI Insights */}
          <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
            <h3 className="mb-4 text-base font-semibold text-white">AI Insights</h3>
            {isLoading ? (
              <div className="space-y-3">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-16 animate-pulse rounded-lg bg-white/5" />
                ))}
              </div>
            ) : data?.insights.length === 0 ? (
              <p className="text-sm text-slate-500 py-8 text-center">No insights generated yet</p>
            ) : (
              <div className="space-y-3">
                {data?.insights.map((insight) => (
                  <div
                    key={insight.id}
                    className="rounded-xl bg-white/[0.03] border border-white/5 px-4 py-3"
                  >
                    <div className="flex items-center justify-between mb-1">
                      <p className="text-sm font-medium text-white">{insight.title}</p>
                      <StatusBadge status={insight.insight_type} />
                    </div>
                    <p className="text-xs text-slate-400 line-clamp-2">{insight.content}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
          <h3 className="mb-4 text-base font-semibold text-white">Recent Activity</h3>
          {isLoading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-10 animate-pulse rounded-lg bg-white/5" />
              ))}
            </div>
          ) : data?.recent_activities.length === 0 ? (
            <p className="text-sm text-slate-500 py-8 text-center">No activity recorded yet</p>
          ) : (
            <div className="space-y-2">
              {data?.recent_activities.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-center justify-between rounded-xl bg-white/[0.03] border border-white/5 px-4 py-3"
                >
                  <div className="flex items-center gap-3">
                    <div className="h-2 w-2 rounded-full bg-violet-400" />
                    <div>
                      <p className="text-sm text-white">
                        <span className="font-medium">{activity.user_name}</span>
                        {" · "}
                        <span className="text-slate-400">{activity.action.replace(/_/g, " ")}</span>
                      </p>
                      {activity.details && (
                        <p className="text-xs text-slate-500">{activity.details}</p>
                      )}
                    </div>
                  </div>
                  <span className="text-xs text-slate-500 shrink-0">
                    {formatRelativeTime(activity.created_at)}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
