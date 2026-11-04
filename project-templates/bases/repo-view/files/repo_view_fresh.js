// Tells the reader when a served page no longer shows what is on disk: a
// built page older than its sources, or a page whose files changed since it
// loaded. Checks only when the reader comes back to the page (it becomes
// visible, gains focus, or the pointer enters it), never on a timer.
(() => {
	const start = () => {
		const meta = document.querySelector('meta[name="repo-fresh"]');
		if (!meta) return;
		const loaded = JSON.parse(meta.content);
		const style = document.createElement("style");
		style.textContent = `
#repo-fresh-notice { all: initial; position: fixed; top: 8px; right: 8px; z-index: 2147483645;
  display: flex; gap: 8px; align-items: center; max-width: min(560px, calc(100vw - 16px));
  padding: 6px 8px 6px 12px; box-sizing: border-box; border-radius: 6px;
  font: 13px/1.4 system-ui, sans-serif; color: #4a3500; background: #fff4d6;
  border: 1px solid #e0b84a; box-shadow: 0 4px 16px #0002; overflow-wrap: anywhere; }
#repo-fresh-notice > span { min-width: 0; }
#repo-fresh-notice code { font: 12px ui-monospace, monospace; }
#repo-fresh-notice button { all: unset; cursor: pointer; padding: 2px 8px; border-radius: 4px;
  font: inherit; font-weight: 600; white-space: nowrap; }
#repo-fresh-notice button:hover, #repo-fresh-notice button:focus-visible { background: #f3dfa4; }
@media (prefers-color-scheme: dark) {
  #repo-fresh-notice { color: #f4e3b5; background: #3b3220; border-color: #8a6d2a; }
  #repo-fresh-notice button:hover, #repo-fresh-notice button:focus-visible { background: #5a4a26; }
}`;
		document.head.append(style);
		const time = (ms) =>
			new Date(ms).toLocaleString([], {
				month: "short",
				day: "numeric",
				hour: "2-digit",
				minute: "2-digit",
			});
		let notice = null;
		let dismissed = "";
		// `action`: the notice's button, `{ label, run(button, text) }`, if any.
		const show = (key, parts, action) => {
			if (key === dismissed) return;
			notice?.remove();
			notice = document.createElement("div");
			notice.id = "repo-fresh-notice";
			notice.setAttribute("role", "status");
			const text = document.createElement("span");
			for (const part of parts) {
				if (typeof part === "string") text.append(part);
				else {
					const code = document.createElement("code");
					code.textContent = part.code;
					text.append(code);
				}
			}
			notice.append(text);
			if (action) {
				const button = document.createElement("button");
				button.type = "button";
				button.textContent = action.label;
				button.onclick = () => action.run(button, text);
				notice.append(button);
			}
			const close = document.createElement("button");
			close.type = "button";
			close.textContent = String.fromCharCode(0xd7); // multiplication sign; ASCII source
			close.setAttribute("aria-label", "Dismiss");
			close.style.fontSize = "18px";
			close.onclick = () => {
				dismissed = key;
				notice?.remove();
				notice = null;
			};
			notice.append(close);
			document.body.append(notice);
		};
		const reload = { label: "Reload", run: () => location.reload() };
		// Rebuilds while this page stays readable, then reloads into the new
		// build; the browser keeps the old page painted until the new one is.
		const rebuild = {
			label: "Rebuild",
			run: async (button, text) => {
				button.disabled = true;
				button.textContent = "Rebuilding...";
				let result;
				try {
					const url = new URL(location.href);
					url.hash = "";
					url.searchParams.set("repo-view", "rebuild");
					const response = await fetch(url, {
						method: "POST",
						headers: { "X-Repo-View": "rebuild" },
					});
					result = response.ok
						? await response.json()
						: { ok: false, log: await response.text() };
				} catch (error) {
					result = { ok: false, log: String(error) };
				}
				if (result.ok) {
					location.reload();
					return;
				}
				button.disabled = false;
				button.textContent = "Rebuild";
				text.textContent =
					"Rebuild failed; the page still shows the old build.";
				text.title = result.log;
				console.warn("repo-view rebuild failed:\n" + result.log);
			},
		};
		const staleParts = (stale) => [
			`Built ${time(stale.builtTime)}; `,
			{
				code:
					stale.project === "."
						? stale.input
						: stale.input.slice(stale.project.length + 1),
			},
			` changed ${time(stale.inputTime)}.`,
			...(stale.rebuild
				? []
				: [
						" Rebuild with ",
						{ code: stale.hint },
						" in ",
						{ code: stale.project },
						".",
					]),
		];
		const showStale = (key, stale) =>
			show(key, staleParts(stale), stale.rebuild ? rebuild : null);
		if (loaded.stale) showStale(`stale:${loaded.stamp}`, loaded.stale);
		let checking = false;
		let lastCheck = 0;
		const check = async () => {
			if (checking || Date.now() - lastCheck < 2000) return;
			checking = true;
			lastCheck = Date.now();
			try {
				const url = new URL(location.href);
				url.hash = "";
				url.searchParams.set("repo-view", "fresh");
				const response = await fetch(url, { cache: "no-store" });
				if (!response.ok) return;
				const now = await response.json();
				if (!now || now.stamp === loaded.stamp) return;
				// The stamp's first segment is the page's own file; when only a
				// build's inputs moved, reloading shows the same stale build.
				const pageChanged =
					now.stamp.split("/")[0] !== loaded.stamp.split("/")[0];
				if (pageChanged)
					show(
						`changed:${now.stamp}`,
						["This page changed on disk since it loaded."],
						reload,
					);
				else if (now.stale) showStale(`stale:${now.stamp}`, now.stale);
			} catch {
				// Offline or the server is restarting: the next return checks again.
			} finally {
				checking = false;
			}
		};
		document.addEventListener("visibilitychange", () => {
			if (document.visibilityState === "visible") void check();
		});
		addEventListener("focus", () => void check());
		document.documentElement.addEventListener(
			"pointerenter",
			() => void check(),
		);
	};
	if (document.readyState === "loading")
		document.addEventListener("DOMContentLoaded", start, { once: true });
	else start();
})();
