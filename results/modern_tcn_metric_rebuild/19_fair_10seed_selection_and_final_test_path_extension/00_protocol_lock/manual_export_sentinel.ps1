# Manual export validation sentinel candidates

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'

# Export each selected validation sentinel candidate after offline screening.
# Read 03_offline_screen/offline_screen_decision.csv and keep rows where enter_validation_sentinel=true.
# For each row run:
#   python src\ModernTCN\export_modern_tcn_onnx.py --checkpoint <checkpoint_file> --onnx-file <candidate.onnx> --sample-file <candidate_pytorch_reference.mat> --no-overwrite
#   python src\ModernTCN\check_onnxruntime_consistency.py --onnx-file <candidate.onnx> --sample-file <candidate_pytorch_reference.mat>
