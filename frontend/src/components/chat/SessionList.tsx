import type { ChatSession } from "../../lib/types";

interface SessionListProps {
  sessions: ChatSession[];
  currentId: string | undefined;
  onSelect: (id: string) => void;
  onDelete: (id: string) => void;
}

export function SessionList({ sessions, currentId, onSelect, onDelete }: SessionListProps) {
  return (
    <div className="flex-1 overflow-y-auto">
      {sessions.length === 0 ? (
        <p className="px-4 py-8 text-center text-sm text-gray-400">
          No conversations yet
        </p>
      ) : (
        <ul className="space-y-1 px-2">
          {sessions.map((s) => (
            <li key={s.id}>
              <button
                onClick={() => onSelect(s.id)}
                className={`group flex w-full items-center justify-between rounded-lg px-3 py-2 text-left text-sm transition ${
                  s.id === currentId
                    ? "bg-primary-50 text-primary-700"
                    : "text-gray-600 hover:bg-gray-100"
                }`}
              >
                <span className="truncate">{s.title}</span>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    onDelete(s.id);
                  }}
                  className="hidden text-gray-400 hover:text-red-500 group-hover:block"
                >
                  ×
                </button>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
