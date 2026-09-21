import "./style.css";
import { notes, filterNotes } from "./notes";

const search = document.querySelector<HTMLInputElement>("#search")!;
const list = document.querySelector<HTMLDivElement>("#notes")!;
const count = document.querySelector<HTMLSpanElement>("#count")!;
const empty = document.querySelector<HTMLParagraphElement>("#empty")!;
const filters = document.querySelectorAll<HTMLButtonElement>("[data-category]");
let category = "all";

function render() {
  const visible = filterNotes(notes, search.value, category);
  list.replaceChildren(
    ...visible.map((note) => {
      const card = document.createElement("article");
      const number = document.createElement("span");
      number.className = "number";
      number.textContent = String(notes.indexOf(note) + 1).padStart(2, "0");
      const title = document.createElement("h3");
      title.textContent = note.title;
      const body = document.createElement("p");
      body.textContent = note.body;
      const label = document.createElement("span");
      label.className = "category";
      label.textContent = note.category;
      card.append(number, title, body, label);
      return card;
    }),
  );
  count.textContent = `${visible.length} ${visible.length === 1 ? "idea" : "ideas"}`;
  empty.hidden = visible.length !== 0;
}

search.addEventListener("input", render);
for (const button of filters) {
  button.addEventListener("click", () => {
    category = button.dataset.category!;
    for (const other of filters)
      other.setAttribute("aria-pressed", String(other === button));
    render();
  });
}
render();
