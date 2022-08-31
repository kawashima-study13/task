# Metronome Response Task

課題の詳細は[Andersonらの論文](https://link.springer.com/article/10.3758/s13414-020-02131-x)を御覧ください。

# Manual

## 被験者IDの入力

起動すると、以下のようにプロンプトが表示されます。

```
Input sub. ID:
```

被験者IDを入力して`Enter`を押すと、指定の場所（`task.ini: misc.dir_home`）にフォルダが作成されます。  
フォルダの名前は被験者IDと同じになります。  
このフォルダ内にデータが保存されます。  

なにも入力せずに`Enter`を押すと、以下のようにプロンプトが表示されます。

```
WONT SAVE! n to reinput ID: 
```

`Enter`を押すとそのまま先に進行しますが、データが保存されなくなります。  
`n`を押して`Enter`で、被験者IDを入力し直せます。

すでに同じ名前のフォルダがある場合、以下のようにプロンプトが表示されます。

```
Already exists. n to reinput:
```

`Enter`を押すとそのまま進行します（データは上書きされてしまいます）。  
`n`を押して`Enter`で、被験者IDを入力し直せます。


## 実験フェーズの選択

続いて、以下のようにプロンプトが表示されます。

```
i. Instrument test
f. Fixation
1. Practice MRT
2. Run MRT
Input phase num and enter:
```

先頭の一文字（i, f, 1, or 2）を入力して`Enter`で、指定されたフェーズが実施されます。

## 全フェーズ共通の仕様

`q`を押すと全画面が終了し、実験フェーズの選択画面に戻ります。  
質問画面提示時など、一部で対応しない場合もあります。  
`c`を押すと、ベースライン測定（注視点のみが一定時間表示される）がスキップされます。  
デバッグ時などに使用してください。

## i. Instrument test

ボタンとの接続や脳波計へのトリガー入力をテストするためのフェーズです。  
ボタンやキー入力をすると、入力されたキー・ボタン名が全画面に表示されます。  
同時に、MISCコードが脳波計へトリガー入力されます。  
`q`を押すと終了し、実験フェーズの選択画面に戻ります。


## f. Fixation

全画面に注視点（＋）が表示されたままになります。  
`q`を押すと終了し、実験フェーズの選択画面に戻ります。

## 1. Practice MRT

MRTの練習が実施されます。  
トリガー入力やデータの保存はされません。

## 2. Run MRT

### 待機画面

MRTが実施されます。  
フェーズが始まると、全画面に以下の文章が表示されます。

「そのままお待ちください。(Press ENTER to test vol)」

このときに`Enter`を押すと、MRIパルス（あるいは`t`入力）を１回（task.ini: mrt_simul.n_mripulse_towait_bfr_voltune）待ってから音量調整が始まります。  

### 音量調整

音量調整画面では、全画面に以下の文章が表示されます。

「２種類の音が聞こえたら上ボタンで課題開始 聞こえなかったら下ボタン」

同時にメトロノーム音が再生されます。

このとき下ボタンを押すと、以下の文章が表示されます。  
「そのままお待ちください。(Volume is too low! press QUIT key)」  
`q`を押してフェーズ選択画面に戻り、音量調整など適切な対応をしてください。

一方、上ボタンを押すと、MRTパルス（あるいは`t`入力）を５回（task.ini: mrt_simul.n_mripulse_towait_aft_voltune）待ってからベースライン測定（pre）が始まります。

### ベースライン測定（pre）

BASE_PREコードが脳波計へトリガー入力されます。  
同時に注視点（＋）が表示されます。  
30秒（task.ini: mrt_simul.sec_baseline_pre）が経過すると、課題が開始されます。

### 課題

課題が始まると、TASKコードが脳波計へトリガー入力されます。

課題では、Blockが18回（stim_generation.ini: mrt.n_block）繰り返されます。  
Blockの開始時にはBLOCKコードが入力されます。  
１つのBlockでは、複数のTrial（平均50個; stim_generation.ini: mrt.total_trial）が繰り返されます。  
Blockの最後には、Probeが提示されます。

Trial開始時には、NORM_TRIALコードまたはODD_TRIALコードが脳波計へ入力されます。  
ビープ音が鳴ると同時に、BEEPコードが入力されます。  
被験者が右ボタンを押すと、MWCAUGHTコードが入力されます。  
他のボタンを押すと、PRESSEDコードが入力されます。

Probeが提示されると、PROBEコードが入力されます。  
被験者がこれに回答すると、CHOICEコードが入力されます。  
3秒（task.ini: mrt_base.itvl_aft_probe）後、次のBlockが開始されます。

## 注意点

課題実施中、実行しているPCを操作しないでください。  
フォーカスが全画面以外に移ると、入力を受け付けなくなったり、Windowsがフリーズ扱いしてきたりします。

課題プログラム起動後、ディスプレイやサウンドデバイスの接続・切断をしないでください。  
画面表示や音提示に不具合が生じます。  
ディスプレイやサウンドデバイスの接続・切断を行った場合は、メインウィンドウ（フェーズ選択のプロンプトなどが表示される画面）を一回閉じて、再度課題を実行してください。

# Install

`conda` を使える状態で、お好きなディレクトリにて下記のようなコマンドを実行してください。  
`{VERSIONAME}` には `v0.4.0` といったバージョン名が入ります。  
コードがダウンロードされるとともに、実行環境がcondaで作られます。

```
mkdir mrt
curl -L https://api.github.com/repos/kawashima-study13/task/tarball/refs/tags/{VERSIONNAME} | tar xzf - -C mrt --strip-components 1
cd mrt
conda env create -n s13t -f conda.yaml
```

# Execution

Conda環境をActivateし、main.py を実行してください。  
必ずmain.pyと同じディレクトリから実行してください。

```
conda activate s13t
python main.py
```

また、別ウィンドウでprogserver.pyを起動しておくと、進行状況が見やすくなります。  
.batファイルや.shファイルを作成すると便利です。

```.batファイルの例
call C:\Users\issakuss\Miniconda3\Script\activate.bat
call activate s13t
call cd mrt
start progbar.cmd
mode con lines=30 cols=90
call python main.py
pause
```

# Requirements

PsychoPyが依存するオーディオパッケージ[PortAudio](https://github.com/PortAudio/portaudio)が最近のmacOSに対応していないようです。  
macOSで実行する場合は[SoX](http://sox.sourceforge.net)をインストールし、 config/task.ini の`use_ppsound`をFalseにしてください。  
ただし、時間精度が不安定になります。
