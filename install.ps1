param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$PassThruArgs
)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Get-Command python3 -ErrorAction SilentlyContinue) {
    & python3 "$ScriptDir\install.py" @PassThruArgs
} else {
    & python "$ScriptDir\install.py" @PassThruArgs
}
exit $LASTEXITCODE
