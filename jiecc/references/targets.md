# メーカー別ターゲット仕様

`-t` オプションは各PLCメーカーの**独自方言・属性・記法**にXML出力を合わせる
ためのフラグ。**言語×メーカーの対応可否**は別の話で、メーカーのエンジニアリング
ツールが該当言語のXMLインポートをサポートしているかに依存する。

このドキュメントは：
- 各ターゲットの方言と注意点
- メーカー間で書き方が違う具体パターン
- どのメーカーがどのバージョン以降でIEC 61131-10対応か

をまとめたもの。**三菱の詳細は `mitsubishi.md` も参照**。

---

## 言語×メーカー対応表

各メーカーが IEC 61131-10 XML経由で実装可能な言語：

| 言語 | standard | omron | keyence | mitsubishi | codesys |
|---|:-:|:-:|:-:|:-:|:-:|
| ST | ✓ | ✓ | ✓ | ✓ | ✓ |
| FB / 関数 | ✓ | ✓ | ✓ | ✓ | ✓ |
| LD（ラダー） | ✓ | ✓ | ✓ | ✗ | ✗ |
| FBD | ✓ | ✗ | ✗ | ✗ | ✗ |
| SFC | ✓ | ✗ | ✗ | ✗ | ✓ |
| IL | ✓ | ✗ | ✗ | ✗ | ✗ |

**ST と FB / 関数は全メーカーで実装可能**（最も移植性が高い）。

ラダー処理を依頼された場合：

| メーカー | 対応 |
|---|---|
| omron / keyence | jieccで `{ld}~{end}` プラグマで IEC 61131-10ネイティブXML埋め込み可能 |
| **mitsubishi / codesys** | jiecc経由ではXML化不可。STで等価実装するか、メーカーツールで直接編集 |

---

## メーカー別エンジニアリングツールのIEC 61131-10対応バージョン

| メーカー | ツール | 対応バージョン |
|---|---|---|
| 三菱電機 | MELSOFT GX Works3 | **Ver.1.110Q 以降** |
| オムロン | Sysmac Studio | Ver.1.30 以降 |
| キーエンス | KV STUDIO | Version 12 以降 |
| CODESYS | CODESYS | V3.5.21.0 (March 2025) 以降 |
| Phoenix Contact | PLCnext Engineer | 2024.0 LTS 以降 |

これらのバージョンに満たないと、jieccで生成したXMLを取り込めない。

---

## 組み込みマクロ

`-t` 指定時に自動で定義されるマクロ。プリプロセッサで条件分岐に使える。

| ターゲット | マクロ |
|---|---|
| `-t standard`（デフォルト） | `_STD` |
| `-t omron` | `_OMRON` |
| `-t keyence` | `_KEYENCE` |
| `-t mitsubishi` | `_MITSUBISHI` |
| `-t codesys` | `_CODESYS` |

例：

```iec
{#if _MITSUBISHI}
    var sensor at %X0.0: bool; end_var
{#elif _OMRON}
    var sensor at %W0.0: bool; end_var
{#elif _KEYENCE}
    var sensor at %R0  : bool; end_var
{#else}
    var sensor at %IX0.0: bool; end_var
{#endif}
```

---

## 三菱電機 GX Works3 (`-t mitsubishi`)

メインターゲット。Jiecc 5.4 以降で対応。

**詳細は `mitsubishi.md` 参照**。要点：

### サポート言語

ST / FB / 関数のみ（LD/FBD/SFC/IL は未対応）。

### 必須オプション

```bash
# 三菱は --retro_caps を必ず付ける（キーワードを大文字化）
jiecc.exe --retro_caps input.txt -t mitsubishi -o output.xml
```

### 主な方言

- 直接アドレス指定は `%X0.0` 形式（`%IX/QX/MX` プレフィックス不可）
- `var constant retain` は使用可
- `r_edge` / `f_edge` は非対応 → `R_TRIG` / `F_TRIG` FB で代替
- `enum` 型はサポート限定的（int 等で代用が無難）
- `interface` / `class` / `oofb`（OOP系）は非対応
- `namespace` は非対応
- `continue` 文 は for ループ内で非対応
- `+intv`（単項プラス）は非対応
- ビット要素 `wordv.%X2` は非対応（`wordv.3` 形式のみ可）
- `at` 指定はローカル `var` では不可（`var_global` のみ）

### 三菱独自データ型

`TIMER` / `LTIMER` / `RETENTIVETIMER` / `LRETENTIVETIMER` / `COUNTER` /
`LCOUNTER` / `POINTER`

### サンプル一覧

`samples/mitsubishi/`:
- 通常サンプル44ファイル（`array_var, configuration, doc, ...`）
- **`_official_complete_sample.xml`** ← 三菱電機公式の完全XMLサンプル

---

## オムロン Sysmac Studio (`-t omron`)

### サポート言語

ST / FB / 関数 / LD（ラダーは `{ld}~{end}` プラグマでXML埋め込み）

### オムロン方言の主な特徴

- 直接アドレス指定は `%W0.0` 等オムロン独自表記が使える
- `enum` 型はサポート
- `namespace` はサポート
- `subrange_var`、`var_external`、`r_edge`/`f_edge` はサポート
- `interface` / `class` / `oofb` / `ref_to` は非対応
- ビット要素 `wordv.%X2` / `wordv.3` は両方非対応
- `?=`（型キャスト演算子）は非対応
- `continue` 文は for ループ内で非対応
- `var public` 等のアクセス指定子は一部非対応
- `return-doc` プラグマで戻り値変数のコメントを設定できる（オムロン独自）

---

## キーエンス KV STUDIO (`-t keyence`)

Jiecc 5.2 以降で対応。

### サポート言語

ST / FB / 関数 / LD（ラダーは `{ld}~{end}` プラグマでXML埋め込み）

### キーエンス方言の主な特徴

- 直接アドレス指定は `%R0` 等キーエンス独自表記
- **`var constant retain`（同時指定）は不可** — `var constant` と `var retain` を分けて宣言する必要あり
- `+intv`（単項プラス）は使用可
- `r_edge` / `f_edge` は非対応
- `enum` 型は非対応
- `interface` / `class` / `oofb` / `ref_to` は非対応
- `namespace` は非対応
- `var_external` は非対応
- `at` 指定はローカル `var` では不可
- ビット要素 `wordv.%X2` は非対応（`wordv.3` 形式は可）
- `append-eilogue-pou-body` プラグマ: KV STUDIOはPOUのXML生成時にEND/ENDH命令を自動挿入する。`{append-eilogue-pou-body: false}` で抑制可能

### 注意（constant retain の分割）

```iec
{#if _KEYENCE}
    // constant と retain を同時指定不可
    var constant
        PI: lreal := 3.141592;
    end_var
    var retain
        PI2: lreal := 9.869604;
    end_var
{#else}
    var constant retain
        PI: lreal := 3.141592;
    end_var
{#endif}
```

---

## CODESYS (`-t codesys`)

Jiecc 5.8 以降で対応。CODESYS V3.5.21.0 (March 2025) 以降のXML形式に対応。

### サポート言語

ST / FB / 関数 / SFC

### CODESYS方言の主な特徴

CODESYSはオブジェクト指向機能を含めて広範囲をサポート：
- `enum`、`subrange`、`namespace`、`named_value`、`variable_length_array` すべて対応
- `interface` / `class` / `ref_to` / `oofb` すべて対応

ただし以下の方言・制限がある：

- `**`（べき乗演算子）は非対応 → `EXPT()` 関数で代替
- `&`（論理ビットAND演算子）は非対応 → `AND` を使用
- `var constant retain`（同時指定）は非対応
- `r_edge` / `f_edge` は非対応
- `task` 定義の一部（`single` トリガ等）は非対応
- ビット要素 `wordv.%X2` は非対応（`wordv.3` 形式は可）
- `?=` 演算子は非対応
- `ref` / `^`（参照演算子）は一部のみ。`rv := ref cv;` は不可、`cv := rv;` は可
- FB呼び出しの出力引数は `=>` 必須（`func(intv, 1, num)` ではなく `func(intv, 1, o=>num)`）
- enum 値アクセスは `e_t.e0` 形式（他は `e_t#e0`）

```iec
{#if _CODESYS}
    boolv := func(intv, 1, o=>num);     // 出力引数に => が必要
    ev := e_t.e0;                        // ドット記法
{#else}
    boolv := func(intv, 1, num);
    ev := e_t#e0;                        // # 記法
{#endif}
```

---

## 標準 (`-t standard`、デフォルト)

IEC 61131-10 規格に厳密準拠。すべての機能・全言語をサポートする「リファレンス」
ターゲット。

メーカー特定の方言調整が不要な場合や、**メーカー固有ターゲットが対応していない
言語要素のサンプルを参照したいとき**に有用。

すべての言語要素・全言語（ST/LD/FBD/SFC/IL）の動作確認用サンプルが
`samples/standard/` に揃っている：80ファイル。

---

## メーカー間移植の指針

メーカーAのコードをメーカーBへ移植したい場合：

1. **両ターゲットの `samples/<feature>.txt` を見比べる**。
   方言の違いが具体的に分かる。
2. **共通化したい部分はプリプロセッサで条件分岐**。
   `_OMRON` や `_MITSUBISHI` 等の組み込みマクロを使う。
3. **片方で非対応の機能は代替手段を用意**。
   - enum → int 定数
   - interface/class → 通常FB
   - r_edge → エッジ検出FB（`R_TRIG`）
   - LD → ST
4. **逆変換 (`-d`) で両ターゲットのXMLを生成 → テキスト化して差分**を見れば、
   実際のコード生成結果の違いが確認できる。

オブジェクト指向機能（class、interface、ref_to）を使うコードは三菱・オムロン・
キーエンスへは移植困難。最初から `_CODESYS` 限定で書くか、あるいは通常FB主体で
書く判断が必要。

ラダーから別メーカーへの移植は、いったんSTに翻訳するのが現実的。

---

## サンプル提供状況の表（参考）

各機能の動作するサンプルが提供されているターゲットを `✓` で示す。
`✗` は単に方言サンプルが用意されていないか、そのメーカーが該当機能を
サポートしていないかのいずれか。

| 機能 | STD | OMRON | KEYENCE | MITSUBISHI | CODESYS |
|---|:-:|:-:|:-:|:-:|:-:|
| alias                  | ✓ |   |   |   |   |
| array_type             | ✓ |   |   |   |   |
| array_var              | ✓ | ✓ | ✓ | ✓ | ✓ |
| class                  | ✓ |   |   |   |   |
| configuration          | ✓ | ✓ |   | ✓ | ✓ |
| doc (ドキュメンテーションコメント) | ✓ | ✓ | ✓ | ✓ | ✓ |
| elementary_types       | ✓ | ✓ | ✓ | ✓ | ✓ |
| en_eno (有効/有効出力) | ✓ | ✓ | ✓ | ✓ | ✓ |
| enum                   | ✓ | ✓ |   |   | ✓ |
| fb (FB)                | ✓ | ✓ | ✓ | ✓ | ✓ |
| fbd (FBD言語)          | ✓ |   |   |   |   |
| func (関数)            | ✓ | ✓ | ✓ | ✓ | ✓ |
| global_var             | ✓ | ✓ | ✓ | ✓ | ✓ |
| header_info            | ✓ | ✓ | ✓ | ✓ | ✓ |
| il (IL言語)            | ✓ |   |   |   |   |
| import                 | ✓ | ✓ | ✓ | ✓ | ✓ |
| include                | ✓ | ✓ | ✓ | ✓ | ✓ |
| interface              | ✓ |   |   |   | ✓ |
| ld (ラダー)            | ✓ | ✓ | ✓ |   |   |
| named_value            | ✓ | ✓ |   |   | ✓ |
| namespace              | ✓ | ✓ |   |   | ✓ |
| oofb (OOファンクションブロック) | ✓ |   |   |   | ✓ |
| pp.fmacro1 (関数マクロ) | ✓ | ✓ | ✓ | ✓ | ✓ |
| pp.fmacro2             | ✓ | ✓ | ✓ | ✓ | ✓ |
| pp.ifmacro (条件)      | ✓ | ✓ | ✓ | ✓ | ✓ |
| pp.omacro (オブジェクトマクロ) | ✓ | ✓ | ✓ | ✓ | ✓ |
| pp.vaargs (可変長引数) | ✓ | ✓ | ✓ | ✓ | ✓ |
| program                | ✓ | ✓ | ✓ | ✓ | ✓ |
| ref_to (参照型)        | ✓ |   |   |   | ✓ |
| sfc (SFC言語)          | ✓ |   |   |   | ✓ |
| st (ST言語)            | ✓ | ✓ | ✓ | ✓ | ✓ |
| string_var             | ✓ | ✓ | ✓ | ✓ | ✓ |
| struct                 | ✓ | ✓ | ✓ | ✓ | ✓ |
| subrange_type          | ✓ |   |   |   |   |
| subrange_var           | ✓ | ✓ |   |   | ✓ |
| task                   | ✓ |   |   | ✓ | ✓ |
| var_access             | ✓ |   |   |   |   |
| var_attrs              | ✓ | ✓ | ✓ | ✓ | ✓ |
| var_config             | ✓ |   |   |   |   |
| variable_length_array  | ✓ | ✓ |   |   | ✓ |

ld/fbd/sfc/il の三菱・CODESYSサンプルがないのは、これらの言語の
インポートをそれぞれのメーカーが対応していないためと考えられる。

---

## まとめ

- ST と FB / 関数は全メーカーで使える（最も汎用的）
- ラダーは三菱・CODESYSではjiecc経由ではXML化不可
- FBD は standardのみ
- SFC は standard と CODESYS のみ
- 三菱は `--retro_caps` 必須
- メーカー側のIEC 61131-10対応バージョンを満たすことが必要
