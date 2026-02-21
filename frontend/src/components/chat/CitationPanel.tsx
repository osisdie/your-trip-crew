import { useEffect, useRef } from "react";
import { X, ExternalLink } from "lucide-react";
import type { Citation } from "./MessageBubble";

interface CitationPanelProps {
  citations: Citation[];
  activeCitationId?: number;
  onClose: () => void;
}

function getHostname(url: string): string {
  try {
    return new URL(url).hostname;
  } catch {
    return url;
  }
}

export function CitationPanel({
  citations,
  activeCitationId,
  onClose,
}: CitationPanelProps) {
  const activeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    activeRef.current?.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [activeCitationId]);

  return (
    <div className="flex w-80 flex-shrink-0 flex-col border-l border-gray-200 bg-white shadow-lg">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <h3 className="text-sm font-semibold text-gray-900">References</h3>
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1 text-gray-400 hover:bg-gray-100 hover:text-gray-600"
          aria-label="Close references panel"
        >
          <X size={16} />
        </button>
      </div>

      {/* Citation list */}
      <div className="flex-1 overflow-y-auto p-3">
        <div className="space-y-2">
          {citations.map((cite) => {
            const hostname = getHostname(cite.url);
            const isActive = cite.id === activeCitationId;
            return (
              <div
                key={cite.id}
                ref={isActive ? activeRef : undefined}
                className={`rounded-lg border p-3 transition ${
                  isActive
                    ? "border-primary-300 bg-primary-50 ring-2 ring-primary-200"
                    : "border-gray-200 hover:border-gray-300 hover:bg-gray-50"
                }`}
              >
                <a
                  href={cite.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-start gap-3"
                >
                  {/* Favicon */}
                  <img
                    src={`https://www.google.com/s2/favicons?domain=${hostname}&sz=32`}
                    alt=""
                    width={32}
                    height={32}
                    className="mt-0.5 flex-shrink-0 rounded"
                  />

                  <div className="min-w-0 flex-1">
                    {/* Citation number + title */}
                    <div className="flex items-baseline gap-1.5">
                      <span className="flex-shrink-0 font-mono text-xs font-semibold text-primary-600">
                        [{cite.id}]
                      </span>
                      <span className="truncate text-sm font-medium text-gray-900 group-hover:text-primary-700">
                        {cite.title}
                      </span>
                    </div>
                    {/* Domain */}
                    <div className="mt-0.5 flex items-center gap-1 text-xs text-gray-400">
                      <span className="truncate">{hostname}</span>
                      <ExternalLink size={10} className="flex-shrink-0" />
                    </div>
                  </div>
                </a>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
