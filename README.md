# ParaConv
Paradox作品で使用される日本語ローカライズファイルの表記ゆれを自動的に統一するツールです

## 概要

### できること

- テキストを敬体（です・ます調）に統一する
- テキストを常体（だ・である調）に統一する
- テキストの一部だけを統一する（イベント本文のみなど）

### 対応作品

    Europa Universalis IV / Crusader Kings II / Hearts of Iron IV / Stellaris

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

### 書式

     ParaConv.py [--options] input output log

#### フォルダ指定（必須）

 - `input`：変換元のローカライズファイルがあるフォルダ
 - `output`：変換後のローカライズファイルが入るフォルダ
 - `log`：変換結果の差分ファイルが入るフォルダ

#### 作品指定（必須）

 - `--eu4`：Europa Universalis IV
 - `--ck2`：Crusader Kings II
 - `--hoi4`：Hearts of Iron IV
 - `--stellaris`：Stellaris

#### 機能指定（必須）

 - `--keitai`：テキストを敬体（です・ます調）に統一する
 - `--joutai`：テキストを常体（だ・である調）に統一する
 - `--da`：テキストを常体に、文末を「だ」に統一する
 - `--dearu`：テキストを常体に、文末を「である」に統一する
 - `--nopronoun`：テキストから不要な代名詞を取り除く

    完全なオプション一覧は`ParaConv.py -h`で見ることができます

## 高度な使い方

### イベント本文のみを変換する

 - `ParaConvEvent.py`を使用してイベント本文のキーリストを作成する

     `$ ParaConvEvent.py --eu4 events keylist.txt`

 - 作成したキーリストを`--key`オプションで`ParaConv.py`に渡す

     `$ ParaConv.py --eu4 --dearu --key keylist.txt utf8/localisation out log`

    `ParaConvEvent.py`の完全なオプション一覧は`ParaConvEvent.py -h`で見ることができます

### 変換したキーだけを出力する

 - `ParaConv.py`に`--difference`オプションを指定する
 
    `$ ParaConv.py --eu4 --nopronoun --difference utf8/localisation out log`
 
    出力ファイルをmodの`localisation/replace`に入れれば、修正部分だけを置換できます

## 制限事項

 - 敬語には対応していません

## 今後の予定

 - セリフと地の文で文体を使い分ける

## 参考資料

 - mocobeta『[janome - Japanese morphological analysis engine written in pure Python](https://github.com/mocobeta/janome)』
 - 林由紀子、松原茂樹『[自然な読み上げ音声出力のための書き言葉から話し言葉へのテキスト変換](http://slp.itc.nagoya-u.ac.jp/web/papers/2007/hayashi_SLP66.pdf)』言語処理学会第14回年次大会発表論文集, pp.790-793, 2008.
 - 一般社団法人 日本翻訳連盟『[JTF日本語標準スタイルガイド（翻訳用）](https://www.jtf.jp/jp/style_guide/pdf/jtf_style_guide.pdf)』
