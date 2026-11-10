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
		// While a rebuild runs, its notice owns the corner; freshness checks
		// would replace it mid-build.
		let rebuilding = false;
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
		// One request to this page's server, given up after `ms` so that a
		// dropped answer can never leave the notice waiting.
		const ask = async (init, ms) => {
			const url = new URL(location.href);
			url.hash = "";
			url.searchParams.set("repo-view", "rebuild");
			const response = await fetch(url, {
				cache: "no-store",
				...init,
				signal: AbortSignal.timeout(ms),
			});
			if (!response.ok) throw new Error(await response.text());
			return response.json();
		};
		const pause = (ms) => new Promise((done) => setTimeout(done, ms));
		// Starts the build, then asks every second how it stands, showing the
		// time so far; reloads into the new build when it succeeds. The
		// browser keeps the old page painted until the new one is.
		const rebuild = {
			label: "Rebuild",
			run: async (button, text) => {
				button.disabled = true;
				rebuilding = true;
				const started = Date.now();
				const say = (message) => {
					text.textContent = message;
				};
				const progress = () =>
					say(`Rebuilding... ${Math.round((Date.now() - started) / 1000)} s`);
				const fail = (message, log) => {
					rebuilding = false;
					button.disabled = false;
					button.style.display = "";
					button.textContent = "Retry";
					say(message);
					text.title = log || "";
					if (log) console.warn(`repo-view rebuild: ${message}\n${log}`);
				};
				// The notice's text carries the progress; `all: unset` on the
				// button defeats the `hidden` attribute.
				button.style.display = "none";
				progress();
				let status;
				try {
					status = await ask(
						{ method: "POST", headers: { "X-Repo-View": "rebuild" } },
						15000,
					);
				} catch (error) {
					fail("Could not start the rebuild.", String(error));
					return;
				}
				// Consecutive unanswered status requests; the server may be
				// restarting, so a few are tolerated.
				let misses = 0;
				while (status.state === "running") {
					progress();
					await pause(1000);
					try {
						status = await ask({}, 5000);
						misses = 0;
					} catch (error) {
						if (++misses >= 15) {
							fail(
								"Lost contact with the server; reload to see whether the build finished.",
								String(error),
							);
							return;
						}
					}
				}
				if (status.state === "done" || status.state === "current") {
					say(
						status.state === "done"
							? `Rebuilt in ${Math.round(status.seconds)} s; reloading...`
							: "Already rebuilt; reloading...",
					);
					location.reload();
				} else if (status.state === "failed")
					fail(
						`Rebuild failed after ${Math.round(status.seconds)} s; the page still shows the old build.`,
						status.log,
					);
				else
					fail(
						"The server no longer knows this build (it may have restarted); reload to check.",
					);
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
			if (checking || rebuilding || Date.now() - lastCheck < 2000) return;
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
