import { useEffect, useRef, useState } from "react";
import { API_BASE_URL, STORAGE_KEYS } from "../lib/constants";

export interface TimelineEvent {
  step: string;
  crew: string | string[] | null;
  status: "active" | "done" | "error";
  slots: Record<string, unknown> | null;
  message: string;
  ts: number;
}

export interface FlowState {
  connected: boolean;
  activeCrews: Set<string>;
  doneCrews: Set<string>;
  errorCrews: Set<string>;
  slots: Record<string, unknown>;
  events: TimelineEvent[];
}

const INITIAL_STATE: FlowState = {
  connected: false,
  activeCrews: new Set(),
  doneCrews: new Set(),
  errorCrews: new Set(),
  slots: {},
  events: [],
};

/** Normalize the `crew` field (string | string[] | null) to a string array. */
function crewsOf(crew: string | string[] | null | undefined): string[] {
  if (!crew) return [];
  return Array.isArray(crew) ? crew : [crew];
}

/**
 * Subscribe to real-time agent flow events via SSE.
 *
 * Opens an EventSource to the backend's `/flow-events` SSE endpoint for the
 * given session.  Returns live state: which crews are active/done, the
 * accumulated slots, and a timestamped event timeline.
 */
export function useFlowEvents(sessionId: string | null): FlowState {
  const [state, setState] = useState<FlowState>(INITIAL_STATE);
  const esRef = useRef<EventSource | null>(null);

  useEffect(() => {
    // Reset state when session changes
    setState(INITIAL_STATE);

    if (!sessionId) return;

    const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
    if (!token) return;

    const url = `${API_BASE_URL}/api/v1/chat/sessions/${sessionId}/flow-events?token=${encodeURIComponent(token)}`;
    const es = new EventSource(url);
    esRef.current = es;

    es.onopen = () => {
      setState((prev) => ({ ...prev, connected: true }));
    };

    es.onmessage = (ev) => {
      try {
        const event: TimelineEvent = JSON.parse(ev.data);
        const crews = crewsOf(event.crew);

        setState((prev) => {
          const active = new Set(prev.activeCrews);
          const done = new Set(prev.doneCrews);
          const errored = new Set(prev.errorCrews);

          for (const c of crews) {
            if (event.status === "active") {
              active.add(c);
              done.delete(c);
              errored.delete(c);
            } else if (event.status === "done") {
              active.delete(c);
              done.add(c);
              errored.delete(c);
            } else if (event.status === "error") {
              active.delete(c);
              errored.add(c);
            }
          }

          return {
            ...prev,
            activeCrews: active,
            doneCrews: done,
            errorCrews: errored,
            slots: event.slots ? { ...prev.slots, ...event.slots } : prev.slots,
            events: [...prev.events, event],
          };
        });

        // Close on terminal events
        if (event.step === "complete" || event.step === "error") {
          es.close();
          setState((prev) => ({ ...prev, connected: false }));
        }
      } catch {
        // ignore non-JSON messages (keepalive comments)
      }
    };

    es.onerror = () => {
      // EventSource auto-reconnects on transient errors.
      // If it gives up (readyState === CLOSED), mark disconnected.
      if (es.readyState === EventSource.CLOSED) {
        setState((prev) => ({ ...prev, connected: false }));
      }
    };

    return () => {
      es.close();
      esRef.current = null;
    };
  }, [sessionId]);

  return state;
}
