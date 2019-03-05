# ParaConv
Paradox作品で使用される日本語ローカライズファイルの表記ゆれを自動的に統一するツールです

## できること

- テキストを敬体（です・ます調）に統一する
- テキストを常体（だ・である調）に統一する
- テキストの一部だけを統一する（イベント本文のみなど）

## 対応作品

- Europa Universalis IV
- Crusader Kings II
- Hearts of Iron IV
- Stellaris

## 使い方

### 必要な環境

 - [python](https://www.python.org) 3.3以上
 - [janome](https://mocobeta.github.io/janome/) 0.3以上
 - [MeCab](http://taku910.github.io/mecab/) 0.996用IPA辞書

### 環境の準備

 - pythonをインストールする
 - janomeをインストールする

     `$ pip install janome`

 - MeCab用IPA辞書をダウンロードし、中にある`Verb.csv`を`ParaConv.py`と同じフォルダに配置する

### 使用例

 - [ParaTranz](https://paratranz.cn/projects)からローカライズファイルをダウンロードする
 - `ParaConv.py`に変換オプションと変換対象のフォルダ、結果の出力先フォルダ、ログの出力先フォルダを渡す

     `$ ParaConv.py --eu4 --keitai utf8/localisation out log`

 - ファイル単位でも変換可能

     `$ ParaConv.py --ck2 --joutai --file sample.csv out log`

### オプション

     ParaConv.py [--keitai] [--joutai] [--da] [--dearu] [--key KEY] [--file] input output log

 - `--keitai`：テキストを敬体（です・ます調）に統一する
 - `--joutai`：テキストを常体（だ・である調）に統一する
 - `--da`：テキストを常体に、文末を「だ」に統一する
 - `--dearu`：テキストを常体に、文末を「である」に統一する
 - `--key`：変換対象のキーリストファイルを指定する（後述）
 - `--file`：引数の`input`をファイル名として扱う

    併せて以下のひとつを必ず指定してください

 - `--eu4`：Europa Universalis IVの場合に指定する
 - `--ck2`：Crusader Kings IIの場合に指定する
 - `--hoi4`：Hearts of Iron IVの場合に指定する
 - `--stellaris`：Stellarisの場合に指定する

    完全なオプション一覧は`ParaConv.py -h`で見ることができます

## 高度な使い方

### イベント本文のみを統一する

 - `ParaConvEvent.py`を使用してイベント本文のキーリストを作成します

     `$ ParaConvEvent.py --eu4 events keylist.txt`

 - 作成したキーリストを`--key`オプションで`ParaConv.py`に渡します

     `$ ParaConv.py --eu4 --dearu --key keylist.txt utf8/localisation out log`

    `ParaConvEvent.py`の完全なオプション一覧は`ParaConvEvent.py -h`で見ることができます

## 制限事項

 - 敬語には対応していません

## 今後の予定

 - 行頭の「我々は」「彼らは」などを一括して省略する
 - セリフと地の文で文体を使い分ける

## 参考資料

 - mocobeta『[janome - Japanese morphological analysis engine written in pure Python](https://github.com/mocobeta/janome)』
 - 林由紀子、松原茂樹『[自然な読み上げ音声出力のための書き言葉から話し言葉へのテキスト変換](http://slp.itc.nagoya-u.ac.jp/web/papers/2007/hayashi_SLP66.pdf)』言語処理学会第14回年次大会発表論文集, pp.790-793, 2008.
 - 一般社団法人 日本翻訳連盟『[JTF日本語標準スタイルガイド（翻訳用）](https://www.jtf.jp/jp/style_guide/pdf/jtf_style_guide.pdf)』
