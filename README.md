# FlacApiServer

## ソフトウェアについて
本ソフトウェアはFlac形式のデータをもとに、取得したデータをソートし、<br />
ソートしたデータをRESTの形式で配信するWEB API サーバです <br />
<br />


## 注意
基本的に、CDから取得したFlac形式のデータや<br />
合法的に取得したFlac形式のデータを用いて、<br />
音源にアーティスト名, アルバム名, 曲名が登録されていることが前提になります。<br />
<br />

## 使用方法
本リポジトリをクローン後<br />
- requirements.txt をもとに必要なライブラリをインストールしてください<br />
- config.ini内の path に音源が格納されているディレクトリのパスを<br />
絶対パスで記入してください。<br />

その後、Main.pyが配置されているディレクトリにて<br />
```
uvicorn Main:app --reload
```
上記のコマンドを入力すると起動します。<br/>

uvicornを使用しているので、様々なオプションがあります。<br >
好みでオプションをつけてください。<br />
## Api Documentation

/api/v1/main <br/>
- ソートされた生のデータが取得できます


/api/v1/artist_album/{artist}
- {artist} をアーティスト名に置き換えると、アーティストのアルバムが取得できます
- アーティスト名が存在しない場合、noneを返します

/api/v1/album_title/{album}
- {album} をアルバム名に置き換えると、アルバムの曲名が取得できます
- アルバム名が存在しない場合、noneを返します

/api/v1/songinfo/{artist}/{album}/{title}
- {artist} にアーティスト名, {album} にアルバム名, {title} に曲名を入れると、その曲に関する情報が取得できます
- アーティスト名, アルバム名, 曲名が　一致しなければ、noneを返します

/api/v1/songplay/{artist}/{album}/{title}
- {artist} にアーティスト名, {album} にアルバム名, {title} に曲名を入れると、その曲のデータをファイルとして返します
- アーティスト名, アルバム名, 曲名が　一致しなければ、noneを返します

/api/v1/artistlist
- ソートされたアーティストのリストが取得できます

/api/v1/albumlist<br />
- ソートされたアルバムのリストが取得できます

/api/v1/titlelist
- ソートされた曲名のリストが取得できます



