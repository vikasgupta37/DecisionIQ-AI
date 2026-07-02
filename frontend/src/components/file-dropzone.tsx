"use client";

import { useCallback, useState } from "react";
import { cn } from "@/lib/utils";

interface FileDropzoneProps {
  onFileSelect: (file: File) => void;
  isUploading?: boolean;
  accept?: string;
}

const SUPPORTED_FORMATS = [
  { ext: "CSV", color: "text-emerald-400" },
  { ext: "XLSX", color: "text-blue-400" },
  { ext: "PDF", color: "text-red-400" },
  { ext: "JSON", color: "text-amber-400" },
  { ext: "TXT", color: "text-slate-400" },
  { ext: "DOCX", color: "text-violet-400" },
];

export function FileDropzone({ onFileSelect, isUploading }: FileDropzoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setIsDragOver(false);
      const file = e.dataTransfer.files[0];
      if (file) onFileSelect(file);
    },
    [onFileSelect]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) onFileSelect(file);
      e.target.value = "";
    },
    [onFileSelect]
  );

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={cn(
        "relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-12 transition-all duration-300 cursor-pointer",
        isDragOver
          ? "border-violet-400 bg-violet-500/10 scale-[1.02]"
          : "border-white/15 bg-white/[0.02] hover:border-white/25 hover:bg-white/[0.04]",
        isUploading && "pointer-events-none opacity-60"
      )}
    >
      <input
        type="file"
        onChange={handleFileInput}
        className="absolute inset-0 cursor-pointer opacity-0"
        accept=".csv,.xlsx,.xls,.pdf,.json,.txt,.docx"
        disabled={isUploading}
      />

      {isUploading ? (
        <div className="flex flex-col items-center gap-4">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-violet-500 border-t-transparent" />
          <p className="text-sm font-medium text-slate-300">Uploading...</p>
        </div>
      ) : (
        <>
          <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500/20 to-indigo-500/20 border border-violet-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" className="text-violet-400"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
          </div>
          <p className="text-base font-semibold text-white mb-1">
            Drop files here or click to browse
          </p>
          <p className="text-sm text-slate-500 mb-4">
            Maximum file size: 50 MB
          </p>
          <div className="flex gap-2 flex-wrap justify-center">
            {SUPPORTED_FORMATS.map((fmt) => (
              <span
                key={fmt.ext}
                className={cn(
                  "rounded-md border border-white/10 bg-white/5 px-2 py-1 text-xs font-medium",
                  fmt.color
                )}
              >
                {fmt.ext}
              </span>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
