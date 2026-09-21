export interface Note {
  title: string;
  body: string;
  category: "make" | "explore";
}

export const notes: Note[] = [
  {
    title: "A small beginning",
    body: "Good things can start with a sketch, a question, or a few lines on a page.",
    category: "make",
  },
  {
    title: "Room to explore",
    body: "Follow a curiosity. Keep what you discover. Leave a little space for the unexpected.",
    category: "explore",
  },
  {
    title: "Made to share",
    body: "Turn your collection into a guide, a portfolio, or a story someone else can enjoy.",
    category: "make",
  },
];

export function filterNotes(
  items: readonly Note[],
  query: string,
  category: string,
): Note[] {
  const words = query.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
  return items.filter(
    (note) =>
      (category === "all" || category === note.category) &&
      words.every((word) =>
        `${note.title} ${note.body}`.toLocaleLowerCase().includes(word),
      ),
  );
}
