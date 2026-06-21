# Theta Error vs Main Error

- main correct theta MAE deg: `0.748159`
- main error theta MAE deg: `2.115911`
- theta absolute error top 5% cutoff deg: `2.281866`
- theta_edge_p95_abs_err_deg: `nan`

| group | n | theta_mae_deg | flat | stall | slope | pred_flat | pred_stall | pred_slope |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| main_correct | 3483 | 0.748159 | 733 | 69 | 2681 | 733 | 69 | 2681 |
| main_error | 119 | 2.115911 | 23 | 27 | 69 | 74 | 4 | 41 |
| flat_to_stall | 0 | nan | 0 | 0 | 0 | 0 | 0 | 0 |
| flat_to_slope | 23 | 1.003981 | 23 | 0 | 0 | 0 | 0 | 23 |
| slope_to_flat | 65 | 1.169136 | 0 | 0 | 65 | 65 | 0 | 0 |
| slope_to_stall | 4 | 2.476802 | 0 | 0 | 4 | 0 | 4 | 0 |
| theta_abs_error_top5pct | 181 | 4.125097 | 17 | 91 | 73 | 30 | 66 | 85 |
| theta_edge_abs_ge8 | 691 | 0.750652 | 0 | 0 | 691 | 0 | 2 | 689 |
