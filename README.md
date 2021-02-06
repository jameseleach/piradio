# piradio

## Requirements

### MusicPlayerDaemon (MPD)
It's supposed to be as easy as `sudo apt-get install mpd mpc` but things are rarely that easy...

https://www.lesbonscomptes.com/pages/raspmpd.html

Well, the issue seems to be .pls files.
Reviewing the PLS and playing the stream inside seems to work.

```
pi@raspberrypi:~/Projects/piradio $ curl https://somafm.com/gsclassic130.pls
[playlist]
numberofentries=4
File1=http://ice4.somafm.com/gsclassic-128-aac
Title1=SomaFM: Groove Salad Classic (#1): The classic (early 2000s) version of a nicely chilled plate of ambient/downtempo beats and grooves.
Length1=-1
File2=http://ice2.somafm.com/gsclassic-128-aac
Title2=SomaFM: Groove Salad Classic (#2): The classic (early 2000s) version of a nicely chilled plate of ambient/downtempo beats and grooves.
Length2=-1
File3=http://ice6.somafm.com/gsclassic-128-aac
Title3=SomaFM: Groove Salad Classic (#3): The classic (early 2000s) version of a nicely chilled plate of ambient/downtempo beats and grooves.
Length3=-1
File4=http://ice1.somafm.com/gsclassic-128-aac
Title4=SomaFM: Groove Salad Classic (#4): The classic (early 2000s) version of a nicely chilled plate of ambient/downtempo beats and grooves.
Length4=-1
Version=2
```

`mpc add http://ice6.somafm.com/gsclassic-128-aac`
`mpc play`

