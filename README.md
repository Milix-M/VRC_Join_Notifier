# VRChat join通知システム
自分がいるワールドにJoinしてきたプレイヤーを通知するシステム。
## 使用方法
main.pyを起動するだけです。
## 指定できるオプション
ウィンドウ上部のメニューバー→設定→環境設定からオプションを設定可能です。使用可能なオプションは以下の通りです。
### 更新頻度(ms)
join通知の更新頻度をミリ秒単位で指定します。値が小さくなるほどCPU負荷が高くなり,ストレージへのアクセスが増えます。
### XSOvelayに送信する
チェックを入れるとXSOverlayに通知を送信します。チェックを入れない場合XSOvelayでの通知はしません。
### Joinログを.txt形式で書き出す
Joinログを.txt形式で書き出します。この機能を有効化すると後述する「Joinログを.txtファイルから読み込み復元する」機能が使用可能になります。
### Joinログを.txtファイルから読み込み復元する
前述した「Joinログを.txt形式で書き出す」機能で生成された.txtファイルを読み込み、メインウィンドウのログ表示エリアに復元します。「Joinログを.txt形式で書き出す」機能が有効化されていない状態で有効化すると自動的に「Joinログを.txt形式で書き出す」が有効化されます。

## 仕組み
ユーザーディレクトリ/AppData/LocalLow/VRChat/VRChatディレクトリ内に生成されるログファイルを一行ずつ読み込み,"[Behaviour] OnPlayerJoined [プレイヤー名]"のある行があった場合、プレイヤー名を抜き出して通知しています。