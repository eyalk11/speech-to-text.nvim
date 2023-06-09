# speech-to-text.nvim
Neovim plugin offer  speech to text capability using [speech_recognition](https://github.com/Uberi/speech_recognition). 

You can select your favorite engine for speech-to-text : whisper, openai, google, azure etc.. 
(All supported engines in speech recognition)

This is basically a tin wrapper around speech_recognition. So, you really want to check out its documentation. 
Should work OOB with whisper function. 

Uses keyboard package , which I think on linux requires admin. Luckily, only used for detection of ESC so ESC might not work. 
Tested on windows only (but should work).

## Installation

Use
```
Plug 'eyalk11/speech-to-text.nvim'
```

And then: 

```
!pip install -r ~/.vim/plugged/speech-to-text.nvim/requirements.txt
:UpdateRemotePlugins
```
(Those are minimal requirements. It may need additional - see [speech_recognition](https://github.com/Uberi/speech_recognition))

### Alternative 
Try  
```
Plug 'eyalk11/speech-to-text.nvim', {'do': ':!python -m pip install -r ./requirements.txt \| :UpdateRemotePlugins'}
```
Should work, but couldn't confirm this due to unclear output by vim-plug. Possibly OS  dependet. 
Let me know if works.

## Usage

It will add the 

`GetVoice()` function - which returns text by speech

`:Voice` which replaces the selected range with text (by speech). Gets the same parameters as the ConfigureVoice commmand. 

You can cancel both voice commands by pressing esc.

`:ConfigureVoice [enginename] [paramsdic]` - which configures engine parameters (can also be done by yaml config). 
The enginename and params would be used for the next Voice/GetVoice call. 

## Mappings

It doesn't add by default.

You may use:
```
nmap <c-L> :Voice<CR>
imap <C-L> <C-R>=GetVoice()<CR>
```

## Credits

https://vi.stackexchange.com/users/23502/vivian-de-smedt for helping out with replacing text. 

