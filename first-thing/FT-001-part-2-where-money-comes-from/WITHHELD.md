# Withheld

What this folder leaves out of the study's files, and why. The values a licence keeps from republication are cited, never republished: each dataset's manifest says where to fetch them.

## Keys removed from a file

| File | Keys | Why |
|---|---|---|
| `results/runs/C21-a4-1870-named.json` | `points` | each economy's ten-year windows from 1870 (money growth, inflation, output growth), computed from JST (CC BY-NC-SA 4.0) |
| `results/runs/C25-a4-base-hko-fill.json` | `points`, `windows_added` | each economy's ten-year windows, part of them computed from Ha, Kose and Ohnsorge's inflation database (cited, never republished) |
| `results/runs/C26-a5-deciders-hko-fill.json` | `episodes` | each episode's outcomes, part of them computed from Ha, Kose and Ohnsorge's inflation database (cited, never republished) |
| `results/runs/C27-a4-broad-hko-fill.json` | `points`, `windows_added` | each economy's ten-year windows, part of them computed from Ha, Kose and Ohnsorge's inflation database (cited, never republished) |
| `results/runs/C28-a4-units-guard.json` | `points`, `windows_changed` | each economy's ten-year windows on the filled grid, part of them computed from Ha, Kose and Ohnsorge's inflation database (cited, never republished) |
| `results/runs/C29-a4-exploration-pace.json` | `windows_dropped` | the windows it drops, taken from C28's filled grid (Ha, Kose and Ohnsorge's database in part) |
| `results/runs/C18-a5-deciders-bare.json` | `O4_nasdaq_pct`, `O4_houses_pct`, `D6_michigan_m0` | 36-month changes derived from NASDAQ's copyrighted index and S&P CoreLogic Case-Shiller's (FRED, pre-approval required), and the University of Michigan's expected inflation (copyrighted); the rest is C15's episodes with IMF IFS, WEO, World Bank, FRED and ECB deciders |
| `results/runs/C38-cs-g-money-and-real-growth.json` | `points` | each economy's ten-year windows from C28's filled grid, part of them computed from Ha, Kose and Ohnsorge's inflation database (cited, never republished); C27's filled windows are left out of the drawing but the rest still rests on the filled grid's units guard |
