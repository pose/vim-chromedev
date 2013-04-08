if !has('python')
    echo "Error: Required vim compiled with +python"
    finish
endif

execute "pyfile ".fnameescape(fnamemodify(expand("<sfile>"), ":h")."/chrome.py")

function! ChromeStart()
    python start()
endfunction

function! ChromeStop()
    python stop()
endfunction

function! ChromePing()
    python ping()
endfunction

function! ChromeTest()
    python test()
endfunction

function! ChromeDebug() 
    " Copy the line to match the tabbing and remove the content of the ine
    execute "normal yy1kp\<S-D>"

    " Insert the magic code
    execute "normal i/*jshint debug:true */\<CR>debugger;\<CR>/*jshint debug:false*/\<ESC>"
    execute "w"
    "execute "normal 2k3dd"
    "execute "wa"
endfunction
