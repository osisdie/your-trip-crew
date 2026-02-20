import { useState } from "react";
import { useT } from "../../i18n";

interface ChatInputProps {
  onSend: (content: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [value, setValue] = useState("");
  const t = useT();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!value.trim() || disabled) return;
    onSend(value.trim());
    setValue("");
  };

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4">
      <div className="flex items-end gap-2">
        <textarea
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
          placeholder={t("chat.placeholder")}
          rows={1}
          className="input flex-1 resize-none"
          disabled={disabled}
        />
        <button
          type="submit"
          disabled={disabled || !value.trim()}
          className="btn-primary"
        >
          {t("chat.send")}
        </button>
      </div>
      <p className="mt-1 text-[10px] text-gray-400">
        {t("chat.hint")}
      </p>
    </form>
  );
}
