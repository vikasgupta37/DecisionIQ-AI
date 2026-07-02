"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { AppShell } from "@/components/layout/app-shell";
import { FileDropzone } from "@/components/file-dropzone";
import { StatusBadge } from "@/components/status-badge";
import { formatBytes, formatDate } from "@/lib/utils";

interface UploadMetadata {
  row_count: number | null;
  column_names: string[] | null;
  page_count: number | null;
  word_count: number | null;
  extra: Record<string, unknown>;
}

interface UploadResponse {
  dataset: DatasetItem;
  metadata: UploadMetadata;
  message: string;
}

interface DatasetItem {
  id: number;
  name: string;
  file_type: string;
  file_size: number;
  status: string;
  row_count: number | null;
  user_id: number;
  created_at: string;
  updated_at: string;
}

interface DatasetListResponse {
  datasets: DatasetItem[];
  total: number;
}

export default function UploadPage() {
  const queryClient = useQueryClient();
  const [lastUpload, setLastUpload] = useState<UploadResponse | null>(null);

  const { data: datasetsData, isLoading: isListLoading } = useQuery<DatasetListResponse>({
    queryKey: ["datasets"],
    queryFn: () => api.get<DatasetListResponse>("/upload"),
  });

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      return api.postForm<UploadResponse>("/upload", formData);
    },
    onSuccess: (data) => {
      setLastUpload(data);
      queryClient.invalidateQueries({ queryKey: ["datasets"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });

  const handleFileSelect = (file: File) => {
    setLastUpload(null);
    uploadMutation.mutate(file);
  };

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold text-white">File Upload</h1>
          <p className="text-sm text-slate-500 mt-1">
            Upload structured and unstructured data for AI-powered analysis
          </p>
        </div>

        {/* Upload Zone */}
        <FileDropzone
          onFileSelect={handleFileSelect}
          isUploading={uploadMutation.isPending}
        />

        {/* Error Message */}
        {uploadMutation.isError && (
          <div className="rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-400">
            {uploadMutation.error instanceof Error
              ? uploadMutation.error.message
              : "Upload failed. Please try again."}
          </div>
        )}

        {/* Upload Success + Metadata */}
        {lastUpload && (
          <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-6">
            <div className="flex items-center gap-2 mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
              <h3 className="text-base font-semibold text-emerald-300">
                {lastUpload.message}
              </h3>
            </div>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {lastUpload.metadata.row_count !== null && (
                <div className="rounded-xl bg-white/5 border border-white/5 px-4 py-3">
                  <p className="text-xs text-slate-500">Rows</p>
                  <p className="text-lg font-bold text-white">{lastUpload.metadata.row_count}</p>
                </div>
              )}
              {lastUpload.metadata.column_names && (
                <div className="rounded-xl bg-white/5 border border-white/5 px-4 py-3 col-span-2">
                  <p className="text-xs text-slate-500 mb-1">Columns</p>
                  <div className="flex flex-wrap gap-1">
                    {lastUpload.metadata.column_names.map((col) => (
                      <span
                        key={col}
                        className="rounded-md bg-violet-500/15 border border-violet-500/20 px-2 py-0.5 text-xs text-violet-300"
                      >
                        {col}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {lastUpload.metadata.page_count !== null && (
                <div className="rounded-xl bg-white/5 border border-white/5 px-4 py-3">
                  <p className="text-xs text-slate-500">Pages</p>
                  <p className="text-lg font-bold text-white">{lastUpload.metadata.page_count}</p>
                </div>
              )}
              {lastUpload.metadata.word_count !== null && (
                <div className="rounded-xl bg-white/5 border border-white/5 px-4 py-3">
                  <p className="text-xs text-slate-500">Words</p>
                  <p className="text-lg font-bold text-white">{lastUpload.metadata.word_count}</p>
                </div>
              )}
              <div className="rounded-xl bg-white/5 border border-white/5 px-4 py-3">
                <p className="text-xs text-slate-500">File Size</p>
                <p className="text-lg font-bold text-white">
                  {formatBytes(lastUpload.dataset.file_size)}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Datasets Table */}
        <div className="rounded-2xl border border-white/10 bg-white/[0.02] p-6">
          <h3 className="mb-4 text-base font-semibold text-white">Your Datasets</h3>

          {isListLoading ? (
            <div className="space-y-3">
              {[...Array(3)].map((_, i) => (
                <div key={i} className="h-14 animate-pulse rounded-lg bg-white/5" />
              ))}
            </div>
          ) : !datasetsData?.datasets.length ? (
            <p className="text-sm text-slate-500 py-8 text-center">
              No datasets uploaded yet. Drop a file above to get started.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-white/10">
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Name</th>
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Type</th>
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Size</th>
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Rows</th>
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Status</th>
                    <th className="pb-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Uploaded</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {datasetsData.datasets.map((ds) => (
                    <tr key={ds.id} className="hover:bg-white/[0.02] transition-colors">
                      <td className="py-3 pr-4">
                        <p className="text-sm font-medium text-white">{ds.name}</p>
                      </td>
                      <td className="py-3 pr-4">
                        <span className="rounded-md bg-white/5 border border-white/10 px-2 py-0.5 text-xs font-medium text-slate-400 uppercase">
                          {ds.file_type}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-sm text-slate-400">
                        {formatBytes(ds.file_size)}
                      </td>
                      <td className="py-3 pr-4 text-sm text-slate-400">
                        {ds.row_count ?? "—"}
                      </td>
                      <td className="py-3 pr-4">
                        <StatusBadge status={ds.status} />
                      </td>
                      <td className="py-3 text-sm text-slate-500">
                        {formatDate(ds.created_at)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
