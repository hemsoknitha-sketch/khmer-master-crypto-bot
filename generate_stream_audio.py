#!/usr/bin/env python3
"""
ANGKOR QUANT - INSTITUTIONAL LIVE STREAM AUDIO SYNTHESIZER
===========================================================
Generates studio-grade 44.1kHz 16-bit PCM WAV chimes and ambient lofi drone
for 24/7 YouTube Live streaming using pure standard Python library.
Zero third-party audio dependencies required.
===========================================================
"""

import os
import sys
import math
import struct
import wave

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

AUDIO_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio")
SAMPLE_RATE = 44100


def _ensure_dir():
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR, exist_ok=True)


def _write_wav(filename: str, samples: list, sample_rate: int = SAMPLE_RATE):
    _ensure_dir()
    filepath = os.path.join(AUDIO_DIR, filename)
    with wave.open(filepath, "w") as wf:
        wf.setnchannels(1)  # Mono
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        packed = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(packed)
    print(f"✅ Generated Audio Asset: {filepath} ({len(samples)/sample_rate:.2f}s)")
    return filepath


def generate_buy_chime():
    """Ascending institutional crystal chime (523Hz -> 659Hz -> 784Hz -> 1046Hz)."""
    duration = 0.8
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    freqs = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        segment_idx = min(int(t / (duration / len(freqs))), len(freqs) - 1)
        base_f = freqs[segment_idx]
        
        # Envelope: Fast attack, gentle decay
        seg_t = (t % (duration / len(freqs))) / (duration / len(freqs))
        env = math.exp(-3.5 * seg_t)

        # Harmonics
        val = (
            math.sin(2.0 * math.pi * base_f * t) * 0.70
            + math.sin(2.0 * math.pi * base_f * 2.0 * t) * 0.20
            + math.sin(2.0 * math.pi * base_f * 3.0 * t) * 0.10
        )
        sample = int(32767.0 * 0.65 * env * val)
        samples.append(max(-32768, min(32767, sample)))

    return _write_wav("buy_chime.wav", samples)


def generate_sell_chime():
    """Descending institutional warning chime (1046Hz -> 784Hz -> 659Hz -> 523Hz)."""
    duration = 0.8
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    freqs = [1046.50, 783.99, 659.25, 523.25]  # C6, G5, E5, C5

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        segment_idx = min(int(t / (duration / len(freqs))), len(freqs) - 1)
        base_f = freqs[segment_idx]

        seg_t = (t % (duration / len(freqs))) / (duration / len(freqs))
        env = math.exp(-3.5 * seg_t)

        val = (
            math.sin(2.0 * math.pi * base_f * t) * 0.70
            + math.sin(2.0 * math.pi * base_f * 2.0 * t) * 0.20
            + math.sin(2.0 * math.pi * base_f * 3.0 * t) * 0.10
        )
        sample = int(32767.0 * 0.65 * env * val)
        samples.append(max(-32768, min(32767, sample)))

    return _write_wav("sell_chime.wav", samples)


def generate_tp_chime():
    """Triple Victory Chime for TP1 / TP2 hit."""
    duration = 0.9
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    freqs = [659.25, 783.99, 1318.51]  # E5, G5, E6

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        segment_idx = min(int(t / (duration / len(freqs))), len(freqs) - 1)
        base_f = freqs[segment_idx]
        seg_t = (t % (duration / len(freqs))) / (duration / len(freqs))
        env = math.exp(-3.0 * seg_t)

        val = math.sin(2.0 * math.pi * base_f * t) * 0.80 + math.sin(2.0 * math.pi * base_f * 2 * t) * 0.20
        sample = int(32767.0 * 0.70 * env * val)
        samples.append(max(-32768, min(32767, sample)))

    return _write_wav("tp_chime.wav", samples)


def generate_sl_chime():
    """Low Breaker Alert for Stop-Loss protection."""
    duration = 0.5
    total_samples = int(SAMPLE_RATE * duration)
    samples = []
    base_f = 220.0  # A3

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        env = math.exp(-4.0 * t)
        val = math.sin(2.0 * math.pi * base_f * t) * 0.85 + math.sin(2.0 * math.pi * (base_f * 0.5) * t) * 0.15
        sample = int(32767.0 * 0.50 * env * val)
        samples.append(max(-32768, min(32767, sample)))

    return _write_wav("sl_chime.wav", samples)


def generate_lofi_ambient_loop(duration_seconds: int = 30):
    """
    Synthesizes a 30s soothing ambient harmonic drone loop
    (F minor 9th chord: F, Ab, C, Eb, G) with slow LFO modulation.
    Guarantees FFmpeg always has a non-stop royalty-free audio bed.
    """
    total_samples = int(SAMPLE_RATE * duration_seconds)
    samples = []
    # F minor 9 chord frequencies: F2 (87.31), C3 (130.81), Ab3 (207.65), Eb4 (311.13), G4 (392.00)
    chord_freqs = [87.31, 130.81, 207.65, 311.13, 392.00]

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        # LFO modulation (0.1 Hz = 10s cycle)
        lfo = 0.85 + 0.15 * math.sin(2.0 * math.pi * 0.10 * t)
        # Slow filter sweep (0.05 Hz = 20s cycle)
        sweep = 0.70 + 0.30 * math.cos(2.0 * math.pi * 0.05 * t)

        val = 0.0
        weights = [0.35, 0.25, 0.20, 0.12, 0.08]
        for f, w in zip(chord_freqs, weights):
            val += w * math.sin(2.0 * math.pi * f * t)
            # Add subtle warm 2nd harmonic
            val += (w * 0.25) * math.sin(2.0 * math.pi * f * 2.0 * t)

        # Smooth loop boundary fade-in/fade-out (0.5s at edges)
        edge_fade = 1.0
        if t < 0.5:
            edge_fade = t / 0.5
        elif t > (duration_seconds - 0.5):
            edge_fade = (duration_seconds - t) / 0.5

        sample = int(32767.0 * 0.25 * lfo * sweep * edge_fade * val)
        samples.append(max(-32768, min(32767, sample)))

    return _write_wav("lofi_ambient.wav", samples)


def generate_all():
    print("🎵 [ANGKOR QUANT AUDIO] Generating stream audio assets...")
    generate_buy_chime()
    generate_sell_chime()
    generate_tp_chime()
    generate_sl_chime()
    generate_lofi_ambient_loop(30)
    print("✅ All audio assets successfully compiled in 'audio/' directory.")


if __name__ == "__main__":
    generate_all()
