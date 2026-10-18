import { all } from "./store.js";

export function searchByTitle(query) {
  const needle = (query || "").trim().toLowerCase();
  if (!needle) return all();
  return all().filter((item) => item.title.toLowerCase().includes(needle));
}
