// Original motion studies for the mystic.code editor. All coordinates use a 560 × 280 design space.
(() => {
  const study = document.querySelector(".motion-study");
  if (!study) return;
  const canvas = study.querySelector("canvas");
  const ctx = canvas.getContext("2d");
  if (!ctx) {
    study.remove();
    return;
  }

  const W = 560;
  const H = 280;
  const TAU = Math.PI * 2;
  const duration = 2800;
  const clamp = (n, low = 0, high = 1) => Math.min(high, Math.max(low, n));
  const ease = (t) => 1 - (1 - t) ** 3;

  // Cache lengths once. Line reveals and traveling highlights share the same geometry.
  function stroke(points, options = {}) {
    let length = 0;
    const distances = [0];
    for (let i = 1; i < points.length; i++) {
      length += Math.hypot(points[i][0] - points[i - 1][0], points[i][1] - points[i - 1][1]);
      distances.push(length);
    }
    return {
      points,
      distances,
      length,
      color: "accent",
      width: 1.5,
      alpha: 1,
      start: 0,
      end: 0.64,
      lift: 0,
      ...options,
    };
  }

  function arc(x, y, rx, ry, start = 0, end = TAU) {
    const steps = Math.max(8, Math.ceil((Math.abs(end - start) * Math.max(rx, ry)) / 4));
    return Array.from({ length: steps + 1 }, (_, i) => {
      const angle = start + ((end - start) * i) / steps;
      return [x + Math.cos(angle) * rx, y + Math.sin(angle) * ry];
    });
  }

  function closed(points) {
    return [...points, points[0]];
  }

  function segmentAt(shape, distance) {
    let lo = 1;
    let hi = shape.distances.length - 1;
    while (lo < hi) {
      const mid = (lo + hi) >> 1;
      if (shape.distances[mid] < distance) lo = mid + 1;
      else hi = mid;
    }
    const a = shape.points[lo - 1];
    const b = shape.points[lo];
    const fraction =
      (distance - shape.distances[lo - 1]) / (shape.distances[lo] - shape.distances[lo - 1] || 1);
    return { index: lo, x: a[0] + (b[0] - a[0]) * fraction, y: a[1] + (b[1] - a[1]) * fraction };
  }

  function trace(shape, from, to, lift) {
    const a = segmentAt(shape, from * shape.length);
    const b = segmentAt(shape, to * shape.length);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y + lift);
    for (let i = a.index; i < b.index; i++) ctx.lineTo(shape.points[i][0], shape.points[i][1] + lift);
    ctx.lineTo(b.x, b.y + lift);
  }

  function hardware(processor) {
    const shapes = [];
    const iso = (x, y, z = 0) => [280 + (x - y) * 1.13, 171 + (x + y) * 0.42 - z];
    const size = processor ? 58 : 67;
    for (const side of [-1, 1]) {
      for (let i = 0; i < 8; i++) {
        const y = 69 + i * 18;
        const socketX = 280 + side * (37 + i * 6);
        const bendX = 280 + side * (117 + (i % 4) * 11);
        const endX = 280 + side * (204 + (i % 3) * 15);
        const points = [
          [socketX, 147 + (i - 4) * 5],
          [bendX - side * 27, 147 + (i - 4) * 5],
          [bendX + side * 9, y],
          [endX, y],
        ];
        shapes.push(
          stroke(points, { color: "wire", width: 1.4, start: i * 0.015, end: 0.52, pulse: i % 3 === 0 }),
        );
        shapes.push(
          stroke(arc(endX, y, 2.6, 2.6), {
            color: i % 3 ? "wire" : "brass",
            start: 0.16 + i * 0.012,
            end: 0.55,
          }),
        );
      }
    }

    function plate(radius, height, thickness, fill, start) {
      const cut = 7;
      const corners = [
        [-radius + cut, -radius],
        [radius - cut, -radius],
        [radius, -radius + cut],
        [radius, radius - cut],
        [radius - cut, radius],
        [-radius + cut, radius],
        [-radius, radius - cut],
        [-radius, -radius + cut],
      ];
      const top = corners.map(([x, y]) => iso(x, y, height));
      const bottom = corners.map(([x, y]) => iso(x, y, height - thickness));
      const motion = { start, end: start + 0.49, lift: -16 - height * 0.22 };
      shapes.push(stroke(closed(bottom), { ...motion, fill: "side", color: "wire", width: 1.4 }));
      for (let i = 2; i < 7; i++) {
        const j = (i + 1) % 8;
        shapes.push(
          stroke(closed([top[i], top[j], bottom[j], bottom[i]]), {
            ...motion,
            fill: "side",
            color: "wire",
            width: 1,
          }),
        );
      }
      shapes.push(stroke(closed(top), { ...motion, fill, color: "accent", width: 1.9 }));
      shapes.push(
        stroke(closed(corners.map(([x, y]) => iso(x * 0.92, y * 0.92, height + 0.5))), {
          ...motion,
          color: "wire",
          width: 1,
        }),
      );
    }
    plate(size + 10, 0, 7, "base", 0.01);
    plate(size, 17, 5, "face", 0.08);
    plate(size - 7, 38, 8, "face", 0.15);
    plate(size - 13, 56, 5, "top", 0.21);

    if (processor) {
      for (let i = -3; i <= 3; i++) {
        for (const side of [-1, 1]) {
          shapes.push(
            stroke([iso(i * 10, side * 47, 36), iso(i * 10, side * 55, 36), iso(i * 10, side * 62, 27)], {
              color: "brass",
              width: 2,
              start: 0.26,
              end: 0.72,
              lift: -18,
            }),
          );
        }
      }
      for (let i = 0; i < 4; i++) {
        shapes.push(
          stroke(
            [
              iso(-23, -20 + i * 12, 57),
              iso(-9, -20 + i * 12, 57),
              iso(-4, -15 + i * 12, 57),
              iso(23, -15 + i * 12, 57),
            ],
            {
              color: i === 1 ? "brass" : "accent",
              width: 2,
              start: 0.33 + i * 0.035,
              end: 0.84,
              lift: -16,
              pulse: i === 1,
            },
          ),
        );
      }
    } else {
      // The nested fork motif is taken from the portfolio's existing mint emblem.
      const rings = [
        [-25, -8],
        [-25, -21],
        [0, -34],
        [25, -21],
        [25, 17],
        [0, 31],
        [-25, 17],
        [-25, -8],
      ];
      shapes.push(
        stroke(
          rings.map(([x, y]) => iso(x, y, 58)),
          { width: 2.9, color: "accent", start: 0.33, end: 0.79, lift: -16 },
        ),
      );
      shapes.push(
        stroke([iso(0, -25, 58), iso(0, 23, 58)], {
          width: 3,
          color: "bright",
          start: 0.38,
          end: 0.77,
          lift: -16,
        }),
      );
      for (const row of [-10, 3, 15]) {
        shapes.push(
          stroke([iso(-15, row + 4, 58), iso(0, row - 6, 58), iso(15, row + 4, 58)], {
            width: 2.4,
            color: "bright",
            start: 0.4 + (row + 10) * 0.003,
            end: 0.84,
            lift: -16,
          }),
        );
      }
    }
    return shapes;
  }

  const routeTrack = stroke(
    [
      [62, 177],
      [148, 177],
      [180, 145],
      [247, 145],
      [291, 101],
      [366, 101],
      [405, 62],
      [479, 62],
    ],
    { color: "accent", width: 3.4, start: 0.1, end: 0.74, pulse: true },
  );
  const gauge = [355, 177];
  function route() {
    const shapes = [];
    const outline = [
      [100, 186],
      [115, 153],
      [137, 137],
      [161, 137],
      [172, 119],
      [223, 119],
      [244, 88],
      [272, 88],
      [291, 114],
      [286, 132],
      [315, 139],
      [337, 160],
      [398, 160],
      [417, 176],
    ];
    for (let i = 0; i < 5; i++) {
      const y = 206 + i * 6;
      shapes.push(
        stroke(
          [
            [70 + i * 8, y],
            [478 - i * 9, y],
          ],
          { color: "wire", alpha: 0.48 - i * 0.06, width: 1, start: 0.05, end: 0.52 },
        ),
      );
    }
    shapes.push(stroke(outline, { color: "wire", width: 1.4, start: 0.05, end: 0.69 }));
    const path = routeTrack.points;
    shapes.push(stroke(path, { color: "wire", width: 10, alpha: 0.65, start: 0, end: 0.64 }));
    shapes.push(routeTrack);
    for (const [i, j] of [0, 3, 5, 7].entries()) {
      const [x, y] = path[j];
      shapes.push(
        stroke(arc(x, y, 7, 7), {
          color: i === 3 ? "brass" : "bright",
          fill: "base",
          width: 2,
          start: 0.22 + i * 0.09,
          end: 0.61 + i * 0.08,
        }),
      );
    }
    const hub = gauge;
    for (const radius of [23, 33, 43]) {
      shapes.push(
        stroke(arc(...hub, radius, radius, -Math.PI, 0.12), {
          color: radius === 43 ? "accent" : "wire",
          start: 0.3,
          end: 0.83,
        }),
      );
    }
    for (let i = 0; i <= 12; i++) {
      const theta = Math.PI + (i * Math.PI) / 12;
      const tick = (r) => [hub[0] + Math.cos(theta) * r, hub[1] + Math.sin(theta) * r];
      shapes.push(
        stroke([tick(i % 3 ? 37 : 33), tick(41)], { color: i % 3 ? "wire" : "brass", start: 0.35, end: 0.81 }),
      );
    }
    return shapes;
  }

  const onPaper = (x, y) => [160 + 172 * x + 64 * y, 70 - 24 * x + 137 * y];
  function grading() {
    const shapes = [];
    const sheet = [
      [160, 70],
      [332, 46],
      [396, 183],
      [224, 207],
    ];
    for (let n = 3; n >= 0; n--) {
      const layer = sheet.map(([x, y]) => [x + n * 13, y + n * 8]);
      shapes.push(
        stroke(closed(layer), {
          color: n ? "wire" : "accent",
          fill: n ? "side" : "face",
          width: n ? 1.3 : 2,
          start: (3 - n) * 0.055,
          end: 0.59 + (3 - n) * 0.045,
          lift: -14 - n * 4,
        }),
      );
    }
    for (let i = 0; i < 5; i++) {
      const y = 0.22 + i * 0.13;
      const last = 0.77 - (i % 3) * 0.12;
      shapes.push(
        stroke([onPaper(0.14, y), onPaper(last, y)], {
          color: i ? "wire" : "bright",
          width: i ? 2 : 3.5,
          start: 0.29 + i * 0.045,
          end: 0.8,
        }),
      );
    }
    const check = [
      [367, 117],
      [377, 126],
      [399, 99],
    ];
    shapes.push(
      stroke(arc(380, 116, 25, 25), { color: "accent", fill: "base", width: 2, start: 0.42, end: 0.86 }),
    );
    shapes.push(stroke(check, { color: "bright", width: 3, start: 0.54, end: 0.9 }));
    shapes.push(
      stroke(
        [
          [96, 119],
          [129, 119],
          [145, 103],
          [165, 103],
        ],
        { color: "wire", start: 0.04, end: 0.6, pulse: true },
      ),
    );
    shapes.push(
      stroke(
        [
          [418, 167],
          [438, 167],
          [451, 154],
          [477, 154],
        ],
        { color: "wire", start: 0.12, end: 0.68, pulse: true },
      ),
    );
    return shapes;
  }

  function branches() {
    const shapes = [];
    const paths = [
      [
        [72, 145],
        [150, 145],
        [190, 105],
        [258, 105],
      ],
      [
        [150, 145],
        [190, 185],
        [258, 185],
      ],
      [
        [258, 105],
        [287, 76],
        [362, 76],
        [391, 48],
        [478, 48],
      ],
      [
        [258, 105],
        [291, 138],
        [365, 138],
        [394, 109],
        [465, 109],
      ],
      [
        [258, 185],
        [294, 149],
        [356, 149],
      ],
      [
        [258, 185],
        [288, 215],
        [364, 215],
        [390, 190],
        [479, 190],
      ],
      [
        [364, 215],
        [392, 243],
        [456, 243],
      ],
    ];
    for (const [i, path] of paths.entries()) {
      const selected = i === 0 || i === 2;
      shapes.push(
        stroke(path, {
          color: selected ? "accent" : "wire",
          width: selected ? 2.9 : 1.5,
          start: i < 2 ? 0.03 : 0.2 + (i - 2) * 0.045,
          end: i < 2 ? 0.52 : 0.73 + (i - 2) * 0.025,
          pulse: selected,
        }),
      );
    }
    for (const [index, point] of [paths[0][0], paths[0][1], ...paths.map((p) => p.at(-1))].entries()) {
      const [x, y] = point;
      const radius = index < 2 ? 6 : 5;
      shapes.push(
        stroke(
          closed([
            [x - radius, y],
            [x, y - radius],
            [x + radius, y],
            [x, y + radius],
          ]),
          {
            color: index === 4 ? "brass" : "accent",
            fill: "base",
            width: 1.8,
            start: 0.16 + index * 0.04,
            end: 0.66 + index * 0.03,
          },
        ),
      );
    }
    return shapes;
  }

  const scenes = {
    welcome: hardware(false),
    scoot: route(),
    "esp-reddit": hardware(true),
    "exam-eval": grading(),
    "detroit-jev": branches(),
  };

  function blend(a, b, ratio) {
    const values = [1, 3, 5].map((i) => {
      const from = parseInt(a.slice(i, i + 2), 16);
      return Math.round(from + (parseInt(b.slice(i, i + 2), 16) - from) * ratio);
    });
    return "rgb(" + values.join(",") + ")";
  }
  function themePalette() {
    const style = getComputedStyle(document.documentElement);
    const accent = style.getPropertyValue("--accent").trim();
    const base = style.getPropertyValue("--editor").trim();
    return {
      accent,
      base,
      bright: blend(accent, "#ffffff", 0.6),
      brass: style.getPropertyValue("--file-json").trim(),
      wire: blend(base, accent, 0.47),
      side: blend(base, accent, 0.09),
      face: blend(base, accent, 0.19),
      top: blend(base, accent, 0.33),
    };
  }
  let palette = themePalette();

  function beacon(x, y, opacity, radius) {
    ctx.fillStyle = palette.bright;
    ctx.globalAlpha = opacity * 0.12;
    ctx.beginPath();
    ctx.arc(x, y, radius * 2.8, 0, TAU);
    ctx.fill();
    ctx.globalAlpha = opacity;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, TAU);
    ctx.fill();
  }

  function drawInstruments(name, time, opacity) {
    if (name === "scoot") {
      if (time < 0.33) return;
      const progress = clamp((time - 0.33) / 0.59);
      const cursor = segmentAt(routeTrack, routeTrack.length * ease(progress));
      const dial = Math.PI * (1 + 0.76 * ease(progress));
      ctx.globalAlpha = opacity * clamp(progress * 10);
      ctx.beginPath();
      ctx.moveTo(...gauge);
      ctx.lineTo(gauge[0] + Math.cos(dial) * 31, gauge[1] + Math.sin(dial) * 31);
      ctx.strokeStyle = palette.bright;
      ctx.lineWidth = 2.8;
      ctx.stroke();
      beacon(cursor.x, cursor.y, ctx.globalAlpha, 3.4);
    } else if (name === "exam-eval" && time > 0.27 && time < 0.79) {
      const progress = (time - 0.27) / 0.52;
      const y = 0.1 + 0.8 * progress;
      const [left, right] = [onPaper(0.06, y), onPaper(0.94, y)];
      const corners = [onPaper(0.06, y - 0.1), onPaper(0.94, y - 0.1), right, left];
      ctx.beginPath();
      ctx.moveTo(...corners[0]);
      for (const point of corners.slice(1)) ctx.lineTo(...point);
      ctx.closePath();
      ctx.globalAlpha = opacity * 0.13 * Math.sin(Math.PI * progress);
      ctx.fillStyle = palette.accent;
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(...left);
      ctx.lineTo(...right);
      ctx.globalAlpha = opacity * 0.85 * Math.sin(Math.PI * progress);
      ctx.strokeStyle = palette.bright;
      ctx.lineWidth = 1.8;
      ctx.stroke();
    } else if (name === "detroit-jev" && time > 0.26) {
      const progress = clamp((time - 0.26) / 0.65) * 2;
      const path = scenes[name][progress < 1 ? 0 : 2];
      const portion = progress < 1 ? progress : progress - 1;
      const cursor = segmentAt(path, ease(portion) * path.length);
      beacon(cursor.x, cursor.y, opacity * clamp(progress * 8), 3.6);
    }
  }

  function drawScene(name, time, opacity) {
    for (const shape of scenes[name]) {
      const reveal = ease(clamp((time - shape.start) / (shape.end - shape.start)));
      if (reveal <= 0 || shape.length === 0) continue;
      const lift = (1 - reveal) * shape.lift;
      if (shape.fill) {
        ctx.globalAlpha = reveal * opacity;
        ctx.fillStyle = palette[shape.fill];
        if (shape.fill === "top") {
          const face = ctx.createLinearGradient(185, 80 + lift, 352, 156 + lift);
          face.addColorStop(0, palette.face);
          face.addColorStop(0.43, palette.top);
          face.addColorStop(1, palette.side);
          ctx.fillStyle = face;
        }
        trace(shape, 0, 1, lift);
        ctx.fill();
      }
      trace(shape, 0, reveal, lift);
      ctx.globalAlpha = shape.alpha * opacity;
      ctx.strokeStyle = palette[shape.color];
      ctx.lineWidth = shape.width;
      ctx.stroke();
      if (shape.pulse && time > 0.42 && time < 0.98) {
        const tip = clamp((time - 0.42) / 0.5);
        const tail = clamp((time - 0.49) / 0.49);
        if (tip > tail) {
          trace(shape, tail, tip, lift);
          ctx.strokeStyle = palette.bright;
          ctx.lineWidth = shape.width + 0.7;
          ctx.stroke();
        }
      }
    }
    drawInstruments(name, time, opacity);
    ctx.globalAlpha = 1;
  }

  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const replay = study.querySelector("button");
  const home = study.dataset.scene;
  const handoffKey = "mystic-study-navigation";
  // Carry the actual pose into the project opened from its Welcome preview.
  function openingTime() {
    try {
      const saved = JSON.parse(sessionStorage.getItem(handoffKey));
      sessionStorage.removeItem(handoffKey);
      if (
        saved?.scene === home &&
        saved.path === location.pathname &&
        Date.now() - saved.at < 4000 &&
        Number.isFinite(saved.elapsed)
      ) {
        return clamp(saved.elapsed, 0, duration);
      }
    } catch {
      // Direct entry and browsers without storage start at the first frame.
    }
    return 0;
  }
  let current = home;
  let previous;
  let previousTime = 1;
  let elapsed = openingTime();
  let lastFrame = 0;
  let frame = 0;
  let visible = true;
  const motionAllowed = () => !reduced.matches && document.documentElement.dataset.motion !== "reduce";

  function markScene(name) {
    study.dataset.activeScene = name;
    study.style.setProperty("--study-transition", "art-" + name);
  }

  function paint() {
    ctx.setTransform(canvas.width / W, 0, 0, canvas.height / H, 0, 0);
    ctx.clearRect(0, 0, W, H);
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    const t = clamp(elapsed / duration);
    const mix = clamp(elapsed / 190);
    if (previous && mix < 1) drawScene(previous, previousTime, 1 - mix);
    if (t < 0.55) drawScene(current, 1, 0.22 * (1 - ease(t / 0.55)) * (previous ? mix : 1));
    drawScene(current, t, previous ? mix : 1);
  }
  function tick(now) {
    frame = 0;
    if (!visible || document.hidden) return;
    if (lastFrame) elapsed = Math.min(duration, elapsed + Math.min(now - lastFrame, 80));
    lastFrame = now;
    paint();
    if (elapsed < duration) frame = requestAnimationFrame(tick);
  }
  function schedule() {
    cancelAnimationFrame(frame);
    frame = 0;
    lastFrame = 0;
    if (!motionAllowed()) elapsed = duration;
    if (visible && !document.hidden) {
      paint();
      if (elapsed < duration) frame = requestAnimationFrame(tick);
    }
    replay.hidden = !motionAllowed();
  }
  function play(name) {
    previousTime = clamp(elapsed / duration);
    previous = current === name ? null : current;
    current = name;
    markScene(name);
    elapsed = motionAllowed() ? 0 : duration;
    schedule();
  }
  function resize() {
    const rect = study.getBoundingClientRect();
    const density = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(1, Math.round(rect.width * density));
    canvas.height = Math.max(1, Math.round(rect.height * density));
    paint();
  }

  markScene(home);
  study.hidden = false;
  resize();
  new ResizeObserver(resize).observe(study);
  new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    schedule();
  }).observe(study);
  reduced.addEventListener("change", schedule);
  document.addEventListener("visibilitychange", schedule);
  window.addEventListener("mystic:preferences", () => {
    palette = themePalette();
    schedule();
  });
  window.addEventListener("pagehide", () => {
    cancelAnimationFrame(frame);
    frame = 0;
  });
  window.addEventListener("pageshow", schedule);
  replay.addEventListener("click", () => play(current));
  schedule();

  study.addEventListener("pointermove", (event) => {
    if (!motionAllowed() || event.pointerType !== "mouse") return;
    const bounds = study.getBoundingClientRect();
    study.style.setProperty(
      "--yaw",
      (((event.clientX - bounds.left) / bounds.width) * 7 - 3.5).toFixed(2) + "deg",
    );
    study.style.setProperty(
      "--pitch",
      (2.5 - ((event.clientY - bounds.top) / bounds.height) * 5).toFixed(2) + "deg",
    );
  });
  study.addEventListener("pointerleave", () => {
    study.style.removeProperty("--yaw");
    study.style.removeProperty("--pitch");
  });

  if (home !== "welcome") return;
  let hover;
  let focused;
  let pending;
  function projectFor(element) {
    const link = element?.closest?.(".project-list [data-preview], .explorer [data-file-id]");
    const id = link?.dataset.preview ?? link?.dataset.fileId;
    return Object.hasOwn(scenes, id) ? id : null;
  }
  document.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    )
      return;
    const link = event.target.closest("a");
    if (!link || current === home || projectFor(link) !== current) return;
    try {
      sessionStorage.setItem(
        handoffKey,
        JSON.stringify({
          scene: current,
          elapsed,
          path: link.pathname,
          at: Date.now(),
        }),
      );
    } catch {
      // File navigation also works without a saved frame.
    }
  });
  function select() {
    clearTimeout(pending);
    const next = hover ?? focused ?? home;
    if (next !== current) pending = setTimeout(() => play(next), 100);
  }
  document.addEventListener("pointerover", (event) => {
    if (event.pointerType === "touch") return;
    hover = projectFor(event.target);
    select();
  });
  document.addEventListener("pointerout", (event) => {
    if (!event.relatedTarget) {
      hover = null;
      select();
    }
  });
  document.addEventListener("focusin", (event) => {
    hover = null;
    focused = projectFor(event.target);
    select();
  });
  document.addEventListener("focusout", (event) => {
    focused = projectFor(event.relatedTarget);
    select();
  });
})();
