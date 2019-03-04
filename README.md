# ParaConv
Paradox作品で使用される日本語ローカライズファイルの表記ゆれを自動的に統一するツールです。

## 現在できること

  常体（だ・である調）の文章を、敬体（です・ます調）に変換する。

## 使用方法

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
 - `ParaConv.py`に`utf8`以下の適当なフォルダ名と出力フォルダ名、ログフォルダ名を渡す

     `$ ParaConv.py utf8/localisation out log`

## 今後の予定

 - 敬体（です・ます調）を常体（だ・である調）に変換する
 - イベントに関連するエントリだけを変換する
 - 行頭の「我々は」「彼らは」などを一括して省略する

## 参考資料

 - mocobeta『[janome - Japanese morphological analysis engine written in pure Python](https://github.com/mocobeta/janome)』
 - 林由紀子、松原茂樹『[自然な読み上げ音声出力のための書き言葉から話し言葉へのテキスト変換](http://slp.itc.nagoya-u.ac.jp/web/papers/2007/hayashi_SLP66.pdf)』言語処理学会第14回年次大会発表論文集, pp.790-793, 2008.
 - 一般社団法人 日本翻訳連盟『[JTF日本語標準スタイルガイド（翻訳用）](https://www.jtf.jp/jp/style_guide/pdf/jtf_style_guide.pdf)』
