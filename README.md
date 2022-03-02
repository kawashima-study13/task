# Metronome Response Task

課題の詳細は[Andersonらの論文](https://link.springer.com/article/10.3758/s13414-020-02131-x)を御覧ください。

# Install

`conda` を使える状態で、お好きなディレクトリにて下記コマンドを実行してください。  
コードがダウンロードされるとともに、実行環境がcondaで作られます。

```
mkdir mrt
curl -L https://api.github.com/repos/kawashima-study13/task/tarball/refs/tags/v0.1.0 | tar xzf - -C mrt --strip-components 1
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

.batファイルや.shファイルを作成すると便利です。

```.batファイルの例
call C:\Users\issakuss\Miniconda3\Script\activate.bat
call activate s13t
call cd mrt
call python main.py
```

# Requirements

PsychoPyが依存するオーディオパッケージ[PortAudio](https://github.com/PortAudio/portaudio)が最近のmacOSに対応していないようです。  
macOSで実行する場合は[SoX](http://sox.sourceforge.net)をインストールし、 config/task.ini の`use_ppsound`をFalseにしてください。  
ただし、時間精度が不安定になります。
