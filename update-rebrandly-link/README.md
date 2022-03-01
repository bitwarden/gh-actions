# Update Rebrandly Link Action

This action is for updating Rebrandly links.  It was designed exclusively for our new `self-host` repository workflows
to update our Rebrandly links to point to the latest released versions of the `bitwarden.ps1/bitwarden.sh` and
`run.ps1/run.sh` scripts.  It works by finding the `id` of the Rebrandly link by using the provided `domain` and
`slashtag` parameters.  After it finds the `id`, it uses that to update the destination of that link to the provided
`destination`.

## Parameters

`apikey`: We have this stored in our Production KeyVault.

`domain`: This is the domain name of the link we have in Rebrandly. (ex: `go.btwrden.co`)

`slashtag`: This is the slashtag of the link we have in Rebrandly. (ex: `bw-ps`)

`destination`: This is the URL that the link in Rebrandly should point to.
