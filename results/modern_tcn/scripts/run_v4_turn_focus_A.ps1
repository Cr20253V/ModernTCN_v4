$ErrorActionPreference = "Stop"

Set-Location "E:\Matlab\Simulink\S-Function_16"
$env:CUDA_VISIBLE_DEVICES = "0"
$env:PYTHONUNBUFFERED = "1"

$Dataset = "data\tcn\ModernTCN_dataset_v4_industrial.mat"
$Seeds = @(11, 21, 42)
$RunPrefix = "modern_tcn_v4_turn_focus_A"
$LogDir = "results\modern_tcn\logs"
New-Item -ItemType Directory -Force $LogDir | Out-Null

foreach ($s in $Seeds) {
    $tag = "{0}_seed{1}" -f $RunPrefix, $s
    $log = Join-Path $LogDir "$tag.log"

    "`n===== START $tag $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" | Tee-Object -FilePath $log

    python src\ModernTCN\train_modern_tcn.py `
      --seed $s `
      --dataset-file $Dataset `
      --run-tag $tag `
      --device cuda `
      --epochs 150 `
      --min-epochs 40 `
      --patience 30 `
      --batch-size 256 `
      --num-workers 0 `
      --turn-head-source full `
      --lambda-turn 0.08 `
      --lambda-theta 0.35 `
      --lambda-theta-flat 0.25 `
      --lambda-theta-near-flat 0.10 `
      --turn-transition-weight 1.50 `
      --turn-class-multipliers 1.15 1.00 1.15 `
      --select-turn-weight 0.35 `
      --select-turn-transition-weight 2.00 `
      --select-turn-left-weight 0.20 `
      --select-turn-left-target 0.90 `
      --select-theta-flat-p95-weight 1.00 `
      --select-theta-flat-bias-weight 0.50 `
      2>&1 | Tee-Object -FilePath $log -Append

    $exitCode = $LASTEXITCODE
    "===== END $tag exit=$exitCode $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') =====" | Tee-Object -FilePath $log -Append

    if ($exitCode -ne 0) {
        throw "Training failed for $tag with exit code $exitCode"
    }
}
