# 三菱電機 GX Works3 サンプル集

## ⭐ 重要: 公式完全サンプルXML

`_official_complete_sample.xml`

三菱電機株式会社が提供するGX Works3用 IEC 61131-10 XMLの**完全リファレンスサンプル**。
以下の全要素が網羅されている：

- 6種類の Resource（initial / scan / standby / fixedScan / event / noExecution）
- POU (Program), FB (FunctionBlock), 関数 (Function) の完全構造
- 構造体定義（Struct1, Struct2）とメンバ別コメント（Bit/Array単位）
- すべての三菱独自データ型（TIMER/COUNTER/POINTER系）
- 全 AddData 拡張要素
  - PouProperties, FbPouProperties, FunPouProperties
  - DataTypeProperties, GlobalVarsProperties
  - VariableComments, VariableLineNumber, VariableRemark
  - VariableSystemLabel, VariableExternalDeviceAccess
  - VariableStructDeviceAssignment
  - BodyProperties (ワークシート機能)
  - ResourceExecutionType, ResourceFolders, PouResourceFolder
  - FbPouFile, FunPouFile, ProgramFileProperties
- グローバル変数（通常/RETAIN/アドレス指定あり）
- ワークシート（複数Body）の構造例
- フォルダ階層構造

**三菱向けXML生成時は、未知の要素や属性を見つけたらまずこのファイルで検索すること**：

```bash
grep -A 10 'VariableSystemLabel' _official_complete_sample.xml
grep -B 2 -A 5 'ResourceExecutionType' _official_complete_sample.xml
```

詳細解説は `references/mitsubishi.md` を参照。

---

## Jiecc公式の機能別テキストサンプル（44ファイル）

| 機能カテゴリ | ファイル |
|---|---|
| 言語の基礎 | `program.txt`, `func.txt`, `fb.txt`, `st.txt`, `elementary_types.txt` |
| 変数 | `array_var.txt`, `string_var.txt`, `global_var.txt`, `struct.txt`, `var_attrs.txt` |
| プリプロセッサ | `pp.fmacro1.txt`, `pp.fmacro2.txt`, `pp.ifmacro.txt`, `pp.omacro.txt`, `pp.vaargs.txt` |
| 上位構造 | `configuration.txt`, `task.txt`, `header_info.txt` |
| ファイル管理 | `include.txt`, `import.txt` |
| ドキュメント | `doc.txt`, `en_eno.txt` |

各ファイルは jiecc 公式の動作確認用サンプル。
`<feature>.txt` (IEC 61131-3 テキスト) と `<feature>.xml` (Jieccが生成した XML) が対。

```bash
# サンプルから三菱用XMLを生成して動作確認
jiecc.exe --retro_caps fb.txt -t mitsubishi -o fb.xml
diff fb.xml fb.xml.expected   # 期待と一致するか
```

---

## 移植・コンバート時の活用法

メーカー間で同じ機能のサンプルを比較できる：

```bash
# 三菱の関数とCODESYSの関数を比較
diff ../mitsubishi/func.txt ../codesys/func.txt

# 三菱のFBとオムロンのFBを比較
diff ../mitsubishi/fb.txt ../omron/fb.txt
```

---

## 注意事項

三菱には以下のサンプルは含まれない：

- **`ld.txt`, `fbd.txt`, `sfc.txt`, `il.txt`** — GX Works3 が IEC 61131-10 経由での
  これら言語のインポートに対応していないため
- **`enum.txt`, `interface.txt`, `class.txt`, `oofb.txt`, `ref_to.txt`,
  `namespace.txt`, `subrange_*.txt`** — GX Works3 Ver.1 が
  これらの機能に未対応のため

これらが必要な場合：
- enum → INT定数で代替
- ラダー → STで等価実装、または GX Works3 で直接編集
- OOP → 通常FBで代替
