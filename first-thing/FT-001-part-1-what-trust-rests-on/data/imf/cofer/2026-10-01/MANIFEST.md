# imf/cofer — vintage 2026-10-01

- **Source**: IMF Currency Composition of Official Foreign Exchange Reserves (COFER), dataflow IMF.STA:COFER 7.0.1, structure DSD_COFER 7.0.0, allocated reserves (AFXRA), shares and nominal USD, quarterly and annual, all reporting groups, as served by the IMF's SDMX 2.1 API (api.imf.org) after the Guard ruled allow (probe, not recorded, 2026-10-01)
- **Retrieved at**: 2026-10-01T12:44:42+00:00
- **Licence**: IMF data: free to use with attribution (the portal's terms were not read here); cited, never republished
- **Notes**: data.imf.org (the host the rules name) answered 403 to the toolkit's client on its dataset page and was not worked around; the same portal's API host api.imf.org, which the Guard allows, served these files. No key used.

| File | URL | Bytes | sha256 |
|---|---|---|---|
| `cofer-dataflow.xml` | https://api.imf.org/external/sdmx/2.1/dataflow/IMF.STA/COFER | 31676 | `566d96ae79f8b10e69c824b806bc0168f14265d4c32ddc700a3e71ee31392c10` |
| `cofer-dsd.xml` | https://api.imf.org/external/sdmx/2.1/datastructure/IMF.STA/DSD_COFER/7.0.0?references=children | 108457 | `39cca93d66d222a5367e86c7ba267a1db5a856d81ad74a6fbae682464e07fca1` |
| `CL_COFER_CURRENCY.xml` | https://api.imf.org/external/sdmx/2.1/codelist/IMF.STA/CL_COFER_CURRENCY/2.0.0 | 109645 | `852e09780fa8c39ee8b340da4c8bda1a0957e85d314b275a633d197424b63110` |
| `CL_COFER_FXR_CURRENCY.xml` | https://api.imf.org/external/sdmx/2.1/codelist/IMF.STA/CL_COFER_FXR_CURRENCY/1.0.0 | 5697 | `8d6a73fba195051f502315f63a3c7fa44f50046969f841e8fa373aeb3a839929` |
| `CL_COFER_INDICATOR.xml` | https://api.imf.org/external/sdmx/2.1/codelist/IMF.STA/CL_COFER_INDICATOR/1.1.0 | 28728 | `6b04ff0974c52a55697c681d373215fee0711cabbe5e8cc4716bb9081257babd` |
| `CL_COFER_TYPE_OF_TRANSFORMATION.xml` | https://api.imf.org/external/sdmx/2.1/codelist/IMF.STA/CL_COFER_TYPE_OF_TRANSFORMATION/2.0.0 | 2215 | `f2b3820c792048466e4fdc687b5e4bd0107e40926d3446603d42a62649bfa376` |
| `cofer-allocated-quarterly.xml` | https://api.imf.org/external/sdmx/2.1/data/IMF.STA,COFER/*.AFXRA.*.*.Q | 174859 | `c0f5d24800f8d6d54115ed785cd91d9fe037468b1ab27615da1ee6463ef5690c` |
| `cofer-allocated-annual.xml` | https://api.imf.org/external/sdmx/2.1/data/IMF.STA,COFER/*.AFXRA.*.*.A | 83515 | `2a3ff265fcfd1999731c4031cd908540ae1e29fb4ff612b0dec6c08add37ea4c` |

The files are not in git (fetched data); this manifest is. Re-fetch and compare with
`ft data refetch imf/cofer 2026-10-01`.
