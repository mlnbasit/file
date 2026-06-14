"""
Regenerate Figure 2 (histogram) with English labels.
Run this script in the same folder as music.wav and hidden.wav.
Output: fig_diff_hist_fulll.png (replaces the old one)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import wave, struct

def read_wav_raw(path):
    """Read raw PCM bytes from WAV, skipping the 44-byte header."""
    with open(path, 'rb') as f:
        f.read(44)  # skip header
        raw = f.read()
    return np.frombuffer(raw, dtype=np.int8)

print("Reading music.wav ...")
cover = read_wav_raw('music.wav')

print("Reading hidden.wav ...")
stego = read_wav_raw('hidden.wav')

print("Computing differences ...")
n = min(len(cover), len(stego))
diff = stego[:n].astype(np.int16) - cover[:n].astype(np.int16)

print(f"  Total bytes compared : {n:,}")
print(f"  Diff range           : [{diff.min()}, {diff.max()}]")
print(f"  Non-zero diffs       : {np.count_nonzero(diff):,}")

fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(diff, bins=300, color='steelblue', edgecolor='none')
ax.set_title('Histogram of Sample Differences', fontsize=12)
ax.set_xlabel('Sample Difference (stego \u2212 cover)', fontsize=10)
ax.set_ylabel('Count (Frequency)', fontsize=10)
ax.yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, _: f'{int(x):,}')
)
plt.tight_layout()
out = 'fig_diff_hist_fulll.png'
plt.savefig(out, dpi=200, bbox_inches='tight')
plt.close()
print(f"\nSaved: {out}")
