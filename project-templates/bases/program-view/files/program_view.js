(() => {
  const main = document.querySelector("[data-program-browser]");
  if (!main) return;
  const controls = document.getElementById("browser-controls");
  const toc = document.getElementById("program-toc");
  const tree = toc.querySelector(".tree");
  const host = main.querySelector(".program-tree");
  const search = controls.querySelector("[name=search]");
  const since = controls.querySelector("[name=since]");
  const range = controls.querySelector("[type=range]");
  const status = controls.querySelector("[role=status]");
  const kindButtons = controls.querySelector(".kind-controls");
  const programs = [...host.querySelectorAll("details.program")].map(
    (node) => ({
      node,
      id: node.id,
      name: node.dataset.name,
      path: node.dataset.repoDir,
      parent: node.parentElement.closest("details.program")?.id || "",
      time: Number(node.dataset.activity),
      groups: [...node.querySelectorAll(":scope > .lists > details.kind")].map(
        (group) => ({
          node: group,
          kind: group.dataset.kind,
          limit: Number(group.dataset.limit),
          rows: [...group.querySelectorAll("tr[data-path]")],
          body: group.querySelector(".kind-body"),
        }),
      ),
    }),
  );
  const byId = new Map(programs.map((p) => [p.id, p]));
  const children = new Map();
  for (const p of programs) {
    if (!children.has(p.parent)) children.set(p.parent, []);
    children.get(p.parent).push(p);
  }
  for (const p of [...programs].reverse()) {
    if (p.parent)
      byId.get(p.parent).time = Math.max(byId.get(p.parent).time, p.time);
  }
  for (const p of programs) {
    const when = p.node.querySelector(":scope > summary .when");
    if (when && p.time) {
      when.textContent = new Date(p.time).toISOString().slice(0, 10);
      when.title = "Latest activity, including child programs";
    }
    for (const link of p.node.querySelectorAll("[data-preview] a"))
      if (link.closest("[data-preview]").dataset.preview)
        link.removeAttribute("title");
  }
  let order = "newest",
    flat = false,
    query = "",
    cutoff = Date.now() - 7 * 864e5;
  let expandAll = false;
  let beforeSearch;
  const collapsedKinds = new Set();
  const kinds = [
    ...new Set(programs.flatMap((p) => p.groups.map((g) => g.kind))),
  ];
  const shortKind = {
    Papers: "Paper",
    "Field surveys": "Survey",
    Sketches: "Sketch",
    Handouts: "Handout",
    "Paper skeletons": "Draft",
    Documents: "Doc",
    Gaps: "Gap",
    Handoffs: "Handoff",
  };
  for (const kind of kinds) {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.kind = kind;
    button.textContent = shortKind[kind] || kind;
    button.setAttribute("aria-label", `Show ${kind.toLowerCase()} previews`);
    button.addEventListener("click", () => {
      collapsedKinds.has(kind)
        ? collapsedKinds.delete(kind)
        : collapsedKinds.add(kind);
      expandAll = false;
      render();
    });
    kindButtons.append(button);
  }
  const compare = (a, b) =>
    order === "alpha"
      ? a.name.localeCompare(b.name)
      : b.time - a.time || a.name.localeCompare(b.name);
  const rowInfo = (row) => ({
    name: row.dataset.name,
    time: Number(row.dataset.activity),
  });
  const match = (value) => value.toLocaleLowerCase().includes(query);
  const ancestors = (p) => {
    const result = [];
    while (p.parent) {
      p = byId.get(p.parent);
      result.unshift(p);
    }
    return result;
  };
  const disclosure = (label, className, open = false) => {
    const d = document.createElement("details");
    d.className = className;
    d.open = open;
    const s = document.createElement("summary");
    s.textContent = label;
    d.append(s);
    return d;
  };
  const table = (rows) => {
    const t = document.createElement("table");
    t.className = "files";
    t.innerHTML = '<colgroup><col><col class="d"></colgroup><tbody></tbody>';
    t.tBodies[0].append(...rows);
    return t;
  };
  function renderGroup(group, programMatch) {
    const rows = group.rows.filter(
      (r) =>
        !query ||
        programMatch ||
        match(
          `${r.dataset.name} ${r.dataset.title} ${r.dataset.path} ${group.kind}`,
        ),
    );
    rows.sort((a, b) => compare(rowInfo(a), rowInfo(b)));
    group.node.hidden = !!query && !rows.length;
    group.node.open = !!query || expandAll || !collapsedKinds.has(group.kind);
    const recent = rows.filter(
      (r) => query || Number(r.dataset.activity) >= cutoff,
    );
    const older = rows.filter(
      (r) => !query && Number(r.dataset.activity) < cutoff,
    );
    group.body.replaceChildren(
      table(query ? recent : recent.slice(0, group.limit)),
    );
    if (!query && recent.length > group.limit) {
      const more = disclosure(
        `${recent.length - group.limit} more`,
        "more",
        expandAll,
      );
      more.append(table(recent.slice(group.limit)));
      group.body.append(more);
    }
    if (older.length) {
      const more = disclosure(`${older.length} older`, "more", expandAll);
      more.append(table(older));
      group.body.append(more);
    }
    return rows.length;
  }
  function render() {
    if (query && !beforeSearch)
      beforeSearch = new Map(programs.map((p) => [p.id, p.node.open]));
    if (!query && beforeSearch) {
      for (const p of programs) p.node.open = beforeSearch.get(p.id);
      beforeSearch = undefined;
    }
    const visible = new Set();
    let fileCount = 0;
    for (const p of programs) {
      const ownMatch = match(
        `${p.name} ${p.path} ${ancestors(p)
          .map((a) => a.name)
          .join(" / ")}`,
      );
      const matchingRows = p.groups.reduce(
        (sum, g) => sum + renderGroup(g, ownMatch),
        0,
      );
      if (!query || ownMatch || matchingRows) visible.add(p.id);
      if (query) fileCount += matchingRows;
      p.node.querySelector(":scope > .breadcrumbs")?.remove();
      p.node.querySelector(":scope > .child-programs")?.remove();
      if (flat && p.parent) {
        const crumb = document.createElement("nav");
        crumb.className = "breadcrumbs";
        crumb.ariaLabel = "Parent programs";
        for (const a of ancestors(p)) {
          const link = document.createElement("a");
          link.href = `#${a.id}`;
          link.textContent = a.name;
          crumb.append(link, document.createTextNode(" / "));
        }
        crumb.append(document.createTextNode(p.name));
        p.node.querySelector("summary").after(crumb);
      }
      const lists = p.node.querySelector(":scope > .lists");
      const groups = [...p.groups].sort((a, b) =>
        compare(
          {
            name: a.kind,
            time: Math.max(0, ...a.rows.map((r) => Number(r.dataset.activity))),
          },
          {
            name: b.kind,
            time: Math.max(0, ...b.rows.map((r) => Number(r.dataset.activity))),
          },
        ),
      );
      if (lists) lists.append(...groups.map((g) => g.node));
    }
    if (!flat)
      for (const id of [...visible])
        for (const p of ancestors(byId.get(id))) visible.add(p.id);
    host.replaceChildren();
    tree.replaceChildren();
    function level(items, parent, nav) {
      const old = [],
        oldNav = [];
      for (const p of [...items].sort(compare)) {
        if (!visible.has(p.id)) continue;
        p.node.hidden = false;
        if (query || expandAll) p.node.open = true;
        const li = document.createElement("li"),
          a = document.createElement("a");
        a.href = `#${p.id}`;
        a.textContent = p.name;
        const date = document.createElement("span");
        date.className = "dim toc-date";
        date.textContent = p.time
          ? new Date(p.time).toISOString().slice(5, 10)
          : "undated";
        a.append(date);
        li.append(a);
        if (!flat && children.has(p.id)) {
          const nested = document.createElement("div");
          nested.className = "child-programs";
          const ul = document.createElement("ul");
          p.node.append(nested);
          li.append(ul);
          level(children.get(p.id), nested, ul);
        }
        if (!query && !expandAll && p.time < cutoff) {
          old.push(p.node);
          oldNav.push(li);
        } else {
          parent.append(p.node);
          nav.append(li);
        }
      }
      if (old.length) {
        const label = `${old.length} older program${old.length === 1 ? "" : "s"}`;
        const d = disclosure(label, "more older-programs");
        d.append(...old);
        parent.append(d);
        const li = document.createElement("li"),
          fold = disclosure(label, "more");
        const ul = document.createElement("ul");
        ul.append(...oldNav);
        fold.append(ul);
        li.append(fold);
        nav.append(li);
      }
    }
    level(flat ? programs : children.get("") || [], host, tree);
    if (!visible.size) host.textContent = "No matching programs or files.";
    status.textContent = query
      ? `${visible.size} programs · ${fileCount} files · Esc to clear`
      : "Includes collapsed items · / to search · Esc to clear";
    for (const b of kindButtons.children)
      b.setAttribute("aria-pressed", !collapsedKinds.has(b.dataset.kind));
    main.querySelector(".view-status").textContent =
      `${order === "newest" ? "Newest first" : "A–Z"} · ${flat ? "flat list" : "each level"} · ${query ? "search results" : expandAll ? "all items expanded" : "older items collapsed"}`;
  }
  function parseCutoff(value) {
    const duration = value.trim().match(/^(\d+(?:\.\d+)?)([hdw]?)$/i);
    if (duration)
      return (
        Date.now() -
        Number(duration[1]) *
          { h: 36e5, d: 864e5, w: 6048e5, "": 864e5 }[duration[2].toLowerCase()]
      );
    const parts = value.trim().match(/^(?:(\d{4})-)?(\d{2})-(\d{2})$/);
    if (!parts) return NaN;
    const iso = `${parts[1] || new Date().getUTCFullYear()}-${parts[2]}-${parts[3]}`;
    const date = new Date(iso + "T00:00:00Z");
    return Number.isFinite(+date) && date.toISOString().slice(0, 10) === iso
      ? +date
      : NaN;
  }
  function applyCutoff() {
    const next = parseCutoff(since.value);
    const feedback = controls.querySelector(".cutoff");
    const valid = Number.isFinite(next) && next <= Date.now();
    since.setAttribute("aria-invalid", !valid);
    feedback.classList.toggle("invalid", !valid);
    if (!valid) {
      feedback.textContent = "Enter a duration or a valid past date.";
      return;
    }
    cutoff = next;
    expandAll = false;
    range.value = Math.max(1, Math.min(90, (Date.now() - cutoff) / 864e5));
    feedback.textContent = `Since ${new Date(cutoff).toISOString().slice(0, 16).replace("T", " ")} UTC`;
    render();
  }
  since.addEventListener("change", applyCutoff);
  since.addEventListener("keydown", (e) => {
    if (e.key === "Enter") applyCutoff();
  });
  range.addEventListener("input", () => {
    since.value = range.value + "d";
    applyCutoff();
  });
  search.addEventListener("input", () => {
    query = search.value.trim().toLocaleLowerCase();
    render();
  });
  controls.addEventListener("change", (e) => {
    if (e.target.name === "grouping") {
      flat = e.target.value === "flat";
      render();
    }
  });
  controls.addEventListener("click", (e) => {
    const button = e.target.closest("button");
    if (!button) return;
    if (button.dataset.order) {
      order = button.dataset.order;
      for (const b of controls.querySelectorAll("[data-order]"))
        b.setAttribute("aria-pressed", b === button);
      render();
    }
    if (button.dataset.action === "expand") {
      expandAll = true;
      collapsedKinds.clear();
      render();
    }
    if (button.dataset.action === "recent") {
      expandAll = false;
      render();
    }
  });
  function reveal(id) {
    const p = byId.get(id);
    if (!p) return;
    if (!host.contains(p.node)) {
      query = "";
      search.value = "";
      render();
    }
    for (let node = p.node; node; node = node.parentElement)
      if (node.tagName === "DETAILS") node.open = true;
    p.node.scrollIntoView({ block: "start" });
  }
  document.addEventListener("click", (e) => {
    const subtree = e.target.closest("button[data-subtree]");
    if (subtree) {
      e.preventDefault();
      e.stopPropagation();
      const scope = subtree.closest(".program");
      const open = subtree.dataset.subtree === "open";
      for (const d of [scope, ...scope.querySelectorAll("details")])
        d.open = open;
      return;
    }
    const summary = e.target.closest("details.kind > summary");
    if (summary && !query) {
      e.preventDefault();
      const kind = summary.parentElement.dataset.kind;
      collapsedKinds.has(kind)
        ? collapsedKinds.delete(kind)
        : collapsedKinds.add(kind);
      expandAll = false;
      render();
      return;
    }
    const a = e.target.closest('a[href^="#program-"]');
    if (a && !e.ctrlKey && !e.metaKey && !e.shiftKey) {
      e.preventDefault();
      const id = a.hash.slice(1);
      history.replaceState(null, "", a.hash);
      reveal(id);
    }
  });
  document.addEventListener("keydown", (e) => {
    if (
      e.key === "/" &&
      !e.ctrlKey &&
      !e.metaKey &&
      !e.altKey &&
      !e.target.closest("input,textarea,[contenteditable]")
    ) {
      e.preventDefault();
      search.focus();
      search.select();
    }
    if (e.key === "Escape" && query) {
      query = "";
      search.value = "";
      render();
      search.focus();
    }
  });
  window.addEventListener("hashchange", () => reveal(location.hash.slice(1)));

  const preview = document.createElement("div");
  preview.className = "content-preview";
  preview.id = "content-preview";
  preview.role = "tooltip";
  preview.hidden = true;
  document.body.append(preview);
  let previewTimer, previewLink, hideTimer;
  function hidePreview() {
    clearTimeout(previewTimer);
    clearTimeout(hideTimer);
    preview.hidden = true;
    previewLink?.removeAttribute("aria-describedby");
    previewLink = undefined;
  }
  function showPreview(link) {
    hidePreview();
    const row = link.closest("[data-preview]");
    if (!row?.dataset.preview) return;
    previewTimer = setTimeout(() => {
      if (!link.isConnected) return;
      previewLink = link;
      const title = document.createElement("strong");
      title.textContent = link.textContent;
      const text = document.createElement("p");
      text.textContent = row.dataset.preview;
      preview.replaceChildren(title, text);
      preview.hidden = false;
      link.setAttribute("aria-describedby", preview.id);
      const rect = link.getBoundingClientRect(),
        tip = preview.getBoundingClientRect();
      preview.style.left =
        Math.max(8, Math.min(rect.left, innerWidth - tip.width - 8)) + "px";
      preview.style.top =
        Math.max(
          8,
          rect.bottom + tip.height + 12 < innerHeight
            ? rect.bottom + 8
            : rect.top - tip.height - 8,
        ) + "px";
    }, 250);
  }
  document.addEventListener("pointerover", (e) => {
    const a = e.target.closest("[data-preview] a");
    if (a && e.pointerType === "mouse") showPreview(a);
  });
  document.addEventListener("pointerout", (e) => {
    if (
      e.target.closest("[data-preview] a") &&
      !preview.contains(e.relatedTarget)
    )
      hideTimer = setTimeout(hidePreview, 180);
  });
  preview.addEventListener("pointerenter", () => clearTimeout(hideTimer));
  preview.addEventListener("pointerleave", hidePreview);
  document.addEventListener("focusin", (e) => {
    if (e.target.matches("[data-preview] a")) showPreview(e.target);
  });
  document.addEventListener("focusout", hidePreview);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") hidePreview();
  });
  document.addEventListener("scroll", hidePreview, true);
  window.addEventListener("resize", hidePreview);
  applyCutoff();
  window.addEventListener("pageshow", () => {
    requestAnimationFrame(() =>
      requestAnimationFrame(() => {
        if (location.hash) reveal(location.hash.slice(1));
        else if (matchMedia("(max-width:860px)").matches) toc.scrollIntoView();
      }),
    );
  });
})();
