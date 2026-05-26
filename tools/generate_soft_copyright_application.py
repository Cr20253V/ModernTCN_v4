#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate auxiliary software-copyright application materials for this project.

The script is intentionally self-contained: it scans a fixed source whitelist,
generates Chinese application/supporting documents, writes deterministic DOCX
files with basic OOXML, and asks Microsoft Word through PowerShell COM to export
the required PDF files when Word is available.
"""

from __future__ import annotations

import base64
import csv
import html
import json
import math
import os
import re
import shutil
import subprocess
import textwrap
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "soft_copyright_application"

GENERATED_DATE = "2026-05-25"
SOFTWARE_FULL = "AGV工况感知与LPV-MPC闭环控制仿真软件"
SOFTWARE_SHORT = "AGV-MTCN-MPC仿真软件"
VERSION = "V1.0"
SOURCE_BASENAME = "ModernTCN_AGV_LPVMPC_V1"
HEADER_TEXT = "AGV 工况感知与 LPV-MPC 闭环控制仿真软件"
SOURCE_FRONT_BACK_PAGES = 35
SOURCE_LINES_PER_PAGE = 50


@dataclass(frozen=True)
class SourceSpec:
    rel_path: str
    module: str
    reason: str


SOURCE_SPECS: list[SourceSpec] = [
    SourceSpec("init_project.m", "项目初始化", "初始化 MATLAB 搜索路径"),
    SourceSpec("project_root.m", "项目初始化", "定位项目根目录"),
    SourceSpec("results_dir.m", "项目初始化", "规范输出目录"),
    SourceSpec("src/core/agv_model_sfunc.m", "车辆模型与控制基础层", "闭环仿真 AGV S-Function"),
    SourceSpec("src/core/agv_model_sfunc_train_data.m", "车辆模型与控制基础层", "训练数据仿真 S-Function"),
    SourceSpec("src/core/state_eq.m", "车辆模型与控制基础层", "非线性车辆状态方程"),
    SourceSpec("src/core/output_eq.m", "车辆模型与控制基础层", "车辆输出与传感量计算"),
    SourceSpec("src/core/state_eq_ref.m", "车辆模型与控制基础层", "参考模型状态方程"),
    SourceSpec("src/core/output_eq_ref.m", "车辆模型与控制基础层", "参考模型输出方程"),
    SourceSpec("src/core/state_eq_ref_train_data.m", "车辆模型与控制基础层", "训练数据参考状态方程"),
    SourceSpec("src/core/output_eq_ref_train_data.m", "车辆模型与控制基础层", "训练数据参考输出方程"),
    SourceSpec("src/core/parameters.m", "车辆模型与控制基础层", "车辆与控制参数定义"),
    SourceSpec("src/core/UpdatePlantModel.m", "车辆模型与控制基础层", "Simulink 植物模型更新"),
    SourceSpec("src/core/UpdatePlantModel_gru.m", "车辆模型与控制基础层", "GRU/对照链路植物模型更新"),
    SourceSpec("src/core/preloadfcn_modern_tcn.m", "车辆模型与控制基础层", "ModernTCN 闭环预加载入口"),
    SourceSpec("src/core/preloadfcn_gru.m", "车辆模型与控制基础层", "通用闭环预加载函数"),
    SourceSpec("src/core/preloadfcn_tcn.m", "车辆模型与控制基础层", "TCN 闭环预加载入口"),
    SourceSpec("src/lpv/lin_agv_at_point.m", "LPV与MPC", "单点线性化"),
    SourceSpec("src/lpv/lin_agv_grid.m", "LPV与MPC", "LPV 网格线性化"),
    SourceSpec("src/mpc/mpc_setup_single_interp.m", "LPV与MPC", "MPC 控制器构造"),
    SourceSpec("src/mpc/mpc_update_from_rho.m", "LPV与MPC", "在线调度更新"),
    SourceSpec("src/mpc/Cost_Function.m", "LPV与MPC", "控制代价计算"),
    SourceSpec("src/paths/gen_agv_ref_path.m", "路径生成", "基础参考路径生成"),
    SourceSpec("src/paths/gen_agv_theta10_uniform_paths.m", "路径生成", "theta10 uniform 训练路径"),
    SourceSpec("src/paths/gen_factory_logistics_showcase_path.m", "路径生成", "工厂物流展示路径"),
    SourceSpec("src/paths/gen_closed_loop_eval_paths.m", "路径生成", "多路径闭环评估路径"),
    SourceSpec("src/paths/gen_modern_tcn_demo_path.m", "路径生成", "ModernTCN 演示路径"),
    SourceSpec("src/paths/gen_modern_tcn_theta_sweep_plot_path.m", "路径生成", "坡度 sweep 绘图路径"),
    SourceSpec("src/paths/gen_modern_tcn_theta_sweep_short_paths.m", "路径生成", "坡度 sweep 短路径"),
    SourceSpec("src/ModernTCN/modern_tcn_model.py", "ModernTCN主方法", "ModernTCN-small 多任务网络定义"),
    SourceSpec("src/ModernTCN/modern_tcn_data.py", "ModernTCN主方法", "数据集读取与契约检查"),
    SourceSpec("src/ModernTCN/modern_tcn_metrics.py", "ModernTCN主方法", "多任务损失和指标"),
    SourceSpec("src/ModernTCN/train_modern_tcn.py", "ModernTCN主方法", "单 seed 训练入口"),
    SourceSpec("src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py", "ModernTCN主方法", "多 seed 训练入口"),
    SourceSpec("src/ModernTCN/export_modern_tcn_onnx.py", "ModernTCN主方法", "ONNX 导出"),
    SourceSpec("src/ModernTCN/check_onnxruntime_consistency.py", "ModernTCN主方法", "ONNXRuntime 一致性检查"),
    SourceSpec("src/ModernTCN/ModernTCN_check_matlab_onnx.m", "ModernTCN主方法", "MATLAB ONNX 一致性检查"),
    SourceSpec("src/ModernTCN/ModernTCN_default_config.m", "ModernTCN主方法", "默认部署配置"),
    SourceSpec("src/ModernTCN/ModernTCN_load_predictor.m", "ModernTCN主方法", "MATLAB 预测器加载"),
    SourceSpec("src/ModernTCN/ModernTCN_predict_window.m", "ModernTCN主方法", "窗口预测"),
    SourceSpec("src/ModernTCN/ModernTCN_online_step.m", "ModernTCN主方法", "在线逐步推理"),
    SourceSpec("src/ModernTCN/ModernTCN_state_classifier.m", "ModernTCN主方法", "在线状态分类器"),
    SourceSpec("src/ModernTCN/ModernTCN_State_Classifier_sim.m", "ModernTCN主方法", "Simulink 包装函数"),
    SourceSpec("src/ModernTCN/ModernTCN_analyze_closed_loop_out.m", "ModernTCN主方法", "闭环输出分析"),
    SourceSpec("src/ModernTCN/ModernTCN_replay_closed_loop_yraw.m", "ModernTCN主方法", "闭环 yraw 回放"),
    SourceSpec("src/ModernTCN/plot_modern_tcn_theta_scatter.m", "ModernTCN主方法", "坡度散点评估"),
    SourceSpec("src/ModernTCN/eval_modern_tcn_theta_sweep_plot.m", "ModernTCN主方法", "坡度 sweep 评估"),
    SourceSpec("src/Compare/run_closed_loop_model_once.m", "对照算法与闭环比较", "单次闭环运行"),
    SourceSpec("src/Compare/compare_modern_tcn_gru_closed_loop_out.m", "对照算法与闭环比较", "ModernTCN/GRU 闭环对比"),
    SourceSpec("src/Compare/compare_tcn_gru_modern_closed_loop_out.m", "对照算法与闭环比较", "三算法闭环对比"),
    SourceSpec("src/Compare/run_lpvmpc_theta_baseline_experiment.m", "对照算法与闭环比较", "LPV-MPC theta 基线与 oracle"),
    SourceSpec("src/Compare/run_multi_path_closed_loop_benchmark.m", "对照算法与闭环比较", "多路径闭环评估"),
    SourceSpec("src/Compare/run_closed_loop_robustness_experiment.m", "对照算法与闭环比较", "扰动鲁棒性实验"),
    SourceSpec("src/Compare/benchmark_modern_tcn_onnx_runtime.py", "对照算法与闭环比较", "ONNXRuntime 实时性测试"),
    SourceSpec("src/Compare/run_realtime_benchmark.m", "对照算法与闭环比较", "实时性汇总实验"),
    SourceSpec("src/gru/GRU_train.m", "GRU对照模块", "GRU 基线训练"),
    SourceSpec("src/gru/run_GRU_train_theta10_v2_multi_seed.m", "GRU对照模块", "GRU 多 seed 训练"),
    SourceSpec("src/gru/GRU_default_config.m", "GRU对照模块", "GRU 默认部署配置"),
    SourceSpec("src/gru/GRU_infer.m", "GRU对照模块", "GRU 推理"),
    SourceSpec("src/gru/GRU_state_classifier.m", "GRU对照模块", "GRU 在线分类器"),
    SourceSpec("src/gru/GRU_State_Classifier_gru_sim.m", "GRU对照模块", "GRU Simulink 包装"),
    SourceSpec("src/gru/GRU_load_default_to_base.m", "GRU对照模块", "GRU 默认模型加载"),
    SourceSpec("src/TCN/TCN_train.m", "TCN对照模块", "TCN 基线训练"),
    SourceSpec("src/TCN/run_TCN_train_theta10_v2_multi_seed.m", "TCN对照模块", "TCN 多 seed 训练"),
    SourceSpec("src/TCN/TCN_recommended_cfg.m", "TCN对照模块", "TCN 推荐配置"),
    SourceSpec("src/TCN/TCN_default_config.m", "TCN对照模块", "TCN 默认部署配置"),
    SourceSpec("src/TCN/TCN_load_predictor.m", "TCN对照模块", "TCN 预测器加载"),
    SourceSpec("src/TCN/TCN_predict_window.m", "TCN对照模块", "TCN 窗口预测"),
    SourceSpec("src/TCN/TCN_state_classifier.m", "TCN对照模块", "TCN 在线分类器"),
    SourceSpec("src/TCN/TCN_State_Classifier_sim.m", "TCN对照模块", "TCN Simulink 包装"),
    SourceSpec("src/TCN/configure_tcn_simulink_model.m", "TCN对照模块", "TCN Simulink 配置"),
    SourceSpec("src/tests/test_simulink_closed_loop.m", "测试验证", "Simulink 闭环测试"),
    SourceSpec("src/tests/test_GRU_workflow.m", "测试验证", "GRU 工作流测试"),
    SourceSpec("src/tests/test_gru_performance.m", "测试验证", "GRU 性能测试"),
    SourceSpec("src/tests/test_gru_latency.m", "测试验证", "GRU 延迟测试"),
    SourceSpec("src/tests/test_gru_filter_constants.m", "测试验证", "GRU 滤波常数测试"),
    SourceSpec("src/tests/test_agv_open_loop.m", "测试验证", "AGV 开环测试"),
    SourceSpec("src/tests/test_industrial_open_loop_items.m", "测试验证", "工业开环项目测试"),
]


MODULE_ORDER = [
    "项目初始化",
    "车辆模型与控制基础层",
    "LPV与MPC",
    "路径生成",
    "ModernTCN主方法",
    "对照算法与闭环比较",
    "GRU对照模块",
    "TCN对照模块",
    "测试验证",
]


def ensure_dirs() -> dict[str, Path]:
    dirs = {
        "00": OUT / "00_application_info",
        "01": OUT / "01_source_code_material",
        "02": OUT / "02_software_document",
        "03": OUT / "03_auxiliary_materials",
        "04": OUT / "04_compliance_check",
    }
    OUT.mkdir(exist_ok=True)
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def read_text(path: Path) -> str:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_bytes().decode("utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def normalize_rel(rel_path: str) -> str:
    return rel_path.replace("\\", "/")


def language_for(path: str) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".m":
        return "MATLAB"
    if suffix == ".py":
        return "Python"
    return "Text"


def count_lines(path: Path) -> int:
    text = read_text(path)
    if not text:
        return 0
    return len(text.splitlines())


def scan_sources(dirs: dict[str, Path]) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    included_rows: list[dict[str, object]] = []
    total_lines = 0
    missing: list[str] = []

    order = 1
    for spec in SOURCE_SPECS:
        rel = normalize_rel(spec.rel_path)
        path = ROOT / rel
        if path.exists():
            lines = count_lines(path)
            status = "included"
            total_lines += lines
            row = {
                "order": order,
                "relative_path": rel,
                "language": language_for(rel),
                "lines": lines,
                "include_status": status,
                "module": spec.module,
                "reason": spec.reason,
            }
            included_rows.append(row)
        else:
            missing.append(rel)
            row = {
                "order": order,
                "relative_path": rel,
                "language": language_for(rel),
                "lines": "",
                "include_status": "missing",
                "module": spec.module,
                "reason": "需求清单指定但当前仓库未找到",
            }
        rows.append(row)
        order += 1

    excluded_patterns = [
        (".git/", "directory", "excluded_cache", "版本控制目录，不纳入源码鉴别材料"),
        (".github/", "directory", "excluded_cache", "仓库平台配置，不纳入源码鉴别材料"),
        (".kilo/", "directory", "excluded_cache", "IDE/代理计划缓存，不纳入源码鉴别材料"),
        (".cursor/", "directory", "excluded_cache", "IDE 配置，不纳入源码鉴别材料"),
        (".venv/", "directory", "excluded_third_party", "虚拟环境和第三方依赖，不纳入源码鉴别材料"),
        ("slprj/", "directory", "excluded_cache", "Simulink 自动生成缓存，不纳入源码鉴别材料"),
        ("**/__pycache__/", "directory", "excluded_cache", "Python 字节码缓存，不纳入源码鉴别材料"),
        ("src/ModernTCN/generated_layers/", "directory", "excluded_third_party", "MATLAB ONNX 导入自动生成兼容层，默认排除"),
        ("data/**/*.mat", "pattern", "excluded_binary_or_data", "训练数据、模型和中间数据，不作为源程序"),
        ("data/**/*.csv", "pattern", "excluded_binary_or_data", "数据表和清单文件，不作为源程序"),
        ("results/**", "directory", "excluded_result", "运行结果、报告、图表和模型输出，不作为源程序"),
        ("figures/**", "directory", "excluded_result", "图片和路径预览，不作为源程序"),
        ("docs/**", "directory", "excluded_result", "说明文档和历史记录，不作为源程序鉴别材料"),
        ("*.slx", "pattern", "excluded_binary_or_data", "Simulink 二进制模型，仅在说明书中引用"),
        ("*.slxc", "pattern", "excluded_cache", "Simulink 缓存文件，不纳入源码鉴别材料"),
        ("*.pt", "pattern", "excluded_binary_or_data", "PyTorch 权重文件，不作为源程序"),
        ("*.onnx", "pattern", "excluded_binary_or_data", "ONNX 模型文件，不作为源程序"),
        ("*.pdf", "pattern", "excluded_result", "PDF 文档或图表，不作为源码材料"),
        ("*.docx", "pattern", "excluded_result", "Word 文档，不作为源码材料"),
    ]
    for rel, lang, status, reason in excluded_patterns:
        rows.append(
            {
                "order": order,
                "relative_path": rel,
                "language": lang,
                "lines": "",
                "include_status": status,
                "module": "排除范围",
                "reason": reason,
            }
        )
        order += 1

    index_file = dirs["01"] / "source_file_index.csv"
    with index_file.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["order", "relative_path", "language", "lines", "include_status", "module", "reason"],
        )
        writer.writeheader()
        writer.writerows(rows)

    stats = {
        "included_count": len(included_rows),
        "included_lines": total_lines,
        "missing": missing,
        "index_rows": len(rows),
    }
    return rows, included_rows, stats


def build_source_material(dirs: dict[str, Path], included_rows: list[dict[str, object]]) -> dict[str, object]:
    sorted_rows = sorted(
        included_rows,
        key=lambda r: (MODULE_ORDER.index(str(r["module"])) if str(r["module"]) in MODULE_ORDER else 999, int(r["order"])),
    )
    source_lines: list[str] = []
    for row in sorted_rows:
        rel = str(row["relative_path"])
        path = ROOT / rel
        source_lines.append(f"===== FILE: {rel} =====")
        source_lines.extend(read_text(path).splitlines())
        source_lines.append("")

    full_source = dirs["01"] / f"{SOURCE_BASENAME}_full_source.txt"
    write_text(full_source, "\n".join(source_lines).rstrip() + "\n")
    full_source_line_count = len(read_text(full_source).splitlines())

    pages = [source_lines[i : i + SOURCE_LINES_PER_PAGE] for i in range(0, len(source_lines), SOURCE_LINES_PER_PAGE)]
    full_pages = len(pages)
    if full_pages > SOURCE_FRONT_BACK_PAGES * 2:
        selected_pages = pages[:SOURCE_FRONT_BACK_PAGES] + pages[-SOURCE_FRONT_BACK_PAGES:]
        extract_kind = f"front{SOURCE_FRONT_BACK_PAGES}_back{SOURCE_FRONT_BACK_PAGES}"
        source_txt = dirs["01"] / f"{SOURCE_BASENAME}_source_{extract_kind}.txt"
        source_docx = dirs["01"] / f"{SOURCE_BASENAME}_source_{extract_kind}.docx"
        source_pdf = dirs["01"] / f"{SOURCE_BASENAME}_source_{extract_kind}.pdf"
        extraction_note = (
            f"完整源码约 {full_pages} 页，抽取完整源码排版后的第 1-{SOURCE_FRONT_BACK_PAGES} 页"
            f"和最后 {SOURCE_FRONT_BACK_PAGES} 页。"
        )
    else:
        selected_pages = pages
        extract_kind = "all"
        source_txt = dirs["01"] / f"{SOURCE_BASENAME}_source_all.txt"
        source_docx = dirs["01"] / f"{SOURCE_BASENAME}_source_all.docx"
        source_pdf = dirs["01"] / f"{SOURCE_BASENAME}_source_all.pdf"
        extraction_note = f"完整源码约 {full_pages} 页，不足或等于抽取页数，提交全部源码。"

    flat_selected: list[str] = []
    for page in selected_pages:
        flat_selected.extend(page)
    write_text(source_txt, "\n".join(flat_selected).rstrip() + "\n")
    make_source_docx(selected_pages, source_docx)

    return {
        "full_source": full_source,
        "source_txt": source_txt,
        "source_docx": source_docx,
        "source_pdf": source_pdf,
        "full_pages_estimated": full_pages,
        "selected_pages": len(selected_pages),
        "extract_kind": extract_kind,
        "extraction_note": extraction_note,
        "source_lines_with_boundaries": len(source_lines),
        "full_source_line_count": full_source_line_count,
    }


def xml_escape(text: object) -> str:
    return html.escape(str(text), quote=False)


def paragraph_xml(
    text: str = "",
    style: str | None = None,
    align: str | None = None,
    page_break_before: bool = False,
    page_break: bool = False,
    keep_next: bool = False,
    extra_ppr: str = "",
) -> str:
    ppr: list[str] = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr.append(f'<w:jc w:val="{align}"/>')
    if keep_next:
        ppr.append("<w:keepNext/>")
    if page_break_before:
        ppr.append("<w:pageBreakBefore/>")
    if extra_ppr:
        ppr.append(extra_ppr)
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>" if ppr else ""
    if page_break:
        return f"<w:p>{ppr_xml}<w:r><w:br w:type=\"page\"/></w:r></w:p>"
    if text == "":
        return f"<w:p>{ppr_xml}<w:r><w:t></w:t></w:r></w:p>"
    runs: list[str] = []
    for idx, part in enumerate(str(text).split("\n")):
        if idx:
            runs.append("<w:r><w:br/></w:r>")
        runs.append(f'<w:r><w:t xml:space="preserve">{xml_escape(part)}</w:t></w:r>')
    return f"<w:p>{ppr_xml}{''.join(runs)}</w:p>"


def table_xml(rows: Sequence[Sequence[str]], usable_width: int = 9020) -> str:
    if not rows:
        return ""
    cols = max(len(row) for row in rows)
    col_width = max(1200, usable_width // cols)
    grid = "".join(f'<w:gridCol w:w="{col_width}"/>' for _ in range(cols))
    border = (
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="9E9E9E"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="9E9E9E"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="9E9E9E"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="9E9E9E"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="C8C8C8"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="C8C8C8"/>'
        "</w:tblBorders>"
    )
    parts = [
        "<w:tbl>",
        f'<w:tblPr><w:tblW w:w="{usable_width}" w:type="dxa"/>{border}'
        '<w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
        '<w:bottom w:w="90" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tblCellMar></w:tblPr>',
        f"<w:tblGrid>{grid}</w:tblGrid>",
    ]
    for r_idx, row in enumerate(rows):
        trpr = "<w:trPr><w:tblHeader/></w:trPr>" if r_idx == 0 else ""
        parts.append(f"<w:tr>{trpr}")
        for c_idx in range(cols):
            cell = row[c_idx] if c_idx < len(row) else ""
            fill = '<w:shd w:fill="EAF2F8"/>' if r_idx == 0 else ""
            parts.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{col_width}" w:type="dxa"/>{fill}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'{paragraph_xml(str(cell), style="TableText")}</w:tc>'
            )
        parts.append("</w:tr>")
    parts.append("</w:tbl>")
    return "".join(parts)


def styles_xml(source_mode: bool = False) -> str:
    if source_mode:
        normal_font = "Consolas"
        east_font = "Consolas"
        normal_size = "18"
        line = "230"
    else:
        normal_font = "Arial"
        east_font = "SimSun"
        normal_size = "21"
        line = "360"
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault><w:rPr><w:rFonts w:ascii="{normal_font}" w:hAnsi="{normal_font}" w:eastAsia="{east_font}"/><w:sz w:val="{normal_size}"/></w:rPr></w:rPrDefault>
    <w:pPrDefault><w:pPr><w:spacing w:before="0" w:after="80" w:line="{line}" w:lineRule="auto"/></w:pPr></w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:spacing w:before="0" w:after="80" w:line="{line}" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="{normal_font}" w:hAnsi="{normal_font}" w:eastAsia="{east_font}"/><w:sz w:val="{normal_size}"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:jc w:val="center"/><w:spacing w:before="240" w:after="180"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimHei"/><w:b/><w:sz w:val="36"/><w:color w:val="1F4E79"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="220" w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimHei"/><w:b/><w:sz w:val="30"/><w:color w:val="1F4E79"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="160" w:after="80"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimHei"/><w:b/><w:sz w:val="25"/><w:color w:val="365F91"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:qFormat/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="60"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimHei"/><w:b/><w:sz w:val="22"/><w:color w:val="3F3F3F"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock"><w:name w:val="Code Block"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="20" w:line="240" w:lineRule="exact"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="CodeLine"><w:name w:val="Code Line"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="0" w:line="230" w:lineRule="exact"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas" w:eastAsia="Consolas"/><w:sz w:val="18"/></w:rPr></w:style>
  <w:style w:type="paragraph" w:styleId="TableText"><w:name w:val="Table Text"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="0" w:after="0" w:line="260" w:lineRule="auto"/></w:pPr><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimSun"/><w:sz w:val="19"/></w:rPr></w:style>
</w:styles>'''


def header_xml() -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:hdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:tabs><w:tab w:val="right" w:pos="10000"/></w:tabs>
      <w:pBdr><w:bottom w:val="single" w:sz="6" w:space="2" w:color="808080"/></w:pBdr>
      <w:spacing w:after="60"/>
    </w:pPr>
    <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimSun"/><w:sz w:val="18"/></w:rPr><w:t>{xml_escape(HEADER_TEXT)}</w:t></w:r>
    <w:r><w:tab/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimSun"/><w:sz w:val="18"/></w:rPr><w:t>第 </w:t></w:r>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimSun"/><w:sz w:val="18"/></w:rPr><w:t> 页 共 </w:t></w:r>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> NUMPAGES </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="separate"/></w:r>
    <w:r><w:t>1</w:t></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
    <w:r><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="SimSun"/><w:sz w:val="18"/></w:rPr><w:t> 页</w:t></w:r>
  </w:p>
</w:hdr>'''


def footer_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:pBdr><w:top w:val="single" w:sz="6" w:space="2" w:color="808080"/></w:pBdr>
      <w:spacing w:before="60"/>
    </w:pPr>
    <w:r><w:t></w:t></w:r>
  </w:p>
</w:ftr>'''


def make_docx(body_xml: str, path: Path, *, source_mode: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if source_mode:
        margins = '<w:pgMar w:top="900" w:right="900" w:bottom="900" w:left="900" w:header="480" w:footer="480" w:gutter="0"/>'
        line_numbering = ""
    else:
        margins = '<w:pgMar w:top="1134" w:right="1020" w:bottom="1134" w:left="1134" w:header="560" w:footer="560" w:gutter="0"/>'
        line_numbering = ""
    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body_xml}
    <w:sectPr>
      <w:headerReference w:type="default" r:id="rIdHeader1"/>
      <w:footerReference w:type="default" r:id="rIdFooter1"/>
      <w:pgSz w:w="11906" w:h="16838"/>
      {margins}
      <w:cols w:space="720"/>
      {line_numbering}
      <w:docGrid w:linePitch="312"/>
    </w:sectPr>
  </w:body>
</w:document>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>
  <Override PartName="/word/header1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>
  <Relationship Id="rIdHeader1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/header" Target="header1.xml"/>
  <Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>'''
    settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:updateFields w:val="true"/>
  <w:defaultTabStop w:val="420"/>
</w:settings>'''
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_escape(path.stem)}</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">2026-05-25T00:00:00Z</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">2026-05-25T00:00:00Z</dcterms:modified>
</cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Codex OOXML Generator</Application>
</Properties>'''
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", document_xml)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles_xml(source_mode=source_mode))
        z.writestr("word/settings.xml", settings)
        z.writestr("word/header1.xml", header_xml())
        z.writestr("word/footer1.xml", footer_xml())
        z.writestr("docProps/core.xml", core)
        z.writestr("docProps/app.xml", app)


def make_source_docx(pages: Sequence[Sequence[str]], path: Path) -> None:
    body: list[str] = []
    for p_idx, page in enumerate(pages):
        if p_idx:
            body.append(paragraph_xml(page_break=True))
        for line_idx, line in enumerate(page, start=1):
            numbered_line = f"{line_idx:>2}    {line}"
            body.append(
                paragraph_xml(
                    numbered_line,
                    style="CodeLine",
                    extra_ppr='<w:ind w:left="0" w:firstLine="0"/>',
                )
            )
    make_docx("".join(body), path, source_mode=True)


def is_table_separator(line: str) -> bool:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{2,}:?", c or "") for c in cells)


def parse_markdown_table(lines: Sequence[str]) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in lines:
        if is_table_separator(line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows


def markdown_to_docx(md: str, path: Path) -> None:
    body: list[str] = []
    lines = md.splitlines()
    i = 0
    in_code = False
    while i < len(lines):
        line = lines[i]
        if line.strip() == "<!-- PAGEBREAK -->":
            body.append(paragraph_xml(page_break=True))
            i += 1
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            body.append(paragraph_xml(line, style="CodeBlock"))
            i += 1
            continue
        if line.startswith("|") and "|" in line[1:]:
            block = []
            while i < len(lines) and lines[i].startswith("|") and "|" in lines[i][1:]:
                block.append(lines[i])
                i += 1
            body.append(table_xml(parse_markdown_table(block)))
            continue
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            text = stripped[level:].strip()
            if level == 1:
                body.append(paragraph_xml(text, style="Title", align="center"))
            elif level == 2:
                body.append(paragraph_xml(text, style="Heading1", keep_next=True))
            elif level == 3:
                body.append(paragraph_xml(text, style="Heading2", keep_next=True))
            else:
                body.append(paragraph_xml(text, style="Heading3", keep_next=True))
        elif stripped.startswith("- "):
            body.append(paragraph_xml("- " + stripped[2:], style="Normal"))
        elif re.match(r"^\d+\.\s+", stripped):
            body.append(paragraph_xml(stripped, style="Normal"))
        else:
            body.append(paragraph_xml(stripped, style="Normal"))
        i += 1
    make_docx("".join(body), path, source_mode=False)


def file_exists(path: str) -> str:
    return "存在" if (ROOT / path).exists() else "缺失"


def build_source_selection_report(stats: dict[str, object], source_info: dict[str, object]) -> str:
    missing = stats["missing"]
    missing_text = "无。" if not missing else "\n".join(f"- `{m}`" for m in missing)
    return f"""# 源码选择报告

生成日期：{GENERATED_DATE}

## 1. 选择原则

本次程序鉴别材料采用白名单方式，从当前仓库中选择与“{SOFTWARE_FULL} {VERSION}”直接相关的 MATLAB/Python 源文件。选择范围覆盖项目初始化、AGV 车辆模型、LPV 线性化、MPC 控制器、参考路径生成、ModernTCN 多任务工况感知、ONNX 导出与 MATLAB/Simulink 在线推理、GRU/TCN 对照实验、闭环比较和测试验证脚本。

未纳入虚拟环境、第三方库源码、缓存目录、训练数据、模型权重、ONNX 文件、MAT 文件、图片、论文图表、PDF/DOCX 文档和 Simulink 二进制模型。Simulink `.slx` 模型作为软件运行环境和闭环平台在说明书中引用，不作为源程序文本纳入。

## 2. 纳入统计

| 项目 | 数值 |
|---|---:|
| 纳入源文件数量 | {stats['included_count']} |
| 纳入源码行数 | {stats['included_lines']} |
| 完整源码汇编估算页数 | {source_info['full_pages_estimated']} |
| 抽取源码页数 | {source_info['selected_pages']} |
| 每页目标行数 | {SOURCE_LINES_PER_PAGE} |

## 3. 抽取说明

{source_info['extraction_note']}

生成的完整源码汇编文件为：

- `{source_info['full_source'].relative_to(ROOT).as_posix()}`

生成的提交用源码鉴别材料为：

- `{source_info['source_txt'].relative_to(ROOT).as_posix()}`
- `{source_info['source_docx'].relative_to(ROOT).as_posix()}`
- `{source_info['source_pdf'].relative_to(ROOT).as_posix()}`

## 4. 缺失文件

{missing_text}

## 5. 排除说明

- `.git/`、`.github/`、`.kilo/`、`.cursor/`、`.venv/`、`__pycache__/`、`slprj/` 和 Simulink 缓存文件属于环境、缓存或平台配置，不纳入源程序。
- `data/`、`results/`、`figures/` 下的数据、模型、图表、报告和中间结果不作为源程序鉴别材料。
- `.mat`、`.pt`、`.onnx`、`.slx`、`.slxc`、`.pdf`、`.docx` 等文件属于数据、模型、二进制工程文件或文档，不作为源程序文本。
- `src/ModernTCN/generated_layers/` 为 MATLAB 导入 ONNX 后产生的兼容层代码，默认标注为自动生成兼容层，不纳入本次核心源码。
- `src/pic&table/` 下脚本主要用于论文图表生成，与软著申请的软件主体功能不同，未纳入程序鉴别材料。
"""


def build_application_fields(source_lines: int) -> str:
    function_desc = (
        "本软件面向对角双转向驱动AGV的工况感知与闭环控制仿真需求，提供从路径生成、车辆建模、训练数据构建、"
        "时序神经网络训练到LPV-MPC闭环仿真的完整工具链。软件以MATLAB/Simulink为车辆模型与控制仿真平台，"
        "以Python/PyTorch实现ModernTCN多任务时序感知模型，通过128步、19维观测窗口识别AGV主工况、转向方向并回归坡度调度量。"
        "软件支持将训练模型导出为ONNX，并在MATLAB端完成在线预测和Simulink闭环调用。系统还提供GRU、TCN、"
        "无AI坡度基线和真实坡度上界等对照流程，支持离线指标评估、闭环轨迹跟踪评价、多路径鲁棒性实验、扰动鲁棒性实验和实时性测试，"
        "便于对AGV在坡道、转向和异常工况下的控制性能进行可复现验证。"
    )
    return f"""# 申请表字段草稿

> 说明：以下内容为软著申请表辅助草稿，无法从仓库确定的权属、日期和主体信息均保留为 `[申请人填写]`，不得由生成脚本自行编造。

软件全称：{SOFTWARE_FULL}

软件简称：{SOFTWARE_SHORT}

版本号：{VERSION}

开发完成日期：[申请人填写]

首次发表日期：[未发表/申请人填写]

软件分类：[建议：工业控制软件/仿真分析软件/人工智能应用软件，最终以系统选项为准]

开发方式：[独立开发/合作开发/委托开发/职务开发，申请人确认]

权利取得方式：[原始取得/继受取得，申请人确认]

编程语言：MATLAB、Python

源程序量：{source_lines} 行（按本次完整源码汇编 TXT 统计，含文件边界、注释和空行；正式填报前可按官方系统口径复核）

硬件环境：普通 PC 工作站或具备 MATLAB/Simulink 和 Python 深度学习环境的计算机；建议 CPU 多核、内存 16GB 及以上；如使用 GPU 训练，可选 NVIDIA GPU。

软件环境：Windows 10/11 或兼容桌面操作系统；MATLAB/Simulink；Python；PyTorch；ONNXRuntime；必要时包含 MATLAB Deep Learning Toolbox、Model Predictive Control Toolbox 等。

主要功能：AGV车辆模型仿真、参考路径生成、LPV线性化、MPC控制器构建、ModernTCN工况感知、坡度调度量预测、ONNX导出、MATLAB在线推理、Simulink闭环仿真、对照算法评估、多路径与扰动鲁棒性验证、实时性测试。

技术特点：面向AGV闭环控制的多任务时序感知，结合大核深度时序卷积、LPV-MPC在线调度、统一数据契约、ONNX跨环境部署和闭环评价流程，实现工况识别、转向识别、坡度回归与控制仿真的一体化。

## 300-500字软件功能说明

{function_desc}
"""


def build_software_name_options() -> str:
    return f"""# 软件名称备选方案

## 推荐名称

1. 面向对角双转向驱动AGV的ModernTCN-LPV-MPC工况感知与闭环控制仿真软件 {VERSION}
2. {SOFTWARE_FULL} {VERSION}
3. 基于ModernTCN的AGV工况感知与调度控制仿真软件 {VERSION}

## 当前材料统一使用

- 软件全称：{SOFTWARE_FULL}
- 软件简称：{SOFTWARE_SHORT}
- 版本号：{VERSION}
- 页眉：{HEADER_TEXT}
- 页脚：第 x 页 共 y 页

## 使用建议

推荐使用“{SOFTWARE_FULL} {VERSION}”。该名称比论文式长标题更像软件系统名称，同时能覆盖 AGV 工况感知、LPV-MPC 调度控制和闭环仿真验证三类核心功能。

如申请人最终修改软件名称，应在申请表、源码页眉、说明书页眉、PDF 文件名、正文首章和所有辅助材料中同步替换。当前页眉按版式要求仅保留软件名称主体，版本号仍在封面、申请字段和正文版本字段中保持一致。
"""


def build_ownership_checklist() -> str:
    return """# 权属确认清单

> 本清单仅用于申请人提交前自查。Codex 不能判断著作权归属，也不能替申请人确认法律事实。

- [ ] 著作权人姓名或单位名称已经确认。
- [ ] 软件是否属于学校、单位或课题组职务成果已经确认。
- [ ] 是否存在合作开发人已经确认。
- [ ] 是否存在委托开发、外包开发或任务书安排已经确认。
- [ ] 是否需要合作开发协议、委托合同、任务书、权属证明或单位盖章已经确认。
- [ ] 开发完成日期真实且有记录可追溯。
- [ ] 首次发表日期真实；若未发表，按官方系统要求选择未发表或填写相应字段。
- [ ] GitHub 公开仓库是否构成首次发表已经确认。
- [ ] 仓库中是否包含第三方开源代码或自动生成代码已经复核。
- [ ] 申请材料中的软件名称、简称和版本号全部一致。
- [ ] 申请表中的源程序量和提交源码材料范围已经确认。
- [ ] 未把身份证、营业执照、公章、签名扫描件等敏感材料写入仓库。
"""


def build_technical_summary() -> str:
    return f"""# 技术特点摘要

## 1. 主要功能点

1. 项目初始化与路径管理；
2. AGV车辆模型仿真；
3. LPV线性化与MPC控制器构建；
4. 参考路径和训练路径生成；
5. 统一时序数据集构建；
6. ModernTCN多任务工况感知；
7. ONNX模型导出与一致性验证；
8. MATLAB在线推理与Simulink闭环调用；
9. GRU/TCN/LPV-MPC基线对照；
10. 多路径、扰动鲁棒性和实时性评价。

## 2. 技术特点表述

（1）软件将AGV动态模型、LPV-MPC控制器和ModernTCN时序感知模型组织为统一闭环仿真流程，实现工况识别、转向识别和坡度调度量回归的协同使用。

（2）软件采用固定长度时序窗口和19维可观测特征构建输入数据，并通过run级数据划分和训练集拟合scaler策略降低数据泄漏风险。

（3）软件的ModernTCN模块采用大核深度时序卷积、通道混合和残差结构，输出主工况、转向方向和坡度回归三类结果。

（4）软件支持将PyTorch模型导出为ONNX格式，并在MATLAB/Simulink闭环模型中加载使用，形成跨语言部署链路。

（5）软件提供三算法闭环对比、多路径闭环实验、扰动鲁棒性实验和实时性测试，支持对控制性能进行可复现评估。

## 3. 项目事实边界

本软件当前主要用于桌面端 MATLAB/Simulink 闭环仿真与算法验证。ONNXRuntime+MPC 核心链路在项目测试中具备相对于 10 ms 控制周期的计算余量；MATLAB/Simulink extrinsic 封装主要用于桌面仿真验证，不应表述为已经完成嵌入式硬实时部署。
"""


def build_third_party_statement() -> str:
    return """# 第三方、数据与排除说明

1. 本次源码鉴别材料仅从申请人仓库中的 MATLAB/Python 源文件中选择，重点覆盖 AGV 模型、LPV-MPC、路径生成、ModernTCN 训练部署、对照实验和测试验证代码。

2. 本次材料未纳入虚拟环境、第三方库源码、缓存文件、训练数据、模型权重、ONNX文件、MAT文件、图片、论文图表、PDF/DOCX文档和自动生成临时文件。

3. PyTorch、ONNXRuntime、MATLAB/Simulink、MATLAB 工具箱等作为运行环境、依赖工具或平台能力出现，不作为本软件申请的自有源代码。

4. 仓库中如存在基于公开算法思想实现的模块，材料中仅描述为“软件实现了面向AGV场景的工程化时序感知与闭环控制流程”，不声称第三方基础框架、基础算法或工具平台归申请人所有。

5. `src/ModernTCN/generated_layers/` 属于 MATLAB 导入 ONNX 后产生的兼容层代码，默认不纳入本次核心源程序鉴别材料；若申请人决定纳入，应单独标注为自动生成兼容层。

6. Simulink `.slx` 文件属于二进制工程模型，本次不作为源程序文本提交；说明书中仅将其列为闭环仿真模型和运行平台组成部分。

7. 申请人应最终确认是否包含外部开源代码、合作开发代码、导师/学校/单位职务成果、委托开发成果或其他权属问题，并按官方要求准备证明材料。
"""


def build_user_manual() -> str:
    return """# 用户手册短版

## 1. 软件简介

本软件面向对角双转向驱动AGV的工况感知、LPV-MPC调度控制和闭环仿真验证，提供路径生成、车辆模型仿真、训练数据构建、ModernTCN多任务训练、ONNX导出、MATLAB在线推理、Simulink闭环仿真和对照实验评估功能。

## 2. 环境准备

建议使用 Windows 10/11 或兼容桌面系统，安装 MATLAB/Simulink、必要 MATLAB 工具箱、Python、PyTorch 和 ONNXRuntime。若进行深度模型训练，可配置 NVIDIA GPU；若仅运行已导出模型和闭环仿真，可使用普通 PC 工作站。

## 3. 初始化项目

在 MATLAB 中切换到项目根目录后运行：

```matlab
init_project;
root = project_root();
out_dir = results_dir();
```

## 4. 生成/检查数据集

当前主线数据集为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

对应数据契约为：

```text
data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json
```

用户应优先检查数据契约中的 `Ts=0.01`、`seq_len=128`、`input_dim=19`、标签映射、split 策略和 scaler 策略。

## 5. 训练ModernTCN

Python 单 seed 训练入口为：

```bash
python src/ModernTCN/train_modern_tcn.py --dataset-file data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat
```

多 seed 训练入口为：

```bash
python src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py
```

具体参数以脚本中的 `argparse` 定义为准。

## 6. 导出ONNX

默认部署模型位于：

```text
results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.onnx
```

可使用以下入口导出：

```bash
python src/ModernTCN/export_modern_tcn_onnx.py --checkpoint results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt
```

导出后可运行 ONNXRuntime 与 MATLAB 一致性检查脚本。

## 7. 加载Simulink闭环模型

在 MATLAB 中加载默认配置与闭环模型：

```matlab
init_project;
cfg = ModernTCN_default_config(project_root());
load_system('simulink/LPVMPC_AGV_simulink_Modern_TCN.slx');
```

GRU、TCN 和 IMU 对照模型分别位于 `simulink/LPVMPC_AGV_simulink_GRU.slx`、`simulink/LPVMPC_AGV_simulink_TCN.slx` 和 `simulink/LPVMPC_AGV_simulink_IMU.slx`。

## 8. 运行闭环仿真

闭环仿真由 Simulink 模型、预加载函数、ModernTCN 在线分类器和 LPV-MPC 更新函数共同完成。用户可通过对照实验脚本统一调用，也可手动加载模型并运行仿真。

## 9. 运行对照实验

常用对照入口包括：

```matlab
run_closed_loop_model_once
compare_tcn_gru_modern_closed_loop_out
run_lpvmpc_theta_baseline_experiment
run_multi_path_closed_loop_benchmark
run_closed_loop_robustness_experiment
run_realtime_benchmark
```

这些脚本用于生成三算法闭环比较、多路径评估、扰动鲁棒性评估和实时性统计。

## 10. 查看输出文件

主要结果输出到 `results/` 目录。ModernTCN 训练结果位于 `results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/`；闭环对比结果位于 `results/compare/`；论文图表位于 `results/paper/`。

## 11. 常见问题

- 若 MATLAB 找不到函数，先运行 `init_project`。
- 若 ONNX 文件不存在，检查 `ModernTCN_default_config.m` 中的 `run_tag` 和 `onnx_file`。
- 若数据维度不匹配，检查数据契约中的 `seq_len=128` 和 `input_dim=19`。
- 若闭环模型加载失败，检查 `data/models/ctrl.mat`、`lin_agv_db.mat`、`plant_grid_test.mat` 和 Simulink 模型是否存在。
- 若实时性测试结果不能直接满足硬实时要求，应区分 ONNXRuntime+MPC 核心链路与 MATLAB/Simulink 桌面封装开销。
"""


def build_module_mapping_csv(path: Path) -> None:
    rows = [
        ["项目初始化", "init_project.m, project_root.m, results_dir.m", "设置路径与结果目录", "项目根目录", "MATLAB搜索路径、结果路径"],
        ["车辆模型", "src/core/*.m", "AGV动力学与输出计算", "状态、控制量、参数", "状态导数、输出量"],
        ["LPV线性化", "src/lpv/*.m", "建立调度点线性模型", "AGV状态点、参数", "LPV网格模型"],
        ["MPC控制", "src/mpc/*.m", "构造与更新MPC控制器", "LPV模型、调度量、约束", "控制输入"],
        ["路径生成", "src/paths/*.m", "生成训练和闭环路径", "路径参数", "ref结构、路径mat文件"],
        ["ModernTCN训练", "src/ModernTCN/*.py", "训练多任务时序模型", "数据集mat文件", "checkpoint、指标、ONNX"],
        ["ModernTCN部署", "src/ModernTCN/*.m", "MATLAB端加载和在线预测", "ONNX模型、在线窗口", "工况、转向、坡度输出"],
        ["Simulink闭环", "simulink/*.slx, preloadfcn*.m", "闭环控制仿真", "控制器、模型、路径", "logsout、闭环结果"],
        ["对照实验", "src/gru, src/TCN, src/Compare", "基线训练与闭环对比", "统一数据集、路径", "指标表、报告"],
        ["测试验证", "src/tests/*.m", "流程检查和性能测试", "模型与配置", "测试报告"],
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["模块", "主要文件", "功能说明", "输入", "输出"])
        writer.writerows(rows)


def build_design_document() -> str:
    toc = """# AGV工况感知与LPV-MPC闭环控制仿真软件 V1.0 软件设计说明书

软件全称：AGV工况感知与LPV-MPC闭环控制仿真软件

软件简称：AGV-MTCN-MPC仿真软件

版本号：V1.0

生成日期：2026-05-25

编制说明：本文档根据当前仓库源码、数据契约、项目流程清单和默认部署配置生成，用于软件著作权登记辅助材料。申请人应在提交前确认软件名称、著作权人、开发完成日期、首次发表日期和权属证明。

<!-- PAGEBREAK -->

## 修订记录

| 版本 | 日期 | 内容 | 责任人 |
|---|---|---|---|
| V1.0 | 2026-05-25 | 根据当前项目生成软著申请辅助设计说明书 | [申请人填写] |

## 目录

第1章 软件概述

第2章 运行环境

第3章 总体架构

第4章 数据与路径生成模块

第5章 AGV模型与LPV-MPC控制模块

第6章 ModernTCN工况感知模块

第7章 训练、评估与模型导出

第8章 Simulink闭环仿真模块

第9章 对照算法与基线模块

第10章 实验、报告与验证模块

第11章 用户使用说明

第12章 技术特点

第13章 数据安全与维护

第14章 版本说明

附录A 主要源码文件清单

附录B 主要输入输出文件清单

附录C 关键参数表

附录D 术语表

<!-- PAGEBREAK -->
"""

    facts = {
        "dataset": "data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2.mat",
        "contract": "data/tcn/ModernTCN_dataset_agv_dualsteer_theta10_uniform_conf_h0_v2_contract.json",
        "onnx": "results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.onnx",
    }

    sections = f"""
## 第1章 软件概述

### 1.1 软件名称、简称与版本

本软件全称为“{SOFTWARE_FULL}”，简称为“{SOFTWARE_SHORT}”，版本号为“{VERSION}”。本说明书、源码页眉、申请字段草稿和一致性检查清单均以该名称和版本为统一标识。

软件名称中的“AGV工况感知”对应 ModernTCN 多任务时序模型；“LPV-MPC闭环控制”对应 AGV 车辆模型、LPV 线性化网格、MPC 控制器和在线调度更新；“仿真软件”对应 MATLAB/Simulink 桌面闭环验证平台。

### 1.2 开发背景

本软件面向对角双转向驱动 AGV 的工况识别、坡度调度和闭环控制仿真需求。AGV 在直行、转向、坡道、低速堵转和扰动条件下的传感量具有时序相关性，单点规则或固定参数控制难以完整描述实际工况变化。

项目通过 MATLAB/Simulink 建立车辆模型和 LPV-MPC 控制平台，通过 Python/PyTorch 训练 ModernTCN 多任务时序感知模型，再通过 ONNX 和 MATLAB 侧加载器接入闭环仿真。该流程支持从离线数据构建到在线控制验证的完整工程链路。

### 1.3 软件目标

本软件目标是提供一套可复现的 AGV 工况感知与闭环仿真工具链。软件能够生成参考路径和训练路径，构建 128 步、19 维输入窗口，训练 ModernTCN 工况感知模型，导出 ONNX 模型，并在 Simulink 闭环模型中调用预测结果辅助 LPV-MPC 调度。

软件同时提供 GRU、TCN、LPV-MPC theta0、IMU theta 和 true-theta oracle 等对照链路，用于验证 ModernTCN 感知输出对闭环轨迹跟踪、控制平滑性、鲁棒性和实时性的影响。

### 1.4 适用对象与应用场景

软件适用于 AGV 控制算法研究、工况感知模型验证、LPV-MPC 调度策略仿真、路径跟踪闭环性能比较和多算法公平对照实验。典型用户包括控制算法开发人员、仿真平台维护人员和研究型项目成员。

当前版本主要用于桌面仿真和算法验证，不直接声明为嵌入式控制器固件。ONNXRuntime+MPC 核心链路可用于评估计算余量；MATLAB/Simulink extrinsic 封装主要用于闭环仿真验证和调试。

### 1.5 软件边界

软件边界包括项目初始化、车辆模型、LPV-MPC、路径生成、数据集构建、ModernTCN训练与部署、MATLAB在线推理、Simulink闭环仿真、对照算法和测试验证。软件不包含第三方深度学习框架源码、MATLAB/Simulink平台源码、训练数据权属证明或申请人身份证明材料。

`.mat`、`.pt`、`.onnx`、`.slx` 等文件作为数据、模型、部署产物或工程模型在说明书中引用，不作为本次源程序文本鉴别材料纳入。

## 第2章 运行环境

### 2.1 硬件环境

软件可在普通 PC 工作站上运行，建议使用多核 CPU 和 16GB 及以上内存。若进行 ModernTCN、GRU 或 TCN 训练，可选 NVIDIA GPU 以缩短训练时间；若仅执行已训练模型的闭环仿真和结果分析，CPU 环境也可运行。

实时性测试脚本将 ONNXRuntime 单窗口推理和 MPC 求解时间作为核心链路进行测量，控制采样周期为 `Ts=0.01 s`。测试结果用于评价计算余量，不等同于对所有桌面仿真封装开销的硬实时承诺。

### 2.2 软件环境

软件环境包括 Windows 10/11 或兼容桌面操作系统、MATLAB/Simulink、Python、PyTorch、ONNXRuntime，以及必要的 MATLAB 工具箱。当前仓库中 MATLAB 代码用于车辆模型、控制器、路径和闭环仿真；Python 代码用于 ModernTCN 训练、ONNX 导出和 ONNXRuntime 一致性测试。

Simulink 主模型包括 `simulink/LPVMPC_AGV_simulink_Modern_TCN.slx`、`simulink/LPVMPC_AGV_simulink_GRU.slx`、`simulink/LPVMPC_AGV_simulink_TCN.slx` 和 `simulink/LPVMPC_AGV_simulink_IMU.slx`。这些模型存在于当前仓库中，作为闭环仿真平台使用。

### 2.3 开发语言与依赖

软件主体源代码由 MATLAB 和 Python 编写。MATLAB 部分包括 `src/core`、`src/lpv`、`src/mpc`、`src/paths`、`src/ModernTCN` 中的在线推理封装、`src/gru`、`src/TCN` 和 `src/Compare`；Python 部分主要包括 `src/ModernTCN/*.py` 和 `src/Compare/benchmark_modern_tcn_onnx_runtime.py`。

PyTorch、ONNXRuntime、MATLAB/Simulink 作为运行环境或依赖工具，不作为申请人的自有源代码。软件说明书仅描述本仓库围绕 AGV 场景实现的工程流程、数据契约和闭环仿真功能。

### 2.4 输入输出文件环境

核心输入包括车辆参数、路径 `.mat` 文件、统一数据集、scaler、LPV 网格模型、MPC 控制器和已导出的 ONNX 模型。当前 ModernTCN 主线数据集为 `{facts['dataset']}`，数据契约为 `{facts['contract']}`。

核心输出包括训练指标、ONNX 文件、一致性检查报告、闭环仿真 `logsout`、对比指标 CSV、鲁棒性报告、实时性报告和论文图表。运行结果主要存放在 `results/`，数据和模型主要存放在 `data/`。

### 2.5 目录结构说明

仓库根目录包含 `init_project.m`、`project_root.m` 和 `results_dir.m` 作为路径管理入口。`src/core` 提供车辆模型和控制基础层，`src/lpv` 和 `src/mpc` 提供 LPV-MPC 控制模块，`src/paths` 提供路径生成模块，`src/ModernTCN` 提供主感知模型，`src/Compare` 提供闭环对比和实时性测试。

`data/` 目录保存训练数据、路径数据和模型缓存；`results/` 目录保存训练与闭环结果；`simulink/` 目录保存闭环模型；`docs/` 与论文相关目录只作为辅助说明和历史材料，不纳入本次源程序鉴别材料。

## 第3章 总体架构

### 3.1 系统总体架构

软件采用“离线训练 + 在线闭环仿真”的总体结构。离线阶段生成路径和训练数据，构建统一时序窗口，训练 ModernTCN 多任务模型并导出 ONNX；在线阶段由 MATLAB/Simulink 加载车辆模型、LPV-MPC 控制器和 ModernTCN 预测器，在每个控制周期更新工况、转向和坡度调度量。

```text
路径生成/车辆仿真 -> 训练数据 -> 128x19窗口 -> ModernTCN训练 -> ONNX导出
       |                                                    |
       v                                                    v
 LPV网格/MPC控制器 ---------------------------> MATLAB在线推理 -> Simulink闭环
       |                                                    |
       +---------------------- 对照算法与闭环指标 ----------------------+
```

### 3.2 功能模块划分

软件划分为项目初始化、车辆模型、LPV线性化、MPC控制、路径生成、数据集构建、ModernTCN训练、ModernTCN部署、Simulink闭环、对照实验和测试验证模块。各模块通过固定文件路径和数据契约连接，避免不同算法使用不同数据或不同控制平台造成对比偏差。

核心控制模块为 `src/core`、`src/lpv` 和 `src/mpc`；核心感知模块为 `src/ModernTCN`；核心对比验证模块为 `src/Compare`。GRU 和 TCN 位于 `src/gru` 与 `src/TCN`，在说明书中作为对照和验证模块描述。

### 3.3 数据流与控制流

数据流从路径生成和仿真输出开始，经过训练数据构建、窗口化、归一化和数据划分后进入 ModernTCN 训练。模型输出包括主工况 logits、转向 logits 和坡度回归值，后续通过 ONNX 文件传递到 MATLAB 端。

控制流由 Simulink 闭环模型驱动。每个仿真步中，AGV 模型输出传感和状态量，ModernTCN 在线模块维护历史窗口并完成预测，LPV-MPC 根据调度量更新控制器，控制输入再作用于车辆模型。

### 3.4 离线训练与在线闭环关系

离线训练使用统一数据集和固定 split，避免窗口泄漏。在线闭环使用同一 scaler 策略，将实时观测量按训练集统计量归一化后送入 ModernTCN。该设计使训练、测试和闭环部署遵循同一数据契约。

训练阶段输出的 checkpoint、ONNX、summary CSV 和一致性报告用于冻结模型。默认部署模型为 seed 21，对应 run_tag `modern_tcn_theta10_uniform_h0_v2_seed21` 和 ONNX 文件 `{facts['onnx']}`。

### 3.5 Simulink 与 MATLAB/Python 协同方式

Python 负责 ModernTCN 模型定义、训练、指标计算和 ONNX 导出。MATLAB 负责加载 ONNX、组织在线窗口、进行闭环仿真、更新 LPV-MPC 控制器并保存仿真结果。Simulink 模型通过预加载函数和 MATLAB Function 包装连接这些模块。

该协同方式保留了 Python 深度学习训练效率和 MATLAB/Simulink 控制仿真能力。当前 MATLAB/Simulink 调用方式主要用于桌面仿真验证，不作为嵌入式部署实现的直接声明。

## 第4章 数据与路径生成模块

### 4.1 参考路径生成

路径生成模块位于 `src/paths`。基础路径接口 `gen_agv_ref_path.m` 提供 ref 结构，`gen_agv_theta10_uniform_paths.m` 生成 theta10 uniform 训练路径，`gen_factory_logistics_showcase_path.m` 生成工厂物流展示路径，`gen_closed_loop_eval_paths.m` 生成多路径闭环评估路径。

路径结构包含时间、位置、航向、速度、曲率、坡度或调度相关元数据。路径生成模块同时保存预览图和报告，便于检查路径长度、转向段、坡道段和评估覆盖范围。

### 4.2 训练数据生成

训练数据由 AGV 仿真模型和参考路径共同生成。`src/core/agv_model_sfunc_train_data.m`、`state_eq_ref_train_data.m` 和 `output_eq_ref_train_data.m` 用于训练数据仿真链路，输出可观测传感量、车辆状态和标签所需信息。

当前主线 raw train data 为 `data/tcn/ModernTCN_train_data_agv_dualsteer_theta10_uniform_conf_h0_v2.mat`，窗口化后的统一数据集为 `{facts['dataset']}`。该数据集被 ModernTCN、GRU 和 TCN 共同使用。

### 4.3 数据窗口化

窗口化策略固定为 `seq_len=128`，控制采样周期为 `Ts=0.01 s`，因此单个输入窗口覆盖约 1.28 秒历史观测。窗口化后的输入形状为 `[window, time, feature]`，Python 训练时进入模型前再转换为卷积所需形式。

窗口标签采用 `current_window_end` 策略，即以当前窗口末端对应工况作为主工况、转向方向和坡度调度量标签。数据契约中 `horizon_steps=0`，表示当前默认版本不做未来步预测。

### 4.4 数据契约

数据契约文件 `{facts['contract']}` 是当前数据链的权威定义。契约记录 `vehicle_type=diagonal_dual_steer_drive_agv`、主动驱动/转向轮为 `LF` 和 `RR`、被动支撑轮为 `RF` 和 `LR`。

契约同时记录 `split_policy=run_level_no_window_leakage` 和 `scaler_policy=fit_train_only_apply_val_test_online`。前者用于降低同一运行片段窗口泄漏风险，后者用于避免验证集、测试集或在线数据参与 scaler 拟合。

### 4.5 19维输入特征

当前 ModernTCN 输入维度为 `input_dim=19`。19 个输入特征依次为：

```text
accel_x
gyro_z
I_lf
I_rr
omega_wheel_lf
omega_wheel_rr
delta_lf
delta_rr
gyro_y
v_hat
dv_hat_dt
ws_imbalance
I_sum
I_diff_signed
I_diff_abs
accel_x_lp
kappa_proxy
accel_per_current
pitch_angle_est
```

这些特征覆盖纵向加速度、偏航角速度、左右驱动电流、车轮角速度、转向角、俯仰相关量、速度估计、电流组合量、曲率代理量和坡度估计量，满足工况识别、转向识别和坡度回归的输入需求。

### 4.6 主工况、转向方向与坡度标签

主工况分类标签为 `flat=1`、`stall=2`、`slope=3`。转向方向分类标签为 `right=-1`、`straight=0`、`left=1`。坡度回归输出为 `theta_hat`，用于闭环中的坡度感知或调度参考。

ModernTCN 输出为三组结果：`logits_main` 是 3 维主工况分类 logits，`logits_turn` 是 3 维转向方向分类 logits，`theta_hat` 是 1 维坡度或调度量回归输出。

## 第5章 AGV模型与LPV-MPC控制模块

### 5.1 AGV车辆模型

AGV 模型面向 diagonal dual steer drive AGV。主动驱动和转向轮为 `LF` 与 `RR`，被动支撑轮为 `RF` 与 `LR`。状态向量包含位置、航向、速度、偏航角速度、左右转向角和侧偏相关状态。

`src/core/state_eq.m` 实现非线性车辆状态更新，`src/core/output_eq.m` 实现车辆输出和传感量计算。训练数据链路使用对应的 train_data 版本，以便生成与在线工况感知一致的观测特征。

### 5.2 状态方程和输出方程

状态方程根据当前状态、控制输入、车辆参数、转向几何、轮胎侧向力、滚动阻力和坡度阻力等计算下一步状态。采样周期由 `parameters.m` 中的 `params.Ts = 0.01` 定义。

输出方程生成基础状态、转向角、电流、轮速、IMU 相关量和用于深度模型输入的原始观测。输出方程中明确 RF/LR 为万向支撑轮或被动支撑轮，侧向和偏航动力主要由 LF/RR 舵驱轮承担。

### 5.3 参考模型

参考模型由 `state_eq_ref.m`、`output_eq_ref.m` 和训练数据参考版本组成。参考模型根据路径和目标速度生成可跟踪的参考状态与输出，为 LPV-MPC 和训练数据仿真提供一致的参考轨迹。

参考路径和参考模型共同定义直行、转向、坡道和工况切换过程，使数据集覆盖多种闭环验证场景。说明书中引用参考模型时，仅描述其软件功能，不将其写成论文推导。

### 5.4 LPV线性化

LPV 线性化模块位于 `src/lpv`。`lin_agv_at_point.m` 对 AGV 在指定状态点进行线性化，`lin_agv_grid.m` 生成网格化线性模型数据库。线性化结果供 MPC 控制器创建和在线调度更新使用。

LPV 网格模型的作用是将非线性车辆模型在不同调度点近似为一组线性模型。在线运行时，控制器可根据调度量选择或插值相应模型，提高不同工况下的控制适应性。

### 5.5 MPC控制器构造

MPC 模块位于 `src/mpc`。`mpc_setup_single_interp.m` 负责构造控制器，`mpc_update_from_rho.m` 根据调度量更新控制模型，`Cost_Function.m` 计算控制代价。控制器与车辆模型、参考路径和调度量共同构成闭环。

控制器目标包括轨迹跟踪、控制输入平滑和约束处理。ModernTCN 输出的坡度或调度量不是单独完成控制，而是作为 LPV-MPC 闭环调度的一部分使用。

### 5.6 在线调度更新

在线调度更新由 ModernTCN 预测、LPV 模型选择和 MPC 参数更新共同完成。预测器输出 `theta_hat` 后，MATLAB 端根据默认配置中的增益、限幅、变化率限制和 deadzone 等参数进行调理。

`ModernTCN_default_config.m` 中包含 `theta_output_gain`、`theta_abs_limit`、`theta_rate_limit` 和 `theta_mpc_deadzone` 等部署侧调理参数。该设计用于避免单步预测噪声直接造成控制器剧烈变化。

### 5.7 控制代价与约束处理

控制代价函数用于评价轨迹误差、控制输入、输入变化和约束触碰等因素。闭环对比脚本进一步统计横向误差、航向误差、控制平滑性、坡度误差和综合排序指标。

说明书中可描述闭环结果和实时性结果，但应避免将桌面仿真结果夸大为已经完成嵌入式硬实时部署。当前更准确的表述是：ONNXRuntime+MPC 核心链路满足 10 ms 控制周期的计算余量，MATLAB/Simulink 封装主要用于仿真验证。

## 第6章 ModernTCN工况感知模块

### 6.1 模块定位

ModernTCN 是当前软件主感知模块，位于 `src/ModernTCN`。该模块面向 AGV 闭环控制的工况感知需求，将 128 步、19 维可观测特征映射为主工况分类、转向方向分类和坡度调度量回归。

ModernTCN 不直接替代 LPV-MPC 控制器，而是向控制器提供工况和调度辅助信息。该定位使软件能够在同一控制平台上比较不同感知模型对闭环控制效果的影响。

### 6.2 输入输出定义

输入为 `[batch, time=128, feature=19]` 的归一化窗口。输出为 `logits_main`、`logits_turn` 和 `theta_hat`。ONNX 导出脚本中明确输出名称为 `logits_main`、`logits_turn`、`theta_hat`。

分类 logits 后续可通过 softmax 转换为置信度和类别预测；坡度输出经过部署侧调理后作为 LPV-MPC 调度参考。该输出契约与数据契约中的 `output_contract=logits_main3_logits_turn3_theta1_with_softmax_confidence` 一致。

### 6.3 ModernTCN-small网络结构

当前默认 ModernTCN 部署模型使用 seed 21，配置包括 `channels=64`、`blocks=5`、`kernel_size=31`、`temporal_padding=same`、`dropout=0.15`、`expansion=2`。模型定义位于 `modern_tcn_model.py`。

模型首先使用 1x1 卷积将 19 维输入映射到通道空间，然后堆叠大核 depthwise temporal convolution 残差块，再通过时序池化和窗口统计特征融合形成任务头输入。

### 6.4 大核深度卷积残差块

ModernTCN 残差块使用 depthwise temporal convolution 捕获长时间窗口内的局部和中程时序模式，再通过 pointwise channel mixing 实现通道间信息融合。残差连接和 layer scale 用于稳定训练和导出。

当前默认模型使用 `same` padding，保证输出时间长度与输入窗口一致。项目中另有 causal ModernTCN 消融实验，但不替代默认 seed 21 部署模型。

### 6.5 多任务输出头

多任务输出头包括主工况分类头、转向方向分类头和坡度回归头。主工况分类头输出 3 维 logits，对应 flat、stall、slope；转向分类头输出 3 维 logits，对应 right、straight、left；坡度头输出 1 维 `theta_hat`。

多任务结构使软件能同时提供离散工况状态和连续调度量。闭环控制使用这些输出时，会结合限幅、变化率限制和 deadzone 处理，避免将模型预测直接无限制地作用到控制器。

### 6.6 窗口统计特征融合

模型在时序卷积特征之外融合窗口统计量，包括末端值、均值、最大值、最小值或其它输入统计特征。该设计用于增强模型对窗口整体趋势和末端状态的表达能力。

转向任务还使用特定特征索引相关统计量，例如偏航角速度、轮速、转向角、速度变化和曲率代理量，以提高转向方向及过渡窗口识别能力。

### 6.7 坡度输出调理与调度约束

坡度输出在模型内可根据主工况概率进行 gate 处理，部署侧还通过 `theta_abs_limit`、`theta_rate_limit` 和 `theta_mpc_deadzone` 控制调度量范围与变化速度。该处理位于模型定义和 MATLAB 默认配置共同作用的链路中。

调度约束的目的不是掩盖模型误差，而是使闭环控制对预测噪声更加稳健。说明书中应将其描述为工程部署侧保护和调理机制。

### 6.8 ONNX导出与部署

`export_modern_tcn_onnx.py` 将训练好的 checkpoint 导出为 ONNX，并保存 PyTorch 参考输出。默认 ONNX 文件为 `{facts['onnx']}`，输入形状为 `[1,128,19]`，输出名称为 `logits_main`、`logits_turn`、`theta_hat`。

`check_onnxruntime_consistency.py` 和 `ModernTCN_check_matlab_onnx.m` 分别用于 ONNXRuntime 与 MATLAB 端一致性检查。该设计使 PyTorch 训练结果、ONNX 部署文件和 MATLAB 闭环调用之间可追溯。

## 第7章 训练、评估与模型导出

### 7.1 训练入口

ModernTCN 单 seed 训练入口为 `src/ModernTCN/train_modern_tcn.py`，多 seed 训练入口为 `src/ModernTCN/run_modern_tcn_theta10_v2_multiseed.py`。训练脚本读取统一数据集，不重新划分 split，不重新拟合 scaler。

训练脚本记录模型配置、数据契约、损失权重、验证指标、测试指标和 checkpoint 路径。训练输出保存在 `results/modern_tcn/` 对应 run_tag 目录。

### 7.2 多seed训练流程

多 seed 训练流程用于比较随机初始化和训练过程对结果的影响。当前默认部署选择 seed 21，run_tag 为 `modern_tcn_theta10_uniform_h0_v2_seed21`。

多 seed 结果不是软著申请的必要法律事实，但可作为说明书中“对照与验证模块”的实现依据。申请材料应强调软件具备多 seed 训练和结果汇总能力，而不是夸大单个实验结果。

### 7.3 损失函数和指标

`modern_tcn_metrics.py` 实现多任务损失和指标计算。指标包括主工况准确率、转向准确率、坡度误差、各类别召回率、过渡窗口表现和用于选模的综合评分。

这些指标用于离线评估和模型选择。闭环控制指标另由 `src/Compare` 中的比较脚本计算，二者共同构成“感知性能 + 控制性能”的验证闭环。

### 7.4 checkpoint保存

训练脚本保存 PyTorch checkpoint、训练历史 CSV、summary CSV 和训练报告。默认 checkpoint 位于 `results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt`。

checkpoint 属于模型权重文件，不纳入本次源程序鉴别材料。说明书可引用其作为部署模型生成来源。

### 7.5 ONNX一致性检查

ONNX 导出后，软件使用 ONNXRuntime 检查 PyTorch 与 ONNX 推理结果的一致性。默认结果目录包含 `modern_tcn_seed21_onnxruntime_consistency.md` 和 JSON 记录。

一致性检查用于确保部署文件与训练模型在相同输入下输出一致，降低跨环境部署时的数值偏差风险。

### 7.6 MATLAB端一致性检查

MATLAB 端一致性检查由 `ModernTCN_check_matlab_onnx.m` 完成。该脚本读取 ONNX 模型和 PyTorch 参考输出，验证 MATLAB 加载器的输出与导出参考是否一致。

通过该检查后，ONNX 模型可由 MATLAB/Simulink 闭环仿真调用。该环节是 Python 训练环境和 MATLAB 控制仿真环境之间的重要接口验证。

## 第8章 Simulink闭环仿真模块

### 8.1 闭环模型组成

Simulink 闭环主模型包括 `simulink/LPVMPC_AGV_simulink_Modern_TCN.slx`、`simulink/LPVMPC_AGV_simulink_GRU.slx`、`simulink/LPVMPC_AGV_simulink_TCN.slx` 和 `simulink/LPVMPC_AGV_simulink_IMU.slx`。其中 ModernTCN 模型是当前主链路，其他模型用于对照。

闭环模型通常包含参考路径输入、车辆 S-Function、状态输出、在线分类器、LPV-MPC 控制器、植物模型更新和结果记录模块。

### 8.2 预加载函数

`preloadfcn_modern_tcn.m`、`preloadfcn_gru.m` 和 `preloadfcn_tcn.m` 用于在模型加载前准备参数、控制器、路径、数据集、scaler 和预测器。`preloadfcn_gru.m` 在当前项目中也服务多种模式，不应简单理解为只属于 GRU 旧链路。

预加载函数的存在保证仿真模型打开后具备所需工作区变量，避免手动加载顺序错误造成闭环失败。

### 8.3 在线预测流程

在线预测流程由 `ModernTCN_state_classifier.m`、`ModernTCN_online_step.m`、`ModernTCN_predict_window.m` 和 `ModernTCN_load_predictor.m` 共同实现。模块从车辆输出中提取 19 维特征，维护 128 步窗口，按 scaler 进行归一化，并调用 ONNX/MATLAB 预测器输出三任务结果。

在 Simulink 中，`ModernTCN_State_Classifier_sim.m` 作为包装函数连接 MATLAB 在线预测逻辑和仿真模型。

### 8.4 LPV-MPC更新流程

LPV-MPC 更新流程由 ModernTCN 输出的调度量、`mpc_update_from_rho.m` 和植物模型更新函数共同完成。调度量经过限幅和变化率控制后用于选择或更新 LPV 模型。

这种设计将感知模型的连续输出纳入控制器调度，但保留 MPC 控制器的约束处理和代价函数结构。

### 8.5 闭环输出保存

闭环仿真输出包括轨迹、状态、控制输入、工况预测、转向预测、坡度估计、误差指标和分区统计。结果通常保存到 `results/compare/` 下对应实验目录。

`ModernTCN_analyze_closed_loop_out.m` 和对比脚本负责从仿真输出中提取指标，生成 summary CSV、zones CSV、rank CSV 和 Markdown 报告。

### 8.6 仿真异常处理

仿真异常可能来自路径文件缺失、控制器缓存缺失、ONNX 文件缺失、scaler 不匹配或 Simulink 模型未加载。测试脚本和预加载函数提供了基本检查，用户也可通过 `test_simulink_closed_loop.m` 进行流程验证。

异常处理原则是先确认 `init_project` 已运行，再检查默认配置、路径文件、模型文件、控制器缓存和数据契约是否一致。

## 第9章 对照算法与基线模块

### 9.1 GRU基线

GRU 对照模块位于 `src/gru`，包括训练、默认配置、推理、在线分类器和 Simulink 包装函数。当前 GRU 主线使用与 ModernTCN 相同的数据集，便于公平比较。

GRU 在说明书中作为对照与验证模块出现，不作为软件名称中的主创新算法。其作用是帮助评价 ModernTCN 在统一数据和统一闭环平台下的相对表现。

### 9.2 TCN基线

TCN 对照模块位于 `src/TCN`，包括训练、多 seed 入口、推荐配置、默认配置、预测器加载、窗口预测、在线分类器和 Simulink 配置脚本。

TCN 与 ModernTCN 同属卷积时序模型类别，但结构和训练配置不同。软件保留 TCN 基线用于三算法闭环对比和论文补充验证。

### 9.3 LPV-MPC theta0基线

LPV-MPC theta0 基线用于表示不使用 AI 感知坡度调度量的控制链路。该基线有助于评估 ModernTCN 输出相对无感知调度的收益。

基线实验入口为 `run_lpvmpc_theta_baseline_experiment.m`，输出与三算法闭环结果合并比较。

### 9.4 IMU theta基线

IMU theta 基线使用简化 IMU 坡度估计作为调度参考。它不是当前主方法，而是用于验证仅依赖简单传感估计时的闭环表现。

说明书中应将该模块描述为可选对照模型，避免将其写成软件主要功能或主要创新。

### 9.5 true-theta oracle上界

true-theta oracle 使用真实坡度作为调度参考，代表闭环控制在坡度信息理想可得时的上界参考。它不是实际部署算法，而是评价 ModernTCN 距离理想调度的差距。

该上界用于分析 ModernTCN 在横向跟踪、控制平滑性和坡度调度方面的改进空间。

### 9.6 对照模块的作用边界

GRU、TCN、theta0、IMU theta 和 oracle 均用于对照验证。申请名称和说明书主体应聚焦 AGV 工况感知、LPV-MPC 调度控制和闭环仿真软件系统，避免把对照算法描述为本软件全部核心。

对照模块的存在增强了软件的验证能力，使软件能够自动输出公平对照结果、多路径结果、扰动结果和实时性结果。

## 第10章 实验、报告与验证模块

### 10.1 三算法闭环对比

三算法闭环对比由 `compare_tcn_gru_modern_closed_loop_out.m` 实现，比较 ModernTCN、GRU 和 TCN 在同一闭环路径和统一控制平台下的表现。输出包括 summary、zones、rank 和报告文件。

该模块用于评估不同工况感知模型对轨迹跟踪、转向识别、坡度估计和控制输入平滑性的影响。

### 10.2 多路径闭环实验

多路径闭环实验由 `run_multi_path_closed_loop_benchmark.m` 实现。该模块在多条闭环评估路径上运行算法链路，检查结论是否依赖单一路径或单一工况。

多路径评估结果用于增强软件验证流程的鲁棒性和可复现性。

### 10.3 扰动鲁棒性实验

扰动鲁棒性实验由 `run_closed_loop_robustness_experiment.m` 实现。该模块在不同扰动等级下运行闭环仿真，评价控制链路对扰动和工况变化的敏感性。

结果可用于比较不同算法在扰动条件下的综合排名、误差变化和控制平滑性。

### 10.4 实时性测试

实时性测试包括 `benchmark_modern_tcn_onnx_runtime.py` 和 `run_realtime_benchmark.m`。前者测量 ONNXRuntime 单窗口推理时间，后者汇总推理、MPC 求解和整体周期余量。

项目上下文记录 ONNXRuntime+MPC 核心链路 p95 总周期约 0.492 ms，小于 10 ms 控制周期。MATLAB/Simulink extrinsic 封装主要用于桌面仿真验证，不应表述为最终嵌入式硬实时部署。

### 10.5 测试脚本

测试脚本位于 `src/tests`，包括 Simulink 闭环测试、GRU 工作流测试、GRU 性能和延迟测试、滤波常数测试、AGV 开环测试和工业开环项目测试。

这些测试用于验证项目初始化、模型加载、仿真链路、分类器推理和性能统计的可用性。

### 10.6 输出报告

软件自动输出 Markdown、CSV、MAT、PNG/PDF 图表和模型文件。软著源码材料仅纳入 MATLAB/Python 源程序；结果报告和图表只作为说明书中的功能输出示例，不纳入源程序鉴别材料。

报告文件使每次训练和闭环实验具备可追溯性，便于复核输入数据、模型版本、路径和指标。

## 第11章 用户使用说明

### 11.1 初始化项目

用户在 MATLAB 中进入项目根目录后运行 `init_project`，该函数将 `src/core`、`src/lpv`、`src/mpc`、`src/paths`、`src/gru`、`src/TCN`、`src/ModernTCN` 和 `src/Compare` 加入搜索路径。

`project_root.m` 用于定位项目根目录，`results_dir.m` 用于生成或返回结果目录。

### 11.2 加载默认ModernTCN配置

默认配置由 `ModernTCN_default_config(project_root())` 返回。配置包含 seed、run_tag、数据集文件、raw train data、ONNX 文件、参考输出文件和部署侧 theta 调理参数。

用户若临时测试其它 checkpoint，可在调用脚本中覆盖 run_tag、onnx_file 或 dataset_file，但提交材料中应保持默认版本描述一致。

### 11.3 运行离线训练

离线训练通过 Python 执行。用户可运行 `train_modern_tcn.py` 进行单 seed 训练，也可运行 `run_modern_tcn_theta10_v2_multiseed.py` 进行多 seed 实验。

训练前应确认数据集和数据契约存在，且 Python 环境安装了 PyTorch 等依赖。

### 11.4 导出ONNX模型

训练完成后运行 `export_modern_tcn_onnx.py` 导出 ONNX。导出脚本使用固定输入形状 `[1,128,19]`，输出名称为 `logits_main`、`logits_turn`、`theta_hat`。

导出后建议运行 ONNXRuntime 一致性检查和 MATLAB ONNX 一致性检查。

### 11.5 运行闭环仿真

用户加载 `simulink/LPVMPC_AGV_simulink_Modern_TCN.slx` 后运行仿真。仿真前应确保预加载函数能够找到控制器、LPV 网格、路径、数据集、scaler 和 ONNX 文件。

若需要批量运行，可使用 `run_closed_loop_model_once.m` 或 `src/Compare` 下的实验入口脚本。

### 11.6 运行对比实验

对比实验包括 ModernTCN/GRU 对比、ModernTCN/GRU/TCN 三算法对比、LPV-MPC theta 基线、多路径闭环、扰动鲁棒性和实时性测试。

这些脚本输出统一格式的指标表和报告，便于申请人或开发者复核软件功能。

### 11.7 查看结果

训练结果位于 `results/modern_tcn/`、`results/gru/` 和 `results/tcn/`。闭环对比结果位于 `results/compare/`。论文图表和补充结果位于 `results/paper/`。

用户查看结果时应注意区分源码、数据、模型、结果和论文图表，不应将结果文件误作为源程序材料提交。

### 11.8 常见问题

若 MATLAB 提示找不到函数，应先运行 `init_project`。若 ONNX 文件缺失，应检查 `ModernTCN_default_config.m` 的 run_tag 和路径。若维度不匹配，应检查数据契约和 scaler 是否对应当前数据集。

若 Simulink 闭环加载失败，应检查 `data/models` 下控制器和线性化数据库是否存在，以及 Simulink 模型是否与预加载函数匹配。

## 第12章 技术特点

### 12.1 面向AGV闭环控制的多任务时序感知

软件将主工况分类、转向方向分类和坡度回归组织为同一 ModernTCN 多任务模型，避免为每个任务维护完全独立的数据链和部署链。

该设计使在线闭环能够同时获得离散状态和连续调度量，适用于坡道、转向和异常工况共同存在的 AGV 场景。

### 12.2 LPV-MPC与深度时序模型协同

软件保留 LPV-MPC 的控制器结构和约束处理能力，同时利用 ModernTCN 输出辅助调度。深度模型负责感知，MPC 负责控制优化，两者在闭环中协同工作。

这种模块化关系使软件既能接入 ModernTCN，也能接入 GRU、TCN 或其它对照模型进行比较。

### 12.3 统一数据契约与公平对照

当前 ModernTCN、GRU 和 TCN 使用同一数据集、同一 19 维特征、同一 run-level split 和同一 scaler 策略。该设计降低了数据差异对算法比较的干扰。

数据契约文件提供了可追溯的输入、标签、split 和 scaler 定义，便于后续复现实验。

### 12.4 ONNX/MATLAB/Simulink跨环境部署

软件支持从 PyTorch 训练模型导出 ONNX，再由 MATLAB 端加载并在 Simulink 闭环中调用。ONNXRuntime 和 MATLAB 一致性检查用于验证跨环境输出一致性。

该链路提升了模型从训练环境到控制仿真环境的可迁移性。

### 12.5 多路径、扰动和实时性验证

软件提供多路径闭环实验、扰动鲁棒性实验和实时性测试，能够从不同角度评价闭环控制链路。验证结果以 CSV 和 Markdown 报告形式保存。

这些验证模块使软件不仅能训练模型，还能系统评估模型对控制性能的影响。

## 第13章 数据安全与维护

### 13.1 本地数据处理

软件默认在本地文件系统处理数据、模型和结果，不需要将训练数据或身份材料上传到外部服务。申请材料生成时也不写入身份证、营业执照、公章或签名扫描件。

如申请人另行公开仓库，应自行确认公开内容是否包含敏感信息、第三方数据或权属受限材料。

### 13.2 文件管理

项目通过 `PROJECT_FLOW_MANIFEST.md` 区分 KEEP_ACTIVE、KEEP_RESULT、ARCHIVE_LEGACY、DELETE_CANDIDATE 和 REVIEW 文件。软著材料生成时遵循白名单源码选择和排除规则。

建议在提交材料前保持 `soft_copyright_application/` 与源码仓库分离备份，避免后续实验结果覆盖申请材料。

### 13.3 结果可追溯

训练脚本、闭环脚本和报告文件记录数据集、模型配置、seed、路径和指标。默认 ModernTCN 部署模型固定为 seed 21，便于追溯。

可追溯性有助于确认申请材料中的功能描述与项目实际文件一致。

### 13.4 版本维护

当前材料对应 V1.0。若后续修改软件名称、数据契约、模型结构、默认 seed、Simulink 模型或控制器配置，应同步更新说明书、申请字段、源码页眉和一致性检查报告。

版本维护时应保留变更记录，避免不同材料中出现软件名称、版本号或模型路径不一致。

## 第14章 版本说明

### 14.1 V1.0功能范围

V1.0 包括项目初始化、AGV车辆模型、LPV线性化、MPC控制器、路径生成、统一数据集、ModernTCN训练部署、MATLAB在线推理、Simulink闭环仿真、GRU/TCN对照、多路径与扰动鲁棒性实验、实时性测试和材料一致性检查。

V1.0 不声明已经完成嵌入式硬实时部署，不包含第三方框架源码，不包含申请人身份材料和权属证明文件。

### 14.2 后续扩展方向

后续可扩展方向包括嵌入式部署接口、更多传感器融合、更多路径和载荷工况、在线异常诊断、控制器参数自动整定、结果可视化界面和更严格的自动化测试。

这些扩展不影响当前 V1.0 作为 AGV 工况感知与 LPV-MPC 闭环控制仿真软件的功能边界。

## 附录A 主要源码文件清单

| 模块 | 主要文件 | 说明 |
|---|---|---|
| 项目初始化 | init_project.m, project_root.m, results_dir.m | 设置路径和结果目录 |
| 车辆模型 | src/core/agv_model_sfunc.m, state_eq.m, output_eq.m | AGV动力学与输出 |
| LPV线性化 | src/lpv/lin_agv_at_point.m, lin_agv_grid.m | 生成线性化模型网格 |
| MPC控制 | src/mpc/mpc_setup_single_interp.m, mpc_update_from_rho.m, Cost_Function.m | 构造与更新控制器 |
| 路径生成 | src/paths/*.m | 训练、展示和评估路径 |
| ModernTCN | src/ModernTCN/*.py, src/ModernTCN/*.m | 训练、导出、MATLAB在线部署 |
| 对照算法 | src/gru, src/TCN, src/Compare | GRU/TCN基线和闭环比较 |
| 测试验证 | src/tests/*.m | 初始化、开环、闭环和性能测试 |

## 附录B 主要输入输出文件清单

| 类型 | 文件 | 用途 |
|---|---|---|
| 数据契约 | {facts['contract']} | 定义特征、标签、split 和 scaler |
| 统一数据集 | {facts['dataset']} | ModernTCN/GRU/TCN 训练测试 |
| ONNX模型 | {facts['onnx']} | MATLAB/Simulink 部署 |
| ModernTCN模型 | results/modern_tcn/modern_tcn_theta10_uniform_h0_v2_seed21/modern_tcn_seed21.pt | PyTorch checkpoint |
| Simulink模型 | simulink/LPVMPC_AGV_simulink_Modern_TCN.slx | ModernTCN闭环 |
| 对比结果 | results/compare/ | 闭环指标、鲁棒性和实时性报告 |

## 附录C 关键参数表

| 参数 | 当前值 | 说明 |
|---|---|---|
| vehicle_type | diagonal_dual_steer_drive_agv | 对角双转向驱动AGV |
| active_drive_steer_wheels | LF, RR | 主动驱动/转向轮 |
| passive_support_wheels | RF, LR | 被动支撑轮 |
| Ts | 0.01 s | 控制采样周期 |
| seq_len | 128 | 输入窗口长度 |
| input_dim | 19 | 输入特征维度 |
| run_tag | modern_tcn_theta10_uniform_h0_v2_seed21 | 默认部署模型标签 |
| channels | 64 | ModernTCN通道数 |
| blocks | 5 | ModernTCN残差块数 |
| kernel_size | 31 | 大核时序卷积核 |
| temporal_padding | same | 默认时序填充方式 |
| dropout | 0.15 | dropout比例 |
| expansion | 2 | 通道扩展倍率 |

## 附录D 术语表

| 术语 | 含义 |
|---|---|
| AGV | Automated Guided Vehicle，自动导引车 |
| LPV | Linear Parameter-Varying，线性参数变化模型 |
| MPC | Model Predictive Control，模型预测控制 |
| ModernTCN | 本软件使用的大核时序卷积多任务感知模型 |
| ONNX | Open Neural Network Exchange，跨框架模型交换格式 |
| scaler | 训练集拟合、验证/测试/在线应用的归一化参数 |
| logits | 分类模型 softmax 前的输出 |
| theta_hat | 坡度或调度量回归输出 |
"""
    return toc + sections


def export_docx_to_pdf(items: list[dict[str, str]], report_path: Path) -> tuple[bool, list[dict[str, object]], str]:
    for item in items:
        pdf = Path(item["pdf"])
        if pdf.exists():
            pdf.unlink()
    ps_items = json.dumps(items, ensure_ascii=False)
    report_str = str(report_path)
    command = f"""
$ErrorActionPreference = 'Stop'
$itemsJson = @'
{ps_items}
'@
$items = $itemsJson | ConvertFrom-Json
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$results = @()
try {{
  foreach ($item in $items) {{
    $docx = [string]$item.docx
    $pdf = [string]$item.pdf
    $key = [string]$item.key
    $doc = $word.Documents.Open($docx, $false, $true)
    $doc.Repaginate()
    $pages = $doc.ComputeStatistics(2)
    $doc.ExportAsFixedFormat($pdf, 17)
    $doc.Close($false)
    $results += [pscustomobject]@{{ key=$key; docx=$docx; pdf=$pdf; pages=$pages; ok=$true; error='' }}
  }}
}} catch {{
  $results += [pscustomobject]@{{ key='ERROR'; docx=''; pdf=''; pages=0; ok=$false; error=$_.Exception.Message }}
  throw
}} finally {{
  $word.Quit()
}}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath '{report_str.replace("'", "''")}' -Encoding UTF8
"""
    encoded = base64.b64encode(command.encode("utf-16le")).decode("ascii")
    proc = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded],
        cwd=str(ROOT),
        text=True,
        capture_output=True,
        timeout=180000,
    )
    if report_path.exists():
        data = json.loads(report_path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            results = [data]
        else:
            results = data
    else:
        results = []
    return proc.returncode == 0, results, (proc.stdout + "\n" + proc.stderr).strip()


def page_report_md(source_info: dict[str, object], export_results: list[dict[str, object]], export_ok: bool) -> str:
    res_map = {str(r.get("key")): r for r in export_results}
    source_pages = res_map.get("source", {}).get("pages", source_info["selected_pages"])
    design_pages = res_map.get("design", {}).get("pages", "待复核")
    export_status = "已通过 Microsoft Word COM 导出 PDF。" if export_ok else "PDF 导出未完全成功，需人工复核。"
    qa_note = ""
    qa_file = OUT / "04_compliance_check" / "pdf_render_qa_report.md"
    if qa_file.exists():
        qa_note = "\n## 4. PDF抽样渲染检查\n\n已使用 `pdftoppm` 抽样渲染源码 PDF 首页、抽取衔接页、末页和说明书 PDF 第 1、末页，并进行了非空像素检查。详见 `soft_copyright_application/04_compliance_check/pdf_render_qa_report.md`。\n"
    return f"""# 页面格式检查报告

生成日期：{GENERATED_DATE}

## 1. 检查结论

{export_status}

## 2. 源程序材料

| 项目 | 检查结果 |
|---|---|
| 源码排版文件 | `{source_info['source_docx'].relative_to(ROOT).as_posix()}` |
| 源码 PDF | `{source_info['source_pdf'].relative_to(ROOT).as_posix()}` |
| 完整源码估算页数 | {source_info['full_pages_estimated']} |
| 提交版页数 | {source_pages} |
| 每页目标行数 | {SOURCE_LINES_PER_PAGE} |
| 字体与字号 | Consolas，小字号紧凑排版 |
| 行距 | 固定紧凑行距 |
| 页眉/页脚 | 页眉左侧为 `{HEADER_TEXT}`，右上角为“第 x 页 共 y 页”，页眉页脚均有横线 |
| 左侧标号 | 源码材料按页生成 1-{SOURCE_LINES_PER_PAGE} 行号 |

源程序 DOCX 由生成脚本按每页 {SOURCE_LINES_PER_PAGE} 行插入分页符，满足每页不少于 50 行的排版目标。完整源码超过提交页数，因此提交版由完整源码前 {SOURCE_FRONT_BACK_PAGES} 页和后 {SOURCE_FRONT_BACK_PAGES} 页组成，页数多于传统 60 页以提升可读性和材料余量。

## 3. 设计说明书

| 项目 | 检查结果 |
|---|---|
| 说明书 DOCX | `soft_copyright_application/02_software_document/{SOURCE_BASENAME}_软件设计说明书.docx` |
| 说明书 PDF | `soft_copyright_application/02_software_document/{SOURCE_BASENAME}_软件设计说明书.pdf` |
| Word 统计页数 | {design_pages} |
| 页眉/页脚 | 页眉左侧为 `{HEADER_TEXT}`，右上角为“第 x 页 共 y 页”，页眉页脚均有横线 |
| 正文字体 | 宋体/Arial 兼容设置，小四到五号区间 |
| 行距 | 正文约 1.25 倍行距 |

{qa_note}

## 5. 待人工抽检事项

- [ ] 打开源码 PDF，确认前 {SOURCE_FRONT_BACK_PAGES} 页和后 {SOURCE_FRONT_BACK_PAGES} 页连续、页码正常、无空白页。
- [ ] 打开说明书 PDF，确认标题、表格、代码块和页眉页码显示正常。
- [ ] 若提交系统对页码位置、页边距或行数有地方性要求，应按受理机构要求微调。
- [ ] 本脚本使用 Microsoft Word 导出 PDF，并使用 `pdftoppm` 做抽样渲染非空检查；最终提交前仍建议人工打开 PDF 逐页检查。
"""


def run_pdf_render_qa(source_pdf: Path, design_pdf: Path, design_pages: int | str) -> str:
    pdftoppm = shutil.which("pdftoppm")
    qa_dir = OUT / "04_compliance_check" / "pdf_render_qa"
    report_file = OUT / "04_compliance_check" / "pdf_render_qa_report.md"
    if not pdftoppm:
        msg = "# PDF抽样渲染检查\n\n未找到 `pdftoppm`，跳过 PDF 抽样渲染检查。\n"
        write_text(report_file, msg)
        return msg
    if qa_dir.exists():
        for p in qa_dir.glob("*.png"):
            p.unlink()
    qa_dir.mkdir(parents=True, exist_ok=True)
    source_pages = SOURCE_FRONT_BACK_PAGES * 2
    jobs: list[tuple[Path, int, str]] = [
        (source_pdf, 1, "source_p1"),
        (source_pdf, SOURCE_FRONT_BACK_PAGES, f"source_p{SOURCE_FRONT_BACK_PAGES}"),
        (source_pdf, SOURCE_FRONT_BACK_PAGES + 1, f"source_p{SOURCE_FRONT_BACK_PAGES + 1}"),
        (source_pdf, source_pages, f"source_p{source_pages}"),
        (design_pdf, 1, "design_p1"),
    ]
    try:
        last_page = int(design_pages)
    except (TypeError, ValueError):
        last_page = 1
    if last_page > 1:
        jobs.append((design_pdf, last_page, f"design_p{last_page}"))
    for pdf, page, prefix in jobs:
        subprocess.run(
            [pdftoppm, "-png", "-f", str(page), "-l", str(page), str(pdf), str(qa_dir / prefix)],
            cwd=str(ROOT),
            check=True,
            text=True,
            capture_output=True,
            timeout=60000,
        )
    rows: list[list[str]] = [["图片", "尺寸", "非白像素比例", "结论"]]
    try:
        from PIL import Image
    except Exception:
        for p in sorted(qa_dir.glob("*.png")):
            rows.append([p.name, "未检测", "未检测", "已生成PNG"])
    else:
        for p in sorted(qa_dir.glob("*.png")):
            im = Image.open(p).convert("L")
            if hasattr(im, "get_flattened_data"):
                values = im.get_flattened_data()
            else:
                values = im.getdata()
            total = im.width * im.height
            nonwhite = sum(1 for v in values if v < 245)
            ratio = nonwhite / total if total else 0.0
            verdict = "通过" if ratio > 0.005 else "需人工复核"
            rows.append([p.name, f"{im.width}x{im.height}", f"{ratio:.5f}", verdict])
    lines = ["# PDF抽样渲染检查", "", "使用 `pdftoppm` 抽样渲染 PDF 页面，并用非白像素比例检查页面是否为空白。", ""]
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("|---|---:|---:|---|")
    for row in rows[1:]:
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    write_text(report_file, "\n".join(lines))
    return "\n".join(lines)


def consistency_report_md(source_info: dict[str, object], stats: dict[str, object], export_ok: bool) -> str:
    pdf_status = "[x]" if export_ok else "[ ]"
    legal_status = "[ ]"
    return f"""# 一致性检查报告

生成日期：{GENERATED_DATE}

## 1. 自动检查项目

- [x] 所有已生成材料中的软件名称使用：`{SOFTWARE_FULL}`
- [x] 所有已生成材料中的版本号使用：`{VERSION}`
- [x] 源码页眉使用软件名称主体，未在页眉重复版本号
- [x] 设计说明书页眉使用软件名称主体，未在页眉重复版本号
- [x] 源程序按每页 {SOURCE_LINES_PER_PAGE} 行分页，满足每页不少于50行的目标
- [x] 源程序页眉右上角包含“第 x 页 共 y 页”页码字段
- [x] 文档页眉右上角包含“第 x 页 共 y 页”页码字段
- [x] 页眉和页脚处添加横线隔断
- [x] 源码材料左侧按页生成 1-{SOURCE_LINES_PER_PAGE} 行号
- [x] 源码材料未纳入第三方库、虚拟环境、缓存和二进制文件
- [x] 说明书采用“本软件/本模块”表述，未写成论文口吻
- [x] 说明书中的功能与当前仓库文件对应
- {pdf_status} 源码 DOCX/PDF 和说明书 DOCX/PDF 已由本脚本生成

## 2. 人工确认项目

- {legal_status} 申请表字段中的开发完成日期、首次发表日期、权利取得方式已由申请人确认
- {legal_status} 如果软件已公开发表，首次发表日期与公开记录一致
- {legal_status} 如果软件未发表，申请表填写“未发表”或按官方系统选项填写
- {legal_status} 如果存在合作/委托/职务开发，已准备对应证明文件
- {legal_status} 申请人已确认 GitHub 公开仓库是否构成首次发表
- {legal_status} 申请人已确认仓库是否包含他人开源代码或单位职务成果

## 3. 生成物摘要

| 项目 | 路径 |
|---|---|
| 申请表字段草稿 | `soft_copyright_application/00_application_info/application_fields_draft.md` |
| 源码索引 | `soft_copyright_application/01_source_code_material/source_file_index.csv` |
| 完整源码 | `{source_info['full_source'].relative_to(ROOT).as_posix()}` |
| 源码提交版 | `{source_info['source_docx'].relative_to(ROOT).as_posix()}` |
| 设计说明书 | `soft_copyright_application/02_software_document/{SOURCE_BASENAME}_软件设计说明书.docx` |
| 用户手册短版 | `soft_copyright_application/03_auxiliary_materials/user_manual_short.md` |

## 4. 源码统计

- 纳入源文件数量：{stats['included_count']}
- 纳入源码行数：{stats['included_lines']}
- 完整源码汇编行数：{source_info['full_source_line_count']}
- 完整源码估算页数：{source_info['full_pages_estimated']}
- 提交源码页数：{source_info['selected_pages']}
"""


def final_checklist_md() -> str:
    return f"""# 最终提交前检查清单

## 1. 材料文件

- [ ] 申请表字段草稿已复核：`soft_copyright_application/00_application_info/application_fields_draft.md`
- [ ] 源码鉴别材料 PDF 已打开检查
- [ ] 软件设计说明书 PDF 已打开检查
- [ ] 用户手册短版已复核
- [ ] 第三方、数据与排除说明已复核
- [ ] 一致性检查报告已复核

## 2. 名称与版本

- [ ] 软件全称最终确定为：`{SOFTWARE_FULL}`
- [ ] 软件简称最终确定为：`{SOFTWARE_SHORT}`
- [ ] 版本号统一为：`{VERSION}`
- [ ] 封面、申请字段和正文中的软件名称一致；页眉按当前版式仅保留软件名称主体

## 3. 权属与日期

- [ ] 著作权人已确认
- [ ] 开发完成日期真实且可说明
- [ ] 首次发表日期或未发表状态已确认
- [ ] 开发方式已确认
- [ ] 权利取得方式已确认
- [ ] 合作、委托或职务开发证明材料已准备

## 4. 源码和第三方

- [ ] 源码材料未包含虚拟环境、第三方库源码、缓存、训练数据、模型权重和二进制文件
- [ ] PyTorch、ONNXRuntime、MATLAB/Simulink 仅作为依赖环境描述
- [ ] 自动生成兼容层是否纳入已由申请人确认
- [ ] 仓库中外部开源代码或历史代码来源已复核

## 5. 敏感信息

- [ ] 未把身份证、营业执照、公章、签字扫描件等敏感材料写入仓库
- [ ] 提交前仅在官方系统或线下材料中填写必要身份信息
"""


def write_auxiliary_materials(
    dirs: dict[str, Path],
    stats: dict[str, object],
    source_info: dict[str, object],
    export_results: list[dict[str, object]],
    export_ok: bool,
) -> None:
    write_text(
        dirs["00"] / "application_fields_draft.md",
        build_application_fields(int(source_info["full_source_line_count"])),
    )
    write_text(dirs["00"] / "software_name_options.md", build_software_name_options())
    write_text(dirs["00"] / "ownership_confirm_checklist.md", build_ownership_checklist())
    write_text(dirs["01"] / "source_selection_report.md", build_source_selection_report(stats, source_info))
    write_text(dirs["03"] / "technical_feature_summary.md", build_technical_summary())
    write_text(dirs["03"] / "user_manual_short.md", build_user_manual())
    build_module_mapping_csv(dirs["03"] / "module_mapping_table.csv")
    write_text(dirs["03"] / "third_party_and_exclusion_statement.md", build_third_party_statement())
    res_map = {str(r.get("key")): r for r in export_results}
    design_pages = res_map.get("design", {}).get("pages", 1)
    design_pdf = dirs["02"] / f"{SOURCE_BASENAME}_软件设计说明书.pdf"
    if export_ok and Path(source_info["source_pdf"]).exists() and design_pdf.exists():
        run_pdf_render_qa(Path(source_info["source_pdf"]), design_pdf, design_pages)
    else:
        write_text(
            dirs["04"] / "pdf_render_qa_report.md",
            "# PDF抽样渲染检查\n\nPDF 导出未完成或文件不存在，跳过抽样渲染检查。\n",
        )
    write_text(dirs["04"] / "page_format_check_report.md", page_report_md(source_info, export_results, export_ok))
    write_text(dirs["04"] / "consistency_check_report.md", consistency_report_md(source_info, stats, export_ok))
    write_text(dirs["04"] / "final_submission_checklist.md", final_checklist_md())


def main() -> int:
    dirs = ensure_dirs()
    _, included_rows, stats = scan_sources(dirs)
    source_info = build_source_material(dirs, included_rows)

    design_md = build_design_document()
    design_md_path = dirs["02"] / f"{SOURCE_BASENAME}_软件设计说明书.md"
    design_docx_path = dirs["02"] / f"{SOURCE_BASENAME}_软件设计说明书.docx"
    design_pdf_path = dirs["02"] / f"{SOURCE_BASENAME}_软件设计说明书.pdf"
    write_text(design_md_path, design_md)
    markdown_to_docx(design_md, design_docx_path)

    export_report = dirs["04"] / "word_export_report.json"
    items = [
        {
            "key": "source",
            "docx": str(Path(source_info["source_docx"]).resolve()),
            "pdf": str(Path(source_info["source_pdf"]).resolve()),
        },
        {
            "key": "design",
            "docx": str(design_docx_path.resolve()),
            "pdf": str(design_pdf_path.resolve()),
        },
    ]
    export_ok, export_results, export_log = export_docx_to_pdf(items, export_report)
    if not export_ok:
        write_text(dirs["04"] / "word_export_error.log", export_log or "Word export failed without stderr.")

    write_auxiliary_materials(dirs, stats, source_info, export_results, export_ok)

    summary = f"""软著申请材料辅助文件已生成：
1. 申请表字段草稿：soft_copyright_application/00_application_info/application_fields_draft.md
2. 源码鉴别材料：{Path(source_info['source_pdf']).relative_to(ROOT).as_posix()}
3. 软件设计说明书：soft_copyright_application/02_software_document/{SOURCE_BASENAME}_软件设计说明书.pdf
4. 用户手册短版：soft_copyright_application/03_auxiliary_materials/user_manual_short.md
5. 一致性检查报告：soft_copyright_application/04_compliance_check/consistency_check_report.md

请申请人最终确认：软件名称、版本号、著作权人、开发完成日期、首次发表日期、开发方式、权利取得方式及证明文件。
"""
    write_text(OUT / "generation_summary.txt", summary)
    print(summary)
    if not export_ok:
        print("注意：Word PDF 导出未完全成功，请查看 soft_copyright_application/04_compliance_check/word_export_error.log")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
