# nvim-voicerec
Neovim text to speech using [speech_recognition](https://github.com/Uberi/speech_recognition)

## Installation

Use
```
Plug 'eyalk11/nvim-voicerec'
```
(You might need to do `:UpdateRemotePlugins`)

```
pip install SpeechRecognition

```
And follow more instuctions 



## Usage

It will add the 

`GetVoice()` function - which returns text by speech

`:Voice` command - which replaces the selected range with text (by speech).

`:ConfigureVoice` - which configures engine parameters (can also be done by lua). 


This is just a tin wrapper around speech_recognition. So, you really want to check out its documentation . 
Should work OOB with google recognize function. 

## Credits

https://vi.stackexchange.com/users/23502/vivian-de-smedt for helping out with replacing text. 

