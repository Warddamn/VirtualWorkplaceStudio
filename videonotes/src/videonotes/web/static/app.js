/* videonotes web UI. Plain JavaScript, no build step, no network use beyond this server.
 *
 * Everything that comes from the library (titles, transcripts, text read off frames,
 * captions) is untrusted and is only ever inserted as text nodes: there is no innerHTML
 * anywhere in this file. */
(() => {
  "use strict";

  // ------------------------------------------------------------------ DOM helpers

  /** Create an element. Strings among the children become text nodes, never markup. */
  function el(tag, props, ...kids) {
    const node = document.createElement(tag);
    if (props) {
      for (const [key, value] of Object.entries(props)) {
        if (value === null || value === undefined || value === false) continue;
        if (key === "class") node.className = value;
        else if (key === "text") node.textContent = value;
        else if (key === "dataset") Object.assign(node.dataset, value);
        else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
        else node.setAttribute(key, value === true ? "" : String(value));
      }
    }
    add(node, kids);
    return node;
  }

  function add(node, kids) {
    for (const kid of kids.flat(Infinity)) {
      if (kid === null || kid === undefined || kid === false) continue;
      node.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
    }
    return node;
  }

  const code = (text) => el("code", { text });
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;

  /** Text with blank-line separated paragraphs as <p> elements. */
  function paragraphs(text, className) {
    return String(text || "")
      .split(/\n\s*\n/)
      .map((block) => block.trim())
      .filter(Boolean)
      .map((block) => el("p", { class: className, text: block }));
  }

  // Only ever point <img> / <video> at this server's own file routes.
  const frameSrc = (url) => (typeof url === "string" && url.startsWith("/frames/") ? url : null);
  const mediaSrc = (url) => (typeof url === "string" && /^\/media\/\d+$/.test(url) ? url : null);

  // ------------------------------------------------------------------ labels

  const MOMENT_KIND = {
    conversation: "Conversation",
    meeting: "Meeting",
    solo_work: "Solo work",
    errand: "Errand",
    transit: "On the move",
    media: "Media playing",
    idle: "Idle",
  };
  const HIT_KIND = { utterance: "Said", ocr: "Text in view", caption: "Seen", moment: "Moment", session: "Note" };
  const SOURCE_KIND = {
    import: "Imported from the camera",
    live: "Recorded live over USB",
    wireless: "Recorded live over Wi-Fi",
    file: "Added from a file",
  };
  const STATUS = { open: "Recording", processing: "Processing", error: "Needs attention" };

  // ------------------------------------------------------------------ routes

  const routes = {
    home: () => "#/",
    day: (date) => "#/day/" + encodeURIComponent(date),
    session(id, focus) {
      const params = new URLSearchParams();
      for (const key of ["m", "kf", "u"]) {
        if (focus && focus[key] !== null && focus[key] !== undefined) params.set(key, String(focus[key]));
      }
      const query = params.toString();
      return "#/session/" + encodeURIComponent(id) + (query ? "?" + query : "");
    },
    search(q, opts) {
      const params = new URLSearchParams();
      if (q) params.set("q", q);
      if (opts && opts.kind) params.set("kind", opts.kind);
      if (opts && opts.day) params.set("day", opts.day);
      return "#/search?" + params.toString();
    },
    ask(q) {
      return "#/ask" + (q ? "?" + new URLSearchParams({ q }).toString() : "");
    },
  };

  function parseRoute() {
    const raw = location.hash.startsWith("#/") ? location.hash.slice(1) : "/";
    const cut = raw.indexOf("?");
    const path = cut >= 0 ? raw.slice(0, cut) : raw;
    const params = new URLSearchParams(cut >= 0 ? raw.slice(cut + 1) : "");
    let parts;
    try {
      parts = path.split("/").filter(Boolean).map(decodeURIComponent);
    } catch (err) {
      return { name: "notfound" };
    }
    if (parts.length === 0) return { name: "home" };
    if (parts[0] === "day" && parts.length === 2) return { name: "day", date: parts[1] };
    if (parts[0] === "session" && parts.length === 2) {
      return { name: "session", id: parts[1], m: params.get("m"), kf: params.get("kf"), u: params.get("u") };
    }
    if (parts[0] === "search" && parts.length === 1) {
      return {
        name: "search",
        q: (params.get("q") || "").trim(),
        kind: params.get("kind") || "",
        day: params.get("day") || "",
      };
    }
    if (parts[0] === "ask" && parts.length === 1) return { name: "ask", q: (params.get("q") || "").trim() };
    return { name: "notfound" };
  }

  // ------------------------------------------------------------------ server API

  class ApiError extends Error {
    constructor(code, message, status) {
      super(message);
      this.code = code;
      this.status = status || 0;
    }
  }

  async function api(path, options) {
    let response;
    try {
      response = await fetch(path, { headers: { Accept: "application/json" }, cache: "no-store", ...options });
    } catch (err) {
      throw new ApiError("offline", "Can't reach videonotes. Is “vnote web” still running in Terminal?");
    }
    let data = null;
    try {
      data = await response.json();
    } catch (err) {
      data = null;
    }
    if (!response.ok) {
      const info = (data && data.error) || {};
      throw new ApiError(
        info.code || "http_" + response.status,
        info.message || `videonotes answered with an error (${response.status}).`,
        response.status
      );
    }
    if (data === null) throw new ApiError("bad_reply", "videonotes sent a reply this page could not read.");
    return data;
  }

  // ------------------------------------------------------------------ state

  const state = {
    overview: null,
    overviewAt: 0,
    overviewLoading: null,
    sessionsByDay: new Map(), // date -> { sessions, at } (sidebar cache)
    expanded: new Set(), // dates whose sessions are shown in the sidebar
    current: { day: null, session: null },
    ticket: 0, // increases with every navigation; late answers of older ones are dropped
    session: null, // data of the session on screen (for the lightbox and player)
    ask: { question: "", pending: false, result: null, error: null },
    pollTimer: null,
  };

  const view = document.getElementById("view");
  const main = document.getElementById("main");
  const dayList = document.getElementById("day-list");
  const libraryStats = document.getElementById("library-stats");
  const announcer = document.getElementById("announcer");
  const searchInput = document.getElementById("search-input");

  function announce(text) {
    announcer.textContent = "";
    window.setTimeout(() => {
      announcer.textContent = text;
    }, 50);
  }

  // ------------------------------------------------------------------ small components

  function chip(text, className) {
    return el("span", { class: "chip" + (className ? " " + className : ""), text });
  }

  function notice(className, ...kids) {
    return el("p", { class: "notice" + (className ? " " + className : "") }, ...kids);
  }

  /** A fixed 16:9 box holding a lazily loaded keyframe (or a placeholder when there is none). */
  function thumb(image) {
    const box = el("span", { class: "thumb" });
    const src = image ? frameSrc(image.url) : null;
    if (!src) {
      box.classList.add("empty");
      return box;
    }
    const img = el("img", {
      src,
      alt: image.alt || "Keyframe",
      loading: "lazy",
      decoding: "async",
      width: 320,
      height: 180,
    });
    img.addEventListener("error", () => {
      img.remove();
      box.classList.add("empty");
    });
    box.append(img);
    return box;
  }

  function section(title, body, className) {
    if (!body) return null;
    return el("section", { class: "block" + (className ? " " + className : "") }, el("h2", { text: title }), body);
  }

  function bulletList(items) {
    if (!items || items.length === 0) return null;
    return el("ul", { class: "bullets" }, items.map((item) => el("li", { text: item })));
  }

  /** Action items with a checkbox look. Read-only: the boxes are decoration, not controls. */
  function checklist(items) {
    if (!items || items.length === 0) return null;
    return el(
      "ul",
      { class: "checklist" },
      items.map((item) => {
        const details = [item.owner, item.due ? "due " + item.due : "", item.time ? item.time.clock : ""].filter(Boolean);
        return el(
          "li",
          null,
          el("span", { class: "box", "aria-hidden": "true" }),
          el(
            "span",
            { class: "check-text" },
            el("span", { class: "visually-hidden", text: "To do: " }),
            item.text,
            details.length ? el("span", { class: "check-meta", text: details.join(" · ") }) : null
          )
        );
      })
    );
  }

  function chipRow(label, values) {
    if (!values || values.length === 0) return null;
    return el("p", { class: "chip-row" }, el("span", { class: "chip-label", text: label }), values.map((v) => chip(v)));
  }

  /** "14:32–15:10", or with seconds when both ends fall in the same minute. */
  function timeRange(start, end) {
    if (!start) return "";
    if (!end || end.ts <= start.ts) return start.clock;
    return end.clock !== start.clock ? `${start.clock}–${end.clock}` : `${start.precise}–${end.precise}`;
  }

  function sessionTimes(s) {
    const bits = [];
    if (s.start) bits.push(s.end && s.end.clock !== s.start.clock ? `${s.start.clock}–${s.end.clock}` : s.start.clock);
    if (s.duration) bits.push(s.duration);
    return bits.join(" · ");
  }

  function statusChip(s) {
    return STATUS[s.status] ? chip(STATUS[s.status], "status-" + s.status) : null;
  }

  function sessionCard(s) {
    return el(
      "li",
      null,
      el(
        "a",
        { class: "card", href: routes.session(s.id) },
        thumb(s.thumbnail),
        el(
          "span",
          { class: "card-body" },
          el("span", { class: "card-title" + (s.untitled ? " untitled" : ""), text: s.title }),
          el("span", { class: "card-meta" }, sessionTimes(s), statusChip(s) ? " " : null, statusChip(s)),
          s.summary
            ? el("span", { class: "card-summary", text: s.summary })
            : el("span", {
                class: "card-summary muted",
                text: s.has_note ? "" : "Not summarised yet.",
              })
        )
      )
    );
  }

  // ------------------------------------------------------------------ sidebar

  function loadOverview(force) {
    if (!force && state.overview && Date.now() - state.overviewAt < 15000) return Promise.resolve(state.overview);
    if (!state.overviewLoading) {
      // one request at a time, shared by everything that asks while it is under way
      state.overviewLoading = (async () => {
        try {
          state.overview = await api("/api/overview");
          state.overviewAt = Date.now();
          if (state.expanded.size === 0 && state.overview.days.length) state.expanded.add(state.overview.days[0].date);
          renderSidebar();
          return state.overview;
        } finally {
          state.overviewLoading = null;
        }
      })();
    }
    return state.overviewLoading;
  }

  function renderSidebar() {
    const overview = state.overview;
    const days = overview ? overview.days : [];
    if (days.length === 0) {
      dayList.replaceChildren(el("p", { class: "side-note", text: "No recordings yet." }));
      libraryStats.textContent = "";
      return;
    }
    const parts = [];
    let month = null;
    let list = null;
    for (const day of days) {
      if (day.month !== month) {
        month = day.month;
        list = el("ul", { class: "days" });
        parts.push(el("h2", { class: "month", text: month }), list);
      }
      list.append(dayItem(day));
    }
    dayList.replaceChildren(...parts);
    const lib = overview.library || {};
    libraryStats.textContent = `${plural(lib.sessions || 0, "session")} · ${lib.media_duration || "0 s"} of footage`;
    markCurrent();
  }

  function dayItem(day) {
    const open = state.expanded.has(day.date);
    const listId = "side-" + day.date;
    const sessions = el("ul", { class: "side-sessions", id: listId, hidden: !open });
    const twisty = el(
      "button",
      {
        type: "button",
        class: "twisty",
        "aria-expanded": String(open),
        "aria-controls": listId,
        "aria-label": "Sessions on " + day.label,
        onclick: () => toggleDay(day.date),
      },
      el("span", { class: "chevron", "aria-hidden": "true" })
    );
    const link = el(
      "a",
      { class: "day-link", href: routes.day(day.date), dataset: { day: day.date } },
      el("span", { class: "day-name", text: day.relative || day.short }),
      day.relative ? el("span", { class: "day-sub", text: day.short }) : null,
      el("span", { class: "count", text: String(day.sessions), title: plural(day.sessions, "session") })
    );
    if (open) fillDaySessions(day.date, sessions);
    return el("li", { class: "day", dataset: { day: day.date } }, el("div", { class: "day-row" }, twisty, link), sessions);
  }

  function toggleDay(date, forceOpen) {
    const open = forceOpen === undefined ? !state.expanded.has(date) : forceOpen;
    if (open) state.expanded.add(date);
    else state.expanded.delete(date);
    const item = dayList.querySelector(`li.day[data-day="${CSS.escape(date)}"]`);
    if (!item) return;
    const list = item.querySelector(".side-sessions");
    item.querySelector(".twisty").setAttribute("aria-expanded", String(open));
    list.hidden = !open;
    if (open && list.childElementCount === 0) fillDaySessions(date, list);
  }

  async function fillDaySessions(date, list) {
    const cached = state.sessionsByDay.get(date);
    if (cached) renderDaySessions(list, cached.sessions); // show what we have at once, then refresh quietly
    else list.replaceChildren(el("li", { class: "side-note", text: "Loading…" }));
    if (cached && cached.at >= state.overviewAt) return;
    let sessions;
    try {
      sessions = (await api("/api/sessions?day=" + encodeURIComponent(date))).sessions;
    } catch (err) {
      if (!cached) list.replaceChildren(el("li", { class: "side-note", text: "Could not load these sessions." }));
      return;
    }
    state.sessionsByDay.set(date, { sessions, at: Date.now() });
    renderDaySessions(list, sessions);
  }

  function renderDaySessions(list, sessions) {
    if (sessions.length === 0) {
      list.replaceChildren(el("li", { class: "side-note", text: "Nothing recorded." }));
      return;
    }
    list.replaceChildren(
      ...sessions.map((s) =>
        el(
          "li",
          null,
          el(
            "a",
            { class: "side-session", href: routes.session(s.id), dataset: { session: s.id } },
            el("span", { class: "side-time", text: s.start ? s.start.clock : "" }),
            el("span", { class: "side-title" + (s.untitled ? " untitled" : ""), text: s.title }),
            STATUS[s.status] ? el("span", { class: "dot status-" + s.status, title: STATUS[s.status] }) : null
          )
        )
      )
    );
    markCurrent();
  }

  function markCurrent() {
    for (const link of dayList.querySelectorAll("a[aria-current]")) link.removeAttribute("aria-current");
    const { day, session } = state.current;
    if (session) {
      const link = dayList.querySelector(`a[data-session="${CSS.escape(session)}"]`);
      if (link) link.setAttribute("aria-current", "page");
    } else if (day) {
      const link = dayList.querySelector(`a.day-link[data-day="${CSS.escape(day)}"]`);
      if (link) link.setAttribute("aria-current", "page");
    }
  }

  function setCurrent(day, session) {
    state.current = { day: day || null, session: session || null };
    if (day && !state.expanded.has(day)) toggleDay(day, true);
    markCurrent();
  }

  // ------------------------------------------------------------------ navigation drawer (narrow screens)

  const navToggle = document.getElementById("nav-toggle");
  const scrim = document.getElementById("scrim");

  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    navToggle.setAttribute("aria-expanded", String(open));
    scrim.hidden = !open;
    if (open) {
      const first = dayList.querySelector("a, button");
      if (first) first.focus();
    }
  }

  navToggle.addEventListener("click", () => setNav(!document.body.classList.contains("nav-open")));
  scrim.addEventListener("click", () => setNav(false));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && document.body.classList.contains("nav-open")) {
      setNav(false);
      navToggle.focus();
    }
  });

  // ------------------------------------------------------------------ views: home and day

  function emptyLibraryView() {
    return el(
      "article",
      { class: "page empty-state" },
      el("h1", { tabindex: "-1", text: "No sessions yet" }),
      el("p", {
        class: "lead",
        text: "videonotes turns footage from your camera into notes you can read and search here. Nothing has been recorded or imported so far.",
      }),
      el("p", { text: "In Terminal, run one of these:" }),
      el(
        "ul",
        { class: "commands" },
        el("li", null, code("vnote demo --keep"), el("span", { text: "try it now with a generated sample clip" })),
        el("li", null, code("vnote import"), el("span", { text: "bring in recordings from the camera or its SD card" })),
        el("li", null, code("vnote live"), el("span", { text: "take notes live with the camera plugged in over USB" }))
      ),
      el(
        "p",
        null,
        el("button", { type: "button", class: "btn", text: "Check again", onclick: () => navigate(true) }),
        el("span", { class: "muted", text: "  New sessions show up here as soon as they are processed." })
      )
    );
  }

  async function homeView() {
    const overview = await loadOverview(true);
    if (overview.days.length === 0) {
      setCurrent(null, null);
      return { title: "", node: emptyLibraryView() };
    }
    location.replace(routes.day(overview.days[0].date));
    return null;
  }

  function dayPager(date) {
    const days = state.overview ? state.overview.days : [];
    const at = days.findIndex((d) => d.date === date);
    if (at < 0) return null;
    const newer = days[at - 1];
    const older = days[at + 1];
    if (!newer && !older) return null;
    return el(
      "nav",
      { class: "pager", "aria-label": "Other days" },
      older ? el("a", { class: "pager-older", href: routes.day(older.date), text: "← " + older.short }) : el("span"),
      newer ? el("a", { class: "pager-newer", href: routes.day(newer.date), text: newer.short + " →" }) : el("span")
    );
  }

  function provenance(backend, what) {
    if (!backend) return null;
    const text =
      backend === "extractive"
        ? `${what} built from excerpts only, without a language model.`
        : `${what} written by ${backend} from what was captured.`;
    return el("p", { class: "fineprint", text });
  }

  async function dayView(route) {
    const [data] = await Promise.all([api("/api/day/" + encodeURIComponent(route.date)), loadOverview(false)]);
    setCurrent(data.day.date, null);
    const total = data.sessions.reduce((sum, s) => sum + (s.duration_s || 0), 0);
    const page = el("article", { class: "page" });
    page.append(
      el(
        "header",
        { class: "page-head" },
        data.day.relative ? el("p", { class: "eyebrow", text: data.day.relative }) : null,
        el("h1", { tabindex: "-1", text: data.day.label }),
        data.sessions.length
          ? el("p", {
              class: "meta",
              text: `${plural(data.sessions.length, "session")} · ${formatDuration(total)} recorded`,
            })
          : null
      )
    );
    if (data.sessions.length === 0) {
      page.append(
        notice(
          "",
          "Nothing was recorded on this day. ",
          state.overview && state.overview.days.length
            ? el("a", { href: routes.day(state.overview.days[0].date), text: "Go to the latest day" })
            : null
        )
      );
      return { title: data.day.label, node: page };
    }
    const digest = data.digest;
    if (digest && (digest.headline || digest.summary || digest.highlights.length || digest.action_items.length)) {
      page.append(
        el(
          "section",
          { class: "digest" },
          digest.headline ? el("p", { class: "lead", text: digest.headline }) : null,
          paragraphs(digest.summary),
          section("Highlights", bulletList(digest.highlights)),
          section("Action items", checklist(digest.action_items)),
          provenance(digest.llm_backend, "Day summary")
        )
      );
    } else {
      page.append(
        notice(
          "quiet",
          "No summary of this day yet. Run ",
          code("vnote day " + data.day.date),
          " in Terminal to write one."
        )
      );
    }
    page.append(
      el("section", { class: "block" }, el("h2", { text: "Sessions" }), el("ul", { class: "cards" }, data.sessions.map(sessionCard)))
    );
    add(page, [dayPager(data.day.date)]);
    return { title: data.day.label, node: page };
  }

  function formatDuration(seconds) {
    const s = Math.max(0, Math.round(seconds));
    if (s < 90) return `${s} s`;
    const m = Math.round(s / 60);
    if (m < 60) return `${m} min`;
    return `${Math.floor(m / 60)} h ${String(m % 60).padStart(2, "0")} min`;
  }

  // ------------------------------------------------------------------ view: session

  /** Up to `limit` items spread evenly over the list (always including the first). */
  function spread(items, limit) {
    if (items.length <= limit) return new Set(items);
    const chosen = new Set();
    for (let i = 0; i < limit; i += 1) chosen.add(items[Math.round((i * (items.length - 1)) / (limit - 1))]);
    return chosen;
  }

  function framesBlock(frames, context) {
    if (!frames || frames.length === 0) return null;
    const first = spread(frames, 6);
    const list = el("ul", { class: "frames" });
    frames.forEach((frame, index) => {
      const button = el(
        "button",
        {
          type: "button",
          class: "frame",
          dataset: { kf: frame.id },
          onclick: () => openLightbox(frames, index, context),
        },
        thumb(frame),
        el(
          "span",
          { class: "frame-meta" },
          el("span", { text: frame.time ? frame.time.precise : "" }),
          frame.ocr_text ? el("span", { class: "frame-flag", text: "text" }) : null
        ),
        el("span", { class: "visually-hidden", text: " (enlarge)" })
      );
      list.append(el("li", { hidden: !first.has(frame) }, button));
    });
    const block = el("div", { class: "frames-block" }, list);
    if (frames.length > first.size) {
      const more = el("button", {
        type: "button",
        class: "link-btn more-frames",
        text: `Show all ${frames.length} frames`,
        onclick: () => {
          for (const item of list.children) item.hidden = false;
          more.remove();
        },
      });
      block.append(more);
    }
    return block;
  }

  function transcriptBlock(lines, context) {
    if (!lines || lines.length === 0) return null;
    const list = el("ol", { class: "lines" });
    for (const line of lines) {
      const clock = line.time ? line.time.precise : "";
      const playable = context.playable.has(line.clip_id);
      const time = playable
        ? el("button", {
            type: "button",
            class: "line-time",
            text: clock,
            title: "Play the video from here",
            "aria-label": "Play the video from " + clock,
            onclick: () => openPlayer(line.clip_id, line.t, context.title),
          })
        : el("span", { class: "line-time", text: clock });
      list.append(
        el(
          "li",
          { id: "u-" + line.id },
          time,
          el("span", { class: "line-text" }, line.speaker ? el("b", { text: line.speaker + ": " }) : null, line.text)
        )
      );
    }
    return el(
      "details",
      { class: "transcript" },
      el("summary", null, "Transcript ", el("span", { class: "muted", text: `· ${plural(lines.length, "line")}` })),
      list
    );
  }

  function momentItem(moment, context) {
    const salience = moment.salience === "highlight" || moment.salience === "background" ? moment.salience : "normal";
    const times = timeRange(moment.start, moment.end);
    const summary = el(
      "summary",
      null,
      el("span", { class: "chevron", "aria-hidden": "true" }),
      el("span", { class: "moment-time", text: times }),
      el("h3", { class: "moment-title", text: moment.title || (salience === "background" ? "Quiet stretch" : "Untitled moment") }),
      el(
        "span",
        { class: "moment-chips" },
        salience === "highlight" ? chip("Highlight", "highlight") : null,
        salience === "background" ? chip("Background", "quiet") : null,
        MOMENT_KIND[moment.kind] ? chip(MOMENT_KIND[moment.kind]) : null
      )
    );
    const body = el("div", { class: "moment-body" });
    add(body, [paragraphs(moment.summary, "moment-summary")]);
    if (moment.play) {
      body.append(
        el(
          "p",
          { class: "moment-actions" },
          el(
            "button",
            {
              type: "button",
              class: "btn small",
              onclick: () => openPlayer(moment.play.clip_id, moment.play.t, moment.title || context.title),
            },
            el("span", { class: "play-icon", "aria-hidden": "true" }),
            "Play from here"
          )
        )
      );
    }
    add(body, [framesBlock(moment.keyframes, context), transcriptBlock(moment.transcript, context)]);
    if (moment.tags && moment.tags.length) body.append(el("p", { class: "chip-row" }, moment.tags.map((t) => chip(t, "tag"))));
    if (!body.hasChildNodes()) body.append(el("p", { class: "muted", text: "Nothing was said or picked out here." }));
    const details = el("details", { class: "moment " + salience, id: "moment-" + moment.id }, summary, body);
    details.open = salience !== "background";
    return el("li", { class: salience }, details);
  }

  function sessionNotices(s, note) {
    const out = [];
    if (s.status === "open") {
      out.push(notice("info", "This session is still being recorded. New material appears here as it is processed."));
    } else if (s.status === "processing") {
      out.push(notice("info", "This session is still being processed. The note fills in as each step finishes."));
    } else if (s.status === "error") {
      out.push(
        notice(
          "warn",
          s.failed_stages && s.failed_stages.length
            ? `Some steps failed for this session (${s.failed_stages.join(", ")}). `
            : "Some steps failed for this session. ",
          "Run ",
          code("vnote process " + s.id),
          " in Terminal to try again; ",
          code("vnote doctor"),
          " shows what is missing."
        )
      );
    }
    if (!note && s.status !== "open" && s.status !== "processing") {
      out.push(notice("quiet", "Not summarised yet. Run ", code("vnote process " + s.id), " in Terminal."));
    }
    return out;
  }

  function sessionSignature(data) {
    const count = (list, key) => list.reduce((sum, item) => sum + item[key].length, 0);
    return JSON.stringify([
      data.session.status,
      data.session.has_note,
      data.moments.length,
      count(data.moments, "keyframes"),
      count(data.moments, "transcript"),
      data.unassigned.keyframes.length,
      data.unassigned.transcript.length,
    ]);
  }

  async function sessionView(route, ticket) {
    const [data] = await Promise.all([api("/api/session/" + encodeURIComponent(route.id)), loadOverview(false)]);
    const s = data.session;
    const note = data.note;
    state.session = data;
    setCurrent(s.day, s.id);

    const playable = new Set(data.clips.filter((c) => mediaSrc(c.url)).map((c) => c.id));
    const context = { playable, title: s.title };
    const dayInfo = state.overview && state.overview.days.find((d) => d.date === s.day);

    const page = el("article", { class: "page" });
    page.append(
      el(
        "header",
        { class: "page-head" },
        s.day ? el("p", { class: "eyebrow" }, el("a", { href: routes.day(s.day), text: dayInfo ? dayInfo.label : s.day })) : null,
        el("h1", { tabindex: "-1", class: s.untitled ? "untitled" : null, text: s.title }),
        el(
          "p",
          { class: "meta" },
          [sessionTimes(s), SOURCE_KIND[s.kind] || "", s.source].filter(Boolean).join(" · "),
          statusChip(s) ? " " : null,
          statusChip(s)
        )
      )
    );
    add(page, [sessionNotices(s, note)]);

    if (note) {
      add(page, [
        note.summary ? el("section", { class: "summary" }, paragraphs(note.summary)) : null,
        section("Key points", bulletList(note.key_points)),
        section("Action items", checklist(note.action_items)),
        section("Decisions", bulletList(note.decisions)),
        section("Open questions", bulletList(note.open_questions)),
        section(
          "Captured text",
          note.captured_text.length
            ? el("div", { class: "captured-list" }, note.captured_text.map((t) => el("pre", { class: "captured", text: t })))
            : null
        ),
      ]);
      const facts = [chipRow("People", note.people), chipRow("Places", note.places), chipRow("Tags", note.tags)].filter(Boolean);
      if (facts.length) page.append(el("section", { class: "facts" }, facts));
      add(page, [provenance(note.llm_backend, "Summary")]);
    }

    // timeline
    const moments = data.moments;
    const quiet = moments.filter((m) => m.salience === "background").length;
    const timeline = el("section", { class: "block timeline-block" });
    const heading = el("div", { class: "block-head" }, el("h2", { text: "Timeline" }));
    timeline.append(heading);
    if (moments.length) {
      const list = el("ol", { class: "timeline" }, moments.map((m) => momentItem(m, context)));
      const toggle = el("button", { type: "button", class: "link-btn", text: "Open all" });
      toggle.addEventListener("click", () => {
        const opening = toggle.textContent === "Open all";
        for (const d of list.querySelectorAll("details.moment")) {
          d.open = opening || !d.classList.contains("background");
        }
        toggle.textContent = opening ? "Collapse quiet stretches" : "Open all";
      });
      add(heading, [
        el("span", {
          class: "muted",
          text: plural(moments.length, "moment") + (quiet ? `, ${plural(quiet, "quiet stretch", "quiet stretches")} collapsed` : ""),
        }),
        quiet ? toggle : null,
      ]);
      if (data.clips.length && !data.playable) {
        timeline.append(
          notice("quiet", "The video of this session is not kept in the library, so playback is off. Keyframes and transcript are all here.")
        );
      }
      timeline.append(list);
    }
    const loose = data.unassigned;
    if (loose.keyframes.length || loose.transcript.length) {
      const body = el("div", { class: "moment-body" });
      add(body, [framesBlock(loose.keyframes, context), transcriptBlock(loose.transcript, context)]);
      const details = el(
        "details",
        { class: "moment normal", id: "moment-loose" },
        el(
          "summary",
          null,
          el("span", { class: "chevron", "aria-hidden": "true" }),
          el("h3", { class: "moment-title", text: moments.length ? "Outside any moment" : "Not organised into moments yet" }),
          el("span", { class: "muted", text: `${plural(loose.keyframes.length, "frame")}, ${plural(loose.transcript.length, "transcript line")}` })
        ),
        body
      );
      details.open = moments.length === 0;
      if (!moments.length) {
        const first = details.querySelector("details.transcript");
        if (first) first.open = true;
      }
      timeline.append(details);
    } else if (!moments.length) {
      timeline.append(notice("quiet", "Nothing on the timeline yet: no speech, keyframes or moments have been stored for this session."));
    }
    page.append(timeline);

    if (s.status === "open" || s.status === "processing") startPolling(route.id, sessionSignature(data), ticket);

    return {
      title: s.title,
      node: page,
      after: () => focusTarget(route),
    };
  }

  /** After a jump from search or ask: open the moment, reveal the line or frame, and scroll to it. */
  function focusTarget(route) {
    let target = null;
    const moment = route.m ? document.getElementById("moment-" + route.m) : null;
    if (route.u) target = document.getElementById("u-" + route.u);
    if (!target && route.kf) target = view.querySelector(`.frame[data-kf="${CSS.escape(route.kf)}"]`);
    const host = (target && target.closest("details.moment")) || moment;
    if (!host) return false;
    host.open = true;
    if (target) {
      const inner = target.closest("details.transcript");
      if (inner) inner.open = true;
      const item = target.closest("li");
      if (item && item.hidden) {
        for (const li of item.parentElement.children) li.hidden = false;
        const more = host.querySelector(".more-frames");
        if (more) more.remove();
      }
    }
    const flash = target || host;
    flash.classList.add("flash");
    window.setTimeout(() => flash.classList.remove("flash"), 2600);
    (target || host).scrollIntoView({ block: target ? "center" : "start" });
    const focusable = target && target.matches("button") ? target : host.querySelector("summary");
    if (focusable) focusable.focus({ preventScroll: true });
    return true;
  }

  function stopPolling() {
    if (state.pollTimer) window.clearInterval(state.pollTimer);
    state.pollTimer = null;
  }

  function startPolling(id, signature, ticket) {
    stopPolling();
    state.pollTimer = window.setInterval(async () => {
      if (document.hidden || ticket !== state.ticket) return;
      let fresh;
      try {
        fresh = await api("/api/session/" + encodeURIComponent(id));
      } catch (err) {
        return;
      }
      if (ticket !== state.ticket || sessionSignature(fresh) === signature) return;
      stopPolling();
      if (view.querySelector(".refresh-bar")) return;
      view.prepend(
        el(
          "p",
          { class: "notice info refresh-bar", role: "status" },
          "This session has new material. ",
          el("button", { type: "button", class: "btn small", text: "Show it", onclick: () => navigate(true) })
        )
      );
    }, 12000);
  }

  // ------------------------------------------------------------------ view: search

  function snippet(parts, fallback) {
    const p = el("span", { class: "result-text" });
    if (!parts || parts.length === 0) {
      p.textContent = fallback || "";
      return p;
    }
    for (const part of parts) p.append(part.match ? el("mark", { text: part.text }) : document.createTextNode(part.text));
    return p;
  }

  function resultLink(item, body, withDate) {
    return el(
      "a",
      {
        class: "result",
        href: routes.session(item.session_id, { m: item.moment_id, kf: item.keyframe_id, u: item.utterance_id }),
      },
      thumb(item.thumbnail),
      el(
        "span",
        { class: "result-body" },
        el(
          "span",
          { class: "result-meta" },
          el("span", { class: "result-time", text: item.time ? (withDate ? item.time.text : item.time.clock) : "" }),
          chip(HIT_KIND[item.kind] || item.kind, "kind-" + item.kind),
          el("span", { class: "result-where", text: item.moment_title ? `${item.session_title} › ${item.moment_title}` : item.session_title }),
          item.similar ? el("span", { class: "result-more", text: `+ ${plural(item.similar, "similar frame")}` }) : null
        ),
        body
      )
    );
  }

  async function searchView(route) {
    setCurrent(null, null);
    searchInput.value = route.q;
    const page = el("article", { class: "page" });
    const head = el("header", { class: "page-head" }, el("h1", { tabindex: "-1", text: "Search" }));
    page.append(head);
    if (!route.q) {
      page.append(notice("quiet", "Type a few words in the search box above. It looks through what was said, text read off frames, frame descriptions and your notes."));
      return { title: "Search", node: page };
    }
    const params = new URLSearchParams({ q: route.q });
    if (route.kind) params.set("kind", route.kind);
    if (route.day) params.set("day", route.day);
    const data = await api("/api/search?" + params.toString());

    head.append(
      el(
        "p",
        { class: "meta" },
        data.count ? `${data.truncated ? "The best " : ""}${plural(data.count, "match", "matches")} for ` : "No matches for ",
        el("q", { text: data.query }),
        data.day ? ` on ${data.day.label}` : ""
      )
    );

    const kinds = [["", "Everything"]].concat(Object.entries(HIT_KIND));
    const filters = el(
      "div",
      { class: "filters", role: "group", "aria-label": "Narrow the search" },
      kinds.map(([kind, label]) =>
        el("a", {
          class: "filter" + (route.kind === kind ? " on" : ""),
          href: routes.search(route.q, { kind, day: route.day }),
          "aria-current": route.kind === kind ? "true" : null,
          text: label,
        })
      ),
      route.day
        ? el("a", { class: "filter clear", href: routes.search(route.q, { kind: route.kind }), text: "All days ✕", "aria-label": "Search all days" })
        : null
    );
    page.append(filters);

    if (data.count === 0) {
      page.append(
        notice(
          "quiet",
          "Nothing matched. Try fewer or different words",
          route.kind || route.day ? ", or widen the search with the buttons above" : "",
          ". ",
          el("a", { href: routes.ask(route.q), text: "Ask it as a question instead" })
        )
      );
      return { title: `Search: ${route.q}`, node: page };
    }

    // group by local day, newest day first; inside a day keep the ranking
    const groups = new Map();
    for (const hit of data.hits) {
      const day = hit.time ? hit.time.day : "";
      if (!groups.has(day)) groups.set(day, []);
      groups.get(day).push(hit);
    }
    const labels = new Map((state.overview ? state.overview.days : []).map((d) => [d.date, d]));
    for (const day of Array.from(groups.keys()).sort().reverse()) {
      const hits = groups.get(day);
      const info = labels.get(day);
      const title = info ? (info.relative ? `${info.relative}, ${info.label}` : info.label) : day || "Undated";
      page.append(
        el(
          "section",
          { class: "result-day" },
          el(
            "h2",
            null,
            day ? el("a", { href: routes.day(day), text: title }) : title,
            el("span", { class: "muted", text: "  " + plural(hits.length, "match", "matches") }),
            day && !route.day && groups.size > 1
              ? el("a", { class: "only-day", href: routes.search(route.q, { kind: route.kind, day }), text: "only this day" })
              : null
          ),
          el("ul", { class: "results" }, hits.map((hit) => el("li", null, resultLink(hit, snippet(hit.parts, hit.snippet)))))
        )
      );
    }
    page.append(el("p", { class: "fineprint" }, "Looking for an answer rather than a passage? ", el("a", { href: routes.ask(route.q), text: "Ask it as a question" }), "."));
    return { title: `Search: ${route.q}`, node: page };
  }

  // ------------------------------------------------------------------ view: ask

  function askResult() {
    const ask = state.ask;
    const box = el("div", { class: "ask-result" });
    if (ask.pending) {
      box.append(
        el(
          "p",
          { class: "notice info working", role: "status" },
          el("span", { class: "spinner", "aria-hidden": "true" }),
          "Looking through your notes… A language model running on this computer can take a minute."
        )
      );
      return box;
    }
    if (ask.error) {
      box.append(el("p", { class: "notice warn", role: "alert", text: ask.error }));
      return box;
    }
    const result = ask.result;
    if (!result) return box;
    box.append(el("h2", { class: "asked", text: result.question }));
    const answer = el("div", { class: "answer" });
    add(answer, [paragraphs(result.answer || "Nothing in the library answers that.")]);
    box.append(answer);
    if (result.extractive && result.sources.length) {
      box.append(
        notice("quiet", "No language model is set up, so these are the closest excerpts rather than a written answer. ", code("vnote doctor"), " shows how to enable one.")
      );
    } else if (result.llm_backend && !result.extractive) {
      box.append(el("p", { class: "fineprint", text: `Written by ${result.llm_backend} from the evidence below. Check it against the evidence before relying on it.` }));
    }
    if (result.sources.length) {
      box.append(
        el(
          "section",
          { class: "block" },
          el("h2", { text: "Evidence" }),
          el(
            "ol",
            { class: "results evidence" },
            result.sources.map((source) =>
              el("li", null, resultLink(source, el("span", { class: "result-text evidence-text", text: source.text }), true))
            )
          )
        )
      );
    } else {
      box.append(notice("quiet", "Nothing relevant was found in the library, so there is no evidence to show."));
    }
    return box;
  }

  async function submitQuestion(question) {
    const ask = state.ask;
    if (ask.pending) return;
    Object.assign(ask, { question, pending: true, result: null, error: null });
    refreshAsk();
    try {
      ask.result = await api("/api/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json", Accept: "application/json" },
        body: JSON.stringify({ question }),
      });
    } catch (err) {
      ask.error =
        err.code === "offline"
          ? "The answer did not arrive. Either “vnote web” was stopped, or the language model took too long. Check the Terminal window, then ask again."
          : err.message;
    }
    ask.pending = false;
    refreshAsk();
    announce(ask.error ? "The question could not be answered." : "The answer is ready.");
  }

  function refreshAsk() {
    const slot = document.getElementById("ask-slot");
    if (!slot) return;
    slot.replaceChildren(askResult());
    const button = document.getElementById("ask-go");
    if (button) {
      button.disabled = state.ask.pending;
      button.textContent = state.ask.pending ? "Thinking…" : "Ask";
    }
  }

  async function askView(route) {
    setCurrent(null, null);
    const ask = state.ask;
    const input = el("textarea", {
      id: "ask-input",
      rows: "2",
      maxlength: "2000",
      placeholder: "For example: Where did I park the car?",
    });
    input.value = route.q || ask.question || "";
    const go = el("button", { type: "submit", class: "btn primary", id: "ask-go", text: ask.pending ? "Thinking…" : "Ask" });
    go.disabled = ask.pending;
    const form = el(
      "form",
      { class: "ask-form", action: "/", method: "get" },
      el("label", { for: "ask-input", class: "visually-hidden", text: "Your question" }),
      input,
      go
    );
    const submit = () => {
      const question = input.value.trim().replace(/\s+/g, " ");
      if (!question) {
        state.ask.error = "Type a question first.";
        state.ask.result = null;
        refreshAsk();
        input.focus();
        return;
      }
      submitQuestion(question);
    };
    form.addEventListener("submit", (event) => {
      event.preventDefault();
      submit();
    });
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey && !event.isComposing) {
        event.preventDefault();
        submit();
      }
    });
    const page = el(
      "article",
      { class: "page" },
      el(
        "header",
        { class: "page-head" },
        el("h1", { tabindex: "-1", text: "Ask about your recordings" }),
        el("p", {
          class: "meta",
          text: "Answers are written only from what was captured. The evidence is listed underneath so you can check it.",
        })
      ),
      form,
      el("div", { id: "ask-slot" }, askResult())
    );
    return { title: "Ask", node: page };
  }

  // ------------------------------------------------------------------ lightbox

  const lightbox = {
    dialog: document.getElementById("lightbox"),
    title: document.getElementById("lightbox-title"),
    count: document.getElementById("lightbox-count"),
    img: document.getElementById("lightbox-img"),
    missing: document.getElementById("lightbox-missing"),
    caption: document.getElementById("lightbox-caption"),
    ocrWrap: document.getElementById("lightbox-ocr-wrap"),
    ocr: document.getElementById("lightbox-ocr"),
    play: document.getElementById("lightbox-play"),
    prev: document.getElementById("lightbox-prev"),
    next: document.getElementById("lightbox-next"),
    frames: [],
    index: 0,
    context: null,
    opener: null,
  };

  function showFrame(index) {
    const frames = lightbox.frames;
    lightbox.index = Math.max(0, Math.min(frames.length - 1, index));
    const frame = frames[lightbox.index];
    const src = frameSrc(frame.url);
    lightbox.title.textContent = frame.time ? `Frame at ${frame.time.precise}` : "Frame";
    lightbox.count.textContent = frames.length > 1 ? `${lightbox.index + 1} of ${frames.length}` : "";
    lightbox.img.hidden = !src;
    lightbox.missing.hidden = Boolean(src);
    if (src) {
      lightbox.img.src = src;
      lightbox.img.alt = frame.alt || "Keyframe";
    } else {
      lightbox.img.removeAttribute("src");
      lightbox.img.alt = "";
    }
    lightbox.caption.textContent = frame.caption || "";
    lightbox.caption.hidden = !frame.caption;
    lightbox.ocr.textContent = frame.ocr_text || "";
    lightbox.ocrWrap.hidden = !frame.ocr_text;
    lightbox.play.hidden = !(lightbox.context && lightbox.context.playable.has(frame.clip_id));
    lightbox.prev.disabled = lightbox.index === 0;
    lightbox.next.disabled = lightbox.index === frames.length - 1;
    lightbox.prev.hidden = lightbox.next.hidden = lightbox.count.hidden = frames.length < 2;
  }

  function openLightbox(frames, index, context) {
    lightbox.frames = frames;
    lightbox.context = context;
    lightbox.opener = document.activeElement;
    showFrame(index);
    if (!lightbox.dialog.open) lightbox.dialog.showModal();
  }

  lightbox.prev.addEventListener("click", () => showFrame(lightbox.index - 1));
  lightbox.next.addEventListener("click", () => showFrame(lightbox.index + 1));
  lightbox.img.addEventListener("error", () => {
    lightbox.img.hidden = true;
    lightbox.missing.hidden = false;
  });
  lightbox.dialog.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") showFrame(lightbox.index - 1);
    else if (event.key === "ArrowRight") showFrame(lightbox.index + 1);
  });
  lightbox.play.addEventListener("click", () => {
    const frame = lightbox.frames[lightbox.index];
    const opener = lightbox.opener;
    lightbox.dialog.close();
    openPlayer(frame.clip_id, frame.t, lightbox.context ? lightbox.context.title : "", opener);
  });
  lightbox.dialog.addEventListener("close", () => {
    lightbox.img.removeAttribute("src");
    if (lightbox.opener && lightbox.opener.isConnected) lightbox.opener.focus();
    lightbox.opener = null;
  });

  // ------------------------------------------------------------------ player

  const player = {
    dialog: document.getElementById("player"),
    title: document.getElementById("player-title"),
    stage: document.getElementById("player-stage"),
    note: document.getElementById("player-note"),
    media: null,
    opener: null,
  };

  function clipById(id) {
    const clips = state.session ? state.session.clips : [];
    return clips.find((clip) => clip.id === id) || null;
  }

  function loadClip(clip, seconds, autoplay) {
    const src = mediaSrc(clip.url);
    if (player.media) {
      player.media.pause();
      player.media.remove();
    }
    player.note.textContent = clip.start ? `Clip recorded ${clip.start.text} · ${clip.duration}` : "";
    const media = el(clip.has_video === false ? "audio" : "video", { controls: true, preload: "metadata", playsinline: true });
    player.media = media;
    media.addEventListener("loadedmetadata", () => {
      const limit = Number.isFinite(media.duration) ? Math.max(0, media.duration - 0.25) : seconds;
      if (seconds > 0) media.currentTime = Math.min(seconds, limit);
      if (autoplay) media.play().catch(() => {});
    });
    media.addEventListener("error", () => {
      player.note.textContent =
        "This clip can't be played here. Its format may not be supported by the browser, or the file is no longer in the library.";
    });
    media.addEventListener("ended", () => {
      const clips = state.session ? state.session.clips : [];
      const next = clips.slice(clips.indexOf(clip) + 1).find((c) => mediaSrc(c.url));
      if (next && player.dialog.open) loadClip(next, 0, true);
    });
    media.src = src;
    player.stage.replaceChildren(media);
  }

  function openPlayer(clipId, seconds, title, opener) {
    const clip = clipById(clipId);
    if (!clip || !mediaSrc(clip.url)) return;
    player.opener = opener || document.activeElement;
    player.title.textContent = title || "Video";
    loadClip(clip, Math.max(0, Number(seconds) || 0), true);
    if (!player.dialog.open) player.dialog.showModal();
  }

  player.dialog.addEventListener("close", () => {
    if (player.media) {
      player.media.pause();
      player.media.removeAttribute("src");
      player.media.load(); // stop downloading
      player.media.remove();
      player.media = null;
    }
    if (player.opener && player.opener.isConnected) player.opener.focus();
    player.opener = null;
  });

  for (const dialog of [lightbox.dialog, player.dialog]) {
    dialog.addEventListener("click", (event) => {
      if (event.target === dialog || event.target.closest("[data-close]")) dialog.close();
    });
  }

  function closeDialogs() {
    for (const dialog of [lightbox.dialog, player.dialog]) if (dialog.open) dialog.close();
  }

  // ------------------------------------------------------------------ navigation

  function errorView(err) {
    const offline = err instanceof ApiError && err.code === "offline";
    const missing = err instanceof ApiError && err.status === 404;
    return el(
      "article",
      { class: "page empty-state" },
      el("h1", { tabindex: "-1", text: offline ? "videonotes is not answering" : missing ? "Not found" : "Something went wrong" }),
      el("p", { class: "lead", text: err instanceof ApiError ? err.message : "This page ran into a problem showing that." }),
      el(
        "p",
        null,
        el("button", { type: "button", class: "btn", text: "Try again", onclick: () => navigate(true) }),
        " ",
        offline ? null : el("a", { href: routes.home(), text: "Go to the latest day" })
      )
    );
  }

  function notFoundView() {
    return {
      title: "Not found",
      node: el(
        "article",
        { class: "page empty-state" },
        el("h1", { tabindex: "-1", text: "Not found" }),
        el("p", { class: "lead" }, "There is no page at this address. ", el("a", { href: routes.home(), text: "Go to the latest day" }))
      ),
    };
  }

  const VIEWS = { home: homeView, day: dayView, session: sessionView, search: searchView, ask: askView, notfound: async () => notFoundView() };

  let userNavigated = false;

  async function navigate(refresh) {
    const route = parseRoute();
    const ticket = (state.ticket += 1);
    closeDialogs();
    setNav(false);
    stopPolling();
    if (route.name !== "session") state.session = null;
    if (route.name !== "search") searchInput.value = "";
    if (refresh) state.overviewAt = 0;
    if (route.name !== "home") {
      loadOverview(false).catch(() => {
        if (!state.overview) dayList.replaceChildren(el("p", { class: "side-note", text: "The list of days could not be loaded." }));
      });
    }
    view.setAttribute("aria-busy", "true");
    const slow = window.setTimeout(() => view.classList.add("is-loading"), 250);
    let result;
    try {
      result = await VIEWS[route.name](route, ticket);
    } catch (err) {
      if (!(err instanceof ApiError)) console.error(err);
      result = { title: "Problem", node: errorView(err) };
    }
    window.clearTimeout(slow);
    if (ticket !== state.ticket) return;
    view.classList.remove("is-loading");
    view.removeAttribute("aria-busy");
    if (!result) return; // the view redirected
    view.replaceChildren(result.node);
    document.title = result.title ? `${result.title} · videonotes` : "videonotes";
    const jumped = result.after ? result.after() === true : false;
    if (!jumped) {
      if (!refresh) window.scrollTo(0, 0);
      const heading = view.querySelector("h1");
      if (heading && userNavigated) heading.focus({ preventScroll: true });
    }
    if (userNavigated) announce(result.title || "videonotes");
    userNavigated = true;
  }

  window.addEventListener("hashchange", () => navigate(false));

  document.getElementById("search-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const q = searchInput.value.trim();
    if (!q) {
      searchInput.focus();
      return;
    }
    const target = routes.search(q);
    if (location.hash === target) navigate(true);
    else location.hash = target;
  });

  document.getElementById("skip-link").addEventListener("click", (event) => {
    event.preventDefault();
    const heading = view.querySelector("h1");
    (heading || main).focus();
  });

  // keep the list of days fresh when the tab is looked at again (new sessions arrive from Terminal)
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden && Date.now() - state.overviewAt > 15000) loadOverview(true).catch(() => {});
  });

  navigate(false);
})();
