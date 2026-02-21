import type { Config } from "tailwindcss";
import typography from "@tailwindcss/typography";

export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
          950: "#172554",
        },
        accent: {
          50: "#fff7ed",
          100: "#ffedd5",
          200: "#fed7aa",
          300: "#fdba74",
          400: "#fb923c",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
          800: "#9a3412",
          900: "#7c2d12",
        },
      },
      fontFamily: {
        sans: [
          "Inter",
          "system-ui",
          "-apple-system",
          "sans-serif",
        ],
      },
      typography: {
        sm: {
          css: {
            // Tighter spacing for chat bubbles
            h2: { marginTop: "0.75em", marginBottom: "0.25em" },
            h3: { marginTop: "0.5em", marginBottom: "0.25em" },
            p: { marginTop: "0.35em", marginBottom: "0.35em" },
            ul: { marginTop: "0.25em", marginBottom: "0.25em" },
            ol: { marginTop: "0.25em", marginBottom: "0.25em" },
            li: { marginTop: "0.1em", marginBottom: "0.1em" },
            // Table styling
            "thead th": {
              borderBottomWidth: "2px",
              backgroundColor: "var(--tw-prose-th-bg, #f9fafb)",
              padding: "0.5em 0.75em",
            },
            "tbody td": {
              borderBottomWidth: "1px",
              borderBottomColor: "#e5e7eb",
              padding: "0.5em 0.75em",
            },
            table: {
              borderCollapse: "collapse",
              width: "100%",
            },
            // Link color
            a: { color: "#1d4ed8" },
          },
        },
      },
    },
  },
  plugins: [typography],
} satisfies Config;
