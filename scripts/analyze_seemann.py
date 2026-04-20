"""
Replicate the in-browser audio-reactive predator logic against seemann.mp3
and plot the resulting energy curves + predator-active windows.

Mirrors index.html:
  - AnalyserNode: fftSize=256 (=> 128 bins), smoothingTimeConstant=0.6
  - Analysis tick: ~10 Hz (every 6 frames at 60 fps)
  - Bands: low = first 18% of bins, high = last 55% of bins
  - Spawn:  total>52 && highMean>22  ||  total>baseline*1.12 && highMean>18
  - Calm:   total<40 && highMean<18
  - Baseline: rolling avg, 0.997 / 0.003 mix per tick
"""
import numpy as np
import matplotlib.pyplot as plt
import librosa
from pathlib import Path

MP3 = Path(__file__).parent.parent / "audio" / "seemann.mp3"
OUT = Path(__file__).parent / "seemann_analysis.png"

FFT       = 256                 # matches analyser.fftSize
BIN_COUNT = FFT // 2            # 128 frequency bins
SMOOTH    = 0.6                 # matches smoothingTimeConstant
TICK_HZ   = 10.0                # ~ every 6 frames at 60 fps
HOP_S     = 1.0 / TICK_HZ       # 0.1 s between analyser reads
LOW_END   = int(BIN_COUNT * 0.18)   # 23
HIGH_START= int(BIN_COUNT * 0.45)   # 57

# Exact thresholds used in page (calibrated against user perceptual data)
SPAWN_ABS = lambda total, high:  total > 100 and high > 30
SPAWN_DYN = lambda total, high, base:  total > base * 1.30 and high > 28
CALM      = lambda total, high:  total < 92 or high < 22

print(f"Loading {MP3.name}...")
y, sr = librosa.load(MP3, sr=44100, mono=True)
duration = len(y) / sr
print(f"  duration = {duration:.1f}s, sr = {sr}")

# Compute STFT with hop matching our 10 Hz tick
hop = int(sr * HOP_S)             # ~4410 samples
S = np.abs(librosa.stft(y, n_fft=FFT, hop_length=hop, window="hann"))
# S has shape (BIN_COUNT+1, n_frames); drop the Nyquist bin to get 128
S = S[:BIN_COUNT, :]

# Web Audio's getByteFrequencyData maps dB into 0-255 using
#   value = 255 * (db - minDecibels) / (maxDecibels - minDecibels)
# defaults: minDecibels = -100, maxDecibels = -30
db = 20 * np.log10(np.maximum(S, 1e-10))
mn, mx = -100.0, -30.0
byte = np.clip(255.0 * (db - mn) / (mx - mn), 0, 255)

# Apply analyser's exponential smoothing across time (per bin)
# Web Audio formula: x_smoothed[t] = SMOOTH * x_smoothed[t-1] + (1-SMOOTH) * x_raw[t]
smoothed = np.zeros_like(byte)
smoothed[:, 0] = byte[:, 0] * (1 - SMOOTH)
for t in range(1, byte.shape[1]):
    smoothed[:, t] = SMOOTH * smoothed[:, t-1] + (1 - SMOOTH) * byte[:, t]

# Per-tick aggregates
low_mean  = smoothed[:LOW_END, :].mean(axis=0)
high_mean = smoothed[HIGH_START:, :].mean(axis=0)
total     = smoothed.mean(axis=0)
times     = np.arange(byte.shape[1]) * HOP_S

# Walk the rolling baseline + spawn/calm logic just like the JS does
baseline = np.zeros_like(total)
predator_active = np.zeros_like(total, dtype=bool)
preds_alive = 0   # mirror of "currentPreds.length"
MAX_PREDS = 3
PREDATOR_LIFETIME_TICKS = 30  # rough — JS keeps them while alpha>0; ~3s feels right

# Track when each predator was spawned to age them out if calm
remaining = []
b = 0.0
for i in range(len(total)):
    b = b * 0.997 + total[i] * 0.003
    baseline[i] = b
    energetic = SPAWN_ABS(total[i], high_mean[i]) or SPAWN_DYN(total[i], high_mean[i], b)
    calm      = CALM(total[i], high_mean[i])

    # Spawn
    if energetic and len(remaining) < MAX_PREDS:
        remaining.append(PREDATOR_LIFETIME_TICKS)

    # Despawn on calm
    if calm:
        remaining = []

    # Tick lifetimes
    remaining = [r - 1 for r in remaining if r - 1 > 0]
    predator_active[i] = len(remaining) > 0

# ===== PLOT =====
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor("#0a0e17")
ax.set_facecolor("#0f1623")

# Pink shaded blocks where predators are active
in_block = False
start = 0
for i, active in enumerate(predator_active):
    if active and not in_block:
        start = times[i]; in_block = True
    elif not active and in_block:
        ax.axvspan(start, times[i], color="#ff4fae", alpha=0.22, lw=0)
        in_block = False
if in_block:
    ax.axvspan(start, times[-1], color="#ff4fae", alpha=0.22, lw=0)

# Energy curves
ax.plot(times, total,     color="#38bdf8", lw=1.4, label="total mean (whole spectrum)")
ax.plot(times, high_mean, color="#a78bfa", lw=1.2, label="highMean (45-100% bins)")
ax.plot(times, low_mean,  color="#fbbf24", lw=1.0, alpha=0.7, label="lowMean (0-18% bins)")
ax.plot(times, baseline,  color="#94a3b8", lw=1.0, ls="--", label="rolling baseline")

# Threshold reference lines (calibrated)
ax.axhline(100, color="#22c55e", lw=0.8, ls=":", alpha=0.7)
ax.text(duration * 0.995, 100, " spawn: total>100", color="#22c55e", fontsize=8,
        va="center", ha="right")
ax.axhline(90, color="#ef4444", lw=0.8, ls=":", alpha=0.7)
ax.text(duration * 0.995, 90, " calm: total<90", color="#ef4444", fontsize=8,
        va="center", ha="right")
ax.axhline(32, color="#f97316", lw=0.8, ls=":", alpha=0.7)
ax.text(duration * 0.995, 32, " spawn: high>32", color="#f97316", fontsize=8,
        va="center", ha="right")
ax.axhline(22, color="#a78bfa", lw=0.8, ls=":", alpha=0.5)
ax.text(duration * 0.995, 22, " calm: high<22", color="#a78bfa", fontsize=8,
        va="center", ha="right")

# Mark user's perceptual reference points
user_pts = [
    (62,   "calm intro (you)"),
    (62,   None),  # ~1:02
    (180,  "intense (you)"),
    (185,  "soft drop (you)"),
    (207,  "still soft"),
    (212,  "intensity returns"),
    (269,  "soft outro"),
]
ref = [(62, "intense ↑"), (185, "soft ↓"), (207, "soft"),
       (212, "intense ↑"), (269, "soft outro")]
for t, label in ref:
    ax.axvline(t, color="#fde047", lw=0.6, alpha=0.5)
    ax.text(t, ax.get_ylim()[1] * 0.93, label, color="#fde047",
            fontsize=7.5, rotation=90, va="top", ha="right")

ax.set_xlim(0, duration)
ax.set_ylim(0, max(total.max(), 100) * 1.05)
ax.set_xlabel("song time (seconds)", color="#e2e8f0")
ax.set_ylabel("byte-scale intensity (0-255)", color="#e2e8f0")
ax.set_title("Apocalyptica ft. Nina Hagen — Seemann\n"
             "spectral energy + predator-active windows (pink)",
             color="#e2e8f0", pad=12)
ax.tick_params(colors="#94a3b8")
for s in ax.spines.values():
    s.set_color("#1e293b")
ax.grid(True, color="#1e293b", lw=0.5, alpha=0.6)

leg = ax.legend(loc="upper right", facecolor="#0a0e17", edgecolor="#1e293b",
                labelcolor="#e2e8f0", fontsize=9)

# Stats footer
n_blocks = 0; total_pred_time = 0.0
in_b = False; b_start = 0
for i, a in enumerate(predator_active):
    if a and not in_b: n_blocks += 1; b_start = times[i]; in_b = True
    elif not a and in_b: total_pred_time += times[i] - b_start; in_b = False
if in_b: total_pred_time += times[-1] - b_start

footer = (f"{n_blocks} predator window(s)   |   "
          f"total active: {total_pred_time:.1f}s  "
          f"({100*total_pred_time/duration:.0f}% of song)   |   "
          f"max total: {total.max():.0f}   max high: {high_mean.max():.0f}")
fig.text(0.5, 0.012, footer, color="#94a3b8", fontsize=8.5, ha="center")

plt.tight_layout(rect=[0, 0.025, 1, 1])
plt.savefig(OUT, dpi=140, facecolor="#0a0e17")
print(f"Saved -> {OUT}")
print(f"Stats: {n_blocks} windows, total active {total_pred_time:.1f}s "
      f"({100*total_pred_time/duration:.0f}%)")
print(f"max total={total.max():.0f}, max highMean={high_mean.max():.0f}, "
      f"max lowMean={low_mean.max():.0f}")
