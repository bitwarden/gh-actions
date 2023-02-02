git filter-branch --commit-filter 'if [ "$GIT_COMMITTER_EMAIL" = "54288773+Eebru-gzy@users.noreply.github.com" ];
  then git commit-tree -S "$@";
  else git commit-tree "$@";
  fi' HEAD
