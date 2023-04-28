# nvim-voicerec
Neovim speech to text using [speech_recognition](https://github.com/Uberi/speech_recognition)

## Installation

Use
```
Plug 'eyalk11/nvim-voicerec'
```
(You might need to do `:UpdateRemotePlugins`)

```
pip install -r ~/.vim/plugged/nvim-voicerec/requirements.txt
```
(Those are minimal requirments. It may need additional - see [speech_recognition](https://github.com/Uberi/speech_recognition))

## Usage

It will add the 

`GetVoice()` function - which returns text by speech

`:Voice` command - which replaces the selected range with text (by speech). Gets the same parameters as the ConfigureVoice commmand. 

`:ConfigureVoice [enginename] [paramsdic]` - which configures engine parameters (can also be done by yaml config). 
The enginename and params would be used for the next Voice/GetVoice call. 


This is just a tin wrapper around speech_recognition. So, you really want to check out its documentation . 
Should work OOB with google recognize function. 

## Credits

https://vi.stackexchange.com/users/23502/vivian-de-smedt for helping out with replacing text. 

