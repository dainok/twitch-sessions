---
title: "Auditing Active Directory passwords against HaveIBeenPwned"
date: 2022-02-08
author: Andrea Dainese
toc: true
images:
- /images/blog/2022/password_audit.png
categories:
- security
---
Any password policy, even with strict rules, can be easily bypassed with simple tricks: `Passw0rd!`, `Passw0rd$`, `Password!1` can be all valid passwords for length and complexity.

It this common scenario it's useful to regularly audit Active Directory passwords against password dictionaries (like RockYou) and/or [HaveIBeenPwned](https://haveibeenpwned.com/ "';--have i been pwned?").

Let's see how to audit Active Directory passwords using [Directory Services Internals
PowerShell Module and Framework](https://github.com/MichaelGrafnetter/DSInternals "DSInternals").

## Install

Open PowerShell with administrative privileges and check PowerShell version:

~~~
PS C:\Windows\system32> $PSVersionTable
~~~

$PSVersionTable must be 5.1 at least.

Install DSInternals:

~~~
PS C:\Windows\system32> Install-Module DSInternals -Force
~~~

If you got the error `PackageManagement\Install-PackageProvider : No match was found for the specified search criteria for the provider 'NuGet'. The package provider requires 'PackageManagement' and 'Provider' tags`, modify the security protocols (default is Ssl3 and Tls) and reinstall:

~~~
PS C:\Windows\system32> [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
PS C:\Windows\system32> $PSVersionTable
~~~

List available cmdlets:

~~~
PS C:\Windows\system32> Get-Command -Module DSInternals*
~~~

## Find weak passwords on a Domain Controller

Before we start the audit process, we need at least one dictionary file. Download any [wordlist](https://github.com/praetorian-inc/Hob0Rules/blob/master/wordlists/rockyou.txt.gz "RockYou wordlist").

Set environment:

~~~
$DictFile = "C:\Users\Administrator\Downloads\rockyou.txt"
$DC = "dc01"
$Domain = "DC=example,DC=com"
~~~

Start the audit:

~~~
Get-ADReplAccount -All -Server $DC -NamingContext $Domain | Test-PasswordQuality -WeakPasswordsFile $DictFile -IncludeDisabledAccounts
~~~

We can also build a report in CSV format:

~~~
PS C:\Users\Administrator> $Accounts = Get-ADReplAccount -All -Server $DC -NamingContext $Domain
PS C:\Users\Administrator> $Results = $Accounts | Test-PasswordQuality -WeakPasswordsFile $DictFile
PS C:\Users\Administrator> $RiskyAccounts = $Accounts | where {$Results.WeakPassword -match $_.SamAccountName}
PS C:\Users\Administrator> $RiskyAccounts | select SamAccountName,DisplayName,DistinguishedName | Export-Csv output.csv
~~~

Mind that there are no built-in tools to set the list of bad password for Active Directory Domain Services.

## Export data for a remote audit

At this moment, DSInternals cannot serialize accounts. See the [associated issue](https://github.com/MichaelGrafnetter/DSInternals/issues/96 "DSAccount XML Serialization").

Once it's fixed, the procedure should be as following.

~~~
PS C:\Users\andrea> $Password = Read-Host "Enter password (16 chars)" -AsSecureString
PS C:\Users\andrea> $Accounts = Get-ADReplAccount -All -Server $DC -NamingContext $Domain
PS C:\Users\andrea> $SerialAccounts = [System.Management.Automation.PSSerializer]::Serialize($Accounts)
PS C:\Users\andrea> $SerialAccounts | ConvertTo-SecureString -AsPlainText -Force | ConvertFrom-SecureString -SecureKey $Password | Set-Content -Path credentials.txt
~~~

Move the file to an external station **with PowerShell 7** and get the data back:

~~~
PS C:\Users\andrea> $Password = Read-Host "Enter password (16 chars)" -AsSecureString
PS C:\Users\andrea> $SerialAccounts = Get-Content -Path credentials.txt | ConvertTo-SecureString -SecureKey $Password | ConvertFrom-SecureString -AsPlainText
PS C:\Users\andrea> $Accounts = [System.Management.Automation.PSSerializer]::DeSerialize($SerialAccounts)
~~~

Analyze the data as we did previously:

~~~
$DictFile = "C:\Users\andrea\Downloads\rockyou.txt"
$DC = "dc01"
$Domain = "DC=example,DC=com"
PS C:\Users\Administrator> $Results = $Accounts | Test-PasswordQuality -WeakPasswordsFile $DictFile
PS C:\Users\Administrator> $RiskyAccounts = $Accounts | where {$Results.WeakPassword -match $_.SamAccountName}
PS C:\Users\Administrator> $RiskyAccounts | select SamAccountName,DisplayName,DistinguishedName | Export-Csv output.csv
~~~

## Check for breached credentials (HaveIBeenPwned)

I'm used to test if users are using leaked passwords. To do that, download the [password list from HaveIBeenPwned](https://haveibeenpwned.com/Passwords "Downloading the Pwned Passwords list"), use the ordered by hash NTLM file.

Analyze the weak passwords using the downloaded file:

~~~
PS C:\Users\Administrator\Downloads> $Accounts | Test-PasswordQuality -WeakPasswordHashesSortedFile .\pwned-passwords-ntlm-ordered-by-hash-v8.txt
PS C:\Users\Administrator> $RiskyAccounts = $Accounts | where {$Results.WeakPassword -match $_.SamAccountName}
PS C:\Users\Administrator> $RiskyAccounts | select SamAccountName,DisplayName,DistinguishedName | Export-Csv output.csv
~~~

## Next steps

Each account with a weak password should be forced to change the password at next logon. The user should also be notified via email. According to the organization policies, this could count as a security incident.

## References

* [Directory Services Internals
PowerShell Module and Framework](https://github.com/MichaelGrafnetter/DSInternals "DSInternals")
* [Auditing Weak Passwords in Active Directory](http://woshub.com/auditing-users-password-strength-in-ad/ "Auditing Weak Passwords in Active Directory")
* [Test-PasswordQuality](https://github.com/MichaelGrafnetter/DSInternals/blob/master/Documentation/PowerShell/Test-PasswordQuality.md#test-passwordquality "Test-PasswordQuality")
* [Active Directory Password Audit – Using Pwned Passwords](https://cybersectalk.com/2019/08/19/active-directory-password-audit-using-pwned-passwords/ "Active Directory Password Audit – Using Pwned Passwords")
* [SecLists](https://github.com/danielmiessler/SecLists "SecLists")
* [Downloading the Pwned Passwords list](https://haveibeenpwned.com/Passwords "Downloading the Pwned Passwords list")
