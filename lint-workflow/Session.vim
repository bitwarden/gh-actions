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
badd +24 cli.py
badd +4 src/load.py
badd +1 config.yaml
badd +1 src/rules/__init__.py
badd +19 src/rules/name_capitalized.py
badd +13 src/rules/name_exists.py
badd +1 src/rule.py
badd +72 tests/test_rule.py
badd +40 tests/rules/test_name_exists.py
badd +100 tests/rules/test_name_capitalized.py
badd +4 rule_settings.py
badd +12 settings.py
badd +3 tests/fixtures/test.yml
badd +1 tests/fixtures/test-min-incorrect.yaml
badd +10 tests/test_load.py
badd +2 src/rules/runs_on_pinned.py
badd +3 src/rules/pinned_workflow_runner.py
badd +3 tests/rules/test_pinned_workflow_runner.py
badd +15 src/models/workflow.py
badd +1 src/rules/pinned_job_runner.py
badd +9 tests/rules/test_pinned_job_runner.py
badd +19 src/rules/job_environment_prefix.py
badd +18 src/models/job.py
badd +72 tests/rules/test_job_environment_prefix.py
badd +19 src/rules/step_hex_length.py
badd +43 tests/rules/test_step_hex_length.py
badd +5 src/rules/step_hex.py
badd +9 tests/rules/test_step_hex.py
badd +47 src/rules/step_approved.py
badd +92 tests/rules/test_step_approved.py
badd +0 src/utils.py
badd +16 src/rules/step_pinned.py
badd +100 tests/rules/test_step_pinned.py
badd +1 tests/fixtures/test-min.yaml
badd +0 actions.json
badd +0 src/models/step.py
badd +0 tests/test_utils.py
badd +0 src/lint.py
badd +0 src/actions.py
badd +0 Taskfile.yml
argglobal
%argdel
$argadd README.md
set stal=2
tabnew +setlocal\ bufhidden=wipe
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
wincmd _ | wincmd |
split
1wincmd k
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
exe '3resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 3resize ' . ((&columns * 108 + 163) / 327)
exe '4resize ' . ((&lines * 31 + 33) / 67)
exe 'vert 4resize ' . ((&columns * 108 + 163) / 327)
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
let s:l = 41 - ((36 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 41
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
let s:l = 29 - ((28 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 29
normal! 021|
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
let s:l = 5 - ((4 * winheight(0) + 16) / 32)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 5
normal! 0
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
let s:l = 5 - ((2 * winheight(0) + 15) / 31)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 5
normal! 021|
wincmd w
exe 'vert 1resize ' . ((&columns * 109 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe '3resize ' . ((&lines * 32 + 33) / 67)
exe 'vert 3resize ' . ((&columns * 108 + 163) / 327)
exe '4resize ' . ((&lines * 31 + 33) / 67)
exe 'vert 4resize ' . ((&columns * 108 + 163) / 327)
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
balt src/actions.py
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
let s:l = 50 - ((49 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 50
normal! 09|
wincmd w
argglobal
if bufexists(fnamemodify("src/actions.py", ":p")) | buffer src/actions.py | else | edit src/actions.py | endif
if &buftype ==# 'terminal'
  silent file src/actions.py
endif
balt cli.py
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
let s:l = 16 - ((10 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 16
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("src/lint.py", ":p")) | buffer src/lint.py | else | edit src/lint.py | endif
if &buftype ==# 'terminal'
  silent file src/lint.py
endif
balt cli.py
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
let s:l = 65 - ((1 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 65
normal! 036|
wincmd w
3wincmd w
exe 'vert 1resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 108 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 109 + 163) / 327)
tabnext
edit src/load.py
let s:save_splitbelow = &splitbelow
let s:save_splitright = &splitright
set splitbelow splitright
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
wincmd _ | wincmd |
vsplit
3wincmd h
wincmd w
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
exe 'vert 1resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 4resize ' . ((&columns * 81 + 163) / 327)
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
let s:l = 67 - ((32 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 67
normal! 042|
wincmd w
argglobal
if bufexists(fnamemodify("tests/test_load.py", ":p")) | buffer tests/test_load.py | else | edit tests/test_load.py | endif
if &buftype ==# 'terminal'
  silent file tests/test_load.py
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
let s:l = 45 - ((44 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 45
normal! 0
wincmd w
argglobal
if bufexists(fnamemodify("src/utils.py", ":p")) | buffer src/utils.py | else | edit src/utils.py | endif
if &buftype ==# 'terminal'
  silent file src/utils.py
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
let s:l = 49 - ((45 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 49
normal! 09|
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
let s:l = 36 - ((35 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 36
normal! 0
wincmd w
exe 'vert 1resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 3resize ' . ((&columns * 81 + 163) / 327)
exe 'vert 4resize ' . ((&columns * 81 + 163) / 327)
tabnext
edit src/rule.py
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
let s:l = 41 - ((40 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 41
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
let s:l = 133 - ((56 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 133
normal! 012|
wincmd w
exe 'vert 1resize ' . ((&columns * 163 + 163) / 327)
exe 'vert 2resize ' . ((&columns * 163 + 163) / 327)
tabnext
edit src/models/step.py
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
let s:l = 23 - ((22 * winheight(0) + 32) / 64)
if s:l < 1 | let s:l = 1 | endif
keepjumps exe s:l
normal! zt
keepjumps 23
normal! 029|
tabnext 2
set stal=1
if exists('s:wipebuf') && len(win_findbuf(s:wipebuf)) == 0 && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20
let &shortmess = s:shortmess_save
let s:sx = expand("<sfile>:p:r")."x.vim"
if filereadable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &g:so = s:so_save | let &g:siso = s:siso_save
set hlsearch
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
