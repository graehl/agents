(() => {
	const start = () => {
		const rootMeta = document.querySelector('meta[name="repo-root"]');
		const pathMeta = document.querySelector('meta[name="repo-path"]');
		if (!rootMeta || !pathMeta) return;
		const root = new URL(rootMeta.content, location.href);
		const current = pathMeta.content;
		let parentOrigin = null;
		let menu = null;
		let returnFocus = null;
		let statusTimer;
		const status = document.createElement("div");
		status.id = "repo-path-status";
		status.setAttribute("role", "status");
		status.hidden = true;
		document.body.append(status);
		const announce = (text) => {
			clearTimeout(statusTimer);
			status.textContent = text;
			status.hidden = false;
			statusTimer = setTimeout(() => {
				status.hidden = true;
			}, 4500);
		};
		const copy = async (text) => {
			try {
				await navigator.clipboard.writeText(text);
				announce(`Copied: ${text}`);
				return;
			} catch {
				// Cross-origin app frames need a selection-based copy when the
				// containing page has not delegated async clipboard permission.
			}
			const selection = getSelection();
			const ranges = Array.from({ length: selection.rangeCount }, (_, index) =>
				selection.getRangeAt(index).cloneRange(),
			);
			const focused = document.activeElement;
			const input = document.createElement("textarea");
			input.value = text;
			input.readOnly = true;
			input.style.cssText = "position:fixed;opacity:0;pointer-events:none";
			document.body.append(input);
			let copied = false;
			try {
				input.select();
				copied = document.execCommand("copy");
			} finally {
				input.remove();
				focused?.focus({ preventScroll: true });
				selection.removeAllRanges();
				for (const range of ranges) selection.addRange(range);
			}
			if (copied) {
				announce(`Copied: ${text}`);
				return;
			}
			announce("Clipboard unavailable. Select and copy: ");
			const value = document.createElement("span");
			value.textContent = text;
			status.append(value);
			const range = document.createRange();
			range.selectNodeContents(value);
			selection.removeAllRanges();
			selection.addRange(range);
		};
		const close = (focus = false) => {
			menu?.remove();
			menu = null;
			if (focus) returnFocus?.focus({ preventScroll: true });
		};
		const pathFor = (element) => {
			const named = element.closest("[data-repo-path], [data-repo-source]");
			if (named) return named.dataset.repoPath ?? named.dataset.repoSource;
			const link = element.closest("a[href]");
			if (!link) return null;
			const url = new URL(link.href);
			if (url.origin !== root.origin || !url.pathname.startsWith(root.pathname))
				return null;
			if (link.getAttribute("href").startsWith("#")) return current;
			try {
				return (
					decodeURIComponent(url.pathname.slice(root.pathname.length)) || "."
				);
			} catch {
				return null;
			}
		};
		const comment = (path, quote) => {
			if (!parentOrigin) return;
			window.parent.postMessage(
				{ type: "yep-anywhere:app-comment", path, ...(quote ? { quote } : {}) },
				parentOrigin,
			);
		};
		const show = (element, x, y, forcedPath) => {
			const code = element.closest("code:not(pre code)");
			const path = forcedPath ?? pathFor(element);
			const quote = getSelection()?.toString() || "";
			if (!code && !path && !quote) return false;
			close();
			returnFocus = element;
			menu = document.createElement("div");
			menu.id = "repo-path-menu";
			menu.setAttribute("role", "menu");
			menu.setAttribute("aria-label", path ? "Path actions" : "Text actions");
			const heading = document.createElement("div");
			heading.className = "repo-menu-heading";
			heading.textContent = path || code?.textContent || current;
			menu.append(heading);
			const action = (label, run) => {
				const button = document.createElement("button");
				button.type = "button";
				button.setAttribute("role", "menuitem");
				button.textContent = label;
				button.onclick = () => {
					close();
					run();
				};
				menu.append(button);
			};
			if (path)
				action("Copy project path", () => {
					void copy(path);
				});
			else if (code)
				action("Copy text", () => {
					void copy(code.textContent);
				});
			if (quote)
				action("Copy selected text", () => {
					void copy(quote);
				});
			if (parentOrigin) {
				if (path) action("Comment on path", () => comment(path));
				if (quote)
					action("Comment on selection", () => comment(current, quote));
			}
			if (element.closest("[data-repo-actions]")) {
				// The breadcrumb row's menu acts on the page itself. Its address keeps
				// a private link's token, which is what lets the copy open this view.
				action("Copy link to this page", () => {
					void copy(location.href);
				});
				if (window.parent !== window)
					action("Open page in new tab", () =>
						window.open(location.href, "_blank", "noopener"),
					);
				action("Reload page", () => location.reload());
			}
			const link = element.closest("a[href]");
			if (link) {
				action("Copy link address", () => {
					void copy(link.href);
				});
				action("Open link in new tab", () =>
					window.open(link.href, "_blank", "noopener"),
				);
			}
			const hint = document.createElement("p");
			hint.className = "repo-menu-hint";
			hint.textContent = "Shift + right-click for browser menu";
			menu.append(hint);
			document.body.append(menu);
			menu.style.left = `${Math.max(8, Math.min(x, innerWidth - menu.offsetWidth - 8))}px`;
			menu.style.top = `${Math.max(8, Math.min(y, innerHeight - menu.offsetHeight - 8))}px`;
			menu.querySelector("button")?.focus({ preventScroll: true });
			return true;
		};
		document.addEventListener("dblclick", (event) => {
			const code = event.target.closest("code");
			if (!code || code.closest("pre, [contenteditable=true]")) return;
			const range = document.createRange();
			range.selectNodeContents(code);
			getSelection().removeAllRanges();
			getSelection().addRange(range);
			event.preventDefault();
		});
		document.addEventListener("contextmenu", (event) => {
			if (
				event.shiftKey ||
				event.target.closest("input, textarea, [contenteditable=true]")
			)
				return;
			if (show(event.target, event.clientX, event.clientY))
				event.preventDefault();
		});
		document.addEventListener("pointerdown", (event) => {
			if (menu && !menu.contains(event.target)) close();
		});
		document.addEventListener("click", (event) => {
			const copyButton = event.target.closest("[data-repo-copy]");
			if (copyButton) {
				void copy(copyButton.dataset.repoCopy);
				return;
			}
			const actions = event.target.closest("[data-repo-actions]");
			if (!actions) return;
			const rect = actions.getBoundingClientRect();
			show(
				actions,
				rect.right - 300,
				rect.bottom + 4,
				actions.dataset.repoActions,
			);
		});
		document.addEventListener("keydown", (event) => {
			if (event.key === "Escape") {
				close(true);
				return;
			}
			if (
				!menu &&
				(event.key === "ContextMenu" || (event.shiftKey && event.key === "F10"))
			) {
				const rect = event.target.getBoundingClientRect();
				if (show(event.target, rect.left, rect.bottom)) event.preventDefault();
				return;
			}
			if (
				!menu ||
				!["ArrowDown", "ArrowUp", "Home", "End", "Tab"].includes(event.key)
			)
				return;
			if (event.key === "Tab") {
				close();
				return;
			}
			event.preventDefault();
			const buttons = [...menu.querySelectorAll("button")];
			const index = buttons.indexOf(document.activeElement);
			const next =
				event.key === "Home"
					? 0
					: event.key === "End"
						? buttons.length - 1
						: (index + (event.key === "ArrowUp" ? -1 : 1) + buttons.length) %
							buttons.length;
			buttons[next].focus();
		});
		addEventListener("message", (event) => {
			if (
				window.parent === window ||
				event.source !== window.parent ||
				event.origin === "null" ||
				event.data?.type !== "yep-anywhere:app-comment-ready"
			)
				return;
			parentOrigin = event.data.enabled === true ? event.origin : null;
		});
		dispatchEvent(new Event("repo-view-path-ready"));
	};
	if (document.readyState === "loading")
		document.addEventListener("DOMContentLoaded", start, { once: true });
	else start();
})();
