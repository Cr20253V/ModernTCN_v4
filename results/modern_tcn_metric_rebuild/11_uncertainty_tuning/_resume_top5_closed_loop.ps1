$ErrorActionPreference = 'Stop'

$root = 'E:\Matlab\Simulink\S-Function_16'
$nodeRoot = Join-Path $root 'results\modern_tcn_metric_rebuild\11_uncertainty_tuning'
$top5Root = Join-Path $nodeRoot '04_closed_loop_top5'

Set-Location -LiteralPath $root

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$logPath = Join-Path $top5Root "matlab_top5_closed_loop_resume_$stamp.log"

$batch = "cd('$root'); addpath(fullfile(pwd,'results','modern_tcn_metric_rebuild','11_uncertainty_tuning')); result = run_uncertainty_tuning_top5_closed_loop(struct('reuse_existing', true));"

"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] resume start" | Set-Content -Path $logPath -Encoding UTF8
matlab -batch $batch *>> $logPath
$exitCode = $LASTEXITCODE
"[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] resume exit_code=$exitCode" | Add-Content -Path $logPath -Encoding UTF8
exit $exitCode
