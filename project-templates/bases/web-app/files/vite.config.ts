import { defineConfig } from "vite";

export default defineConfig(({ command }) => ({
  base: command === "serve" ? process.env.BASE_PATH || "/" : "./",
  build: { target: "es2022" },
  server: {
    host: "127.0.0.1",
    port: process.env.PORT ? Number(process.env.PORT) : 5173,
    strictPort: true,
    // YA supplies an unguessable base path and confines this process to its
    // sandbox loopback. The external app host is chosen by YA, not Vite.
    ...(process.env.BASE_PATH ? { allowedHosts: true, cors: true } : {}),
  },
}));
