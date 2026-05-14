from __future__ import annotations

import numpy as np
from pathlib import Path
from scipy.io import loadmat


def _get_attr(obj, name: str):
    if obj is None:
        return None
    if hasattr(obj, name):
        return getattr(obj, name)
    if isinstance(obj, dict) and name in obj:
        return obj[name]
    return None


def _to_str(v) -> str:
    if isinstance(v, bytes):
        return v.decode("utf-8", errors="ignore")
    return str(v)


def main() -> None:
    mat_path = Path("e:/Matlab/Simulink/S-Function_16/data/paths/path_industrial.mat")
    if not mat_path.exists():
        raise SystemExit(f"MAT file not found: {mat_path}")

    m = loadmat(mat_path, squeeze_me=True, struct_as_record=False)
    ref = m.get("ref", None)
    if ref is None:
        raise SystemExit("ref not found in mat")

    t = np.asarray(_get_attr(ref, "t"), dtype=float)
    x = np.asarray(_get_attr(ref, "X_ref"), dtype=float)
    y = np.asarray(_get_attr(ref, "Y_ref"), dtype=float)
    psi = np.asarray(_get_attr(ref, "psi_ref"), dtype=float)
    omega = np.asarray(_get_attr(ref, "omega_ref"), dtype=float)

    meta = _get_attr(ref, "meta")
    segments = _get_attr(meta, "segments") if meta is not None else None

    ts = float(np.median(np.diff(t)))
    print(f"Loaded: {mat_path}")
    print(f"N={t.size}  Ts~={ts:.6f}  t_end={float(t[-1]):.3f}")
    print(f"Start: X={float(x[0]):.3f} Y={float(y[0]):.3f} psi={float(psi[0])*180/np.pi:.3f}deg")
    print(f"End  : X={float(x[-1]):.3f} Y={float(y[-1]):.3f} psi={float(psi[-1])*180/np.pi:.3f}deg")

    # Requirement A: end point should be about 1m left of start (same y).
    x_target = float(x[0] - 1.0)
    y_target = float(y[0])
    dx = float(x[-1] - x_target)
    dy = float(y[-1] - y_target)
    print(f"Target end (start_left_1m): X={x_target:.3f} Y={y_target:.3f}")
    print(f"End error vs target: dX={dx:.3f} dY={dy:.3f} norm={float(np.hypot(dx, dy)):.3f}")

    # Requirement B: decel segment should be straight (omega~0, psi change~0).
    if segments is None:
        print("Segments: N/A (ref.meta.segments missing)")
        return

    seg_list = np.atleast_1d(segments)
    idx_decel = None
    idx_hold = None

    for i, seg in enumerate(seg_list, start=1):
        desc = _to_str(_get_attr(seg, "desc"))
        if "末端减速" in desc:
            idx_decel = i
        if "末端保持" in desc:
            idx_hold = i

    print(f"Segments: {len(seg_list)}  decel_idx={idx_decel}  hold_idx={idx_hold}")

    def report_segment(idx: int | None, name: str) -> None:
        if idx is None:
            print(f"{name}: not found")
            return
        seg = seg_list[idx - 1]
        t0_raw = _get_attr(seg, "t0")
        if t0_raw is None:
            t0_raw = _get_attr(seg, "t_start")
        t1_raw = _get_attr(seg, "t1")
        if t1_raw is None:
            t1_raw = _get_attr(seg, "t_end")
        if t0_raw is None or t1_raw is None:
            print(f"{name} #{idx}: missing time range fields (expected t_start/t_end)")
            return
        t0 = float(t0_raw)
        t1 = float(t1_raw)
        msk = (t >= t0) & (t <= t1)
        if not np.any(msk):
            print(f"{name} #{idx}: t=[{t0:.3f},{t1:.3f}] has no samples")
            return
        om = omega[msk]
        ps = psi[msk]
        dpsi = float(ps[-1] - ps[0])
        print(f"{name} #{idx}: t=[{t0:.3f},{t1:.3f}] n={int(msk.sum())}")
        print(f"  omega_abs_max={float(np.max(np.abs(om))):.6f}  omega_abs_mean={float(np.mean(np.abs(om))):.6f}")
        print(f"  delta_psi={dpsi:.6f} rad ({dpsi*180/np.pi:.3f} deg)")

    report_segment(idx_decel, "Decel")
    report_segment(idx_hold, "Hold")


if __name__ == "__main__":
    main()
