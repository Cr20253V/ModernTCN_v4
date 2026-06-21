"""将训练好的 ModernTCN checkpoint 导出为 ONNX，并保存 PyTorch 参考输出。

导出前强制 `model.eval()`，固定输入形状 `[batch, 128, input_dim]`，不启用
dynamic axes。第一版默认 opset=17；如果 MATLAB 导入报算子不支持，再按
错误信息降级或替换模型算子。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import warnings
from pathlib import Path

import numpy as np
import torch
from scipy.io import savemat

from modern_tcn_data import find_project_root, load_modern_tcn_dataset
from modern_tcn_model import build_model_from_checkpoint_dict


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="导出 ModernTCN ONNX")
    p.add_argument("--checkpoint", type=str, required=True)
    p.add_argument("--onnx-file", type=str, default="")
    p.add_argument("--opset", type=int, default=17)
    p.add_argument("--sample-count", type=int, default=16)
    p.add_argument("--no-overwrite", "--no_overwrite", dest="no_overwrite", action="store_true")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if importlib.util.find_spec("onnx") is None:
        raise SystemExit("缺少 onnx。请先运行：python -m pip install onnx")
    if importlib.util.find_spec("onnxscript") is None:
        raise SystemExit("缺少 onnxscript。请先运行：python -m pip install onnxscript")
    root = find_project_root()
    checkpoint = Path(args.checkpoint)
    if not checkpoint.exists():
        raise FileNotFoundError(f"找不到 checkpoint：{checkpoint}")

    # checkpoint 内含普通 Python dict/list，显式关闭 weights_only 以兼容新版 PyTorch 默认策略。
    ckpt = torch.load(checkpoint, map_location="cpu", weights_only=False)
    model = build_model_from_checkpoint_dict(ckpt)
    model.eval()

    out_dir = checkpoint.parent
    onnx_file = Path(args.onnx_file) if args.onnx_file else out_dir / checkpoint.name.replace(".pt", ".onnx")
    sample_file = out_dir / checkpoint.name.replace(".pt", "_pytorch_reference.mat")
    meta_file = onnx_file.with_name(onnx_file.stem + "_onnx_export.json")
    if args.no_overwrite:
        existing = [p for p in [onnx_file, sample_file, meta_file] if p.exists()]
        if existing:
            raise FileExistsError("--no-overwrite enabled and export outputs already exist: " + ", ".join(str(p) for p in existing))

    dummy = torch.zeros(1, ckpt["model_config"]["seq_len"], ckpt["model_config"]["input_dim"], dtype=torch.float32)
    with torch.no_grad():
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                message="You are using the legacy TorchScript-based ONNX export.*",
                category=DeprecationWarning,
            )
            torch.onnx.export(
                model,
                dummy,
                onnx_file,
                export_params=True,
                opset_version=args.opset,
                do_constant_folding=True,
                input_names=["input_window"],
                output_names=["logits_main", "logits_turn", "theta_hat"],
                dynamo=False,
            )

    # 保存一组 test 窗口的 PyTorch 输出，供 ONNXRuntime 和 MATLAB 做三方一致性。
    data = load_modern_tcn_dataset(Path(ckpt["contract"]["dataset_file"]))
    X_sample = data["test"].X[: args.sample_count].astype(np.float32)
    with torch.no_grad():
        lm, lt, th = model(torch.from_numpy(X_sample).float())
    savemat(
        sample_file,
        {
            "X_sample": X_sample,
            "logits_main_pytorch": lm.numpy().astype(np.float32),
            "logits_turn_pytorch": lt.numpy().astype(np.float32),
            "theta_hat_pytorch": th.numpy().astype(np.float32),
        },
    )

    meta = {
        "checkpoint": str(checkpoint),
        "model_family": str(ckpt.get("model_family", "small")),
        "onnx_file": str(onnx_file),
        "sample_file": str(sample_file),
        "opset": args.opset,
        "input_shape": [1, ckpt["model_config"]["seq_len"], ckpt["model_config"]["input_dim"]],
        "output_names": ["logits_main", "logits_turn", "theta_hat"],
        "note": "导出前已调用 model.eval()；dropout 在 ONNX 推理中关闭；第一版固定 batch=1，离线批量检查脚本会逐窗口推理；当前默认使用 legacy TorchScript ONNX exporter 以获得更稳定的 PyTorch/ONNXRuntime 数值一致性。",
    }
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[ModernTCN ONNX] 导出完成")
    print(f"  onnx: {onnx_file}")
    print(f"  sample: {sample_file}")
    print(f"  meta: {meta_file}")


if __name__ == "__main__":
    main()
