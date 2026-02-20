import { create } from "zustand";
import type { ChatMessage, ChatSession } from "../lib/types";
import { chatApi } from "../lib/api";

interface ChatState {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  messages: ChatMessage[];
  isLoading: boolean;
  isSending: boolean;
  fetchSessions: () => Promise<void>;
  createSession: (title?: string) => Promise<ChatSession>;
  selectSession: (id: string) => Promise<void>;
  sendMessage: (content: string) => Promise<void>;
  addMessage: (msg: ChatMessage) => void;
  deleteSession: (id: string) => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  currentSession: null,
  messages: [],
  isLoading: false,
  isSending: false,

  fetchSessions: async () => {
    set({ isLoading: true });
    try {
      const { data } = await chatApi.listSessions();
      set({ sessions: data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  createSession: async (title) => {
    const { data } = await chatApi.createSession(title);
    set((s) => ({ sessions: [data, ...s.sessions], currentSession: data, messages: [] }));
    return data;
  },

  selectSession: async (id) => {
    set({ isLoading: true });
    try {
      const [sessionRes, msgRes] = await Promise.all([
        chatApi.getSession(id),
        chatApi.getMessages(id),
      ]);
      set({
        currentSession: sessionRes.data,
        messages: msgRes.data.messages,
        isLoading: false,
      });
    } catch {
      set({ isLoading: false });
    }
  },

  sendMessage: async (content) => {
    const { currentSession } = get();
    if (!currentSession) return;

    // Optimistic user message
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      session_id: currentSession.id,
      role: "user",
      content,
      created_at: new Date().toISOString(),
    };
    set((s) => ({ messages: [...s.messages, tempUserMsg], isSending: true }));

    try {
      const { data } = await chatApi.sendMessage(currentSession.id, content);
      set((s) => ({
        messages: [
          ...s.messages.filter((m) => m.id !== tempUserMsg.id),
          { ...tempUserMsg, id: data.id },
          data,
        ],
        isSending: false,
      }));
    } catch {
      set({ isSending: false });
    }
  },

  addMessage: (msg) => {
    set((s) => ({ messages: [...s.messages, msg] }));
  },

  deleteSession: async (id) => {
    await chatApi.deleteSession(id);
    set((s) => ({
      sessions: s.sessions.filter((sess) => sess.id !== id),
      currentSession: s.currentSession?.id === id ? null : s.currentSession,
      messages: s.currentSession?.id === id ? [] : s.messages,
    }));
  },
}));
