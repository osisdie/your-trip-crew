import type { ChatMessage } from "../../lib/types";

export function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";

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
        <div className="text-sm whitespace-pre-wrap">{message.content}</div>
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
