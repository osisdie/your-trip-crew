import { WS_BASE_URL, STORAGE_KEYS } from "./constants";
import type { WsMessage } from "./types";

export function createChatWebSocket(
  sessionId: string,
  onMessage: (msg: WsMessage) => void,
  onClose?: () => void
): WebSocket {
  const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  const ws = new WebSocket(
    `${WS_BASE_URL}/api/v1/ws/chat/${sessionId}?token=${token}`
  );

  ws.onmessage = (event) => {
    const data: WsMessage = JSON.parse(event.data);
    onMessage(data);
  };

  ws.onclose = () => {
    onClose?.();
  };

  return ws;
}
