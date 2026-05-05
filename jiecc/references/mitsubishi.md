# 三菱電機 GX Works3 IEC 61131-10 XML 詳細仕様

GX Works3 がインポート/エクスポートする IEC 61131-10 XML の三菱独自拡張要素・
プロパティ・データ型・記述方法を網羅。**三菱向けXML生成時の必読リファレンス**。

このドキュメントは、三菱電機提供の公式完全サンプルXML
（`samples/mitsubishi/_official_complete_sample.xml`）を分析した結果を整理したもの。

---

## 目次

1. 基本情報
2. サポート言語と制約
3. 三菱固有データ型
4. 三菱独自XML拡張（AddData）一覧
5. プラグマでの拡張属性指定
6. プログラムファイル（Resource）の実行種別
7. ワークシート（複数Body）
8. 変数アクセス指定子と保持属性
9. 構造体メンバの細分化コメント
10. グローバル変数とアドレス指定
11. キーワード大文字化（必須）
12. ハマりどころ

---

## 1. 基本情報

### 必要なバージョン

| 製品 | 必要バージョン |
|---|---|
| MELSOFT GX Works3 | **Ver.1.110Q 以降** |

これ未満では IEC 61131-10 XML インポート機能自体がない。

### XMLスキーマ

GX Works3 が出力するXMLは、IEC 61131-10 規格のスキーマではなく、
**三菱拡張版スキーマ** `GXW3_IEC61131_10_Ed1_0_ForGXW3.xsd` を参照する：

```xml
<Project xmlns="www.iec.ch/public/TC65SC65BWG7TF10"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         schemaVersion="1.000"
         xsi:schemaLocation="www.iec.ch/public/TC65SC65BWG7TF10 GXW3_IEC61131_10_Ed1_0_ForGXW3.xsd">
```

### FileHeader / ContentHeader

```xml
<FileHeader companyName="..." companyURL="..." productName="GX Works3" productVersion="ver.1.0"/>
<ContentHeader name="..." creationDateTime="2023-09-17T00:00:00+09:00"
               modificationDateTime="2023-09-17T00:00:01+09:00"/>
```

jieccのプラグマで設定する：

```iec
//{company-name: MITSUBISHI ELECTRIC CORPORATION}
//{company-url: http://www.mitsubishielectric.com}
//{product-name: GX Works3}
//{product-version: ver.1.0}
//{content-name: MyProject}
//{creation-datetime: 2023-09-17T00:00:00+09:00}
//{modification-datetime: 2023-09-17T00:00:01+09:00}
```

---

## 2. サポート言語と制約

| 言語 | XMLインポート対応 |
|---|:-:|
| ST（Structured Text） | ✓ |
| FB（FunctionBlock） | ✓ |
| 関数（Function） | ✓ |
| LD（ラダー） | **✗** |
| FBD | **✗** |
| SFC | **✗** |
| IL | **✗** |

**ラダーはGX Works3で直接編集する必要がある**。jieccで生成したXMLをラダーとして
取り込むことはできない。

ラダー処理を依頼された場合は：
1. STで等価実装する
2. GX Works3 のラダーから呼び出すFB群をjieccで作る
3. GX Works3 上で直接ラダー編集してもらう

---

## 3. 三菱固有データ型

IEC 61131-3 標準にはなく、GX Works3 が独自に提供する型：

| 型 | サイズ | 用途 |
|---|---|---|
| `TIMER` | 32bit | 標準タイマー |
| `LTIMER` | 64bit | ロングタイマー |
| `RETENTIVETIMER` | 32bit | 積算タイマー（停電保持） |
| `LRETENTIVETIMER` | 64bit | ロング積算タイマー |
| `COUNTER` | 32bit | カウンタ |
| `LCOUNTER` | 64bit | ロングカウンタ |
| `POINTER` | - | ポインタ（ラダーのジャンプ先ラベル等） |

### 使用例

```iec
//{retro_caps: true}

program Main
    var
        T1: TIMER;                  // タイマー変数
        C1: COUNTER;                // カウンタ変数
        T_long: LTIMER;             // ロングタイマー
        T_retain: RETENTIVETIMER;   // 積算タイマー
    end_var
//{st}
// ラダー側のOUT_T、OUT_C命令で参照される変数として使う
//{end}
end_program
```

XMLでは大文字で出力される：

```xml
<Variable name="T1">
    <Type><TypeName>TIMER</TypeName></Type>
</Variable>
```

### 標準IEC型との対応

GX Works3 で使える IEC 61131-3 標準型（大文字表記）：

`BOOL` `BYTE` `WORD` `DWORD` `LWORD` `INT` `DINT` `LINT` `UINT` `UDINT`
`SINT` `USINT` `REAL` `LREAL` `TIME` `STRING[N]` `WSTRING[N]`

文字列は長さ指定が必須：`STRING[32]` のように書く。

---

## 4. 三菱独自XML拡張（AddData）一覧

GX Works3 は IEC 61131-10 標準の `<AddData>` 機構を使い、独自拡張属性を
名前空間 `http://www.mitsubishielectric.com/xml/` で追加する。

### POU/型レベルの拡張

| 拡張名 | 主な属性 | 用途 |
|---|---|---|
| `PouProperties` | `title`, `version`, `helpFilePath`, `supportVersion` | POU共通プロパティ |
| `FbPouProperties` | `isEnEno`, `isMcMcr`, `labelAssignmentArea`, `latchLabelAssignmentArea`, `signalFlowAssignmentArea` | FB固有プロパティ |
| `FunPouProperties` | `isEnEno` | 関数固有プロパティ |
| `DataTypeProperties` | `title`, `version`, `helpFilePath`, `supportVersion`, `reservedArea` | 構造体プロパティ |
| `GlobalVarsProperties` | `name`, `title`, `version`, `helpFilePath`, `supportVersion` | グローバル変数群プロパティ |

### ファイル/フォルダ階層関連

| 拡張名 | 主な属性 | 用途 |
|---|---|---|
| `FbPouFile` | `name` | FBが所属するFBファイル |
| `FbFiles` | (子要素 `<FbFile>`) | FBファイル一覧 |
| `FunPouFile` | `name` | 関数が所属するFUNファイル |
| `FunFiles` | (子要素 `<FunFile>`) | FUNファイル一覧 |
| `ProgramFileProperties` | `title` | プログラムファイル（リソース）のタイトル |
| `PouResourceFolder` | `name` | POUが所属するフォルダ |
| `ResourceFolders` | (子要素 `<ResourceFolder>`) | リソース内のフォルダ階層 |
| `ResourceExecutionType` | `type` | プログラムファイルの実行種別 |

### 変数レベルの拡張

| 拡張名 | 内容 | 用途 |
|---|---|---|
| `VariableComments` | 子要素 `<Comment>`, `<Bit>`, `<Array>` | 変数コメント（ビット/配列要素別も可） |
| `VariableLineNumber` | 属性 `number` | エディタ表示時の行番号 |
| `VariableRemark` | 子要素 `<RemarkText>` | 注釈 |
| `VariableSystemLabel` | 属性 `name`, `attribute`, `relation` | システムラベル |
| `VariableExternalDeviceAccess` | 属性 `isAccess` | 外部機器アクセス可否 |
| `VariableStructDeviceAssignment` | 子要素 `<Member>` | 構造体メンバへのデバイス割付 |

### Body（プログラム本体）レベルの拡張

| 拡張名 | 主な属性 | 用途 |
|---|---|---|
| `BodyProperties` | `orderWithinBodyProperties`, `workSheetName`, `executeOrder` | ワークシート（複数Body）情報 |

---

## 5. プラグマでの拡張属性指定

jieccはこれらの三菱拡張属性をプラグマ経由で指定できる。`{key: value}` または
`{key.attribute: value}` の形式で記述する。

### POU共通プロパティ

```iec
program {PouProperties.title: "メインプログラム",
         PouProperties.version: "ver.1.003",
         PouProperties.helpFilePath: "doc/main.html",
         PouProperties.supportVersion: "1.001W"} Main
end_program
```

### FB固有プロパティ

```iec
function_block {PouProperties.title: "カウンタFB",
                FbPouProperties.isEnEno: true,
                FbPouProperties.isMcMcr: false,
                FbPouProperties.labelAssignmentArea: 20,
                FbPouProperties.latchLabelAssignmentArea: 12,
                FbPouProperties.signalFlowAssignmentArea: 5,
                FbPouFile.name: "FbFile1"} CounterFB
end_function_block
```

### 関数プロパティ

```iec
function {PouProperties.title: "加算関数",
          FunPouProperties.isEnEno: false,
          FunPouFile.name: "FunFile1"} Add: int
end_function
```

### 変数の三菱属性

行番号、コメントなど（変数宣言内のプラグマで指定）：

```iec
var
    Counter: int := 0   // {VariableLineNumber.number: 1}
                        // {doc: カウンタ変数}
                        // {VariableRemark.RemarkText: "リセット時0"};
end_var
```

### 構造体プロパティ

```iec
type
    PointStruct: struct
        // {DataTypeProperties.title: "座標構造体"}
        // {DataTypeProperties.version: "ver.1.002"}
        // {DataTypeProperties.reservedArea: 4}
        x: int;
        y: int;
    end_struct;
end_type
```

---

## 6. プログラムファイル（Resource）の実行種別

GX Works3 ではプログラムは **6種類の実行種別** に分けて配置される。
XMLでは `ResourceExecutionType.type`（AddData 拡張）で指定する。

| type値 | GX Works3 表示 | 用途 |
|---|---|---|
| `initial` | 初期 | PLC起動時に1回実行 |
| `scan` | スキャン | 通常のスキャン実行（最頻） |
| `standby` | 待機 | 通常実行されず、別プログラムから呼び出されたときのみ実行 |
| `fixedScan` | 定周期 | 指定周期で実行 |
| `event` | イベント | 特定イベント発生時に実行 |
| `noExecution` | 実行種別なし | 実行されない（編集中等） |

### ⚠️ jiecc 5.14.x の制約（2025年5月時点）

**`resource Name: prgFile` 構文および `ResourceExecutionType.type` プラグマは jiecc 5.14.x では未サポート。**

```
// ❌ 以下はいずれも jiecc 5.14.x でエラー
resource {ResourceExecutionType.type: "scan"} MainScan: prgFile
```

エラー例：
```
0x20008001: 'ResourceExecutionType.type'; UNKNOWN_PRAGMA_WARNING
0x44000004: ':'; INVALID_SYNTAX
```

### 正しいjieccテキスト記述（jiecc 5.14.x）

jiecc の公式サンプル（`samples/mitsubishi/task.txt`）に従い、
`resource Name on plc` を使う。

#### ⚠️ `task` 宣言を使用しないこと

`task` 構文はjieccとしては有効（エラーなし）だが、生成された `<Task>` 要素を
**GX Works3 インポート時に「読み込めないXML要素 'Task'」として無視する**。
その結果、`program ... with taskName:` の関連付けも失敗し、
プログラムが**「未登録プログラム」**に配置される。

```iec
// ❌ task使用 → <Task>生成 → GX Works3でWarning + 未登録プログラム
configuration config1
    resource MainScan on plc
        task tsk1(interval := T#10ms, priority := 1);
        program ProgramScan with tsk1: MyProgram();
    end_resource
end_configuration

// ✅ task不使用 → ProgramInstance が正常に登録される
configuration config1
    resource MainScan on plc
        program ProgramScan: MyProgram();
    end_resource
end_configuration
```

これにより生成されるXMLは `resourceTypeName="plc"` となる。
GX Works3 インポート時のデフォルト値（GX Works3 オペレーティングマニュアル 付8 より）：

| XML要素 | 生成値 | GX Works3デフォルト動作 |
|---|---|---|
| `resourceTypeName` | `"plc"` | プログラムファイル作成 |
| `<Task>` | 省略（task不使用） | — |
| `ResourceExecutionType` | 省略 | **実行タイプ指定なし** |

**インポート後、GX Works3 側で実行種別（スキャン等）を手動設定すること。**

### 公式サンプルXMLでの記述（参考）

公式サンプル（`_official_complete_sample.xml`）には `resourceTypeName="prgFile"` と
`ResourceExecutionType` が使われているが、これはGX Works3からのエクスポートXMLの形式。
jieccのテキストから生成する場合は上記の `on plc` 構文を使うこと。

```xml
<!-- 公式サンプルXMLの形式（エクスポート/手書きXML用参考） -->
<Resource name="MainScan" resourceTypeName="prgFile">
    <AddData>
        <Data name="http://www.mitsubishielectric.com/xml/ResourceExecutionType">
            <ResourceExecutionType type="scan"/>
        </Data>
    </AddData>
    <ProgramInstance name="ProgramScan" typeName="pou" evaluationOrder="1"/>
</Resource>
```

---

## 7. ワークシート（複数Body）

GX Works3 では1つのPOUを**複数のワークシート**に分けて記述できる。
XMLでは `<MainBody>` 内に複数の `<BodyContent>` を持つ：

```xml
<MainBody>
    <AddData>
        <Data name="http://www.mitsubishielectric.com/xml/BodyProperties">
            <BodyProperties orderWithinBodyProperties="1"
                            workSheetName="workSheet1"
                            executeOrder="2"/>
        </Data>
        <Data name="http://www.mitsubishielectric.com/xml/BodyProperties">
            <BodyProperties orderWithinBodyProperties="2"
                            workSheetName="workSheet2"
                            executeOrder="1"/>
        </Data>
    </AddData>
    <BodyContent xsi:type="ST">
        <ST>Local1_1:=B0;</ST>
    </BodyContent>
    <BodyContent xsi:type="ST">
        <ST>Local1_6:=W0;</ST>
    </BodyContent>
</MainBody>
```

- `orderWithinBodyProperties` — XML内での順序
- `workSheetName` — ワークシート名（GX Works3 上の表示名）
- `executeOrder` — **実行順序**（これが実際の実行順を決める）

### jieccで複数ボディを使うには

通常のテキストでは1つのPOUに1つの `{st}~{end}` ブロックしか書けないが、
複数の `{st}~{end}` を並べることで複数Body出力になる：

```iec
program Main
    var local1: bool; end_var
//{st}
local1 := B0;
//{end}

    var local2: word; end_var
//{st}
local6 := W0;
//{end}
end_program
```

逆に、複数の `{st}~{end}` を1つにまとめたい場合は `single-body` プラグマ：

```iec
program {single-body: true} Main
    ...
end_program
```

ワークシート名や実行順を指定したい場合：

```iec
program Main
    var ... end_var
//{BodyProperties.workSheetName: "初期化"}
//{BodyProperties.executeOrder: 1}
//{st}
init_processing();
//{end}
//{BodyProperties.workSheetName: "メイン処理"}
//{BodyProperties.executeOrder: 2}
//{st}
main_processing();
//{end}
end_program
```

---

## 8. 変数アクセス指定子と保持属性

`<Vars>` 要素には3つの属性がある：

```xml
<Vars constant="false" retain="false" accessSpecifier="private">
```

| 属性 | 値 | 意味 |
|---|---|---|
| `constant` | `true`/`false` | 定数（`var constant`） |
| `retain` | `true`/`false` | 停電保持（`var retain`） |
| `accessSpecifier` | `private`/`public` | アクセス指定子 |

### jieccでの記述

```iec
function_block MyFB
    // private（デフォルト）
    var
        priv_var: int;
    end_var

    // public
    var public
        pub_var: int;
    end_var

    // retain
    var retain
        latch_var: int;
    end_var

    // constant
    var constant
        FB_VERSION: int := 1;
    end_var

    // constant + retain（三菱は同時指定可）
    var constant retain
        IMMUTABLE_LATCH: int := 100;
    end_var
end_function_block
```

### OutputVars の retain 属性

`<OutputVars retain="true">` のように出力変数群にも retain を指定できる。
公式サンプルでは：

```xml
<OutputVars retain="false">
    <Variable name="fb1_vo">
        <Type><TypeName>BOOL</TypeName></Type>
    </Variable>
</OutputVars>
<OutputVars retain="true">
    <Variable name="fb1_vor">
        <Type><TypeName>BOOL</TypeName></Type>
    </Variable>
</OutputVars>
```

jiecc側ではvar_outputグループを分けることで対応：

```iec
function_block MyFB
    var_output
        normal_out: bool;
    end_var
    var_output retain
        latch_out: bool;
    end_var
end_function_block
```

---

## 9. 構造体メンバの細分化コメント

GX Works3 では、構造体メンバや配列要素の**個別位置にコメント**を付けられる。
公式サンプルから：

```xml
<Member name="member1_2">
    <AddData>
        <Data name="http://www.mitsubishielectric.com/xml/VariableComments">
            <VariableComments>
                <Comment number="6">
                    <CommentText>member1_2のコメント</CommentText>
                </Comment>
                <Bit index="0">
                    <Comment number="6">
                        <CommentText>member1_2.0のコメント</CommentText>
                    </Comment>
                </Bit>
            </VariableComments>
        </Data>
    </AddData>
    <Type><TypeName>INT</TypeName></Type>
</Member>
```

INT 型変数の bit 0 だけに別コメントを付けている。

配列要素の場合：

```xml
<Array>
    <Element index="0">
        <Comment number="6">
            <CommentText>member1_3[0]のコメント</CommentText>
        </Comment>
    </Element>
</Array>
```

`Comment` の `number` 属性は GX Works3 のコメント番号（1〜16の番号で
複数言語コメント等を切り替え）。

### jieccで記述する難易度

これら細分化コメントは jieccのテキスト構文では直接書けない可能性が高い。
必要な場合は：

1. GX Works3 で雛形を作って書き出し → XMLを直接編集して詳細コメントを追加
2. または逆変換（`-d`）でテキストに変換しコメントを記述、再度XML化

---

## 10. グローバル変数とアドレス指定

GX Works3 ではグローバル変数（ラベル）を `Configuration` 内に複数の
`<GlobalVars>` グループとして配置できる。

### 公式サンプルから

```xml
<GlobalVars constant="false" retain="false">
    <Documentation>MAINのグローバルラベルのコメント</Documentation>
    <AddData>
        <Data name="http://www.mitsubishielectric.com/xml/GlobalVarsProperties">
            <GlobalVarsProperties name="Global1" title="タイトル (一般)"
                                  version="ver.1.020" supportVersion="1.018W"/>
        </Data>
    </AddData>
    <Variable name="global_label1_2">
        <Type><TypeName>DWORD</TypeName></Type>
        <InitialValue><SimpleValue value="12"/></InitialValue>
    </Variable>
</GlobalVars>

<GlobalVars constant="false" retain="true">
    <Variable name="global_label1_3">
        <Type><TypeName>BOOL</TypeName></Type>
        <InitialValue><SimpleValue value="TRUE"/></InitialValue>
        <Address address="L0"/>           <!-- アドレス指定 -->
    </Variable>
</GlobalVars>
```

### jieccでの記述

```iec
configuration Config1
    resource MainScan on plc
        // 通常グローバル
        var_global
            // {GlobalVarsProperties.name: "Global1"}
            // {GlobalVarsProperties.title: "通常ラベル"}
            global_label1: dword := 12;
        end_var

        // RETAINグローバル
        var_global retain
            global_label3 at %L0 : bool := true;   // ラッチデバイスL0に割付
        end_var

        program ProgramScan: ProgramScan_pou();
    end_resource
end_configuration
```

### 三菱のアドレス指定の方言

| プレフィックス | 意味 | 例 |
|---|---|---|
| `%X` | ビットデバイス | `%X0`, `%X100` |
| `%Y` | 出力 | `%Y10` |
| `%M` | 内部リレー | `%M0` |
| `%L` | ラッチリレー | `%L0` |
| `%D` | データレジスタ | `%D100` |
| `%W` | ワード（リンク） | `%W0` |
| `%R` | ファイルレジスタ | `%R0` |

**`%IX`、`%QX`、`%MX` のような IEC標準プレフィックスは使えない**。
かならず `%X`、`%Y`、`%M` 等の三菱表記。

---

## 11. キーワード大文字化（必須）

GX Works3 はキーワードを大文字（`PROGRAM`, `VAR`, `INT` 等）として扱う。

### jieccでの対応

**必ず `--retro_caps` オプションを付ける**：

```bash
jiecc.exe --retro_caps input.txt -t mitsubishi -o output.xml
```

または、IEC 61131-3 テキスト先頭にプラグマ：

```iec
//{retro_caps: true}

program Main
    var i: int; end_var
//{st}
i := 0;
//{end}
end_program
```

これがないと、生成XMLのキーワードが小文字になり、GX Works3 の
インポート時にエラーや警告が出る可能性がある。

### 大文字化されるもの

- IEC キーワード: `PROGRAM`, `FUNCTION`, `FUNCTION_BLOCK`, `VAR`, `END_VAR` 等
- データ型: `BOOL`, `INT`, `WORD`, `STRING[32]` 等
- 真偽値: `TRUE`, `FALSE`
- ST文: `IF`, `THEN`, `ELSIF`, `ELSE`, `END_IF`, `FOR`, `TO`, `BY`, `DO`, `END_FOR` 等
- 演算子: `AND`, `OR`, `XOR`, `NOT`, `MOD`

---

## 12. ハマりどころ

### ① ラダー処理を依頼されたとき

jiecc経由ではXML化できない。STで等価実装するか、GX Works3で直接編集
してもらう。最も多い誤解ポイント。

### ② キーワードが小文字でインポートエラー

`--retro_caps` または `{retro_caps: true}` を忘れると発生。

### ② prgFile / ResourceExecutionType が使えない（jiecc 5.14.x）

`resource Name: prgFile` 構文および `ResourceExecutionType.type` プラグマは
**jiecc 5.14.x では未サポート**（INVALID_SYNTAX）。

代わりに `resource Name on plc` を使い、GX Works3 インポート後に
実行種別を手動設定すること（セクション6 参照）。

### ② BOM付きUTF-8が通らない（jiecc 5.14.6）

公式ページには "5.14~BOM有り・無し双方をサポート" と記載があるが、
**jiecc 5.14.6 の実測では BOM付きUTF-8は `INVALID_CHARACTER` エラー**。

PowerShell 5.1 の `Set-Content -Encoding UTF8` は BOM 付きで書き込む。
jieccに渡すファイルを生成・上書きするスクリプトでは `Set-Content` を避け、
`[System.IO.File]::WriteAllLines(path, lines, UTF8Encoding($false))` を使うこと。

### ③ アドレスプレフィックスの違い

- ❌ `at %IX0.0` (IEC標準だが三菱では認識されない)
- ✅ `at %X0.0` (三菱の正しい記法)

### ④ enum型の使用

GX Works3 Ver.1 では enum 型のサポートが限定的。
**INT型と定数（var constant）の組み合わせで代替**するのが安全：

```iec
// ❌ 推奨されない
type
    Mode_t: (Stop, Run, Pause);
end_type

// ✅ 推奨
var constant
    MODE_STOP:  int := 0;
    MODE_RUN:   int := 1;
    MODE_PAUSE: int := 2;
end_var
```

### ⑤ オブジェクト指向機能

GX Works3 Ver.1 では `interface`, `class`, `oofb`, `ref_to` は非対応。
通常FBで代替する。

### ⑥ namespace

GX Works3 Ver.1 では `namespace` は非対応。フラットな名前空間で命名規則
（プレフィックス等）で区別する。

### ⑦ continue文

for ループ内の `continue` 文は GX Works3 では非対応。
`if not (skip_condition) then ... end_if;` で代替。

### ⑧ 単項プラス演算子

`+intv` は非対応。`intv` だけで書く。

### ⑨ ビット要素アクセス

- ❌ `wordv.%X2` (非対応)
- ✅ `wordv.3` (整数インデックス形式のみ可)

### ⑩ static変数のat指定

ローカルの `var ... end_var` での `at` 指定は不可。
グローバル変数（`var_global`）でのみ使用できる。

### ⑪ `<Task>` 要素によるプログラム「未登録」（GX Works3 インポート時）

configuration の `task` 構文を使うとjieccは `<Task>` 要素を生成するが、
**GX Works3 はインポート時にこの要素を無視**（Warning:「読み込めないXML要素 'Task'」）し、
`program ... with taskName:` の `associatedTaskName` 関連付けも失敗する。
その結果、プログラムが **「未登録プログラム」** に配置される。

**回避策1（推奨）**: task 構文をソースから取り除く（セクション6 参照）

**回避策2**: jiecc 出力XMLを `fix-gx-xml.py` で後処理する:

```bash
# scripts/ 内の Python スクリプトで <Task> と associatedTaskName を除去
python scripts/fix-gx-xml.py output.xml           # 上書き
python scripts/fix-gx-xml.py output.xml -o fixed.xml  # 別ファイル出力
```

スクリプト動作：`<Task .../>` 要素を削除し、`associatedTaskName="..."` 属性を
`<ProgramInstance>` から除去する。

### ⑫' ProgramInstance の `name` が POU 名と不一致だと「未登録」

GX Works3 は `<ProgramInstance name="X" typeName="Y">` を処理する際、
**`name` 属性（インスタンス名）でプロジェクト内の Program POU を検索する**。

そのため `name != typeName` だと POU が見つからず「未登録プログラム」に落ちる：

```xml
<!-- ❌ name="ProgramScan" が POU を見つけられず未登録 -->
<ProgramInstance name="ProgramScan" typeName="MultiAxis"/>

<!-- ✅ name == typeName → 正常登録 -->
<ProgramInstance name="MultiAxis" typeName="MultiAxis"/>
```

jieccのソースでは `program <PouName>: <PouName>()` と書いてインスタンス名を
POU名と同一にすること：

```iec
configuration config1
    resource MainScan on plc
        program MultiAxis: MultiAxis();   // name == typeName（必須）
    end_resource
end_configuration
```

### ⑫ モーション制御ライブラリ定数のインライン展開

MotionControl_RD77.mslm / MotionControl_J4GFIO.mslm が提供するグローバルラベル定数は、
**GX Works3 にライブラリがロードされていないとXMLインポート時に未解決**になる。

| 定数名 | ライブラリ | 値 |
|---|---|---|
| `mcPositiveDirection` | MotionControl_RD77 / J4GFIO | `1` |
| `mcNegativeDirection` | MotionControl_RD77 / J4GFIO | `2` |
| `mcShortestWay` | MotionControl_RD77 | `3` |
| `MasterRJ71GF` | MotionControl_J4GFIO | `1` |
| `MasterRJ71EN_F` | MotionControl_J4GFIO | `2` |
| `MasterRJ71EN_EF` | MotionControl_J4GFIO | `3` |
| `MasterRD77GF` | MotionControl_J4GFIO | `4` |

**対処**: ソースファイル内でシンボル名の代わりにリテラル値を直接記述し、
コメントで意味を補足する：

```iec
FB_Move(
    ...
    Direction := 3   // mcShortestWay
);
AxisJ1.MasterModule := 1;  // MasterRJ71GF
```

### ⑬ MotionControl ライブラリ FB の型名フォーマット（`_` → `+`）

GX Works3 はライブラリ提供の FB を**プロジェクト内部で `TypeBase+ModuleName` 形式**
（プラス区切り）で管理する。しかし IEC 61131-3 識別子に `+` は使えないため、
jieccのテキストは `TypeBase_ModuleName` 形式（アンダースコア）で記述する。

その結果、jiecc が生成したXMLの `<TypeName>` はアンダースコア形式となるが、
**GX Works3 はプラス形式しか認識しない**。ライブラリがロード済みでも型が「赤」
（データ型不正エラー）になるのはこの不一致による。

| jiecc ソース（アンダースコア） | GX Works3 内部（プラス） |
|---|---|
| `MC_Power_RD77` | `MC_Power+RD77` |
| `MCv_Home_RD77` | `MCv_Home+RD77` |
| `MC_MoveAbsolute_RD77` | `MC_MoveAbsolute+RD77` |
| `MCv_ReadServoParameter_RD77GF` | `MCv_ReadServoParameter+RD77GF` |
| `MC_Power_J4GFIO` | `MC_Power+J4GFIO` |
| `AXIS_REF` | `AXIS_REF`（構造体は変換不要） |
| `AXIS_REF_J4GF` | `AXIS_REF_J4GF`（変換不要）|

**対処**: jiecc でXML生成後に `fix-gx-xml.py` を適用する（自動変換）：

```bash
python scripts/fix-gx-xml.py output.xml
```

`fix-gx-xml.py` は `<TypeName>` 要素内の `MC_*/MCv_*` 型名に限定して
`_RD77`/`_RD77GF`/`_RD77MS`/`_J4GFIO` サフィックスを `+` 形式に変換する。
構造体型（`AXIS_REF`、`AXIS_REF_J4GF`）・標準FB（`TON`等）は変換しない。

---

## 公式サンプルファイルの活用

`samples/mitsubishi/_official_complete_sample.xml` には以下が網羅されている：

- 6種類の Resource (initial/scan/standby/fixedScan/event/noExecution)
- POU (Program), FB (FunctionBlock), 関数 (Function) の完全構造
- 構造体定義とメンバ別コメント
- すべての三菱独自データ型（TIMER/COUNTER/POINTER系）の使用例
- 全 AddData 拡張要素の使用例
- グローバル変数（通常/RETAIN/アドレス指定あり）
- ワークシート（複数Body）の構造
- フォルダ階層（ResourceFolders, PouResourceFolder）
- 構造体メンバへのデバイス割付（VariableStructDeviceAssignment）

未知のXML要素や属性が出てきた場合、まずこのファイルでgrep検索して
使われ方を確認するのが最速。

```bash
# 例: VariableSystemLabel の使用例を探す
grep -A 10 'VariableSystemLabel' samples/mitsubishi/_official_complete_sample.xml
```
