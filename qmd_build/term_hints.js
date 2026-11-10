(() => {
	function initializeTermHints() {
		const templates = new Map(
			[...document.querySelectorAll("template[data-term-card]")].map((el) => [
				el.dataset.termCard,
				el,
			]),
		);
		const card = document.createElement("aside");
		card.id = "qmd-term-card";
		card.setAttribute("role", "dialog");
		card.setAttribute("aria-label", "Term definition");
		card.setAttribute("popover", "manual");
		card.hidden = true;
		document.body.append(card);
		let active = null;
		let pinned = false;
		let timer;
		let generation = 0;
		let restoringFocus = false;

		function dismiss() {
			const previous = active;
			hide();
			restoringFocus = true;
			previous?.focus({ preventScroll: true });
			restoringFocus = false;
		}

		function target(node) {
			const anchor = node instanceof Element ? node.closest("a[href]") : null;
			if (!anchor || card.contains(anchor)) return null;
			const href = anchor.getAttribute("href");
			return href?.startsWith("#term-") && templates.has(href.slice(1))
				? anchor
				: null;
		}

		// Closes the card once its link, having been visible, no longer is:
		// scrolled out of the page or of a scrolling box, or hidden by a
		// resize. A link still on its way into view (a smooth focus scroll)
		// has not been visible yet and keeps its card.
		let seen = false;
		const watcher = new IntersectionObserver((entries) => {
			const visible = entries.at(-1).isIntersecting;
			if (visible) seen = true;
			else if (seen) hide();
		});

		function hide() {
			clearTimeout(timer);
			watcher.disconnect();
			seen = false;
			generation += 1;
			active?.removeAttribute("aria-expanded");
			if (card.matches(":popover-open")) card.hidePopover();
			card.hidden = true;
			active = null;
			pinned = false;
		}

		function place() {
			if (!active) return;
			const box = active.getBoundingClientRect();
			const viewport = window.visualViewport;
			const left = viewport?.offsetLeft || 0;
			const top = viewport?.offsetTop || 0;
			const width = viewport?.width || innerWidth;
			const height = viewport?.height || innerHeight;
			card.style.maxWidth = `${Math.max(0, width - 24)}px`;
			card.style.maxHeight = `${Math.max(0, height - 24)}px`;
			const bounds = card.getBoundingClientRect();
			card.style.left = `${Math.max(left + 12, Math.min(box.left, left + width - bounds.width - 12))}px`;
			const below = box.bottom + 8;
			card.style.top = `${Math.max(top + 12, below + bounds.height < top + height - 12 ? below : box.top - bounds.height - 8)}px`;
		}

		async function show(anchor, pin = false) {
			clearTimeout(timer);
			if (active === anchor) {
				pinned ||= pin;
				return;
			}
			hide();
			const current = ++generation;
			active = anchor;
			pinned = pin;
			// Decided now, not at the observer's first report a frame later:
			// by then a quick scroll may already have taken the link away.
			const box = anchor.getBoundingClientRect();
			seen =
				box.bottom > 0 &&
				box.right > 0 &&
				box.top < innerHeight &&
				box.left < innerWidth;
			watcher.observe(anchor);
			const id = anchor.getAttribute("href").slice(1);
			const template = templates.get(id);
			const heading = document.createElement("header");
			const label = document.createElement("strong");
			label.textContent = template.dataset.termKind;
			const close = document.createElement("button");
			close.type = "button";
			close.textContent = "Close";
			close.addEventListener("click", dismiss);
			heading.append(label, close);
			const body = document.createElement("div");
			body.className = "term-card-body";
			body.append(template.content.cloneNode(true));
			// Preview copies never create duplicate document IDs or nested term hints.
			for (const el of body.querySelectorAll("[id]")) el.removeAttribute("id");
			const jump = document.createElement("a");
			jump.href = `#${id}`;
			jump.textContent =
				template.dataset.termKind === "First mention"
					? "Go to first mention"
					: "Go to definition";
			jump.addEventListener("click", hide);
			card.replaceChildren(heading, body, jump);
			card.hidden = false;
			card.showPopover?.();
			anchor.setAttribute("aria-expanded", "true");
			place();
			if (window.MathJax?.typesetPromise) {
				await window.MathJax.typesetPromise([body]);
				if (current === generation) place();
			}
		}

		function leave() {
			if (!pinned) timer = setTimeout(hide, 180);
		}
		document.addEventListener("pointerover", (event) => {
			const anchor = target(event.target);
			if (!anchor || event.buttons || event.pointerType === "touch" || pinned)
				return;
			clearTimeout(timer);
			timer = setTimeout(() => show(anchor), 240);
		});
		document.addEventListener("pointerout", (event) => {
			if (
				target(event.target) &&
				!target(event.target)?.contains(event.relatedTarget)
			)
				leave();
		});
		card.addEventListener("pointerenter", () => clearTimeout(timer));
		card.addEventListener("pointerleave", leave);
		document.addEventListener("focusin", (event) => {
			const anchor = target(event.target);
			if (anchor && !restoringFocus) show(anchor);
		});
		document.addEventListener("focusout", (event) => {
			if (!card.contains(event.relatedTarget) && !target(event.relatedTarget))
				leave();
		});
		document.addEventListener("click", (event) => {
			const anchor = target(event.target);
			if (
				anchor &&
				!event.metaKey &&
				!event.ctrlKey &&
				!event.shiftKey &&
				!event.altKey
			) {
				if (!window.getSelection()?.isCollapsed) return;
				event.preventDefault();
				show(anchor, true).then(() => {
					if (event.detail === 0) card.querySelector("button")?.focus();
				});
			} else if (!card.contains(event.target)) hide();
		});
		document.addEventListener("keydown", (event) => {
			if (event.key === "Escape") dismiss();
			if (event.key === " " && target(event.target)) {
				event.preventDefault();
				show(target(event.target), true);
			}
		});
		// Scrolling or resizing moves the link the card belongs to, so the card
		// is placed again; `watcher` closes it when the link goes out of view.
		window.addEventListener("resize", place);
		window.visualViewport?.addEventListener("resize", place);
		document.addEventListener(
			"scroll",
			(event) => {
				if (!card.contains(event.target)) place();
			},
			true,
		);
		window.addEventListener("beforeprint", hide);
	}
	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", initializeTermHints, {
			once: true,
		});
	} else initializeTermHints();
})();
