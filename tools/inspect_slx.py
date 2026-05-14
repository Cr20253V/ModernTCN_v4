import zipfile
import re
from pathlib import Path

slx_path = Path(r"E:/Matlab/Simulink/S-Function_16/simulink/LPVMPC_AGV_simulink_Mamba.slx")
with zipfile.ZipFile(slx_path) as z:
    data = z.read("simulink/stateflow/chart_60.xml").decode("utf-8", errors="ignore")

m = re.search(r'<P Name="script">([\s\S]*?)</P>', data)
script = m.group(1) if m else ""
# Script uses XML newline entity
lines = script.split("&#10;")

for i, line in enumerate(lines):
    if "y_wt" in line or "u_wt" in line or "du_wt" in line or "ecr_wt" in line:
        print("\n".join(lines[max(0, i-3):i+4]))
        print("---")
