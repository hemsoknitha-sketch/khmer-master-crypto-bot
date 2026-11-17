$p = 'E:\AI CODE PYTHON\ANGKOR QUANT\.git\worktrees\push_quant_gold_script'
$acl = Get-Acl $p
$acl.SetAccessRuleProtection($true, $true)
$denies = @($acl.Access | Where-Object { $_.AccessControlType -eq 'Deny' })
foreach ($d in $denies) {
    $acl.RemoveAccessRuleSpecific($d)
}
Set-Acl -Path $p -AclObject $acl
Write-Host "ACL fix complete!"
