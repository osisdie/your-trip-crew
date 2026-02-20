import { useEffect, useRef, useState } from "react";
import { useChatStore } from "../stores/chatStore";
import { LoadingSpinner } from "../components/common/LoadingSpinner";
import { MessageBubble } from "../components/chat/MessageBubble";
import { ChatInput } from "../components/chat/ChatInput";
import { SessionList } from "../components/chat/SessionList";
import { useT } from "../i18n";

export function ChatPage() {
  const {
    sessions,
    currentSession,
    messages,
    isSending,
    fetchSessions,
    createSession,
    selectSession,
    sendMessage,
    deleteSession,
  } = useChatStore();

  const t = useT();
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [showSidebar, setShowSidebar] = useState(true);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleNewChat = async () => {
    await createSession();
  };

  const handleSend = async (content: string) => {
    if (!currentSession) {
      await createSession("New Trip Plan");
      // After creating, send the message
    }
    await sendMessage(content);
  };

  const prompts = [
    t("chat.prompt1"),
    t("chat.prompt2"),
    t("chat.prompt3"),
    t("chat.prompt4"),
  ];

  return (
    <div className="flex h-[calc(100vh-4rem)]">
      {/* Sidebar */}
      {showSidebar && (
        <div className="w-72 flex-shrink-0 border-r border-gray-200 bg-gray-50">
          <div className="flex h-full flex-col">
            <div className="p-4">
              <button onClick={handleNewChat} className="btn-primary w-full">
                {t("chat.newChat")}
              </button>
            </div>
            <SessionList
              sessions={sessions}
              currentId={currentSession?.id}
              onSelect={selectSession}
              onDelete={deleteSession}
            />
          </div>
        </div>
      )}

      {/* Chat area */}
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <div className="flex items-center gap-3 border-b border-gray-200 px-4 py-3">
          <button
            onClick={() => setShowSidebar(!showSidebar)}
            className="text-gray-400 hover:text-gray-600"
          >
            ☰
          </button>
          <h2 className="font-medium text-gray-900">
            {currentSession?.title || t("chat.defaultTitle")}
          </h2>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4">
          {!currentSession ? (
            <div className="flex h-full items-center justify-center">
              <div className="text-center">
                <span className="text-5xl">✈️</span>
                <h3 className="mt-4 text-lg font-semibold text-gray-900">
                  {t("chat.emptyTitle")}
                </h3>
                <p className="mt-2 max-w-sm text-sm text-gray-500">
                  {t("chat.emptyDesc")}
                </p>
                <div className="mt-4 flex flex-wrap justify-center gap-2">
                  {prompts.map((prompt) => (
                    <button
                      key={prompt}
                      onClick={() => handleSend(prompt)}
                      className="rounded-full border border-gray-200 px-3 py-1.5 text-xs text-gray-600 transition hover:bg-gray-100"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex h-full items-center justify-center text-gray-400">
              {t("chat.startMsg")}
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((msg) => (
                <MessageBubble key={msg.id} message={msg} />
              ))}
              {isSending && (
                <div className="flex items-center gap-2 text-sm text-gray-400">
                  <LoadingSpinner size="sm" />
                  {t("chat.planning")}
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <ChatInput onSend={handleSend} disabled={isSending} />
      </div>
    </div>
  );
}
