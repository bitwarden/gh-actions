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
badd +0 README.md
badd +0 Taskfile.yml
badd +150 src/bitwarden_workflow_linter/utils.py
badd +0 src/bitwarden_workflow_linter/default_actions.json
badd +10 src/bitwarden_workflow_linter/default_settings.py
badd +11 settings.py
badd +5 tests/test_utils.py
badd +2 settings.yaml
badd +0 src/bitwarden_workflow_linter/default_settings.yaml
badd +0 src/bitwarden_workflow_linter/load.py
badd +8 tests/fixtures/test-alt.yml
badd +4 tests/fixtures/test-min.yaml
badd +3 tests/fixtures/test_a.yaml
badd +0 tests/test_load.py
badd +0 src/bitwarden_workflow_linter/models/job.py
badd +0 tests/test_job.py
argglobal
%argdel
$argadd README.md
set stal=2
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit README.md
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
balt Taskfile.yml
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
let s:l = 143 - ((61 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 143
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("Taskfile.yml", ":p")) | buffer Taskfile.yml | else | edit Taskfile.yml | endif
if &buftype ==# 'terminal'
  silent file Taskfile.yml
endif
balt README.md
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
let s:l = 57 - ((56 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 57
normal! 058|
wincmd w
exe 'vert 1resize ' . ((&columns * 163 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 163 + 163) / 327)
tabnext
edit src/bitwarden_workflow_linter/load.py
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
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
argglobal
balt tests/test_load.py
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
let s:l = 57 - ((32 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 57
normal! 09|
wincmd w
argglobal
if bufexists(fnamemodify("tests/test_load.py", ":p")) | buffer tests/test_load.py | else | edit tests/test_load.py | endif
if &buftype ==# 'terminal'
  silent file tests/test_load.py
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
let s:l = 4 - ((3 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 4
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("tests/fixtures/test_a.yaml", ":p")) | buffer tests/fixtures/test_a.yaml | else | edit tests/fixtures/test_a.yaml | endif
if &buftype ==# 'terminal'
  silent file tests/fixtures/test_a.yaml
endif
balt tests/test_load.py
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
let s:l = 3 - ((2 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 3
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
tabnext
edit src/bitwarden_workflow_linter/models/job.py
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
balt tests/test_job.py
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
let s:l = 1 - ((0 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("tests/test_job.py", ":p")) | buffer tests/test_job.py | else | edit tests/test_job.py | endif
if &buftype ==# 'terminal'
  silent file tests/test_job.py
endif
balt src/bitwarden_workflow_linter/models/job.py
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
let s:l = 11 - ((10 * winheight(0) + 33) / 67)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 11
normal! 0
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 163 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 163 + 163) / 327)
tabnext 3
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
