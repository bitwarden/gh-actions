let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/bitwarden/official-repos/gh-actions/lint-workflow-v2
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +33 tests/test_lint.py
badd +33 tests/test_utils.py
badd +38 Taskfile.yml
badd +0 src/rules/job_environment_prefix.py
badd +0 tests/rules/test_job_environment_prefix.py
badd +0 tests/fixtures/test_a.yaml
badd +4 src/load.py
argglobal
%argdel
$argadd tests/test_lint.py
set stal=2
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit src/rules/job_environment_prefix.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 163 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 163 + 163) / 327)
argglobal
balt tests/rules/test_job_environment_prefix.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 70 - ((58 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 70
normal! 018|
wincmd w
argglobal
if bufexists(fnamemodify("tests/rules/test_job_environment_prefix.py", ":p")) | buffer tests/rules/test_job_environment_prefix.py | else | edit tests/rules/test_job_environment_prefix.py | endif
if &buftype ==# 'terminal'
  silent file tests/rules/test_job_environment_prefix.py
endif
balt src/rules/job_environment_prefix.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 40 - ((32 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 40
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 163 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 163 + 163) / 327)
tabnext
edit src/load.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
2wincmd h
wincmd w
wincmd w
let &splitbelow = s:save_splitbelow
let &splitright = s:save_splitright
wincmd t
let s:save_winminheight = &winminheight
let s:save_winminwidth = &winminwidth
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 109 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 108 + 163) / 327)
argglobal
balt tests/fixtures/test_a.yaml
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 60 - ((26 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 60
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("tests/fixtures/test_a.yaml", ":p")) | buffer tests/fixtures/test_a.yaml | else | edit tests/fixtures/test_a.yaml | endif
if &buftype ==# 'terminal'
  silent file tests/fixtures/test_a.yaml
endif
balt src/load.py
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 8 - ((7 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 8
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("Taskfile.yml", ":p")) | buffer Taskfile.yml | else | edit Taskfile.yml | endif
if &buftype ==# 'terminal'
  silent file Taskfile.yml
endif
balt tests/fixtures/test_a.yaml
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let &fdl = &fdl
let s:l = 39 - ((38 * winheight(0) + 30) / 61)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 39
normal! 063|
wincmd w
exe 'vert 1resize ' . ((&columns * 109 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 108 + 163) / 327)
tabnext 2
set stal=1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let &winminheight = s:save_winminheight
let &winminwidth = s:save_winminwidth
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
