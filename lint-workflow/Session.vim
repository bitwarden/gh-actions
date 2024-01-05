let SessionLoad = 1
let s:so_save = &g:so | let s:siso_save = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
let v:this_session=expand("<sfile>:p")
silent only
silent tabonly
cd ~/projects/workflow-linter
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
let s:shortmess_save = &shortmess
if &shortmess =~ 'A'
  set shortmess=aoOA
else
  set shortmess=aoO
endif
badd +1 README.md
badd +1 cli.py
badd +4 src/load.py
badd +1 config.yaml
badd +1 src/rules/__init__.py
badd +16 src/rules/name_capitalized.py
badd +17 src/rules/name_exists.py
badd +1 src/rule.py
badd +72 tests/test_rule.py
badd +40 tests/rules/test_name_exists.py
badd +2 tests/rules/test_name_capitalized.py
badd +4 rule_settings.py
badd +3 settings.py
badd +1 tests/fixtures/test.yml
badd +1 tests/fixtures/test-min-incorrect.yaml
badd +10 tests/test_load.py
badd +2 src/rules/runs_on_pinned.py
badd +3 src/rules/pinned_workflow_runner.py
badd +3 tests/rules/test_pinned_workflow_runner.py
badd +15 src/models/workflow.py
badd +9 src/rules/pinned_job_runner.py
badd +9 tests/rules/test_pinned_job_runner.py
badd +3 src/rules/job_environment_prefix.py
badd +14 src/models/job.py
badd +4 tests/rules/test_job_environment_prefix.py
badd +19 src/rules/step_hex_length.py
badd +43 tests/rules/test_step_hex_length.py
badd +5 src/rules/step_hex.py
badd +9 tests/rules/test_step_hex.py
badd +26 src/rules/step_approved.py
badd +59 tests/rules/test_step_approved.py
badd +0 src/utils.py
badd +28 src/rules/step_pinned.py
badd +82 tests/rules/test_step_pinned.py
badd +0 tests/fixtures/test-min.yaml
badd +0 actions.json
badd +0 src/models/step.py
badd +0 tests/test_utils.py
argglobal
%argdel
$argadd README.md
set stal=2
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabnew +setlocal\ bufhidden=wipe
tabrewind
edit README.md
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
balt tests/fixtures/test.yml
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
let s:l = 61 - ((57 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 61
normal! 04|
wincmd w
argglobal
if bufexists(fnamemodify("settings.py", ":p")) | buffer settings.py | else | edit settings.py | endif
if &buftype ==# 'terminal'
  silent file settings.py
endif
balt actions.json
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
let s:l = 6 - ((5 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 6
normal! 019|
wincmd w
argglobal
if bufexists(fnamemodify("actions.json", ":p")) | buffer actions.json | else | edit actions.json | endif
if &buftype ==# 'terminal'
  silent file actions.json
endif
balt settings.py
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
let s:l = 6 - ((5 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 6
normal! 068|
wincmd w
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
tabnext
edit cli.py
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
balt settings.py
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
let s:l = 21 - ((20 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 21
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("src/utils.py", ":p")) | buffer src/utils.py | else | edit src/utils.py | endif
if &buftype ==# 'terminal'
  silent file src/utils.py
endif
balt tests/test_utils.py
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
let s:l = 25 - ((24 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 25
normal! 035|
wincmd w
argglobal
if bufexists(fnamemodify("tests/test_utils.py", ":p")) | buffer tests/test_utils.py | else | edit tests/test_utils.py | endif
if &buftype ==# 'terminal'
  silent file tests/test_utils.py
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
let s:l = 1 - ((0 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 1
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
tabnext
edit src/models/job.py
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
balt src/rule.py
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
let s:l = 18 - ((17 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 18
normal! 016|
wincmd w
argglobal
if bufexists(fnamemodify("src/rule.py", ":p")) | buffer src/rule.py | else | edit src/rule.py | endif
if &buftype ==# 'terminal'
  silent file src/rule.py
endif
balt tests/test_rule.py
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
let s:l = 19 - ((6 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 19
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("tests/test_rule.py", ":p")) | buffer tests/test_rule.py | else | edit tests/test_rule.py | endif
if &buftype ==# 'terminal'
  silent file tests/test_rule.py
endif
balt tests/fixtures/test-min-incorrect.yaml
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
let s:l = 48 - ((30 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 48
normal! 09|
wincmd w
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
tabnext
edit src/models/step.py
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
balt src/rules/step_approved.py
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
let s:l = 33 - ((32 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 33
normal! 044|
wincmd w
argglobal
if bufexists(fnamemodify("src/rules/step_approved.py", ":p")) | buffer src/rules/step_approved.py | else | edit src/rules/step_approved.py | endif
if &buftype ==# 'terminal'
  silent file src/rules/step_approved.py
endif
balt src/models/step.py
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
let s:l = 43 - ((42 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 43
normal! 018|
wincmd w
argglobal
if bufexists(fnamemodify("tests/rules/test_step_approved.py", ":p")) | buffer tests/rules/test_step_approved.py | else | edit tests/rules/test_step_approved.py | endif
if &buftype ==# 'terminal'
  silent file tests/rules/test_step_approved.py
endif
balt src/rules/step_approved.py
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
let s:l = 63 - ((35 * winheight(0) + 32) / 65)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 63
normal! 029|
wincmd w
exe 'vert 1resize ' . ((&columns * 109 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 108 + 163) / 327)
tabnext 1
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
