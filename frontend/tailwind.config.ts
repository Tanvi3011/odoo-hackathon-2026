import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#1e293b",
          hover: "#0f172a",
          foreground: "#ffffff",
        },
        secondary: {
          DEFAULT: "#0d9488",
          hover: "#0f766e",
          foreground: "#ffffff",
        },
        success: "#10b981",
        danger: "#ef4444",
        warning: "#f59e0b",
        info: "#3b82f6",
        background: "#f8fafc",
        card: "#ffffff",
        border: "#e2e8f0",
        muted: "#f1f5f9",
        foreground: "#0f172a",
        "text-secondary": "#64748b",
        "text-muted": "#94a3b8",
      },
      borderRadius: {
        lg: "0.5rem",
        md: "0.375rem",
        sm: "0.25rem",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
