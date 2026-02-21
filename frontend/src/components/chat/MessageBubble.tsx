import { useMemo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import type { ChatMessage } from "../../lib/types";

// ─── Citation types ────────────────────────────────
export interface Citation {
  id: number;
  url: string;
  title: string;
}

interface Props {
  message: ChatMessage;
  onOpenCitations?: (citations: Citation[], activeId?: number) => void;
}

// ─── Content parsing helpers ───────────────────────

/** Split content at "## References" / "**References**" / first bare "[1]:" line */
function splitContent(content: string): {
  body: string;
  citations: Citation[];
} {
  // Find the references section divider
  const refPatterns = [
    /^## References\s*$/m,
    /^\*\*References\*\*\s*$/m,
    /^### References\s*$/m,
  ];

  let splitIdx = -1;
  for (const pattern of refPatterns) {
    const match = pattern.exec(content);
    if (match) {
      splitIdx = match.index;
      break;
    }
  }

  // Fallback: first bare [1]: line (not inside markdown link)
  if (splitIdx === -1) {
    const bareRef = /^\[1\]:\s+/m.exec(content);
    if (bareRef) splitIdx = bareRef.index;
  }

  if (splitIdx === -1) {
    return { body: content, citations: [] };
  }

  const body = content.slice(0, splitIdx).trimEnd();
  const refBlock = content.slice(splitIdx);

  // Parse [N]: url "title" lines
  const citationRegex = /\[(\d+)\]:\s+(https?:\/\/\S+)(?:\s+"([^"]*)")?/g;
  const citations: Citation[] = [];
  let m: RegExpExecArray | null;
  while ((m = citationRegex.exec(refBlock)) !== null) {
    const urlStr = m[2]!;
    let title = m[3] ?? "";
    if (!title) {
      try {
        title = new URL(urlStr).hostname;
      } catch {
        title = urlStr;
      }
    }
    citations.push({ id: parseInt(m[1]!, 10), url: urlStr, title });
  }

  return { body, citations };
}

/** Convert inline [N] markers to citation links (rendered as superscript by custom `a` component) */
function linkifyCitations(body: string, citationIds: Set<number>): string {
  return body.replace(/\[(\d+)\]/g, (match, num) => {
    const id = parseInt(num, 10);
    if (citationIds.has(id)) {
      return `[${id}](#cite-${id})`;
    }
    return match;
  });
}

// ─── Component ─────────────────────────────────────

export function MessageBubble({ message, onOpenCitations }: Props) {
  const isUser = message.role === "user";

  const { citations, processedBody } = useMemo(() => {
    if (isUser) return { citations: [] as Citation[], processedBody: message.content };
    const parsed = splitContent(message.content);
    const citationIds = new Set(parsed.citations.map((c) => c.id));
    const linked = citationIds.size > 0
      ? linkifyCitations(parsed.body, citationIds)
      : parsed.body;
    return { citations: parsed.citations, processedBody: linked };
  }, [message.content, isUser]);

  const handleCiteClick = (id: number) => {
    if (onOpenCitations && citations.length > 0) {
      onOpenCitations(citations, id);
    }
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-primary-600 text-white"
            : "bg-gray-100 text-gray-900"
        }`}
      >
        {!isUser && (
          <div className="mb-1 text-xs font-medium text-primary-600">
            AI Trip Planner
          </div>
        )}

        {isUser ? (
          <div className="text-sm whitespace-pre-wrap">{message.content}</div>
        ) : (
          <>
            <div className="prose prose-sm max-w-none prose-headings:mt-3 prose-headings:mb-1 prose-p:my-1 prose-ul:my-1 prose-ol:my-1 prose-li:my-0 prose-table:my-2 prose-pre:my-2 prose-a:text-primary-700 prose-a:underline">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  a: ({ children, href, ...props }) => {
                    // Intercept citation links → render as superscript badges
                    const citeMatch = href?.match(/^#cite-(\d+)$/);
                    if (citeMatch) {
                      const citeId = parseInt(citeMatch[1]!, 10);
                      return (
                        <button
                          type="button"
                          onClick={() => handleCiteClick(citeId)}
                          className="ml-0.5 inline-flex translate-y-[-4px] cursor-pointer items-center rounded bg-primary-100 px-1 py-0 text-[10px] font-semibold text-primary-700 no-underline hover:bg-primary-200"
                          title={`Reference ${citeId}`}
                        >
                          <sup>{children}</sup>
                        </button>
                      );
                    }
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        {...props}
                      >
                        {children}
                      </a>
                    );
                  },
                }}
              >
                {processedBody}
              </ReactMarkdown>
            </div>

            {/* Collapsible References section */}
            {citations.length > 0 && (
              <details className="mt-3 border-t border-gray-200 pt-2">
                <summary className="cursor-pointer text-xs font-medium text-gray-500 select-none hover:text-gray-700">
                  References ({citations.length})
                </summary>
                <ul className="mt-1 space-y-1">
                  {citations.map((cite) => (
                    <li key={cite.id}>
                      <button
                        type="button"
                        onClick={() => handleCiteClick(cite.id)}
                        className="flex w-full items-center gap-2 rounded px-2 py-1 text-left text-xs text-gray-600 hover:bg-gray-200"
                      >
                        <span className="font-mono text-primary-600">
                          [{cite.id}]
                        </span>
                        <span className="truncate">{cite.title}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </>
        )}

        <div
          className={`mt-1 text-right text-[10px] ${
            isUser ? "text-primary-200" : "text-gray-400"
          }`}
        >
          {new Date(message.created_at).toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </div>
      </div>
    </div>
  );
}
