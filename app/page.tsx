"use client";

import { useState } from "react";
import { createNote } from "../lib/api";

export default function Home() {
  const [msg, setMsg] = useState<string>("");

  async function onCreate() {
    setMsg("Creating...");
    try {
      const note = await createNote({ title: "Test", content: "From Next.js" });
      setMsg(`Created note: ${note.id}`);
    } catch (e: any) {
      setMsg(e.message || "Error");
    }
  }

  return (
    <main className="min-h-screen p-8">
      <h1 className="text-2xl font-bold">Insight Inbox</h1>

      <button
        onClick={onCreate}
        className="mt-6 rounded bg-black px-4 py-2 text-white"
      >
        Create test note
      </button>

      <p className="mt-4">{msg}</p>
    </main>
  );
}