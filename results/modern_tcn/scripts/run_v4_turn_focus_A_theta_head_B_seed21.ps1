$ErrorActionPreference = "Stop"

Set-Location "E:\Matlab\Simulink\S-Function_16"
$env:CUDA_VISIBLE_DEVICES = "0"
$env:PYTHONUNBUFFERED = "1"

$Tag = "modern_tcn_v4_turn_focus_A_theta_head_B_seed21"
$LogDir = "results\modern_tcn\logs"
$Log = Join-Path $LogDir "$Tag.log"
New-Item -ItemType Directory -Force $LogDir | Out-Null

"`n===== START $Tag $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" | Tee-Object -FilePath $Log

python src\ModernTCN\finetune_modern_tcn_theta.py `
  --checkpoint results\modern_tcn\modern_tcn_v4_turn_focus_A_seed21\modern_tcn_seed21.pt `
  --dataset-file data\tcn\ModernTCN_dataset_v4_industrial.mat `
  --run-tag $Tag `
  --seed 21 `
  --device cuda `
  --epochs 50 `
  --min-epochs 10 `
  --patience 12 `
  --batch-size 512 `
  --lr 1e-3 `
  --weight-decay 1e-5 `
  --lambda-theta 0.45 `
  --lambda-theta-flat 1.00 `
  --lambda-theta-near-flat 1.50 `
  --theta-near-flat-deg 0.50 `
  --select-theta-flat-p95-weight 2.00 `
  --select-theta-flat-bias-weight 1.00 `
  2>&1 | Tee-Object -FilePath $Log -Append

$exitCode = $LASTEXITCODE
"===== END $Tag exit=$exitCode $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" | Tee-Object -FilePath $Log -Append

if ($exitCode -ne 0) {
    throw "Theta fine-tune failed with exit code $exitCode"
}
