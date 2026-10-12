# Redactions

Each place below was a private path (a path on the author's machine, or a link to a private repository) and is replaced by `(private path)` in the public copy. The workshop file is kept as it was: for a card, the one that was locked. The first hash is the workshop file's, the second the public copy's. Apart from the redaction nothing in a file is changed, except `README.md`, which also has its links rewritten to the public layout and the workshop's generated mark removed, a file whose keys `WITHHELD.md` lists as removed, and a register whose quoted passages are shortened (below).

| File | Workshop sha256 | Public sha256 | Places redacted |
|---|---|---|---|
| protocols/FT-001-M4-frame-a.md | 7149851f8aeb5a99ff7922f966a23f76c91d64b8960b48a74109955bc36edb6e | 4a8683d684fafc10ddcafdbf1c13b87304c9463566534e816376a34a3f73dafa | 1 |

## Passages shortened

Each source's passage quoted in the files below is shortened, in this copy, to at most 25 words (`...` marks a cut), so that no work is quoted at length; the locator beside it says where the whole passage is read. Figures read from a dataset are left whole.

| File | Workshop sha256 | Public sha256 | Passages shortened |
|---|---|---|---|
| code/p1_claims.yaml | 8cc9629a9297bd339a640b7d94594e7f44bbe227e6dd0771bbce6d87c1330b49 | 1440ee2c232012e88e164cf18c785b770ae52ac019206e2dd9936ea663f88253 | 148 |
| results/numbers.json | 822de24ffc038877fef542a2aa575beeddff95e3b972f2708eb1ae3085a52733 | 0a339b8204320f4cf3eea794f7c815507896e6dc16bfee7912506ecbe11625f0 | 148 |

## Second pass: internal wording removed (2026-10-12)

The first publication of this folder carried the project's internal vocabulary: the name of the person who decided, internal rule labels, paths in a private working tree, the names and versions of the models used, the name of the fetch-policy tool, and the process remarks that go with them. This pass replaces or removes that wording in every text file of the folder (49 files changed, plus the README). Labels such as W12 that remain in a code file or a manifest are the local numbering of rules defined in that same file; they are not references to anything outside this folder. No rule, number, source, date, code path or result was changed; the code still imports the same modules. Some scripts name internal notes that are not published, so they cannot be rerun from this folder, as the README says.

The hash that `results/runs/*.json` records for a card (`card_hash`) is that of the card as it was locked, before any result. Each card and protocol whose wording changed is listed here, with its sha256 as first published and as it stands now; the locked hash of a card is the first one, except for `protocols/FT-001-M4-frame-a.md`, listed above.

| File | sha256 as first published | sha256 now |
|---|---|---|
| cards/C18-cs-a-consumer-prices-off-gold.yaml | 09385dfdd821414b6d8ae1a234b02737ea59154e5193684b7bea8c3317a58424 | b24fde3a457d9c825155048f695440a87b1e8092b013d621577fc92e9f5a5eb8 |
| cards/C19-cs-b-inflation-by-convertibility.yaml | db75f966d7aa275723a4a9d8c039e51d04a9a88d7001299896e64ca0d15a131d | 0d26a8721b62ebcfa5c533425d57fe1b65a1fffc933df1045c52f9efd6199bc3 |
| cards/C20-cs-b-without-hyperinflation-years.yaml | 1ce4a63e9962a5195219aa03fc9c169f4133f86b28fbc26d84c21bb1507bc12d | 35b93bf14b01e5dcb9fd2d05c19187107336deb23b7bfa1805f98352433abcc1 |
| cards/C21-cs-a-what-a-unit-buys.yaml | 09255ff62cd9d893e7e253b8ade029945a3ead38c12e81428ef027d688d102ba | e710fd411dd657a035126de4c0158e9dc7fa59f0bd8e50fbc3f9ff543b82f4ae |
| cards/C22-cs-b-the-franc.yaml | c235dd7892bbd15151a0f802e284a6697831b28d9d82a958292b0fdfed2c9808 | ed437ec99d1711ef5c359938d04887690dc538fee16530d3f1a51759c1fff6fd |
| cards/C23-cs-c-losses-by-era.yaml | ed2506a667bd382c2a0177117030c8c546f8cb1f2a96551732941f3c784b8fd4 | 8319b5876eba6ad4973db6640731cfa97b0a5d7ba06ed260ad32016da328eedc |
| cards/C25-k9-crises-by-debt.yaml | 9a5377710ce9aff695a672b76a83400478501d44781255f8929c947ef4489282 | b4b1142587f671e5a301e202ceba3c4727dcab87695cca1b39b441ac4ee227ba |
| protocols/FT-001-M0-rules.md | ec966025dd97fb932527e54789da21047c75cc46e0a53166e0411d81df6b90f5 | 9efb362d602c4d13bde59491f8bf2a5bdb587404d56662052e4c51e1c28d3b4d |
| protocols/FT-001-M0-rules.yaml | 49adc537818184b9b48c9091bc59f296b50a59813b5eb9da5b87bb6a64985c04 | f1d31bfebd060f7090409921a21d2831cf9bee994d0501e55d9fb3195249742c |
| protocols/FT-001-M3-panel.md | f993b1be87c8dfbc769b13939b8b458c7b711a40b89a75ca542f10e74972ceb4 | e26413f3fae1a4315288db1eaffdd7e246291af0d24df4dd360eda07b4dba713 |
| protocols/FT-001-M4-A3-premiums.md | 2cf75f63c19f919abc3386be2070865990cb01f286abc2bd11bf7f626a37009b | ae970f945f929f2366bfec5d74adf1baf750a3018aabba8416aac0bdbc6f19c4 |
| protocols/FT-001-M4-frame-a.md | 4a8683d684fafc10ddcafdbf1c13b87304c9463566534e816376a34a3f73dafa | c8e1c186c4a3b2a4e4afee2c5ef9f013433a834d3a436379f6c58772976cae9e |
| protocols/a3.py | 0bbdf9d010f3b63b8d05f66828799c25e970d03d1952fc5289ff1d302975b6f0 | fb75a3d02e865199787c1a7b24745fbff33c8f9b0d85c409cd959493c7cdaaeb |
| protocols/breaks.py | de91930beb1faba1691e29bcf85f922ada7791fa71bba324e01b7f306b4e69ad | 55e20721734cd7fe69c1eb8df8fb1e63091d81f6682886f97f1958dfd9f29516 |
| protocols/economies.py | 7c644e78ba5a614d61cb1f2ba593c9c866760fe68e210cbbb5eca70e9117dca9 | c3d94b551db15c6e2ac6761cdcfdbf4e31d6272e3a765967afd8daa94322a3d7 |
| protocols/frame_a.py | 89404af2a326c7555ca7da25bac02aff8fb16d9f8be72dc2d24f7a5dcb482169 | 45086ec8758f9fcb43d84720c1cb9abbed91cec332e4605a3d30350237229933 |
| protocols/m0.py | 1f6c3c000e1e060fb527988acce95001720dbc4c0e600e7ee1c934750a911192 | e2e4cabca5f5a2e7887f25cc285647704f8a2ef420018e3302fe30fc7da74adb |
| protocols/panel.py | e74c00c234d3abe33494186dae98aadca9499e11db08e7bf5167129a6a8432a6 | 57415e1a3fba82f04d0c8af5388b2ae45304c7bdb4532490b2cc6e32b95e90f4 |
