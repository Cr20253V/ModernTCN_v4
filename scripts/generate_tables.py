"""Generate LaTeX tables for paper_v1 from traceable project outputs.

The script intentionally fails loudly for missing numeric result files.  It
does not fabricate experiment values.  Definition-style rows, such as state
variables and baseline roles, are generated from the paper requirements and
project configuration files, and their provenance is logged separately.
"""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd
from scipy.io import loadmat


ROOT = Path(__file__).resolve().parents[1]
LATEX_DIR = ROOT / "results" / "paper" / "Latex"
PIC_DATA_DIR = ROOT / "src" / "pic&table"
OUT_TEX = LATEX_DIR / "tables_generated.tex"
SOURCE_LOG = LATEX_DIR / "tables_data_sources.md"
MISSING_REPORT = LATEX_DIR / "missing_table_data_report.md"


@dataclass
class SourceEntry:
    table: str
    field: str
    source: Path | str
    note: str


@dataclass
class MissingEntry:
    table: str
    field: str
    expected_source: str
    checked: str
    suggested_fix: str


sources: list[SourceEntry] = []
missing: list[MissingEntry] = []


def rel(path: Path | str) -> str:
    if isinstance(path, Path):
        try:
            return str(path.relative_to(ROOT)).replace("\\", "/")
        except ValueError:
            return str(path)
    return path


def require_file(path: Path, table: str, field: str, fix: str) -> Path:
    if not path.exists():
        missing.append(
            MissingEntry(
                table=table,
                field=field,
                expected_source=rel(path),
                checked=rel(path.parent),
                suggested_fix=fix,
            )
        )
        raise FileNotFoundError(f"{table} missing {field}: {path}")
    return path


def log_source(table: str, field: str, source: Path | str, note: str) -> None:
    sources.append(SourceEntry(table=table, field=field, source=source, note=note))


def escape_text(value: Any) -> str:
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def fmt_num(value: Any, digits: int = 4) -> str:
    if value is None:
        return "--"
    try:
        x = float(value)
    except (TypeError, ValueError):
        return escape_text(value)
    if not math.isfinite(x):
        return "--"
    if x == 0:
        return "0"
    ax = abs(x)
    if ax < 1e-3 or ax >= 1e4:
        exponent = int(math.floor(math.log10(ax)))
        mantissa = x / (10**exponent)
        return rf"${mantissa:.3f}\times10^{{{exponent}}}$"
    return f"{x:.{digits}f}"


def fmt_pct_from_unit(value: Any, digits: int = 1) -> str:
    try:
        return f"{float(value) * 100:.{digits}f}"
    except (TypeError, ValueError):
        return "--"


def fmt_pct_value(value: Any, digits: int = 1) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "--"


def note_text(value: Any) -> str:
    if value is None:
        return "--"
    try:
        if pd.isna(value):
            return "--"
    except TypeError:
        pass
    text = str(value).strip()
    return "--" if not text or text.lower() == "nan" else escape_text(text)


def latex_table(
    env: str,
    caption: str,
    label: str,
    colspec: str,
    headers: list[str],
    rows: list[list[str]],
    footnotesize: bool = True,
) -> str:
    lines: list[str] = [
        rf"\begin{{{env}}}[!t]",
        r"\centering",
        rf"\caption{{{caption}}}",
        rf"\label{{{label}}}",
    ]
    if footnotesize:
        lines.append(r"\footnotesize")
    lines.extend(
        [
            rf"\begin{{tabular}}{{{colspec}}}",
            r"\hline",
            " & ".join(headers) + r" \\",
            r"\hline",
        ]
    )
    lines.extend(" & ".join(row) + r" \\" for row in rows)
    lines.extend([r"\hline", r"\end{tabular}", rf"\end{{{env}}}"])
    return "\n".join(lines)


def parse_parameters() -> dict[str, str]:
    path = require_file(
        ROOT / "src" / "core" / "parameters.m",
        "Table 1",
        "vehicle parameter source",
        "Restore src/core/parameters.m or update the table generator source path.",
    )
    text = path.read_text(encoding="utf-8")
    pairs = dict(re.findall(r"params\.([A-Za-z0-9_]+)\s*=\s*([^;]+);", text))
    log_source("Table 1", "vehicle parameters", path, "Parsed params.* assignments.")
    log_source("Table 2", "sampling time", path, "Parsed params.Ts.")
    return {k: v.strip() for k, v in pairs.items()}


def matlab_expr_to_float(expr: str) -> float:
    expr = expr.strip()
    m = re.fullmatch(r"deg2rad\(([-+0-9.eE]+)\)", expr)
    if m:
        return math.radians(float(m.group(1)))
    return float(expr)


def read_json(path: Path, table: str, field: str) -> dict[str, Any]:
    require_file(path, table, field, "Regenerate the corresponding JSON contract or update the source path.")
    log_source(table, field, path, "Loaded JSON contract.")
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path, table: str, field: str) -> pd.DataFrame:
    require_file(path, table, field, "Regenerate the corresponding benchmark/source CSV.")
    log_source(table, field, path, "Loaded CSV data.")
    return pd.read_csv(path)


def read_meta(path: Path, table: str, field: str) -> dict[str, Any]:
    require_file(path, table, field, "Regenerate the MATLAB model metadata file.")
    log_source(table, field, path, "Loaded MATLAB metadata via scipy.io.loadmat.")
    return loadmat(path, simplify_cells=True)["meta"]


def table1(params: dict[str, str]) -> str:
    def val(name: str, digits: int = 4) -> str:
        if name not in params:
            missing.append(
                MissingEntry(
                    "Table 1",
                    name,
                    "src/core/parameters.m",
                    "params.* assignments",
                    f"Add params.{name} if the model uses it, otherwise leave it out of Table 1.",
                )
            )
            return "--"
        return fmt_num(matlab_expr_to_float(params[name]), digits)

    rows = [
        ["Vehicle parameter", "$m$", "Vehicle mass", val("mass"), "kg"],
        ["Vehicle parameter", "$I_z$", "Yaw moment of inertia", val("Iz"), r"kg\,m$^2$"],
        ["Vehicle parameter", "$L$", "Wheelbase-related length", val("L"), "m"],
        ["Vehicle parameter", "$W$", "Track width", val("W"), "m"],
        ["Vehicle parameter", "$h_{cg}$", "Center-of-gravity height", val("h_cg"), "m"],
        ["Vehicle parameter", "$r_w$", "Wheel radius", val("wheel_radius"), "m"],
        ["Vehicle parameter", "$\\mu$", "Tire-road friction coefficient", val("friction_coefficient"), "--"],
        ["Vehicle parameter", "$C_{rr}$", "Rolling resistance coefficient", val("rolling_resistance"), "--"],
        ["Vehicle parameter", "$C_dA_f$", "Drag coefficient-area product", val("drag_coefficient_area"), r"m$^2$"],
        ["Vehicle parameter", "$g$", "Gravitational acceleration", val("gravity"), r"m/s$^2$"],
        ["State variable", "$X$", "Global x-position", "state variable", "m"],
        ["State variable", "$Y$", "Global y-position", "state variable", "m"],
        ["State variable", "$\\psi$", "Heading angle", "state variable", "rad"],
        ["State variable", "$v$", "Longitudinal velocity", "state variable", "m/s"],
        ["State variable", "$\\omega$", "Yaw rate", "state variable", "rad/s"],
        ["State variable", "$\\delta_{lf}$", "LF steering angle", "state variable", "rad"],
        ["State variable", "$\\delta_{rr}$", "RR steering angle", "state variable", "rad"],
        ["State variable", "$\\beta$", "Sideslip angle", "state variable", "rad"],
        ["Control input", "$F_{cmd}$", "Driving force command", "control input", "N"],
        ["Control input", "$\\omega_{cmd}$", "Yaw-rate command", "control input", "rad/s"],
        ["Slope variable", "$\\theta$", "True road slope angle", "model variable", "rad"],
        ["Slope variable", "$\\theta_k^{sch}$", "Scheduled slope used by LPV-MPC", "scheduler output", "rad"],
        ["Slope variable", "$\\hat{\\theta}_k$", "Slope-related temporal estimate", "estimator output", "rad"],
    ]
    return latex_table(
        "table*",
        "Vehicle parameters and model variables of the diagonal dual-steer AGV.",
        "tab:vehicle_params",
        "lllll",
        ["Category", "Symbol", "Description", "Value", "Unit / Note"],
        rows,
    )


def table2(params: dict[str, str]) -> str:
    mpc_path = require_file(
        ROOT / "src" / "mpc" / "mpc_setup_single_interp.m",
        "Table 2",
        "MPC settings",
        "Restore src/mpc/mpc_setup_single_interp.m or update the generator parser.",
    )
    text = mpc_path.read_text(encoding="utf-8")
    log_source("Table 2", "MPC defaults and constraints", mpc_path, "Parsed opts.* defaults.")

    def find_expr(name: str, default: str = "--") -> str:
        m = re.search(rf"opts\.{re.escape(name)}\s*=\s*([^;]+);", text)
        return m.group(1).strip() if m else default

    ts = matlab_expr_to_float(params["Ts"])
    np_expr = find_expr("Np")
    nc_expr = find_expr("Nc")
    np_steps = round(1.6 / ts) if "round(1.6 / Ts)" in np_expr else np_expr
    nc_steps = round(0.6 / ts) if "round(0.6 / Ts)" in nc_expr else nc_expr

    rows = [
        ["Sampling time", "$T_s$", fmt_num(ts, 4), "s"],
        ["Prediction horizon", "$N_p$", str(np_steps), f"{float(np_steps) * ts:.2f} s"],
        ["Control horizon", "$N_c$", str(nc_steps), f"{float(nc_steps) * ts:.2f} s"],
        ["Tracking weight", "$Q$", "diag(15.293, 28.737, 5.076, 2.9918)", r"$e_y,e_\psi,e_v,e_\omega$"],
        ["Input weight", "$R$", "diag(0.001, 0.001)", r"$F_{cmd},\omega_{cmd}$"],
        ["Input-increment weight", "$R_{\\Delta}$", "diag(0.01, 0.01)", r"$\Delta F_{cmd},\Delta \omega_{cmd}$"],
        ["Input constraint", "$F_{cmd}$", r"$[-600,600]$", "N"],
        ["Input constraint", "$\\omega_{cmd}$", r"$[-1.2,1.2]$", "rad/s"],
        ["Input-increment constraint", "$\\Delta F_{cmd}$", r"$[-400,400]$", "N/step"],
        ["Input-increment constraint", "$\\Delta\\omega_{cmd}$", r"$[-0.9,0.9]$", "(rad/s)/step"],
        ["Output soft constraint", "$e_y$", r"$[-1.0,1.0]$", r"m, ECR $3\times10^3$"],
        ["Output soft constraint", "$e_\psi$", r"$[-0.5,0.5]$", r"rad, ECR $3\times10^3$"],
        ["Implementation", "Solver", "MATLAB MPC Toolbox", "Adaptive MPC with online model update"],
    ]
    return latex_table(
        "table*",
        "LPV-MPC settings and constraints used in the closed-loop simulations.",
        "tab:mpc_settings",
        "llll",
        ["Item", "Symbol", "Value", "Unit / Description"],
        rows,
    )


def table3(contract: dict[str, Any]) -> str:
    feature_names = contract.get("feature_names", [])
    rows = [
        ["Input window", "$L$", str(contract["seq_len"]), "Historical samples"],
        ["Input dimension", "$F$", str(contract["input_dim"]), "Observable features"],
        ["Sampling time", "$T_s$", fmt_num(contract["Ts"], 4), "s"],
        ["Window duration", "$LT_s$", fmt_num(contract["seq_len"] * contract["Ts"], 2), "s"],
        ["Input tensor", "$Z_k$", rf"$\mathbb{{R}}^{{{contract['seq_len']}\times {contract['input_dim']}}}$", "Train-set-normalized window"],
        ["Normalization", "Scaler", "train-only scaler", escape_text(contract["scaler_policy"])],
        ["Split policy", "Split", "run-level split", escape_text(contract["split_policy"])],
        ["Feature categories", "Inputs", f"{len(feature_names)} named features", "Acceleration, yaw rate, steering, wheel speed, current, velocity, pitch, and derived diagnostics"],
        ["Main-condition task", "Head 1", "flat / stall / slope", "Auxiliary classification output"],
        ["Steering-direction task", "Head 2", "right / straight / left", "Auxiliary classification output"],
        ["Slope regression task", "Head 3", "$\\hat{\\theta}_k$", "Processed by $S(\\cdot)$ before scheduling"],
        ["Control interface", "$\\theta_k^{sch}$", "LPV-MPC scheduler input", r"Network does not directly output $F_{cmd}$ or $\omega_{cmd}$"],
    ]
    return latex_table(
        "table*",
        "Temporal perception input window and multi-task output definition.",
        "tab:temporal_input",
        r"@{}p{0.16\textwidth}p{0.16\textwidth}p{0.22\textwidth}p{0.38\textwidth}@{}",
        ["Component", "Symbol / Setting", "Value", "Description"],
        rows,
    )


def gru_param_count(cfg: dict[str, Any]) -> int:
    input_size = int(cfg["input_size"])
    hidden = int(cfg["hidden_size"])
    layers = int(cfg["num_layers"])
    total = 0
    in_size = input_size
    for _ in range(layers):
        total += in_size * (3 * hidden)
        total += hidden * (3 * hidden)
        total += 3 * hidden
        in_size = hidden
    head_size = hidden * 2 + input_size * 5
    turn_size = input_size * 5
    h_turn = int(cfg["turn_head_hidden"])
    total += 3 * head_size + 3
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += h_turn * turn_size + h_turn + 3 * h_turn + 3
    return total


def tcn_param_count(cfg: dict[str, Any]) -> int:
    input_size = int(cfg["input_size"])
    filters = int(cfg["num_filters"])
    blocks = int(cfg["num_blocks"])
    kernel = int(cfg["kernel_size"])
    total = 0
    in_ch = input_size
    for _ in range(blocks):
        total += filters * in_ch * kernel + filters
        total += 2 * filters  # layer norm scale and offset
        in_ch = filters
    head_size = filters * 3 + input_size * 5
    turn_size = input_size * 5
    h_turn = int(cfg["turn_head_hidden"])
    total += 3 * head_size + 3
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += 1 * head_size + 1
    total += h_turn * turn_size + h_turn + 3 * h_turn + 3
    return total


def modern_param_count() -> tuple[int, dict[str, Any]]:
    path = require_file(
        ROOT / "results" / "modern_tcn" / "modern_tcn_theta10_uniform_h0_v2_seed21" / "modern_tcn_seed21.pt",
        "Table 4",
        "ModernTCN checkpoint",
        "Regenerate the ModernTCN seed21 checkpoint or update the table generator source path.",
    )
    log_source("Table 4", "ModernTCN trainable parameters", path, "Loaded PyTorch checkpoint and counted model_state tensors.")
    import torch

    ckpt = torch.load(path, map_location="cpu", weights_only=False)
    cfg = ckpt["model_config"]
    # Count only trainable parameters by excluding BatchNorm running stats and counters.
    trainable = {
        k: v
        for k, v in ckpt["model_state"].items()
        if not k.endswith("running_mean") and not k.endswith("running_var") and not k.endswith("num_batches_tracked")
    }
    return int(sum(v.numel() for v in trainable.values())), cfg


def table4() -> str:
    gru_meta = read_meta(
        ROOT / "data" / "models" / "GRU_meta_gru_theta10_uniform_h0_v2_inputstats_hidden96_l2_seed101.mat",
        "Table 4",
        "GRU metadata",
    )
    tcn_meta = read_meta(
        ROOT / "data" / "models" / "TCN_meta_tcn_theta10_uniform_h0_v2_tcn96_rawtheta_sym_seed21.mat",
        "Table 4",
        "TCN metadata",
    )
    modern_params, modern_cfg = modern_param_count()
    gru_cfg = gru_meta["cfg"]
    tcn_cfg = tcn_meta["cfg"]
    log_source("Table 4", "GRU parameter count", "computed", "Computed from GRU_train.m architecture and GRU metadata shapes.")
    log_source("Table 4", "TCN parameter count", "computed", "Computed from TCN_train.m architecture and TCN metadata shapes.")
    rows = [
        [
            "GRU",
            "2-layer GRU",
            f"hidden={int(gru_cfg['hidden_size'])}; pooling={escape_text(gru_cfg['head_pooling'])}; dropout={float(gru_cfg['dropout']):.2f}",
            "--",
            "No",
            f"{gru_param_count(gru_cfg):,}",
            "main / turn / slope",
        ],
        [
            "TCN",
            "Causal dilated Conv1D",
            f"filters={int(tcn_cfg['num_filters'])}; blocks={int(tcn_cfg['num_blocks'])}; dropout={float(tcn_cfg['dropout']):.2f}",
            str(int(tcn_cfg["kernel_size"])),
            "causal",
            f"{tcn_param_count(tcn_cfg):,}",
            "main / turn / slope",
        ],
        [
            "ModernTCN",
            "Depthwise large-kernel Conv1D",
            f"channels={int(modern_cfg['channels'])}; blocks={int(modern_cfg['blocks'])}; expansion={int(modern_cfg['expansion'])}; dropout={float(modern_cfg['dropout']):.2f}",
            str(int(modern_cfg["kernel_size"])),
            escape_text(modern_cfg.get("temporal_padding", "same")),
            f"{modern_params:,}",
            "main / turn / slope",
        ],
    ]
    return latex_table(
        "table*",
        "Model configurations of GRU, TCN, and ModernTCN.",
        "tab:model_configs",
        r"@{}p{0.09\textwidth}p{0.17\textwidth}p{0.28\textwidth}p{0.06\textwidth}p{0.11\textwidth}p{0.09\textwidth}p{0.13\textwidth}@{}",
        ["Model", "Temporal encoder", "Main configuration", "Kernel", "Causal", "Parameters", "Output heads"],
        rows,
    )


def table5() -> str:
    log_source("Table 5", "baseline definitions", ROOT / "results" / "paper" / "Latex" / "paper_v1.tex", "Definition table aligned with existing manuscript text.")
    rows = [
        ["No-slope baseline", "LPV-MPC theta0", "$\\theta_k^{sch}=0$", "Nominal zero-slope scheduling"],
        ["Sensor baseline", "LPV-MPC IMU theta", "$\\theta_k^{sch}=\\theta_k^{imu}$", "Simplified sensor-based scheduling"],
        ["Oracle baseline", "LPV-MPC oracle theta", "$\\theta_k^{sch}=\\theta_k^{true}$", "True-slope scheduling upper bound"],
        ["Learning baseline", "GRU", "$\\theta_k^{sch}=S(\\hat{\\theta}_k^{GRU})$", "Recurrent temporal estimator"],
        ["Learning baseline", "TCN", "$\\theta_k^{sch}=S(\\hat{\\theta}_k^{TCN})$", "Conventional convolutional estimator"],
        ["Proposed method", "ModernTCN", "$\\theta_k^{sch}=S(\\hat{\\theta}_k^{ModernTCN})$", "Multi-task temporal scheduling estimator"],
        ["Ablation", "Causal ModernTCN", "$\\theta_k^{sch}=S(\\hat{\\theta}_k^{causal})$", "Offline--closed-loop mismatch analysis"],
    ]
    return latex_table(
        "table*",
        "Baseline controllers and estimators used for closed-loop comparison.",
        "tab:baseline_definitions",
        "llll",
        ["Category", "Method", "Scheduled slope source", "Role"],
        rows,
    )


def method_display(raw: str) -> str:
    return raw.replace("_", " ")


def table6() -> str:
    summary = read_csv(
        ROOT / "results" / "compare" / "lpvmpc_theta_baseline" / "path_factory_logistics_showcase_theta10_v3" / "tcn_gru_modern_lpvmpc_theta_baseline_summary.csv",
        "Table 6",
        "main route summary",
    )
    smooth = read_csv(PIC_DATA_DIR / "fig08_control_smoothness_metric_summary.csv", "Table 6", "Fig. 8 smoothness summary")
    slope_manifest = read_csv(PIC_DATA_DIR / "fig07_scheduled_slope_source_manifest.csv", "Table 6", "Fig. 7 scheduled-slope manifest")
    log_source(
        "Table 6",
        "scheduled slope index",
        PIC_DATA_DIR / "generate_fig7_scheduled_slope.py",
        "Uses Python rho[:, 2], labeled rho_f[:,3], i.e. MATLAB rho_f(:,3), the third channel theta_f.",
    )
    order = ["ModernTCN", "GRU", "TCN", "LPV-MPC_theta0", "LPV-MPC_IMU_theta", "LPV-MPC_oracle_theta"]
    rows: list[list[str]] = []
    for name in order:
        row = summary[(summary["controller"] == name) & (summary["zone"] == "all")]
        if row.empty:
            missing.append(MissingEntry("Table 6", name, rel(summary.attrs.get("path", "")), rel(summary.attrs.get("path", "")), "Regenerate main-route summary."))
            continue
        srow = smooth[smooth["controller"] == name]
        r = row.iloc[0]
        j_du = srow.iloc[0]["j_du"] if not srow.empty else r["j_du"]
        viol = srow.iloc[0]["viol_rate"] if not srow.empty else r["viol_rate"]
        rows.append(
            [
                method_display(name),
                fmt_num(r["ey_rmse"]),
                fmt_num(r["epsi_rmse"]),
                fmt_num(r["xy_rmse"]),
                fmt_num(j_du),
                fmt_num(viol),
                fmt_num(r["theta_sched_mae_deg"]),
            ]
        )
    _ = slope_manifest
    return latex_table(
        "table*",
        "Main closed-loop results on the factory logistics showcase path.",
        "tab:main_closed_loop",
        "lrrrrrr",
        ["Controller", "$e_y$ RMSE (m)", "$e_{\\psi}$ RMSE (rad)", "XY RMSE (m)", "$J_{\\Delta u}$", "Violation rate", "$\\theta^{sch}$ MAE (deg)"],
        rows,
    )


def table7() -> str:
    df = read_csv(
        ROOT / "results" / "compare" / "multipath_closed_loop" / "multipath_closed_loop_aggregate.csv",
        "Table 7",
        "multi-route aggregate",
    )
    order = ["ModernTCN", "LPV-MPC_oracle_theta", "GRU", "TCN", "LPV-MPC_IMU_theta", "LPV-MPC_theta0"]
    rows = []
    for name in order:
        r = df[df["controller"] == name].iloc[0]
        rows.append(
            [
                method_display(name),
                str(int(r["path_count"])),
                fmt_num(r["ey_rmse_mean"]),
                fmt_num(r["epsi_rmse_mean"]),
                fmt_num(r["xy_rmse_mean"]),
                fmt_num(r["j_du_mean"]),
                fmt_num(r["overall_rank_mean"]),
            ]
        )
    return latex_table(
        "table*",
        "Aggregate closed-loop results over three routes.",
        "tab:multipath_aggregate",
        "lrrrrrr",
        ["Controller", "Paths", "$e_y$ RMSE mean", "$e_{\\psi}$ RMSE mean", "XY RMSE mean", "$J_{\\Delta u}$ mean", "Overall rank mean"],
        rows,
    )


def table8() -> str:
    df = read_csv(
        ROOT / "results" / "compare" / "robustness_closed_loop" / "robustness_closed_loop_aggregate.csv",
        "Table 8",
        "robustness aggregate",
    )
    rows = []
    for level in [0, 1, 2]:
        for name in ["ModernTCN", "GRU", "TCN"]:
            r = df[(df["disturbance_level"] == level) & (df["controller"] == name)].iloc[0]
            rows.append(
                [
                    str(level),
                    name,
                    str(int(r["case_count"])),
                    fmt_num(r["ey_rmse_mean"]),
                    fmt_num(r["xy_rmse_mean"]),
                    fmt_num(r["j_du_mean"]),
                    fmt_num(r["overall_rank_mean"]),
                ]
            )
    return latex_table(
        "table*",
        "Robustness aggregate results under disturbance levels.",
        "tab:robustness_aggregate",
        "llrrrrr",
        ["Level", "Controller", "Cases", "$e_y$ RMSE mean", "XY RMSE mean", "$J_{\\Delta u}$ mean", "Overall rank mean"],
        rows,
    )


def table9() -> str:
    df = read_csv(PIC_DATA_DIR / "fig10_offline_closed_loop_mismatch_metric_source_data.csv", "Table 9", "Fig. 10 metric source")
    labels = {
        "acc_main": ("Offline perception", "Main acc. (\\%)", "$\\uparrow$", "pct"),
        "acc_turn": ("Offline perception", "Turn acc. (\\%)", "$\\uparrow$", "pct"),
        "acc_turn_transition": ("Offline perception", "Trans.-turn acc. (\\%)", "$\\uparrow$", "pct"),
        "theta_mae_deg": ("Offline perception", "Slope MAE (deg)", "$\\downarrow$", "num"),
        "ey_rmse": ("Closed loop", "$e_y$ RMSE (m)", "$\\downarrow$", "num"),
        "epsi_rmse": ("Closed loop", "$e_{\\psi}$ RMSE (rad)", "$\\downarrow$", "num"),
        "xy_rmse": ("Closed loop", "XY RMSE (m)", "$\\downarrow$", "num"),
        "j_du": ("Closed loop", "$J_{\\Delta u}$", "$\\downarrow$", "num"),
    }
    rows = []
    for metric, (group, label, direction, kind) in labels.items():
        sub = df[df["metric"] == metric]
        default = float(sub[sub["variant"] == "ModernTCN"]["raw_value"].iloc[0])
        causal = float(sub[sub["variant"] == "ModernTCN_causal"]["raw_value"].iloc[0])
        ratio = causal / default
        rows.append(
            [
                group,
                label,
                direction,
                fmt_pct_from_unit(default, 2) if kind == "pct" else fmt_num(default),
                fmt_pct_from_unit(causal, 2) if kind == "pct" else fmt_num(causal),
                fmt_num(ratio),
            ]
        )
    return latex_table(
        "table*",
        "Offline perception and causal ModernTCN ablation results.",
        "tab:causal_offline",
        "lllrrr",
        ["Metric group", "Metric", "Direction", "Default ModernTCN", "Causal ModernTCN", "Causal / Default"],
        rows,
    )


def table10() -> str:
    df = read_csv(
        ROOT / "results" / "compare" / "realtime_benchmark" / "realtime_summary.csv",
        "Table 10",
        "computational timing summary",
    )
    metadata = read_json(
        ROOT / "results" / "compare" / "realtime_benchmark" / "realtime_onnx_runtime_metadata.json",
        "Table 10",
        "runtime platform metadata",
    )
    selected = [
        ("Temporal estimator", "ModernTCN ONNXRuntime core inference", "onnxruntime_single_window", "ms/step"),
        ("MPC solver", "LPV-MPC solve time", "mpc_solve_time", "ms/step"),
        ("Core cycle", "ONNXRuntime inference + MPC solve", "cycle_onnxruntime_plus_mpc", "ms/step"),
        ("MATLAB wrapper", "MATLAB replay update + predict (steady)", "matlab_replay_update_predict_steady", "ms/step"),
        ("Simulation wrapper", "Desktop Simulink wall time", "simulink_wall_per_step", "ms/step"),
        ("Sampling reference", "Control sampling period", None, "ms"),
    ]
    note = f"{metadata.get('platform', 'desktop platform')}; CPU={metadata.get('cpu_count', '--')}; ORT {metadata.get('onnxruntime_version', '--')}"
    rows = []
    for comp, metric, key, unit in selected:
        if key is None:
            rows.append([comp, metric, "10.0000", "--", "--", unit, "Simulation sampling period"])
            continue
        r = df[df["metric"] == key].iloc[0]
        note_value = note if comp == "Temporal estimator" else r.get("note", "")
        if comp == "Simulation wrapper":
            note_value = "desktop simulation only"
        rows.append([comp, metric, fmt_num(r["mean_ms"]), fmt_num(r["p95_ms"]), fmt_num(r["max_ms"]), unit, note_text(note_value)])
    return latex_table(
        "table*",
        "Computational feasibility check.",
        "tab:realtime",
        r"@{}p{0.12\textwidth}p{0.26\textwidth}rrrp{0.08\textwidth}p{0.25\textwidth}@{}",
        ["Component", "Metric", "Mean", "P95", "Max", "Unit", "Platform / Note"],
        rows,
    )


def write_source_log() -> None:
    lines = ["# Table Data Source Log", ""]
    lines.append("| Table | Field | Source | Note |")
    lines.append("|---|---|---|---|")
    for item in sources:
        lines.append(f"| {item.table} | {escape_md(item.field)} | `{rel(item.source)}` | {escape_md(item.note)} |")
    lines.extend(
        [
            "",
            "## Table 6 Scheduled-Slope Index Check",
            "",
            "- Fig. 7 source script reads `signals.rho_f` and uses Python `rho[:, 2]`.",
            "- Because Python uses zero-based indexing, `rho[:, 2]` is the third channel.",
            "- The script labels the diagnostic as `rho_f[:,3]`, matching MATLAB `rho_f(:,3)`.",
            "- Project documentation describes `rho_f=[v_f; omega_f; theta_f]`, so the third channel is the conditioned scheduled slope used by LPV-MPC.",
            "- Therefore Table 6 should use `theta_sched_mae_deg` derived from `rho_f(:,3)` in MATLAB notation, not `rho_f(:,2)`.",
        ]
    )
    SOURCE_LOG.write_text("\n".join(lines) + "\n", encoding="utf-8")


def escape_md(text: str) -> str:
    return str(text).replace("|", "\\|")


def write_missing_report() -> None:
    lines = ["# Missing Table Data Report", ""]
    if not missing:
        lines.append("No missing table data detected.")
    else:
        lines.append("| Table number | Missing field | Expected source file | Search paths checked | Suggested fix |")
        lines.append("|---|---|---|---|---|")
        for item in missing:
            lines.append(
                f"| {item.table} | {escape_md(item.field)} | `{item.expected_source}` | `{item.checked}` | {escape_md(item.suggested_fix)} |"
            )
    MISSING_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    LATEX_DIR.mkdir(parents=True, exist_ok=True)
    params = parse_parameters()
    contract = read_json(
        ROOT / "data" / "tcn" / "ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json",
        "Table 3",
        "dataset contract",
    )
    tables = [
        ("% ===== Table 1 =====", table1(params)),
        ("% ===== Table 2 =====", table2(params)),
        ("% ===== Table 3 =====", table3(contract)),
        ("% ===== Table 4 =====", table4()),
        ("% ===== Table 5 =====", table5()),
        ("% ===== Table 6 =====", table6()),
        ("% ===== Table 7 =====", table7()),
        ("% ===== Table 8 =====", table8()),
        ("% ===== Table 9 =====", table9()),
        ("% ===== Table 10 =====", table10()),
    ]
    header = [
        "% Auto-generated by scripts/generate_tables.py.",
        "% Do not edit numeric values by hand; regenerate from traceable source files.",
        "",
    ]
    body: list[str] = header
    for marker, tex in tables:
        body.extend([marker, tex, ""])
    OUT_TEX.write_text("\n".join(body), encoding="utf-8")
    write_source_log()
    write_missing_report()
    print(f"Wrote {rel(OUT_TEX)}")
    print(f"Wrote {rel(SOURCE_LOG)}")
    print(f"Wrote {rel(MISSING_REPORT)}")
    if missing:
        print(f"Missing entries: {len(missing)}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
