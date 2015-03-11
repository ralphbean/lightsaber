"colorscheme tango
"colorscheme kib_darktango

let g:colorizer_auto_color = 1
let g:colorizer_x11_names = 1

syntax enable

colorscheme Tomorrow-Night-Bright

let maplocalleader = ",,"

au BufNewFile,BufRead *.otl colorscheme solarized
au BufNewFile,BufRead *.otl set nolist

map ,gtd :!gtd %<C-M>:e<C-M><C-M> 

nmap <C-p> :set paste!<CR>

python << endpython
import vim

def rstheader(char='='):
    (row, col) = vim.current.window.cursor
    line = vim.current.buffer[row-1]
    underline = ''.join([char for c in line.strip()])
    vim.current.buffer[row:row] = [underline]

endpython

map ,= :python rstheader('=')<Enter>
map ,- :python rstheader('-')<Enter>
map ,~ :python rstheader('~')<Enter>
map ,^ :python rstheader('^')<Enter>

" Make hlsearch work like less(1)
set hlsearch
nnoremap <ESC>u :nohlsearch<CR>
hi Search ctermfg=black ctermbg=white

map ,d :VCSDiff<Enter>
map ,q :q<Enter>
map ,c :VCSCommit<Enter>
map ,v :sp ~/.vimrc<Enter>
map ,s :split<Enter>
map ,e :E<Enter>
map ,p :Project<Enter>

set nocompatible

set guifont=Liberation\ Mono\ 9

set sw=4
set ts=4
set softtabstop=4
set expandtab
set smarttab
set enc=utf-8
set number

" Enable a nice big viminfo file
set viminfo='1000,f1,:1000,/1000

" Make backspace delete lots of things
set backspace=indent,eol,start


" Show us the command we're typing
set showcmd

" Highlight matching parens
set showmatch

" Search options: incremental search, do clever case things, highlight
" search
set incsearch
set ignorecase
set infercase
set hlsearch

set showfulltag " Show full tags when doing search completion
" set lazyredraw " Speed up macros

" No annoying error noises
set noerrorbells
set visualbell t_vb=
autocmd GUIEnter * set visualbell t_vb=

" Try to show at least three lines and two columns of context when
" scrolling
set scrolloff=3
"set sidescrolloff=2

" Wrap on these
"set whichwrap+=<,>,[,]

" Use the cool tab complete menu
set wildmenu
set wildignore=*.o,*.obj,*.bak,*.exe,*.pyc,*.swp

" Allow edit buffers to be hidden
set hidden

" 1 height windows
set winminheight=1

" Enable syntax highlighting
syntax on

if has('gui')
     set guioptions-=m
     set guioptions-=T
     set guioptions-=l
     set guioptions-=L
     set guioptions-=r
     set guioptions-=R
end

" By default, go for an indent of 4
set shiftwidth=4

" Do clever indent things. Don't make a # force column zero.
set smartindent
"inoremap # X<BS>#
set autoindent
set cindent                     " Use c-style indentation
set cinkeys=!^F                 " Only indent when requested
set cinoptions=(0t0c1           " :help cinoptions-values

" Syntax when printing
set popt+=syntax:y

" Enable filetype settings
filetype on
filetype plugin on
filetype indent on

" gitcomment.vim 
autocmd BufNewFile,BufRead COMMIT_EDITMSG set filetype=gitcommit

" taglist.vim stuff
let Tlist_Use_Right_Window = 1
let Tlist_Compact_Format = 1
let Tlist_Enable_Fold_Column = 0
map <Leader>ta :Tlist<CR>

" Show tabs and trailing whitespace visually
if (&termencoding == "utf-8") || has("gui_running")
     if v:version >= 700
        set list listchars=tab:»·,trail:·,extends:…,nbsp:‗
     else
         set list listchars=tab:»·,trail:·,extends:…
     endif
 else
     if v:version >= 700
         set list listchars=tab:>-,trail:.,extends:>,nbsp:_
     else
         set list listchars=tab:>-,trail:.,extends:>
     endif
 endif

if has("cscope")
    set csprg=/usr/bin/cscope
    set csto=0
    set cst
    set nocsverb
    " add any database in current directory
    if filereadable("cscope.out")
        cs add cscope.out
    " else add database pointed to by environment
    elseif $CSCOPE_DB != ""
        cs add $CSCOPE_DB
    endif
    set csverb
endif

"pressing l at the end of this line
"should move to the beginning of this line
set ww=h,l

"pressing h at the start of the next line
"should move to the end of the previous line
set ww=b,s,<,>,[,],h,l

set wrap

" Decrease annoying message size
set shortmess=a

inoremap <F5> <C-R>=strftime("* %a %b %d %Y Remy D <remyd@civx.us> ")<CR>

" Automatic python folding
augroup python_prog
au!
fun! Python_fold()
  execute 'syntax clear pythonStatement'
  execute 'syntax keyword pythonStatement break continue del'
  execute 'syntax keyword pythonStatement except exec finally'
  execute 'syntax keyword pythonStatement pass print raise'
  execute 'syntax keyword pythonStatement return try'
  execute 'syntax keyword pythonStatement global assert'
  execute 'syntax keyword pythonStatement lambda yield'
  execute 'syntax match pythonStatement /\<def\>/ nextgroup=pythonFunction skipwhite'
  execute 'syntax match pythonStatement /\<class\>/ nextgroup=pythonFunction skipwhite'
  execute 'syntax region pythonFold start="^\z(\s*\)\%(class\|def\)" end="^\%(\n*\z1\s\)\@!" transparent fold'
  execute 'syntax sync minlines=2000 maxlines=4000'
  set autoindent
  set foldmethod=syntax
  " set foldopen=all foldclose=all
  set foldtext=substitute(getline(v:foldstart),'\\t','\ \ \ \ ','g')
  set fillchars=vert:\|,fold:-
  set tabstop=4 shiftwidth=4 guioptions+=b
endfun
autocmd FileType python call Python_fold()
augroup END


" <C-l> redraws the screen and removes any search highlighting.
nnoremap <silent> <C-l> :nohl<CR><C-l>

" Move between files easly
map <silent><C-Left> <C-T>
map <silent><C-Right> <C-]>

set tags+=$HOME/.vim/tags/python.ctags

" Python code completion
autocmd FileType python set omnifunc=pythoncomplete#Complete

" bind ctrl+space for omnicompletion
inoremap <Nul> <C-x><C-o>

" :make for python files
" autocmd BufRead *.py set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
" autocmd BufRead *.py set efm=%C\ %.%#,%A\ \ File\ \"%f\"\\,\ line\ %l%.%#,%Z%[%^\ ]%\\@=%m


" add breakpoints for python 

"python << EOF
"import vim
"def SetBreakpoint():
"    import re
"    nLine = int( vim.eval( 'line(".")'))
"
"    strLine = vim.current.line
"    strWhite = re.search( '^(\s*)', strLine).group(1)
"
"    vim.current.buffer.append(
"       "%(space)spdb.set_trace() %(mark)s Breakpoint %(mark)s" %
"         {'space':strWhite, 'mark': '#' * 30}, nLine - 1)
"
"    for strLine in vim.current.buffer:
"        if strLine == "import pdb":
"            break
"    else:
"        vim.current.buffer.append( 'import pdb', 0)
"        vim.command( 'normal j1')
"
"vim.command( 'map <f7> :py SetBreakpoint()<cr>')
"
"def RemoveBreakpoints():
"    import re
"
"    nCurrentLine = int( vim.eval( 'line(".")'))
"
"    nLines = []
"    nLine = 1
"    for strLine in vim.current.buffer:
"        if strLine == 'import pdb' or strLine.lstrip()[:15] == 'pdb.set_trace()':
"            nLines.append( nLine)
"        nLine += 1
"
"    nLines.reverse()
"
"    for nLine in nLines:
"        vim.command( 'normal %dG' % nLine)
"        vim.command( 'normal dd')
"        if nLine < nCurrentLine:
"            nCurrentLine -= 1
"
"    vim.command( 'normal %dG' % nCurrentLine)
"
"vim.command( 'map <s-f7> :py RemoveBreakpoints()<cr>')
"EOF

" add python libs to vim path
python << EOF

import os
import sys
import vim
for p in sys.path:
    if os.path.isdir(p):
        vim.command(r"set path+=%s" % (p.replace(" ", r"\ ")))
EOF

" evaluate selected text via python
python << EOL
import vim
def EvaluateCurrentRange():
    eval(compile('\n'.join(vim.current.range),'','exec'),globals())
EOL
map <C-h> :py EvaluateCurrentRange()



if has("autocmd")
augroup vimrcEx
au!
    " In plain-text files and svn commit buffers, wrap automatically at 78 chars
    au FileType text setlocal tw=78 fo+=t

    " Switch to the directory of the current file, unless it's a help file.
    au BufEnter * if &ft != 'help' | silent! cd %:p:h | endif

    " smart indenting for python
    au FileType python set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

    " allows us to run :make and get syntax errors for our python scripts
    au FileType python set makeprg=python\ -c\ \"import\ py_compile,sys;\ sys.stderr=sys.stdout;\ py_compile.compile(r'%')\"
    au FileType python set expandtab
    au BufRead,BufNewFile *.mak setfiletype mako

    augroup END
endif

autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
autocmd FileType xml set omnifunc=xmlcomplete#CompleteTags
autocmd FileType mako set expandtab
autocmd FileType mako set ts=4
autocmd FileType html set ts=4
autocmd FileType html set expandtab

au BufWritePost *.py !pyflakes %
au BufWritePost *.py !pep8 %

call pathogen#infect('bundle')
call pathogen#runtime_append_all_bundles()
call pathogen#helptags()
let g:Powerline_symbols = 'fancy'
set laststatus=2
set encoding=utf-8
filetype plugin indent on

" Shoutout Ralph Bean <rbean@redhat.com> for overflow highlight hottness
highlight BadWhitespace ctermbg=red guibg=red
au BufRead,BufNewFile *.rst match BadWhitespace /*\t\*/
au BufRead,BufNewFile *.rst match BadWhitespace /\s\+$/
au BufRead,BufNewFile *.py match BadWhitespace /*\t\*/
au BufRead,BufNewFile *.py match BadWhitespace /\s\+$/

highlight OverLength ctermbg=red ctermfg=white guibg=#592929
match OverLength /\%80v.\+/
