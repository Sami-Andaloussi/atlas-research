# Redactions

Each place below was a private path (a path on the author's machine, or a link to a private repository) and is replaced by `(private path)` in the public copy. The workshop file is kept as it was: for a card, the one that was locked. The first hash is the workshop file's, the second the public copy's. Apart from the redaction nothing in a file is changed, except `README.md`, which also has its links rewritten to the public layout and the workshop's generated mark removed, and a file whose keys `WITHHELD.md` lists as removed.

| File | Workshop sha256 | Public sha256 | Places redacted |
|---|---|---|---|
| protocols/FT-001-M4-frame-a.md | 7149851f8aeb5a99ff7922f966a23f76c91d64b8960b48a74109955bc36edb6e | 4a8683d684fafc10ddcafdbf1c13b87304c9463566534e816376a34a3f73dafa | 1 |
| results/runs/C17-cs-e-second-model.json | 9bd2937240ef9740c9bd44eb9354e14822f16071502d7f41e2c3c464e36d27dd | a1fbeab39938238ad3cc56046a860bf52f6495a1957303fba29aa05d1c3df85b | 3 |

## Second pass: internal wording removed (2026-10-12)

The first publication of this folder carried the project's internal vocabulary: the name of the person who decided, internal rule labels, paths in a private working tree, the names and versions of the models used, the name of the fetch-policy tool, and the process remarks that go with them. This pass replaces or removes that wording in every text file of the folder (104 files changed, plus the README). Labels such as W12 that remain in a code file or a manifest are the local numbering of rules defined in that same file; they are not references to anything outside this folder. No rule, number, source, date, code path or result was changed; the code still imports the same modules. Some scripts name internal notes that are not published, so they cannot be rerun from this folder, as the README says.

The hash that `results/runs/*.json` records for a card (`card_hash`) is that of the card as it was locked, before any result. Each card and protocol whose wording changed is listed here, with its sha256 as first published and as it stands now; the locked hash of a card is the first one, except for `protocols/FT-001-M4-frame-a.md`, listed above.

| File | sha256 as first published | sha256 now |
|---|---|---|
| cards/C04-claim1-dated-lines.yaml | 17de551edbd00e1a578a6a342abd4bac936b8845491e9463a8aa342fe7fd524d | b7873f935d0ecac74d02056fe458d864e64e4908475ab38b68001a82229a66bc |
| cards/C05-claim2-supports.yaml | b656278fb1b795f5509d27a55571b58644ff854791dbde259487f7ca2155453b | 008aa9f9dc47ac534d2adda279059a974f101b62641226bc281eeaf7ef07e4c0 |
| cards/C06-now-coded.yaml | c0a5e40350e0667f6d7cc028c72c98e18fdd0f2e3cb1cbff2d3fc7c9b045d949 | 60a1b35db1a143876fde224fe3c99f117dc5a55541de5b66d51c0ee6d6a496f8 |
| cards/C07-claim1-dated-lines-v2.yaml | 65a62ac42998c216c1239961575e7cd1c2ef825ec1208772dbd2ed34f1fbe7ec | d66c8d1dce9372b8aff438195614de47b5d72901dc22026f63edf03291fcfda5 |
| cards/C08-now-coded-g25.yaml | 6141af33a32a51a1c626bf0fd2f2e70e35e201f2eb648612be4aedd60e0bb7d7 | 63e06cb6d15cdabb02d21a30682d02bf9d649bf79ee2844abf82e8ce982c6008 |
| cards/C09-now-coded-g25-checked.yaml | 8d62dcb5d5af29fe6367e5cd9859ae365b41c90c8e88ee73739c50b875a41acb | 47eccc0a918085437b13c53b0dbd81c9df49cfd0d33b8385a698c8b10000e5ea |
| cards/C10-now-who-rule.yaml | 25e26610878702e6dd0c3e6d81789c9e33eda3f9ba76297977407b08adc7fefd | 138c6b868675825765a890ce358fb42d7a7713757ab5dcdd599867fe3f481440 |
| cards/C11-claim2-cfa-out.yaml | 62e6c72eaaafc72f52092eed3b45bfbe03fbe5c3e38f6db1b78290b20f1e1c2b | 384ebbc68dca177480bc6ac151e514188fd3dd3d6450751b145e852ee95469b8 |
| cards/C12-now-coded-g25b.yaml | 049ffa5255d6fc490f79ef626fc2b8defcd5c1353a95416f21d73f48213ba7cf | 4adbcc6d833a747a337f921a5576789a20cf0810c709831ac4129139935d09cf |
| cards/C13-claim2-institution-m0.yaml | 3b9acf07bc1fbeb5396adbe2f7a736aa12facfb94911ab2ad357fd29a15f7329 | 7f365cedc10614896a39be2db8c4c4ac0f9ef48e298faaa36d3491a1f3683e82 |
| cards/C14-now-institution-m0.yaml | 3c07b559579d60a92971bdbecf5c7818fc9df2fc53716ef378c0547b531238c1 | ab3005072a4c96074de14fa679ff92c21cdd25671771c89509ed99659a8b9a81 |
| cards/C15-claim1-institution-m0.yaml | a6aadcab79011eaca7a21a8a2f63641d126975a0e0d5559f4b85116fc3dff9d7 | 1fd45e6a7efd8aa964552a63419841347b3a4a05156baf83f67616660d074a1b |
| cards/C16-cs-d-default-ratio.yaml | 3b1add04d0006ea98a19518d795c2123417ca99f24bc88726bb6a7d045690152 | 82087b61b39da7834f8b365319a0e402385414adb0c7f4a3e9793b64789399b2 |
| cards/C17-cs-e-second-model.yaml | ffc48eaf0e2f1ff51cc55950e6e66d43c087f29473993ac3b1e6be8f17e4f73c | 3a89c0525252c3059c01fe90ea0fcb46fce8a8e3234f5159f652acec64dea7cf |
| cards/C18-cs-a-consumer-prices-off-gold.yaml | 09385dfdd821414b6d8ae1a234b02737ea59154e5193684b7bea8c3317a58424 | b24fde3a457d9c825155048f695440a87b1e8092b013d621577fc92e9f5a5eb8 |
| cards/C19-cs-b-inflation-by-convertibility.yaml | db75f966d7aa275723a4a9d8c039e51d04a9a88d7001299896e64ca0d15a131d | 0d26a8721b62ebcfa5c533425d57fe1b65a1fffc933df1045c52f9efd6199bc3 |
| cards/C20-cs-b-without-hyperinflation-years.yaml | 1ce4a63e9962a5195219aa03fc9c169f4133f86b28fbc26d84c21bb1507bc12d | 35b93bf14b01e5dcb9fd2d05c19187107336deb23b7bfa1805f98352433abcc1 |
| protocols/FT-001-M0-rules.md | ec966025dd97fb932527e54789da21047c75cc46e0a53166e0411d81df6b90f5 | 9efb362d602c4d13bde59491f8bf2a5bdb587404d56662052e4c51e1c28d3b4d |
| protocols/FT-001-M0-rules.yaml | 49adc537818184b9b48c9091bc59f296b50a59813b5eb9da5b87bb6a64985c04 | f1d31bfebd060f7090409921a21d2831cf9bee994d0501e55d9fb3195249742c |
| protocols/FT-001-M3-acts.md | b274f51192e1f6beffbf00fbfa89843838526c25a4ae6285fe60b7eeb4c65202 | 3f18ca8266905beab8de43e085a1a083a6ab8e9cf9da4e46e50567bb3f2c3b8c |
| protocols/FT-001-M3-boards.md | 29ad68b1f57feb0a60187f74149a55677ca64958ecb654bde7ca145ef9bf4803 | 46096b89d6c2195329a6bce1de1a4209589225fcc73f8fff0c1826c5d953e9e5 |
| protocols/FT-001-M3-frame-k.md | 06b3437b32dbe9d76b4215fc1503913599b0600a8302ad0857674c3a0479ee1c | a522203bc1e7a028ad96ab92b96733e966d524184f64393b034882e70d217b87 |
| protocols/FT-001-M3-panel.md | f993b1be87c8dfbc769b13939b8b458c7b711a40b89a75ca542f10e74972ceb4 | e26413f3fae1a4315288db1eaffdd7e246291af0d24df4dd360eda07b4dba713 |
| protocols/FT-001-M4-A3-premiums.md | 2cf75f63c19f919abc3386be2070865990cb01f286abc2bd11bf7f626a37009b | ae970f945f929f2366bfec5d74adf1baf750a3018aabba8416aac0bdbc6f19c4 |
| protocols/FT-001-M4-frame-a.md | 4a8683d684fafc10ddcafdbf1c13b87304c9463566534e816376a34a3f73dafa | c8e1c186c4a3b2a4e4afee2c5ef9f013433a834d3a436379f6c58772976cae9e |
| protocols/FT-001-M7-frame-g.md | 81de6358f94e5cb59cc4dd28fcf4204dc72ca8539d277ab79d5b8f4c83f4d5bf | 578283b3bc4d6c2298023233a6ac399caa2dfe90e5e4e1c64f91497d8f5164c6 |
| protocols/a3.py | 0bbdf9d010f3b63b8d05f66828799c25e970d03d1952fc5289ff1d302975b6f0 | fb75a3d02e865199787c1a7b24745fbff33c8f9b0d85c409cd959493c7cdaaeb |
| protocols/acts.py | 983fc3894da4a6d8ce6d1ed44e81825672dfb1fb948efb31019a1ab146a2364c | e3b5637f099c0db9f05465e93807db8a34320d5d2fa1ec46875bbb5f6a8ab738 |
| protocols/breaks.py | de91930beb1faba1691e29bcf85f922ada7791fa71bba324e01b7f306b4e69ad | 55e20721734cd7fe69c1eb8df8fb1e63091d81f6682886f97f1958dfd9f29516 |
| protocols/economies.py | 7c644e78ba5a614d61cb1f2ba593c9c866760fe68e210cbbb5eca70e9117dca9 | c3d94b551db15c6e2ac6761cdcfdbf4e31d6272e3a765967afd8daa94322a3d7 |
| protocols/frame_a.py | 89404af2a326c7555ca7da25bac02aff8fb16d9f8be72dc2d24f7a5dcb482169 | 45086ec8758f9fcb43d84720c1cb9abbed91cec332e4605a3d30350237229933 |
| protocols/frame_g.py | 768244151c6ab2103f84e870f50a39014eab9ee2d50b29913b9327455585ecab | a3204ea5e225a88cf31579bca48123d484663c64f7a323a1e343e281c41004d5 |
| protocols/frame_g_list.py | fe76cdc3a67df9f0fbdf2f8071006a4b6b69045529a08fd18868fea7958e662b | 3c3ac64b302b397bdb0d2f8e68b0a042f36b725ebd2875d110ddbffe6e286ad2 |
| protocols/frame_g_mapping.py | bc7c2b8f8bd5f871bd06d96a49f403bcb2a98ba92aee672aaa213b38413e0318 | e97ce492e065b3d8601b51aa992b867f3682e5763942b89752fb236780ccf9df |
| protocols/frame_g_packet.py | 8d62fc96df04a6cb4f8fce57d2a21a5af6e4348204bf8f36703588de6c8b1657 | 06409b01ef2fa88b9887e86f19503545a1c0122b4af37d903073b532a4d38983 |
| protocols/frame_k.py | 7a6fbc0b6310313b7cdfb745d540a334331d01754d43f8a59ce2b21b28fcdf48 | 9dd9813560196b25c863e3f2ffbfbb6b2efcbbce044861889465749d270014ad |
| protocols/m0.py | 1f6c3c000e1e060fb527988acce95001720dbc4c0e600e7ee1c934750a911192 | e2e4cabca5f5a2e7887f25cc285647704f8a2ef420018e3302fe30fc7da74adb |
| protocols/panel.py | 996ffda3f050b98d23eef4b0c8c5e18d3f6f0c871a4c4501920578e15e4c5623 | 2d2b8279a74cda476f17961a166f907ae34ec3b58fd1f92a7d3acda7a0a8e1e9 |
| protocols/war.py | 8bc154c31eaca340781b5d713644df2d41e9ff2e127351732c6950b823efebd2 | 5bfd3fb1a47160796226f0d5dfa986e801cc20ddd5f34eca76f861d5c46c5908 |
| protocols/window_a.py | f9b10a52f552d2a947f78c9e701b3d12247c5e71e218e28288debb41a9712ec0 | 8475269c137edbea7a23e123b8e7040850249286b32b9568f13483b79515f4c5 |
