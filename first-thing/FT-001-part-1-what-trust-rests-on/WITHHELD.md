# Withheld

What this folder leaves out of the study's files, and why. The values a licence keeps from republication are cited, never republished: each dataset's manifest says where to fetch them.

## Datasets published as their manifest only

Built by us, but not republished: they hold values from sources whose licence does not allow it, or transcribe a printed work's table (each row names its page). Each manifest says what it holds and where its sources are:

- `data/reconstructed/ft001-a/`
- `data/reconstructed/ft001-a-areaer/`
- `data/reconstructed/ft001-a-window/`
- `data/reconstructed/ft001-a3/`
- `data/reconstructed/ft001-acts/`
- `data/reconstructed/ft001-b/`
- `data/reconstructed/ft001-boards/`
- `data/reconstructed/ft001-bs3/`
- `data/reconstructed/ft001-c/`
- `data/reconstructed/ft001-cs-tables/`
- `data/reconstructed/ft001-k/`

## Files withheld

| File | Why |
|---|---|
| `figures/c1-lines.svg` | draws each economy's line of C07 (onsets, crossings and dated acts as coordinates), redacted from the run |
| `figures/c1-lines.png` | draws each economy's line of C07 (onsets, crossings and dated acts as coordinates), redacted from the run |

## Keys removed from a file

| File | Keys | Why |
|---|---|---|
| `results/runs/C06-now-coded.json` | `ka_open`, `irr_class_2016` | Chinn and Ito's KAOPEN values (all rights reserved) and Ilzetzki, Reinhart and Rogoff's 2016 classes (cited, never republished) |
| `results/runs/C08-now-coded-g25.json` | `ka_open`, `irr_class_2016` | Chinn and Ito's KAOPEN values (all rights reserved) and Ilzetzki, Reinhart and Rogoff's 2016 classes (cited, never republished) |
| `results/runs/C09-now-coded-g25-checked.json` | `ka_open`, `irr_class_2016` | Chinn and Ito's KAOPEN values (all rights reserved) and Ilzetzki, Reinhart and Rogoff's 2016 classes (cited, never republished) |
| `results/runs/C10-now-who-rule.json` | `ka_open`, `irr_class_2016` | Chinn and Ito's KAOPEN values (all rights reserved) and Ilzetzki, Reinhart and Rogoff's 2016 classes (cited, never republished) |
| `results/runs/C12-now-coded-g25b.json` | `ka_open`, `irr_class_2016` | Chinn and Ito's KAOPEN values (all rights reserved) and Ilzetzki, Reinhart and Rogoff's 2016 classes (cited, never republished) |
| `results/runs/C14-now-institution-m0.json` | `ka_open`, `irr_class_2016`, `cobham_first_year` | Chinn and Ito's KAOPEN values (all rights reserved), Ilzetzki, Reinhart and Rogoff's 2016 classes and Cobham's first years (cited, never republished) |
| `results/runs/C04-claim1-dated-lines.json` | `lines` | each economy's line: its crossing and onset dates, computed in part from Reinhart and Rogoff's and JST's series, frame c's entry and tercile (built in part from JST and Reinhart and Rogoff's debt), and its dated acts with each act's year before: ft001-acts, -b and -c ship their manifests only |
| `results/runs/C07-claim1-dated-lines-v2.json` | `lines` | each economy's line: its crossing and onset dates, computed in part from Reinhart and Rogoff's and JST's series, frame c's entry and tercile (built in part from JST and Reinhart and Rogoff's debt), and its dated acts with each act's year before: ft001-acts, -b and -c ship their manifests only |
| `results/runs/C15-claim1-institution-m0.json` | `lines` | each economy's line: its crossing and onset dates, computed in part from Reinhart and Rogoff's and JST's series, frame c's entry and tercile (built in part from JST and Reinhart and Rogoff's debt), and its dated acts with each act's year before: ft001-acts, -b and -c ship their manifests only |
| `results/runs/C18-cs-a-consumer-prices-off-gold.json` | `status_1932_34` | each economy's on- or off-gold status, 1932-34, from Bernanke and James's Table 2.1 (a table of a printed work, not republished) |
| `results/runs/C19-cs-b-inflation-by-convertibility.json` | `adoption_years`, `unclassed` | each economy's inflation-target adoption year, from ft001-a's frame a (Hammond's handbook and central banks' announcements), and the year ranges Bordo and Schwartz's Table 1A leaves unclassed (cited, never republished) |
| `results/runs/C20-cs-b-without-hyperinflation-years.json` | `set_apart` | the economy-years above 100% inflation with their yearly rates, JST's values (CC BY-NC-SA 4.0) |
| `results/numbers.json` | `bs3_arg_bw`, `bs3_arg_float`, `bs3_arg_gold`, `bs3_aus_bw`, `bs3_aus_float`, `bs3_aus_gold`, `bs3_bel_bw`, `bs3_bel_float`, `bs3_bel_gold`, `bs3_bra_bw`, `bs3_bra_float`, `bs3_bra_gold`, `bs3_can_bw`, `bs3_can_float`, `bs3_can_gold`, `bs3_che_bw`, `bs3_che_float`, `bs3_chl_bw`, `bs3_chl_float`, `bs3_chl_gold`, `bs3_deu_bw`, `bs3_deu_float`, `bs3_deu_gold`, `bs3_dnk_bw`, `bs3_dnk_float`, `bs3_dnk_gold`, `bs3_esp_bw`, `bs3_esp_float`, `bs3_esp_gold`, `bs3_fin_bw`, `bs3_fin_float`, `bs3_fin_gold`, `bs3_fra_bw`, `bs3_fra_float`, `bs3_fra_gold`, `bs3_gbr_bw`, `bs3_gbr_float`, `bs3_gbr_gold`, `bs3_grc_bw`, `bs3_grc_float`, `bs3_ita_bw`, `bs3_ita_float`, `bs3_ita_gold`, `bs3_jpn_bw`, `bs3_jpn_float`, `bs3_jpn_gold`, `bs3_nld_bw`, `bs3_nld_float`, `bs3_nld_gold`, `bs3_nor_bw`, `bs3_nor_float`, `bs3_nor_gold`, `bs3_prt_bw`, `bs3_prt_float`, `bs3_prt_gold`, `bs3_swe_bw`, `bs3_swe_float`, `bs3_swe_gold`, `bs3_usa_bw`, `bs3_usa_gold`, `door_boe_bullion_1796`, `door_boe_bullion_1797`, `door_boe_bullion_1798`, `door_boe_bullion_1799`, `door_boe_bullion_1800`, `door_boe_bullion_1801`, `door_boe_cover_1796`, `door_boe_cover_1797`, `door_boe_cover_1798`, `door_boe_cover_1799`, `door_boe_cover_1800`, `door_boe_cover_1801`, `door_boe_notes_1796`, `door_boe_notes_1797`, `door_boe_notes_1798`, `door_boe_notes_1799`, `door_boe_notes_1800`, `door_boe_notes_1801`, `door_cpi_fall_1797`, `door_cpi_infl_1797`, `door_cpi_infl_1798`, `door_cpi_infl_1799`, `door_cpi_infl_1800`, `csa_year_1930`, `csa_year_1935`, `csa_year_1936`, `now_usd_cobham_year` | Bordo and Schwartz's Table 3 cell by cell (a table of a printed work, not republished; the study prints only the G10 row, the exits' range, the gaps and the US float), the Bank of England Millennium dataset's 1796-1801 values, its bullion, notes, cover and consumer-price inflation (sheet A47) (never republished without the Bank's permission), Cobham's first US year (cited, never republished), and CS-A's yearly gaps for 1930, 1935 and 1936, where one side rests on two or three economies (close to single JST values, CC BY-NC-SA); no text prints them |
