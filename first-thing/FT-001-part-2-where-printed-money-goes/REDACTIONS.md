# Redactions

## Second pass: internal wording removed (2026-10-12)

The first publication of this folder carried the project's internal vocabulary: the name of the person who decided, internal rule labels, paths in a private working tree, the names and versions of the models used, the name of the fetch-policy tool, and the process remarks that go with them. This pass replaces or removes that wording in every text file of the folder (63 files changed, plus the README). Labels such as W12 that remain in a code file or a manifest are the local numbering of rules defined in that same file; they are not references to anything outside this folder. No rule, number, source, date, code path or result was changed; the code still imports the same modules. Some scripts name internal notes that are not published, so they cannot be rerun from this folder, as the README says.

The hash that `results/runs/*.json` records for a card (`card_hash`) is that of the card as it was locked, before any result. Each card and protocol whose wording changed is listed here, with its sha256 as first published and as it stands now; the locked hash of a card is the first one, except for `protocols/FT-001-M4-frame-a.md`, listed above.

| File | sha256 as first published | sha256 now |
|---|---|---|
| cards/C01-door.yaml | 1d4eb51811637662a436e3197673541d59bbac7defa59162a6b060c12af4db58 | 1aa00d2f9f93bab9c66c0f8e974cd47cc3306f826a4d19efa9cc8195b9758eb0 |
| cards/C04-a4-1870.yaml | e19d5977f0fd6ecde69b63cea38f3180cddec4a94d0e4fd8f5f3da6c675ddb71 | c6fd42acd1c1c69efd515dbaf50c07995cda8609b22d3e843eb79936f8787b94 |
| cards/C05-e-episodes.yaml | 7e743af3e5a1282494d3db00a216c31447ecf2d06a2e2c0b300cf9e7cf050743 | 2d8c0fd81f7d205bcd3100d613b46d850389ea4317f76a925c46c1d0a1cd816f |
| cards/C09-e-episodes-excess.yaml | 28504e1ae3871322ac81338f661957b8e82d2b971009bcc78938c96d6b1e866e | 97c82a556f41717f1d76cd19fcd5f3b32b07398fe3ad05190d8b86fb93f13940 |
| cards/C11-e-episodes-checked.yaml | 5ed77d07d61bd28b4e95f072f653a7330f6ff348e9e9fe43f65142859a53d856 | 092b75494037a1cd0ef81c96bdaf46bc8f827c7c4c13be19c4c6ea5347a45bf6 |
| cards/C12-a5-deciders-checked.yaml | ac337b03d7de27687a18b3064c1f368443e41b23543c52af7837fc7af4b3b5a0 | 5059311a42152751d0620ddb210ac3bee6bf3c9490d7a78fd95a437092ceda6c |
| cards/C13-a6-checked.yaml | 77cd14e25f640ca1fdaba97b355454a80a7f25b032979096e0cb3c73119991bc | 5e11f22f538c712729332d5d6acfbde58e14af2d10c15f4c9704aff0553f8d9a |
| cards/C14-velocity-net.yaml | 286014706725f1f18ecda00d98c45f0167d2a7895ca7bb0cbee2a501a2db1434 | 852cf7268ae3da787cae494cce23ab3635be594d104c46e2c6c1122258aae561 |
| cards/C15-e-episodes-closed.yaml | 20b8923cddc8e1962e13db36a2795d50d18bda9c2336d8b032520aa8df30d309 | 38e97affdd2e1246a2aa749a353c1e73aaff77b7bbfb68958cc9537deaa1b2ab |
| cards/C16-a5-deciders-closed.yaml | a8075fe2b04bae69f1f9cd440565ad003f5a7bba840b9b8e37cbeb43a9055ffe | 07c3bcaa3c3b023da86615bede7923ba871a72fa8a07ac49a81d1907c169d056 |
| cards/C17-velocity-worded.yaml | 39d3caaab8de60fed2ea715bd4477ec579ef08694b42dce09bf3243961763ecd | 10641e30a452b507064ce47d79aef7d38d32e1db0151d71b607b16194b6e6cd3 |
| cards/C18-a5-deciders-bare.yaml | feeb9d67df7c0a75177874e19c6252a4fb963989ee0a2c945a71f7d0f191ded1 | 38f23ce06ebce1f09b400d4b5ea6f57b255f0928fea259587ee975022d0c9b85 |
| cards/C19-velocity-bare.yaml | 950bd03458e289fd793bea232ecca7c0539d3a09a3536a8224ecaf9475974cd5 | ca89d63e05d5685d588a1b6106cb2c1ba7dbe94f4f7b6622b46eda24042e53fd |
| cards/C20-a4-base-2019.yaml | 9c3f3708e36f70469de9c841dc0c48178f8bc68c5ca325989bfa6fbed245e986 | 807c90f463caa5d4e57849528c3fedb2d410c0970965e23de925351fadae616e |
| cards/C21-a4-1870-named.yaml | 9507836bd4f556c311be02da26ac0558dd45c9833130eedb43ff93fd50191710 | 7a737ae28b9cd2bb9b90884b9b02cf52dc78beb7c72b4ef714a49430e336a87a |
| cards/C22-a4-base-2019-narrowed.yaml | 365e49d4fe23cf19e74fd3b31e4d876f18f2edd1dc997a637df78268b392994c | c59926872d3ec2044f83e0661a0808738a050c8b0f96569ff3b9a47d381c65a8 |
| cards/C25-a4-base-hko-fill.yaml | 59227b8c008e7e04003931d56ab3700d8d7d18c4df814e58725cb02fa2bd02a6 | 52ef34e94a499684fa7e4e6cdafab9528c880e1e2f200b8ed1844c722db463aa |
| cards/C26-a5-deciders-hko-fill.yaml | 1c106d27b3ebca6daa11f196edbc3be47a82a139133736c213853d8a46274eb2 | af7fd49db89c88b29e4eed283a7910161779bf596408e93fd06cc4616162bcb1 |
| cards/C27-a4-broad-hko-fill.yaml | ffc824fb4a5dd978850b8e1adcf022fa0c9469f59c01af64d5bce2cb7006ce61 | 8612509dc96cd258cea225bcedfbd2d1ef5d6256fd0df6d4619906b2fe19a284 |
| cards/C28-a4-units-guard.yaml | 7a5e7dcb03ec6186e7e4384d138cf0666de898ada87d7f36e059c926255c6b21 | bfb6a802549cc0514cbec2a4feac5fff08a5aaeecb8ea98750ea17b9a0f2a3c1 |
| cards/C29-a4-exploration-pace.yaml | f1dcd282e7bae1b39447c35e960864241a05412a6ce682eee9248db10d0357fb | 272c3d0780eee6dff3864dda902bf37710791cc7740c94aacbc9bd1b39f04b4a |
| cards/C30-cs-b-base-against-broad.yaml | 1ff115a022bfd3b5210302bc4eeacc8c76f6d365c52af21e7d9ee8b5d0ec42f8 | 27c1b58eb18ef376fe7a99414a51ddd4c39ee781d9438abd30db35fc94d3b7c8 |
| cards/C31-cs-e-pandemic-cross-section.yaml | 37204ae43a8de787e0609fe90e6e9cf1f3c1ef2dd19605296d167986cc380852 | a9a801132b806526e7e6b5fab892359b369e6c90e7da06b89335d1657c52391a |
| cards/C32-cs-c-door-timeline.yaml | 328039de2eed5d4124f8d5dba60453700d04cbabe998c6fff2e81db6e9547125 | 41f90bd92fe0213e4cc27626d8b2c08ef3d0e0fbcc3113cf89ae4f2c1a150bc9 |
| cards/C33-cs-f-reclassification.yaml | b2c7c2b00c0d82845e88fdcef9c60b8f1ef443af217652ed220e6aee3025d808 | 3824c91d4894bde0a00c8822887cdd99030d8ebc5b2140ceeec1a30f189ff66a |
| cards/C34-cs-c-vu-bls.yaml | 046d69c59d39429b73a8915d17912364ed1c7537a9e59f3ea25d940075aea904 | ad7700c263eb563e5d46791ab48405b8218198c635783cd8a661500c80490cc6 |
