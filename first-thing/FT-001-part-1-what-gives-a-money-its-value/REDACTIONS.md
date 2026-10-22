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

## Private paths redacted, added 2026-10-22

| File | Workshop sha256 | Public sha256 | Places redacted |
|---|---|---|---|
| protocols/FT-001-M4-frame-a.md | 7149851f8aeb5a99ff7922f966a23f76c91d64b8960b48a74109955bc36edb6e | c8e1c186c4a3b2a4e4afee2c5ef9f013433a834d3a436379f6c58772976cae9e | 1 |

## Passages shortened, added 2026-10-22

| File | Workshop sha256 | Public sha256 | Passages shortened |
|---|---|---|---|
| code/p1_claims.yaml | 508f6eb5b1c8f5b7504c985e99d610491dcd835acc78b49ed17ae0780038291b | db385bd47dd8a310f9c7f88f1dfe771a2660e48efb564af8fb71df5b0fc15f7e | 148 |
| results/numbers.json | d04d92c99eda73c946d85c3b10040a9361172f3118fa14e6e4202a4dee9bc585 | a518dcf37348e72adb0d578981e62f7f592c4742210d12622af7a110a846f9d7 | 148 |

## Wording neutralised, added 2026-10-22

| File | Workshop sha256 | Public sha256 | Card hash (workshop, public) |
|---|---|---|---|
| README.md | 0864fed39e7b14ff0dc5367fde78a3568c8a1f1649710009b66370dce165b222 | d0403c1c9bd9dcd062820cf93988ddfe8d457563efda233496e083682f8f38f2 | — |
| cards/C18-cs-a-consumer-prices-off-gold.yaml | 09385dfdd821414b6d8ae1a234b02737ea59154e5193684b7bea8c3317a58424 | b24fde3a457d9c825155048f695440a87b1e8092b013d621577fc92e9f5a5eb8 | 9e49813f70ec606d13495ffdad808ed2406c7c8f493ca802b17ee1185f10d847 a8b4d2f2a9915655bd5c431c8b9758bb01d09918e244762e3ad0ac3a70669296 |
| cards/C19-cs-b-inflation-by-convertibility.yaml | db75f966d7aa275723a4a9d8c039e51d04a9a88d7001299896e64ca0d15a131d | 0d26a8721b62ebcfa5c533425d57fe1b65a1fffc933df1045c52f9efd6199bc3 | 9ac1b8d2d7bd94f0571fffb3988e1d06ea05e9da4dfdcb7c497a8ceb611b21f3 b6a2bdcdd5b3792a57021de65406ef91c20750862111477574bc8a497f7804d0 |
| cards/C20-cs-b-without-hyperinflation-years.yaml | 1ce4a63e9962a5195219aa03fc9c169f4133f86b28fbc26d84c21bb1507bc12d | 35b93bf14b01e5dcb9fd2d05c19187107336deb23b7bfa1805f98352433abcc1 | 0998117e5c12461d36682c4bfb60d36c4788c8ce0289a8573dab046a25bea992 8bbf822d4da8da33dcfec900e2de79e287152d6db9e2b7694ca16ae90d31a44e |
| cards/C21-cs-a-what-a-unit-buys.yaml | 09255ff62cd9d893e7e253b8ade029945a3ead38c12e81428ef027d688d102ba | e710fd411dd657a035126de4c0158e9dc7fa59f0bd8e50fbc3f9ff543b82f4ae | 3f8540426f0bb90b4da1dc32691b923eb27fd01bc69afeded0b0e9399e2e5249 63543c8b7303dde77cda921938fa16ec71f9177d1d34510d6619e439d4867678 |
| cards/C22-cs-b-the-franc.yaml | c235dd7892bbd15151a0f802e284a6697831b28d9d82a958292b0fdfed2c9808 | ed437ec99d1711ef5c359938d04887690dc538fee16530d3f1a51759c1fff6fd | 6f335cbf73b7915453469cadbe950ca3d9753935ec4b7c9a72440d0b4939c09f 9562960a1b311ababd01bc10feb079aaceb269dbb1c3303c2ac92cf2ea483a00 |
| cards/C23-cs-c-losses-by-era.yaml | ed2506a667bd382c2a0177117030c8c546f8cb1f2a96551732941f3c784b8fd4 | 8319b5876eba6ad4973db6640731cfa97b0a5d7ba06ed260ad32016da328eedc | 3a5e95ea2f864a10aa38acc97865cc45874c45133eb12eacce77812f0c1f566f 3e476f50e18fb2ba3c2a6e1ef1c4f66694e420b248ab3318d14afa1301daa47f |
| cards/C25-k9-crises-by-debt.yaml | 9a5377710ce9aff695a672b76a83400478501d44781255f8929c947ef4489282 | b4b1142587f671e5a301e202ceba3c4727dcab87695cca1b39b441ac4ee227ba | 0bef4079cb40ddad35f36a9b9a8c556843d2ddbfea1341152ba317d93192cdfc a1c580e8e5ed86e336122d5d72fd4dd29a14709ef5ce15d2caef72361ca73bd5 |
| cards/C26-cs-c-losses-by-era-corrected.yaml | 324e3e326f441b7e1952626fbbe8ce8d00f32cc1bd5d4e03be2838a01b15bb51 | 2f97188955e1798ab47405d8e5358b2805010769e8b0bc24d10f2e1d115b4b16 | d2e7e4f2b85fc475dc348dbfc78b5ce8b7f5c7b1809e55ffad579e969cbb6b93 503ee9515e9d82c7b4724c900b5dbffd397e7ae96801759d55a74dec2bdd8294 |
| cards/C27-cs-c-years-in-crisis-corrected.yaml | de1e0b10b4423450f6df88dc0e06aaedce45272af4dda21fb4908e76d38dee9f | ece100cddaa97c2827e7bb04c4db39c380674ce8d7197dfa64137995b8a1b001 | 8cef023b7efc93bb49d1bb73024fa8ee53a798e2a430ca58d3b99266e2aa0e81 ac982644a2fd99fe27ba2df10a2329b75bdbbaeea8ed68a661f546ea1ec319b5 |
| cards/C28-cs-c-losses-by-era-kazakhstan.yaml | e6d21fe6696719f11009ab90f420181b11089614cc213f21fda0f049c52c41fc | b6ea4cf964b2a43ba020f63b3738bdb5fdd35bef7ef1f98e2fb3558b33bcf13d | 2dc05f4469a74e348e279616e2291a6b0e87c6274a7324cd894cc155e8ca06d0 1741f2b6ab0b2f7943d0bbf5003549f0e58276595f9d642ce864eec2e38f47fc |
| cards/C29-cs-c-years-in-crisis-kazakhstan.yaml | 021cd47f0812923ff9c1bbb1fa5ead04c5f7d76efcd08e7689bb19101fd9722d | 7b4a1ce173bb68d21a9c2436bbb7bca0873758069a1d9c4930ecfdb069e76099 | c10adf3f2344f333ca98d648676dfafd6547cbbac9ee4f6a5b96bcd00f5faafe 805ff577cd1280e9c06aec6631aeb1067e65ed5366913300550a6940b97cfb5a |
| code/case_sweep.py | 42b4ab84f67bd43a62afeb054709fa23fd73bf7af0ac0c7f5d9d05c9b995c9ef | ae1ad7b52c354f1d42093bf8357d893d5f094f79a2e712d71f4acee15ceb09ae | — |
| code/cs_a.py | 036c7ce71ecb4f0a9f168d3e5603e9212ea26f404e6c92059cf345b5c1c4ec2a | 89c1ebfa1188306175517a3c8477e76b0078c571d9f0f54337e1c28a5cae57ac | — |
| code/cs_b.py | bd062dd72e6b13e592a70645f3d90319391de1c9115326331bf605e492da65f8 | e0d532583ae694c32624688a3a7beb0dba69db17a354bb584cc38e993a343ce9 | — |
| code/cs_b_trim.py | 9b388ec5f944fc7614bd50be581853dc0ecd67c72494b50efb2c78d37d1dc891 | ff274841260753b06a14439042f6a615fb4a8e28fa3f1f367beb200ee94b5b25 | — |
| code/p1_claims.yaml | 508f6eb5b1c8f5b7504c985e99d610491dcd835acc78b49ed17ae0780038291b | db385bd47dd8a310f9c7f88f1dfe771a2660e48efb564af8fb71df5b0fc15f7e | — |
| code/p1_cs_a.py | 1fc1796830a657542807f80496483aca0064600264d0aee8979049b7a34b893a | 548ac94869bee97ca6018e8743a0cd6a33abb3ff6231f85c3819f0d9ba5ab7ef | — |
| code/p1_cs_b.py | b12411a800bb838ba6ae647a2e76ea26600447205a68c76c00a03af0911f2168 | bd98d9ec0fe4f9d96e9c37d8c2300f7fafaeca572900a4b28e9bddb540e2f2f8 | — |
| code/p1_cs_c.py | e644c0ea92654d6bd1a0174d204f58715f1ceb75b45cedb86880dc7994977def | 9c22ac331f4e4249dfc9aaddff8fc571ab3163910e42e5fc1b47440780b6307e | — |
| code/p1_cs_c_years.py | 16c342552b47bcae356f4e42b44c1ec9fd56e21b86973548b6d11fac954698a6 | d7f43c06a91c719072de02bf41800aa0746ebc332d9fc1e4a56433fd04e861c6 | — |
| code/p1_figures.py | 2388049f5658a51b071103cd608521d5fa5071e4a935c14e6e9991299eefc6c1 | d8ed6611f3a94c83b4b9349fb6d81084af29cd0a621c4c0e50930d6079b45bf6 | — |
| code/p1_k9_debt.py | 1bc34a4260917aad63e18ecf585247985006b9555edc7c58eb86a9fc5c7e28b0 | 0f2d4d849447c2723fd94dcde695764b6eab9773b9fe6c2d6d5e05021a9e17a3 | — |
| code/p1_og.py | 01408441115d0075a954d86728cfcdd26b7205e3d80c2c6d4013da7d9038fa95 | b012a8b85a7aa22cf6447631147c8b269c8e6cd38b376344561721baa41c5986 | — |
| code/p1_registry.py | a4d7e860b1683ac055ef5db8c7a45e1d58fe7389a23cf4e4550c2d9b446026ff | 7f304dc1d7345c8485300bedcb7c92a7e0653238ceaf449bd12893c0095e9de1 | — |
| code/run.py | 6fb5664dbfd08b5d8cbb593c9ba07ec7ac7ca6cb654a586bde70edbb62ec15d4 | d54950cde9d9d55b8aaf56b31bb36ba778cb410e240567ccf73ff48b8df7fd9d | — |
| data/archive-a3/goldpricesandwa00mitcgoog/2026-10-02/MANIFEST.md | 73b86c2dac28270d7b1028fc4ec5c4a54237c7a5908d53ca300d59afb8010831 | c54b5814d73e5cb69dbca6d7b75680942f6b07f74d33e2bb87fbc22e57e1cf80 | — |
| data/archive-a3/goldpriceswages0000unse/2026-10-02/MANIFEST.md | 86bf7c074117e2647a88bcfdb36d7b51b20343fb771ce73906aee24cf00723be | be3d5ad22739ac37f2bc5e74db0f57632a6243201379aa0a1709cf577f0fb212 | — |
| data/archive-a3/historyofgreenba00mitcuoft/2026-10-02/MANIFEST.md | 2fed3400ea30d99819a870e2e27a1621df28388b7e6388b1c732c206c80ecd18 | 96e4f62aed8c9cb13e518e860ac4ced0ca7a23388a618f3bec3c822c8ec00692 | — |
| data/archive-a3/historyofpriceso01tookuoft/2026-10-02/MANIFEST.md | 8473196287c2bb41520251c3f5839c06f3a2f179626a234e6b7703a30379f703 | 3f4e524054d602abe17a846d32434e7976510164439c9a1757b9a34b83be7fb8 | — |
| data/archive-a3/historyofpriceso03tookuoft/2026-10-02/MANIFEST.md | d19f9d5d5892a4b79358efebb07bad791ee97f217fbaef8285b0452eacdaa8f5 | b6dce727acb731dbda18de8c9e9afedb22b874bb72dc98c63e7d5f5cf393879e | — |
| data/archive-a3/historyofpriceso04took/2026-10-02/MANIFEST.md | b701c1292f89a4500ff7b3fa63f48e49835f435cd9f1ddb1b89c759378d01fa3 | 431d4dcab9cd6d7224f63747853f547fb4ea3717617f5df920b66672544c481c | — |
| data/archive-a3/historyofpriceso06tookuoft/2026-10-02/MANIFEST.md | 539d8ea3c0bc1f6c509e91fe398c903f22c63d54545b5c8946fbc33da6c0db05 | 3f80dff4b5f31c965de70ce697fa61b2f3d3d007a4a4b0c796824d9fcc83e0cc | — |
| data/archive-a3/india.history.resource.37818/2026-10-02/MANIFEST.md | 71c2c00dc50ee66d77d17f67812a93e12ae28a4d9246e3b9fbfc88c8923afbcd | 328f6a635ec9789aad9b639e1854c83e8447bbe8a6b51985fcce66d2a33d23b0 | — |
| data/archive-a3/jstor-1928689/2026-10-02/MANIFEST.md | e82c0de24f0614aa5884c2dfea2fe66c323335e61872e46c9fe82c7344b2ad74 | 9194c26f22f85ef00ebbef26de58484b01f5d3607048009b3718a1acca7f4e94 | — |
| data/archive-a3/reporttogetherwi00grea_0/2026-10-02/MANIFEST.md | 62e19d800366b4150939b236588c6af9066f24a9b296a8442a75caba7fb4041d | c3f8f2d9a298d18f2f46872541d83e4c4737b516687c596397fd3e409afb1845 | — |
| data/archive-a3/reporttogetherwi10grea/2026-10-02/MANIFEST.md | b785669921b80d65f846506f40ed79eaa4f73174953dc646d7173579eb2f00ee | a06266d21b0cbe97fca6dbd637e7914a25fee5b44f02bf5f115f5f54a9b0ad74 | — |
| data/frame-a/areaer-2011-2023/2026-10-01/MANIFEST.md | adc7f8fd1f0fefa8e8f8999019d6fcd30202bf4fae800c6d32fb6754f3767b8c | 299b2f2a8ba963ee85b27833905725caf7543454d8b3e7a8ac1eb469cf247b25 | — |
| data/reconstructed/ft001-a/MANIFEST.md | 4058a07a2dbcb6d258870c3af255023d8c7af2cfea0a9544d0da9f3db505c777 | 2d213cc6017e5906fa229720bc227c87cfb2e36faa62d667db577e85b7ad3586 | — |
| data/reconstructed/ft001-a3/MANIFEST.md | 7604c1ffead463b73c9d06da5ae6c3473f1b59037dc7e1899dd98cc0ca0301b5 | d4f96976f973a7cb9969256cb8b38fc42abb7a2dc21dabbbbf23dfc18c8b3452 | — |
| data/reconstructed/ft001-b/MANIFEST.md | 27b1121f99a00caf960097465392823d253d683d215e42af96138327eb1821c1 | 634af5c2b18d49707941642c7a3abfab7015c003a03200650594e879260e5431 | — |
| data/reconstructed/ft001-cs-tables/MANIFEST.md | 3ca271dc4b7427f4e562123f4ab42dbe2ddc64aa87cc949e46e455a743d07c5c | 218447d44580642ef723b476d0caffb28a0fe641737a45a8c8545bd35de80395 | — |
| protocols/FT-001-M0-rules.md | ec966025dd97fb932527e54789da21047c75cc46e0a53166e0411d81df6b90f5 | 9efb362d602c4d13bde59491f8bf2a5bdb587404d56662052e4c51e1c28d3b4d | — |
| protocols/FT-001-M0-rules.yaml | 49adc537818184b9b48c9091bc59f296b50a59813b5eb9da5b87bb6a64985c04 | f1d31bfebd060f7090409921a21d2831cf9bee994d0501e55d9fb3195249742c | — |
| protocols/FT-001-M3-panel.md | f993b1be87c8dfbc769b13939b8b458c7b711a40b89a75ca542f10e74972ceb4 | e26413f3fae1a4315288db1eaffdd7e246291af0d24df4dd360eda07b4dba713 | — |
| protocols/FT-001-M4-A3-premiums.md | 2cf75f63c19f919abc3386be2070865990cb01f286abc2bd11bf7f626a37009b | ae970f945f929f2366bfec5d74adf1baf750a3018aabba8416aac0bdbc6f19c4 | — |
| protocols/FT-001-M4-frame-a.md | 7149851f8aeb5a99ff7922f966a23f76c91d64b8960b48a74109955bc36edb6e | c8e1c186c4a3b2a4e4afee2c5ef9f013433a834d3a436379f6c58772976cae9e | — |
| protocols/a3.py | 0bbdf9d010f3b63b8d05f66828799c25e970d03d1952fc5289ff1d302975b6f0 | fb75a3d02e865199787c1a7b24745fbff33c8f9b0d85c409cd959493c7cdaaeb | — |
| protocols/breaks.py | de91930beb1faba1691e29bcf85f922ada7791fa71bba324e01b7f306b4e69ad | 55e20721734cd7fe69c1eb8df8fb1e63091d81f6682886f97f1958dfd9f29516 | — |
| protocols/economies.py | 7c644e78ba5a614d61cb1f2ba593c9c866760fe68e210cbbb5eca70e9117dca9 | c3d94b551db15c6e2ac6761cdcfdbf4e31d6272e3a765967afd8daa94322a3d7 | — |
| protocols/frame_a.py | 89404af2a326c7555ca7da25bac02aff8fb16d9f8be72dc2d24f7a5dcb482169 | 45086ec8758f9fcb43d84720c1cb9abbed91cec332e4605a3d30350237229933 | — |
| protocols/m0.py | 1f6c3c000e1e060fb527988acce95001720dbc4c0e600e7ee1c934750a911192 | e2e4cabca5f5a2e7887f25cc285647704f8a2ef420018e3302fe30fc7da74adb | — |
| protocols/panel.py | 22d705dbba48ea6f1df6b7913f3b9b80dadd76e43859fdcb76e910fbd8562d08 | 79df1fc4c61ee2fa39c223bb3c73e1b7d71e007fba124fc48bef5f69734bb443 | — |
| results/numbers.json | d04d92c99eda73c946d85c3b10040a9361172f3118fa14e6e4202a4dee9bc585 | a518dcf37348e72adb0d578981e62f7f592c4742210d12622af7a110a846f9d7 | — |
