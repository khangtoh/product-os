const KEY = "pocketgarden.saved";

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || [];
  } catch (error) {
    return [];
  }
}

function persist(items) {
  localStorage.setItem(KEY, JSON.stringify(items));
}

export function save(url, title) {
  if (!url) throw new Error("A saved article needs a url");
  const items = load();
  items.push({ url, title: title || url, savedAt: new Date().toISOString() });
  persist(items);
  return items;
}

export function all() {
  return load();
}
